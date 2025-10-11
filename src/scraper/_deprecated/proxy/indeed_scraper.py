"""Indeed job scraper using BrightData proxies.

Lightweight HTTP scraper focusing on:
- Job URL extraction
- Job Description retrieval  
- Skills extraction from descriptions
"""

from typing import List, Optional
from datetime import datetime
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

from src.models import JobModel
from src.scraper.proxy.config import BrightDataProxy, ProxySession


async def scrape_indeed_jobs(
    query: str,
    location: str = "United States",
    limit: int = 50,
    proxy: Optional[BrightDataProxy] = None
) -> List[JobModel]:
    """Scrape Indeed jobs using BrightData proxies.
    
    Args:
        query: Job search query (e.g., "Data Scientist")
        location: Location filter (e.g., "Seattle, WA")
        limit: Maximum number of jobs to scrape
        proxy: BrightData proxy instance. If None, loads from environment.
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"\n🚀 Indeed Proxy Scraper")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize proxy
    if proxy is None:
        proxy = BrightDataProxy.from_env()
    
    # Use session for consistent IP
    session_proxy = proxy.with_session()
    print(f"   Using session: {session_proxy.session_id[:8]}...")
    
    # Create proxy session
    session = ProxySession(proxy_pool=None, timeout=30.0)
    
    # Indeed base URL
    base_url = "https://www.indeed.com/jobs"
    
    jobs = []
    start = 0
    
    try:
        while len(jobs) < limit:
            params = {
                "q": query,
                "l": location,
                "start": start,
                "fromage": 7  # Last 7 days
            }
            
            url = f"{base_url}?{urlencode(params)}"
            
            print(f"\n📄 Fetching results (start={start})...")
            
            # Make request through BrightData proxy
            response = await session.get(url, proxies=session_proxy.auth_dict)
            
            if response.status_code != 200:
                print(f"⚠️  Failed to fetch results: Status {response.status_code}")
                break
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find job cards (Indeed uses mosaic-* classes and data-jk attributes)
            job_cards = soup.find_all("div", class_=re.compile("job_seen_beacon|cardOutline"))
            
            # Alternative: Find by data-jk attribute
            if not job_cards:
                job_cards = soup.find_all("div", attrs={"data-jk": True})
            
            if not job_cards:
                print("⚠️  No job cards found. Indeed may have changed their HTML structure.")
                break
            
            print(f"   Found {len(job_cards)} job cards")
            
            for card in job_cards:
                if len(jobs) >= limit:
                    break
                
                try:
                    # Extract job key (Indeed's job ID)
                    job_key = card.get("data-jk") or card.get("id", "").replace("job_", "")
                    
                    if not job_key:
                        continue
                    
                    job_id = f"indeed_{job_key}"
                    job_url = f"https://www.indeed.com/viewjob?jk={job_key}"
                    
                    # Extract title
                    title_elem = card.find("h2", class_=re.compile("jobTitle"))
                    if not title_elem:
                        title_elem = card.find("a", attrs={"data-jk": job_key})
                    
                    job_title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                    
                    # Extract company
                    company_elem = card.find("span", class_=re.compile("companyName"))
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    
                    # Extract location
                    location_elem = card.find("div", class_=re.compile("companyLocation"))
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    print(f"\n   📝 Job {len(jobs) + 1}: {job_title} at {company}")
                    print(f"      Fetching full description...")
                    
                    # Fetch full job description
                    job_desc = await _fetch_indeed_job_description(job_url, session, session_proxy)
                    
                    if not job_desc:
                        print("      ⚠️  Failed to fetch job description, skipping...")
                        continue
                    
                    print(f"      ✅ Got description ({len(job_desc)} chars)")
                    
                    # Extract skills from description
                    from src.scraper.brightdata.parsers.skills_parser import SkillsParser
                    skills_parser = SkillsParser()
                    skills_list = skills_parser.extract_from_text(job_desc)
                    skills_str = ", ".join(skills_list) if skills_list else ""
                    
                    print(f"      🎯 Extracted {len(skills_list)} skills")
                    
                    # Create JobModel
                    job = JobModel(
                        job_id=str(job_id),
                        Job_Role=job_title,
                        Company=company,
                        Experience="",
                        Skills=skills_str,
                        jd=job_desc,
                        company_detail="",
                        platform="indeed",
                        url=job_url,
                        location=job_location,
                        salary=None,
                        posted_date=datetime.now(),
                        skills_list=skills_list,
                        normalized_skills=[s.lower() for s in skills_list]
                    )
                    
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"      ❌ Error processing job card: {e}")
                    continue
            
            if len(job_cards) < 10:
                # Last page reached
                print("\n   📭 No more jobs available")
                break
            
            start += len(job_cards)
            
            # Small delay between pages
            await asyncio.sleep(1)
    
    except Exception as e:
        print(f"\n❌ Scraping error: {e}")
    
    print(f"\n✅ Scraped {len(jobs)} Indeed jobs with skills")
    return jobs


async def _fetch_indeed_job_description(
    job_url: str,
    session: ProxySession,
    proxy: BrightDataProxy,
    max_retries: int = 2
) -> Optional[str]:
    """Fetch full job description from individual Indeed job page.
    
    Args:
        job_url: URL of the job posting
        session: ProxySession instance
        proxy: BrightData proxy configuration
        max_retries: Maximum retry attempts
    
    Returns:
        Job description text or None if failed
    """
    for attempt in range(max_retries):
        try:
            response = await session.get(job_url, proxies=proxy.auth_dict)
            
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Try multiple selectors for job description
            desc_elem = (
                soup.find("div", id="jobDescriptionText") or
                soup.find("div", class_=re.compile("jobsearch-jobDescriptionText")) or
                soup.find("div", class_=re.compile("job-description"))
            )
            
            if desc_elem:
                return desc_elem.get_text(separator=" ", strip=True)
            
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            else:
                print(f"         ⚠️  Failed after {max_retries} attempts: {e}")
    
    return None


# Test function
async def test_indeed_scraper():
    """Test Indeed scraper with sample query."""
    proxy = BrightDataProxy.from_env()
    
    # Add country targeting
    proxy = proxy.with_country("us")
    
    jobs = await scrape_indeed_jobs(
        query="Python Developer",
        location="Seattle, WA",
        limit=5,
        proxy=proxy
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        print(f"\n   - {job.Job_Role} at {job.Company}")
        print(f"     Skills ({len(job.skills_list)}): {', '.join(job.skills_list[:10])}")
        print(f"     URL: {job.url}")


if __name__ == "__main__":
    asyncio.run(test_indeed_scraper())
