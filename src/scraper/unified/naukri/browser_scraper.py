"""Naukri Browser Scraper - Direct HTML extraction via Playwright
EMD Compliance: ≤80 lines, browser automation
"""
from __future__ import annotations
from typing import List
from bs4 import BeautifulSoup
from src.models import JobDetailModel, JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser
import asyncio
import logging

logger = logging.getLogger(__name__)


async def scrape_naukri_jobs_browser(
    keyword: str,
    location: str = "",
    limit: int = 20,
    headless: bool = False
) -> List[JobDetailModel]:
    """Scrape Naukri jobs using direct browser HTML extraction"""
    
    jobs: List[JobDetailModel] = []
    search_url = f"https://www.naukri.com/{keyword.lower().replace(' ', '-')}-jobs"
    
    async with PlaywrightBrowser(headless=headless) as browser:
        try:
            # Render search page
            html = await browser.render_url(search_url, wait_seconds=3.0)
            
            if not html:
                logger.error("Failed to render search page")
                return jobs
            
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find job cards - try multiple selectors
            selectors = [
                '.cust-job-tuple',
                'article.jobTuple',
                'article[data-job-id]'
            ]
            
            job_cards = []
            for selector in selectors:
                job_cards = soup.select(selector)
                if job_cards:
                    logger.info(f"Found {len(job_cards)} jobs using selector: {selector}")
                    break
            
            # Extract job data
            for card in job_cards[:limit]:
                try:
                    # Extract title
                    title_elem = card.select_one('.title, .jobTuple-title a, [class*="title"]')
                    title = title_elem.text.strip() if title_elem else "Unknown Title"
                    
                    # Extract URL
                    link_elem = card.select_one('a[href*="job-listings"]')
                    href = link_elem.get('href', '') if link_elem else ''
                    url = href if href.startswith('http') else f"https://www.naukri.com{href}"
                    
                    # Extract company (2025 Naukri: .comp-name inside .comp-dtls-wrap)
                    company_elem = card.select_one('.comp-name, .companyInfo, [class*="company"]')
                    company = company_elem.text.strip() if company_elem else "Unknown Company"
                    
                    # Generate job_id from URL
                    job_id = JobUrlModel.generate_job_id("naukri", url) if url else JobUrlModel.generate_job_id("naukri", f"{title}-{company}")
                    
                    # Extract posted date (2025 Naukri: .job-post-day)
                    date_elem = card.select_one('.job-post-day, [class*="date"], [class*="post"]')
                    posted_date = date_elem.text.strip() if date_elem else None
                    
                    jobs.append(JobDetailModel(
                        job_id=job_id,
                        platform="naukri",
                        actual_role=title,
                        url=url,
                        job_description="",
                        company_name=company,
                        posted_date=posted_date
                    ))
                    
                except Exception as e:
                    logger.warning(f"Failed to parse job card: {e}")
                    continue
            
            logger.info(f"✅ Scraped {len(jobs)} jobs from Naukri browser")
            
            # Enrich with parallel page scraping (5 concurrent tabs)
            if jobs:
                jobs = await _enrich_parallel_pages(jobs, browser)
            
        except Exception as e:
            logger.error(f"Browser scraping failed: {e}")
    
    return jobs[:limit]


async def _enrich_parallel_pages(
    jobs: List[JobDetailModel], browser: PlaywrightBrowser
) -> List[JobDetailModel]:
    """Enrich jobs by scraping individual pages in parallel (5 tabs)"""
    try:
        # Create 5 concurrent tasks (semaphore limits to 5 at once)
        semaphore = asyncio.Semaphore(5)
        tasks = [_scrape_job_page(job, browser, semaphore) for job in jobs]
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"✅ Enriched {len(jobs)} jobs via parallel page scraping")
    except Exception as e:
        logger.warning(f"Parallel page scraping failed: {e}")
    return jobs


async def _scrape_job_page(
    job: JobDetailModel, browser: PlaywrightBrowser, semaphore: asyncio.Semaphore
) -> None:
    """Scrape individual job page for description and skills"""
    async with semaphore:
        page = None
        try:
            page = await browser.new_page()
            await page.goto(job.url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract description (more specific selectors)
            desc_elem = soup.select_one('.styles_JDC__dang-inner-html__h0K4t, [class*="job-description"], .dang-inner-html')
            if not desc_elem:
                desc_elem = soup.select_one('.job-description, section[class*="job"] p, div[class*="description"] p')
            if desc_elem:
                job.job_description = desc_elem.get_text(separator=" ", strip=True)[:2000]
            
            # Extract skills (target skill chips/tags specifically)
            skills_container = soup.select_one('.styles_jhc__key-skill__DKjCg, [class*="key-skill"], .key-skill')
            if skills_container:
                skills_elems = skills_container.select('a, span.chip, .chip-text')
                skills = [s.get_text(strip=True) for s in skills_elems if s.get_text(strip=True)][:10]
                job.skills = ",".join(skills)
                
        except Exception as e:
            logger.warning(f"Failed to scrape {job.url}: {e}")
        finally:
            if page:
                await page.close()
