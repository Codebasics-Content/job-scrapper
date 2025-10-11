"""Naukri scraper using BrightData Scraping Browser.

Uses BrightData's infrastructure for reliable real-time scraping,
bypassing reCAPTCHA and anti-bot measures.
"""
from __future__ import annotations
from typing import List, Optional
import asyncio
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout, ElementHandle
from urllib.parse import quote_plus
import re
import time

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from src.scraper.brightdata.config.settings import get_settings


class NaukriBrightDataScraper:
    """Naukri scraper using BrightData Scraping Browser."""
    
    def __init__(self):
        self.settings = get_settings()
        if not self.settings.browser_url:
            raise ValueError("BRIGHTDATA_BROWSER_URL not configured in .env")
        
        self.browser_url = self.settings.browser_url
        self.browser: Optional[Browser] = None
        self.playwright = None
        self.skills_parser = SkillsParser()
    
    async def connect(self):
        """Connect to BrightData Scraping Browser."""
        if self.browser:
            return
        
        self.playwright = await async_playwright().start()
        
        # Connect to BrightData's remote browser
        self.browser = await self.playwright.chromium.connect_over_cdp(
            self.browser_url
        )
        
        print(f"✅ Connected to BrightData Scraping Browser for Naukri")
    
    async def disconnect(self):
        """Disconnect from browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
    
    async def create_page(self) -> Page:
        """Create a new page in the browser."""
        if not self.browser:
            await self.connect()
        
        assert self.browser is not None, "Browser should be connected"
        page = await self.browser.new_page()
        
        # Note: BrightData manages User-Agent and headers automatically
        # Don't override - BrightData handles anti-detection
        
        return page
    
    async def scrape_jobs(
        self,
        keyword: str,
        limit: int = 50
    ) -> List[JobModel]:
        """Scrape jobs from Naukri using BrightData browser.
        
        Args:
            keyword: Job search keyword (e.g., "Python Developer")
            limit: Maximum number of jobs to scrape
        
        Returns:
            List of JobModel objects
        """
        print(f"🚀 Starting Naukri scraping via BrightData...")
        print(f"   Keyword: {keyword}")
        print(f"   Limit: {limit}")
        
        page = await self.create_page()
        jobs: List[JobModel] = []
        
        try:
            # Build search URL
            search_url = f"https://www.naukri.com/{keyword.lower().replace(' ', '-')}-jobs"
            
            print(f"🔍 Navigating to: {search_url}")
            
            # Navigate to search page
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            except PlaywrightTimeout:
                print("⚠️  Page load timeout, continuing anyway...")
            
            # Wait for job listings with multiple selector attempts
            await asyncio.sleep(3)  # Give page time to load
            
            try:
                await page.wait_for_selector("article.jobTuple, .srp-jobtuple-wrapper", timeout=10000)
            except PlaywrightTimeout:
                print("⚠️  Job listings not found")
                # Take screenshot for debugging
                await page.screenshot(path="naukri_debug.png")
                print("📸 Screenshot saved to naukri_debug.png")
                return []
            
            # Scroll to load more jobs
            print("📜 Scrolling to load more jobs...")
            for i in range(min(10, (limit // 20) + 2)):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
            
            # Extract job cards - try multiple selectors
            job_cards = await page.query_selector_all("article.jobTuple")
            
            if not job_cards:
                # Try alternative selector
                job_cards = await page.query_selector_all(".srp-jobtuple-wrapper")
            
            print(f"📥 Found {len(job_cards)} job cards")
            
            for card in job_cards[:limit]:
                try:
                    job_data = await self._extract_job(card)
                    if job_data:
                        # Create JobModel
                        job = JobModel(
                            job_id=job_data['job_id'],
                            Job_Role=job_data['title'],
                            Company=job_data['company'],
                            Experience=job_data['experience'],
                            Skills=", ".join(job_data['skills']) if job_data['skills'] else "",
                            jd=job_data['description'],
                            company_detail="",
                            platform="naukri",
                            url=job_data['url'],
                            location=job_data['location'],
                            salary=job_data.get('salary'),
                            posted_date=None,
                            skills_list=job_data['skills'],
                            normalized_skills=[s.lower() for s in job_data['skills']]
                        )
                        jobs.append(job)
                        
                except Exception as e:
                    print(f"⚠️  Error extracting job: {e}")
                    continue
            
            print(f"✅ Extracted {len(jobs)} jobs from Naukri")
            
        finally:
            await page.close()
        
        return jobs
    
    async def _extract_job(self, card: ElementHandle) -> Optional[dict]:
        """Extract job details from a Naukri job card."""
        try:
            job_data = {}
            
            # Title - try multiple selectors
            title_elem = await card.query_selector("a.title, .title a, h2 a")
            if title_elem:
                job_data['title'] = (await title_elem.inner_text()).strip()
            else:
                job_data['title'] = "Unknown"
            
            # Company
            company_elem = await card.query_selector(".companyInfo a, .comp-name, .company a")
            if company_elem:
                job_data['company'] = (await company_elem.inner_text()).strip()
            else:
                job_data['company'] = "Unknown"
            
            # Experience
            exp_elem = await card.query_selector(".expwdth, .experience, li.experience")
            if exp_elem:
                exp_text = await exp_elem.inner_text()
                job_data['experience'] = exp_text.strip()
            else:
                job_data['experience'] = "Not specified"
            
            # Salary
            salary_elem = await card.query_selector(".salary, .sal, li.salary")
            if salary_elem:
                salary_text = await salary_elem.inner_text()
                job_data['salary'] = salary_text.strip() if salary_text else None
            else:
                job_data['salary'] = None
            
            # Location
            location_elem = await card.query_selector(".locWdth, .location, li.location")
            if location_elem:
                location_text = await location_elem.inner_text()
                job_data['location'] = location_text.strip()
            else:
                job_data['location'] = "Not specified"
            
            # Description
            desc_elem = await card.query_selector(".job-description, .desc, .job-desc")
            if desc_elem:
                description = await desc_elem.inner_text()
                job_data['description'] = description.strip()
            else:
                job_data['description'] = "No description"
            
            # Skills - try tags first, then parse from description
            skills_elem = await card.query_selector(".tags, .skill-tags, ul.tags")
            if skills_elem:
                skills_text = await skills_elem.inner_text()
                job_data['skills'] = [s.strip() for s in skills_text.replace('\n', ',').split(',') if s.strip()]
            else:
                # Extract from description using skills parser
                job_data['skills'] = self.skills_parser.extract_from_text(job_data['description'])
            
            # URL
            link_elem = await card.query_selector("a.title, .title a, h2 a")
            if link_elem:
                href = await link_elem.get_attribute("href")
                if href:
                    if href.startswith('http'):
                        job_data['url'] = href
                    else:
                        job_data['url'] = f"https://www.naukri.com{href}"
                else:
                    job_data['url'] = ""
            else:
                job_data['url'] = ""
            
            # Job ID (extract from URL)
            if job_data['url']:
                match = re.search(r'-(\d+)(?:\?|$)', job_data['url'])
                job_data['job_id'] = match.group(1) if match else f"naukri_{int(time.time())}_{job_data['title'][:10]}"
            else:
                job_data['job_id'] = f"naukri_{int(time.time())}_{job_data['title'][:10]}"
            
            return job_data
            
        except Exception as e:
            print(f"⚠️  Error in _extract_job: {e}")
            return None


# Async function for use in async context
async def scrape_naukri_jobs_brightdata(keyword: str, limit: int = 50) -> List[JobModel]:
    """Async Naukri BrightData scraping for use in async context."""
    scraper = NaukriBrightDataScraper()
    try:
        jobs = await scraper.scrape_jobs(keyword, limit)
        return jobs
    finally:
        await scraper.disconnect()
