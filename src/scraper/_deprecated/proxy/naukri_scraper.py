"""Naukri job scraper using BrightData proxies.

Naukri (India's #1 job portal) scraper focusing on:
- Job URL extraction
- Job Description retrieval
- Skills extraction for trend analysis
"""

from typing import List, Optional
from datetime import datetime
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from src.models import JobModel
from src.scraper.proxy.config import BrightDataProxy, ProxySession


async def scrape_naukri_jobs(
    keyword: str,
    location: str = "India",
    limit: int = 50,
    proxy: Optional[BrightDataProxy] = None
) -> List[JobModel]:
    """Scrape Naukri jobs using BrightData proxies.
    
    Args:
        keyword: Job search keyword (e.g., "Python Developer")
        location: Location filter (e.g., "Bangalore", "Mumbai")
        limit: Maximum number of jobs to scrape
        proxy: BrightData proxy instance. If None, loads from environment.
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"\n🚀 Naukri Proxy Scraper")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize proxy
    if proxy is None:
        proxy = BrightDataProxy.from_env()
    
    # Use session for consistent IP + India geo-targeting
    session_proxy = proxy.with_session().with_country("in")
    print(f"   Using session: {session_proxy.session_id[:8]}... (country: IN)")
    
    # Create proxy session
    session = ProxySession(proxy_pool=None, timeout=30.0)
    
    # Naukri search URL
    base_url = "https://www.naukri.com"
    search_path = f"/{quote_plus(keyword)}-jobs"
    
    if location and location.lower() != "india":
        search_path += f"-in-{quote_plus(location)}"
    
    jobs = []
    page = 1
    
    try:
        while len(jobs) < limit:
            url = f"{base_url}{search_path}"
            if page > 1:
                url += f"?{page}"
            
            print(f"\n📄 Fetching page {page}...")
            
            # Make request through BrightData proxy
            response = await session.get(url, proxies=session_proxy.auth_dict)
            
            if response.status_code != 200:
                print(f"⚠️  Failed to fetch page {page}: Status {response.status_code}")
                break
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find job cards (Naukri uses article tags with class "jobTuple")
            job_cards = soup.find_all("article", class_=re.compile("jobTuple"))
            
            # Alternative selectors
            if not job_cards:
                job_cards = soup.find_all("div", class_=re.compile("srp-jobtuple"))
            
            if not job_cards:
                print("⚠️  No job cards found. Naukri may have changed their HTML structure.")
                break
            
            print(f"   Found {len(job_cards)} job cards")
            
            for card in job_cards:
                if len(jobs) >= limit:
                    break
                
                try:
                    # Extract job URL (title link)
                    title_elem = card.find("a", class_=re.compile("title"))
                    if not title_elem:
                        continue
                    
                    job_url = title_elem.get("href", "")
                    if not job_url.startswith("http"):
                        job_url = base_url + job_url
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r"job-listings-([a-zA-Z0-9]+)", job_url)
                    if job_id_match:
                        job_id = f"naukri_{job_id_match.group(1)}"
                    else:
                        job_id = f"naukri_{abs(hash(job_url)) % (10 ** 8)}"
                    
                    # Extract title
                    job_title = title_elem.get_text(strip=True)
                    
                    # Extract company
                    company_elem = card.find("a", class_=re.compile("comp-name|companyInfo"))
                    if not company_elem:
                        company_elem = card.find("div", class_=re.compile("comp-name|companyInfo"))
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    
                    # Extract location
                    location_elem = card.find("span", class_=re.compile("location|locWdth"))
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Extract experience
                    exp_elem = card.find("span", class_=re.compile("expwdth|experience"))
                    experience = exp_elem.get_text(strip=True) if exp_elem else ""
                    
                    print(f"\n   📝 Job {len(jobs) + 1}: {job_title} at {company}")
                    print(f"      Fetching full description...")
                    
                    # Fetch full job description
                    job_desc = await _fetch_naukri_job_description(job_url, session, session_proxy)
                    
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
                        Experience=experience,
                        Skills=skills_str,
                        jd=job_desc,
                        company_detail="",
                        platform="naukri",
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
            
            page += 1
            
            # Small delay between pages
            await asyncio.sleep(1)
    
    except Exception as e:
        print(f"\n❌ Scraping error: {e}")
    
    print(f"\n✅ Scraped {len(jobs)} Naukri jobs with skills")
    return jobs


async def _fetch_naukri_job_description(
    job_url: str,
    session: ProxySession,
    proxy: BrightDataProxy,
    max_retries: int = 2
) -> Optional[str]:
    """Fetch full job description from individual Naukri job page.
    
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
                soup.find("div", class_=re.compile("jd-content|job-description")) or
                soup.find("div", class_=re.compile("JDC")) or
                soup.find("section", class_=re.compile("job-desc"))
            )
            
            if desc_elem:
                # Also try to extract key skills section if available
                skills_section = soup.find("div", class_=re.compile("key-skill"))
                if skills_section:
                    desc_text = desc_elem.get_text(separator=" ", strip=True)
                    skills_text = skills_section.get_text(separator=" ", strip=True)
                    return f"{desc_text} Key Skills: {skills_text}"
                
                return desc_elem.get_text(separator=" ", strip=True)
            
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            else:
                print(f"         ⚠️  Failed after {max_retries} attempts: {e}")
    
    return None


# Test function
async def test_naukri_scraper():
    """Test Naukri scraper with sample query."""
    proxy = BrightDataProxy.from_env()
    
    jobs = await scrape_naukri_jobs(
        keyword="Python Developer",
        location="Bangalore",
        limit=5,
        proxy=proxy
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        # Use field names (not aliases) for attributes and handle Optionals safely
        title = job.job_role
        company = job.company
        skills = job.skills_list or []
        top_skills = ", ".join(skills[:10]) if skills else ""
        print(f"\n   - {title} at {company}")
        print(f"     Skills ({len(skills)}): {top_skills}")
        print(f"     URL: {job.url}")


if __name__ == "__main__":
    asyncio.run(test_naukri_scraper())
