"""LinkedIn scraper using LOCAL BrightData Proxy Manager + Playwright.

Fast method:
- Local proxy server (luminati-proxy)
- BrightData's residential IPs
- Playwright for scraping
- Much faster than cloud browser scraping!
"""

import asyncio
from typing import List
from datetime import datetime
from playwright.async_api import async_playwright, Page
from typing import cast
try:
    # ProxySettings is a TypedDict provided by Playwright's type hints
    from playwright.async_api import ProxySettings  # type: ignore
except Exception:  # pragma: no cover
    ProxySettings = dict  # fallback for environments without type hints
import re

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser


# Local proxy configuration
LOCAL_PROXY = {
    "server": "http://localhost:24000",  # US residential IPs
}


async def scrape_linkedin_jobs_local_proxy(
    keyword: str,
    location: str = "United States",
    limit: int = 50
) -> List[JobModel]:
    """Scrape LinkedIn using local BrightData proxy + Playwright.
    
    Prerequisites:
        - Run: ./start_proxy_manager.sh (in separate terminal)
        - Proxy will be available at localhost:24000
    
    Args:
        keyword: Job search keyword
        location: Location filter
        limit: Max jobs to scrape
    
    Returns:
        List of JobModel with skills extracted
    """
    print(f"\n🚀 LinkedIn Local Proxy Scraper")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    print(f"   Proxy: {LOCAL_PROXY['server']}")
    
    skills_parser = SkillsParser()
    jobs = []
    
    async with async_playwright() as p:
        # Launch browser with local proxy
        print("\n🌐 Launching browser with BrightData proxy...")
        browser = await p.chromium.launch(
            headless=True,
            proxy=cast(ProxySettings, LOCAL_PROXY)
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        try:
            # Navigate to LinkedIn jobs search
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
            
            print(f"\n📄 Loading LinkedIn jobs...")
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)  # Wait for dynamic content
            
            # Scroll to load more jobs
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(1000)
            
            # Extract job cards
            job_cards = await page.query_selector_all(".job-search-card, .base-card")
            print(f"   Found {len(job_cards)} job cards")
            
            for idx, card in enumerate(job_cards[:limit], 1):
                try:
                    # Extract job URL
                    link_elem = await card.query_selector("a.base-card__full-link")
                    if not link_elem:
                        continue
                    
                    job_url = await link_elem.get_attribute("href")
                    if not job_url:
                        continue
                    
                    # Extract job ID
                    job_id_match = re.search(r"/view/(\d+)", job_url)
                    job_id = f"linkedin_{job_id_match.group(1)}" if job_id_match else job_url
                    
                    # Extract title
                    title_elem = await card.query_selector("h3")
                    job_title = await title_elem.inner_text() if title_elem else "Unknown"
                    
                    # Extract company
                    company_elem = await card.query_selector("h4")
                    company = await company_elem.inner_text() if company_elem else "Unknown"
                    
                    # Extract location
                    location_elem = await card.query_selector(".job-search-card__location")
                    job_location = await location_elem.inner_text() if location_elem else location
                    
                    print(f"\n   📝 Job {idx}: {job_title} at {company}")
                    print(f"      Fetching description...")
                    
                    # Fetch full job description
                    job_desc = await _fetch_job_description(page, job_url)
                    
                    if not job_desc:
                        print(f"      ⚠️  No description found")
                        continue
                    
                    print(f"      ✅ Got description ({len(job_desc)} chars)")
                    
                    # Extract skills
                    skills_list = skills_parser.extract_from_text(job_desc)
                    skills_str = ", ".join(skills_list) if skills_list else ""
                    print(f"      🎯 Extracted {len(skills_list)} skills")
                    
                    # Create JobModel
                    job = JobModel(
                        job_id=job_id,
                        Job_Role=job_title.strip(),
                        Company=company.strip(),
                        Experience="",
                        Skills=skills_str,
                        jd=job_desc,
                        company_detail="",
                        platform="linkedin",
                        url=job_url,
                        location=job_location.strip(),
                        salary=None,
                        posted_date=datetime.now(),
                        skills_list=skills_list,
                        normalized_skills=[s.lower() for s in skills_list]
                    )
                    
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"      ❌ Error: {e}")
                    continue
        
        finally:
            await browser.close()
    
    print(f"\n✅ Scraped {len(jobs)} LinkedIn jobs with skills")
    return jobs


async def _fetch_job_description(page: Page, job_url: str) -> str:
    """Fetch full job description from job page."""
    try:
        await page.goto(job_url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Try multiple selectors
        desc_elem = await page.query_selector(".description__text, .show-more-less-html__markup, .jobs-description")
        
        if desc_elem:
            return await desc_elem.inner_text()
        
        return ""
        
    except Exception as e:
        print(f"         ⚠️  Failed to fetch description: {e}")
        return ""


# Test function
async def test_scraper():
    """Test the local proxy scraper."""
    print("⚠️  Make sure Proxy Manager is running!")
    print("   Run: ./start_proxy_manager.sh")
    print()
    input("Press Enter when proxy is ready...")
    
    jobs = await scrape_linkedin_jobs_local_proxy(
        keyword="Python Developer",
        location="United States",
        limit=5
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        title = job.job_role
        company = job.company
        skills = job.skills_list or []
        print(f"\n   - {title} at {company}")
        print(f"     Skills: {', '.join(skills[:10])}")


if __name__ == "__main__":
    asyncio.run(test_scraper())
