"""Naukri scraper using LOCAL BrightData Proxy Manager + Playwright.

Fast method:
- Local proxy server (luminati-proxy)
- BrightData's residential IPs (India)
- Playwright for scraping
- Much faster than cloud browser scraping!
"""

import asyncio
from typing import List
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page
import re

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser


# Local proxy configuration - India IPs for Naukri
LOCAL_PROXY = {
    "server": "http://localhost:24001",  # India residential IPs
}


async def scrape_naukri_jobs_local_proxy(
    keyword: str,
    location: str = "India",
    limit: int = 50
) -> List[JobModel]:
    """Scrape Naukri using local BrightData proxy + Playwright.
    
    Prerequisites:
        - Run: ./start_proxy_manager.sh (in separate terminal)
        - Proxy will be available at localhost:24001 (India IPs)
    
    Args:
        keyword: Job search keyword
        location: Location filter (India by default)
        limit: Max jobs to scrape
    
    Returns:
        List of JobModel with skills extracted
    """
    print(f"\n🚀 Naukri Local Proxy Scraper")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    print(f"   Proxy: {LOCAL_PROXY['server']} (India IPs)")
    
    skills_parser = SkillsParser()
    jobs = []
    
    async with async_playwright() as p:
        # Launch browser with local proxy
        print("\n🌐 Launching browser with BrightData proxy...")
        browser = await p.chromium.launch(
            headless=True,
            proxy=LOCAL_PROXY
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        try:
            # Navigate to Naukri jobs search
            search_url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs"
            
            print(f"\n📄 Loading Naukri jobs...")
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)  # Wait for dynamic content
            
            # Scroll to load more jobs
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(1000)
            
            # Extract job cards
            job_cards = await page.query_selector_all("article.jobTuple, .jobTuple")
            print(f"   Found {len(job_cards)} job cards")
            
            for idx, card in enumerate(job_cards[:limit], 1):
                try:
                    # Extract job link
                    link_elem = await card.query_selector("a.title, .jobTupleHeader a")
                    if not link_elem:
                        continue
                    
                    job_url = await link_elem.get_attribute("href")
                    if not job_url:
                        continue
                    
                    # Make URL absolute
                    if job_url.startswith("/"):
                        job_url = f"https://www.naukri.com{job_url}"
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r"job-listings-(.+?)(?:\?|$)", job_url)
                    job_id = f"naukri_{job_id_match.group(1)}" if job_id_match else job_url
                    
                    # Extract title
                    title_elem = await card.query_selector("a.title, .jobTupleHeader .title")
                    job_title = await title_elem.inner_text() if title_elem else "Unknown"
                    
                    # Extract company
                    company_elem = await card.query_selector(".companyInfo a, .comp-name")
                    company = await company_elem.inner_text() if company_elem else "Unknown"
                    
                    # Extract experience
                    exp_elem = await card.query_selector(".expwdth, .experience")
                    experience = await exp_elem.inner_text() if exp_elem else ""
                    
                    # Extract location
                    location_elem = await card.query_selector(".locWdth, .location")
                    job_location = await location_elem.inner_text() if location_elem else location
                    
                    # Extract salary (if available)
                    salary_elem = await card.query_selector(".salaryWdth, .salary")
                    salary = await salary_elem.inner_text() if salary_elem else None
                    
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
                        Experience=experience.strip(),
                        Skills=skills_str,
                        jd=job_desc,
                        company_detail="",
                        platform="naukri",
                        url=job_url,
                        location=job_location.strip(),
                        salary=salary,
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
    
    print(f"\n✅ Scraped {len(jobs)} Naukri jobs with skills")
    return jobs


async def _fetch_job_description(page: Page, job_url: str) -> str:
    """Fetch full job description from job page."""
    try:
        await page.goto(job_url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Try multiple selectors for Naukri
        desc_elem = await page.query_selector(".jdSection, .job-description, [class*='jobDesc']")
        
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
    
    jobs = await scrape_naukri_jobs_local_proxy(
        keyword="Python Developer",
        location="India",
        limit=5
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        print(f"\n   - {job.Job_Role} at {job.Company}")
        print(f"     Skills: {', '.join(job.skills_list[:10])}")


if __name__ == "__main__":
    asyncio.run(test_scraper())
