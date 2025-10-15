"""LinkedIn Detail Scraping via Playwright (Phase 2)
EMD Compliance: ≤80 lines, 5 concurrent contexts (Naukri pattern)
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import List
from playwright.async_api import async_playwright
from src.models import JobDetailModel, JobUrlModel
from src.db.operations import JobStorageOperations
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
from .selector_config import DETAIL_SELECTORS, WAIT_TIMEOUTS

logger = logging.getLogger(__name__)


async def scrape_linkedin_details_playwright(
    platform: str,
    input_role: str,
    limit: int = 100,
    store_to_db: bool = True,
) -> List[JobDetailModel]:
    """Phase 2: Extract LinkedIn job details with skills from JD"""
    
    db_ops = JobStorageOperations()
    
    # Get URLs to scrape
    url_models = db_ops.get_urls_to_scrape(platform, limit)
    logger.info(f"📋 Found {len(url_models)} URLs to scrape")
    
    if not url_models:
        return []
    
    # Initialize skills extractor
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    
    proxy_url = os.getenv("PROXY_URL")
    if not proxy_url or not proxy_url.startswith("wss://"):
        raise ValueError("PROXY_URL must be wss:// format")
    
    jobs: List[JobDetailModel] = []
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(proxy_url)
        
        # Concurrent scraping (5 tabs like Naukri)
        semaphore = asyncio.Semaphore(5)
        
        async def scrape_job(url_model: JobUrlModel) -> JobDetailModel | None:
            async with semaphore:
                try:
                    page = await browser.new_page()
                    await page.goto(url_model.url, timeout=WAIT_TIMEOUTS["navigation"])
                    
                    try:
                        show_more = await page.query_selector(DETAIL_SELECTORS["show_more_button"][0])
                        if show_more:
                            await show_more.click()
                            await asyncio.sleep(1)
                    except:
                        pass
                    
                    desc_elem = await page.query_selector(DETAIL_SELECTORS["description"][0])
                    description = await desc_elem.inner_text() if desc_elem else ""
                    
                    skills = extractor.extract(description) if len(description.strip()) > 50 else []
                    skill_str = ','.join([s for s in skills if isinstance(s, str)])
                    
                    await page.close()
                    
                    if skill_str:
                        return JobDetailModel(
                            job_id=url_model.job_id, platform=platform,
                            actual_role=input_role, url=url_model.url,
                            job_description=description[:2000], skills=skill_str,
                            company_name="", posted_date=None
                        )
                except Exception as e:
                    logger.warning(f"Failed {url_model.url}: {e}")
                return None
        
        tasks = [scrape_job(u) for u in url_models]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        jobs = [r for r in results if isinstance(r, JobDetailModel)]
        
        await browser.close()
    
    # Deduplicate and store
    if store_to_db and jobs:
        existing = db_ops.get_existing_urls([j.url for j in jobs])
        new_jobs = [j for j in jobs if j.url not in existing]
        db_ops.store_details(new_jobs)
        logger.info(f"✅ Stored {len(new_jobs)} NEW LinkedIn jobs")
    
    return jobs
