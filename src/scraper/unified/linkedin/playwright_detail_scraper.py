"""LinkedIn Detail Scraping via Playwright (Phase 2)
EMD Compliance: ≤80 lines, Naukri batching pattern
"""
from __future__ import annotations

import asyncio
import logging
from typing import List
from src.models import JobDetailModel, JobUrlModel
from src.db.operations import JobStorageOperations
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
from src.scraper.services.playwright_browser import PlaywrightBrowser
from .selector_config import DETAIL_SELECTORS, WAIT_TIMEOUTS

logger = logging.getLogger(__name__)


async def scrape_linkedin_details_playwright(
    platform: str,
    input_role: str,
    limit: int = 100,
    store_to_db: bool = True,
    headless: bool = False,
) -> List[JobDetailModel]:
    """Phase 2: Extract LinkedIn job details with Naukri batching pattern"""
    
    db_ops = JobStorageOperations()
    url_models = db_ops.get_urls_to_scrape(platform, limit)
    
    if not url_models:
        logger.info(f"No URLs to scrape for {platform}")
        return []
    
    logger.info(f"📋 Found {len(url_models)} URLs to scrape")
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    jobs: List[JobDetailModel] = []
    
    # Use PlaywrightBrowser service (same as Naukri)
    async with PlaywrightBrowser(headless=headless) as browser:
        concurrent_jobs = 5  # Same as Naukri
        
        # Process in batches (Naukri pattern)
        for batch_start in range(0, len(url_models), concurrent_jobs):
            batch = url_models[batch_start:batch_start + concurrent_jobs]
            
            async def scrape_job(url_model: JobUrlModel) -> JobDetailModel | None:
                try:
                    # Render URL using browser service
                    html = await browser.render_url(
                        url_model.url,
                        wait_seconds=2.0,
                        timeout_ms=WAIT_TIMEOUTS["navigation"],
                        wait_until='networkidle'
                    )
                    
                    # Extract description from HTML
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    desc_elem = soup.select_one(DETAIL_SELECTORS["description"][0])
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    skills = extractor.extract(description) if len(description.strip()) > 50 else []
                    skill_str = ','.join([s for s in skills if isinstance(s, str)])
                    
                    return JobDetailModel(
                        job_id=url_model.job_id,
                        platform=platform,
                        actual_role=url_model.actual_role,
                        url=url_model.url,
                        job_description=description,
                        skills=skill_str,
                        company_name="",
                        company_detail="",
                        posted_date=None
                    )
                except Exception as e:
                    logger.warning(f"Failed {url_model.url}: {e}")
                    return None
            
            # Gather batch results
            batch_results = await asyncio.gather(*[scrape_job(u) for u in batch])
            batch_jobs = [j for j in batch_results if j]
            jobs.extend(batch_jobs)
            
            # Store batch
            if store_to_db and batch_jobs:
                stored = db_ops.store_details(batch_jobs)
                logger.info(f"💾 Batch {batch_start // concurrent_jobs + 1}: {stored} stored")
            
            await asyncio.sleep(1.5)
            logger.info(f"📈 Progress: {len(jobs)}/{len(url_models)}")
    
    return jobs
