"""LinkedIn job scraper using BrightData proxies.

This scraper uses direct HTTP requests through BrightData proxies instead of
the Scraping Browser, making it much faster while still bypassing anti-bot measures.

Focus: Extract only URL, Job Description, and Skills
"""

from typing import List, Optional
from datetime import datetime
import asyncio
import re
from bs4 import BeautifulSoup

from src.models import JobModel
from src.scraper.proxy.config import BrightDataProxy, ProxySession


async def scrape_linkedin_jobs(
    keyword: str,
    location: str = "United States",
    limit: int = 50,
    proxy: Optional[BrightDataProxy] = None
) -> List[JobModel]:
    """Scrape LinkedIn jobs using BrightData proxies.
    
    Args:
        keyword: Job search keyword (e.g., "Machine Learning Engineer")
        location: Location filter (e.g., "United States", "India")
        limit: Maximum number of jobs to scrape
        proxy: BrightData proxy instance. If None, loads from environment.
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"\n🚀 LinkedIn Proxy Scraper")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize proxy
    if proxy is None:
        proxy = BrightDataProxy.from_env()
    
    # Use session for consistent IP across requests
    session_proxy = proxy.with_session()
    print(f"   Using session: {session_proxy.session_id[:8]}...")
    
    # Create proxy session
    session = ProxySession(proxy_pool=None, timeout=30.0)
    
    # LinkedIn job search URL
    base_url = "https://www.linkedin.com/jobs/search/"
    params = {
        "keywords": keyword,
        "location": location,
        "start": 0
    }
    
    jobs = []
    page = 0
    
    try:
        while len(jobs) < limit:
            params["start"] = page * 25  # LinkedIn shows 25 jobs per page
            
            print(f"\n📄 Fetching page {page + 1}...")
            
            # Build URL with query parameters
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{base_url}?{query_string}"
            
            # Make request through BrightData proxy
            response = await session.get(url, proxies=session_proxy.auth_dict)
            
            if response.status_code != 200:
                print(f"⚠️  Failed to fetch page {page + 1}: Status {response.status_code}")
                break
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find job cards
            job_cards = soup.find_all("div", class_=re.compile("job-search-card|base-card"))
            
            if not job_cards:
                print("⚠️  No job cards found. LinkedIn may have changed their HTML structure.")
                break
            
            print(f"   Found {len(job_cards)} job cards")
            
            for card in job_cards:
                if len(jobs) >= limit:
                    break
                
                try:
                    # Extract basic info from card
                    job_url_elem = card.find("a", class_=re.compile("base-card__full-link"))
                    if not job_url_elem:
                        continue
                    
                    job_url = job_url_elem.get("href", "")
                    if not job_url:
                        continue
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r"/view/(\d+)", job_url)
                    job_id = f"linkedin_{job_id_match.group(1)}" if job_id_match else job_url
                    
                    # Extract title
                    title_elem = card.find("h3", class_=re.compile("base-search-card__title"))
                    job_title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                    
                    # Extract company
                    company_elem = card.find("h4", class_=re.compile("base-search-card__subtitle"))
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    
                    # Extract location
                    location_elem = card.find("span", class_=re.compile("job-search-card__location"))
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    print(f"\n   📝 Job {len(jobs) + 1}: {job_title} at {company}")
                    print(f"      Fetching full description from: {job_url[:80]}...")
                    
                    # Fetch full job description (this is where we get skills)
                    job_desc = await _fetch_job_description(job_url, session, session_proxy)
                    
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
                        platform="linkedin",
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
            
            if len(job_cards) < 25:
                # Last page reached
                print("\n   📭 No more jobs available")
                break
            
            page += 1
            
            # Small delay between pages
            await asyncio.sleep(1)
    
    except Exception as e:
        print(f"\n❌ Scraping error: {e}")
    
    print(f"\n✅ Scraped {len(jobs)} LinkedIn jobs with skills")
    return jobs


async def _fetch_job_description(
    job_url: str,
    session: ProxySession,
    proxy: BrightDataProxy,
    max_retries: int = 2
) -> Optional[str]:
    """Fetch full job description from individual job page.
    
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
                soup.find("div", class_=re.compile("description__text")) or
                soup.find("div", class_=re.compile("show-more-less-html__markup")) or
                soup.find("article", class_=re.compile("jobs-description"))
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
async def test_linkedin_scraper():
    """Test LinkedIn scraper with sample query."""
    proxy = BrightDataProxy.from_env()
    
    # Add country targeting if needed
    proxy = proxy.with_country("us")  # Target US IPs
    
    jobs = await scrape_linkedin_jobs(
        keyword="Python Developer",
        location="United States",
        limit=5,
        proxy=proxy
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        print(f"\n   - {job.Job_Role} at {job.Company}")
        print(f"     Skills ({len(job.skills_list)}): {', '.join(job.skills_list[:10])}")
        print(f"     URL: {job.url}")


if __name__ == "__main__":
    asyncio.run(test_linkedin_scraper())
