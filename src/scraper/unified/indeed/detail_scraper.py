# Phase 2: Indeed Detail Scraping - Only unscraped jobs
# EMD Compliance: ≤80 lines, Optimized deduplication via LEFT JOIN
from __future__ import annotations

import logging
import asyncio

from src.models import JobDetailModel, JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.db.operations import JobStorageOperations
from .parser import create_job_detail_model

logger = logging.getLogger(__name__)


async def scrape_indeed_details(
    platform: str,
    input_role: str,
    limit: int = 100,
    headless: bool = True,
    store_to_db: bool = True,
) -> list[JobDetailModel]:
    """Phase 2: Scrape full job details only for URLs not in jobs table"""
    detail_models: list[JobDetailModel] = []
    db_ops = JobStorageOperations() if store_to_db else None

    if not db_ops:
        logger.error("Database operations required for Phase 2")
        return detail_models

    # Normalize input_role to match database format
    normalized_role = JobUrlModel.normalize_role(input_role)
    
    # Query unscraped URLs (LEFT JOIN deduplication)
    unscraped = db_ops.get_unscraped_urls(platform, normalized_role, limit)
    if not unscraped:
        logger.info(f"No unscraped URLs for {platform}/{normalized_role}")
        return detail_models

    logger.info(f"Found {len(unscraped)} unscraped URLs, processing...")

    async with PlaywrightBrowser(headless=headless) as browser:
        concurrent_jobs = 5

        for batch_start in range(0, len(unscraped), concurrent_jobs):
            batch = unscraped[batch_start:batch_start + concurrent_jobs]

            async def scrape_detail(job_url: str, job_id: str, platform: str, actual_role: str) -> JobDetailModel | None:
                try:
                    detail_html = await browser.render_url(job_url, wait_seconds=3.0, wait_until='domcontentloaded')
                    if not detail_html:
                        return None
                    return create_job_detail_model(job_id, platform, actual_role, job_url, detail_html)
                except Exception as e:
                    logger.error(f"Failed to scrape {job_url}: {e}")
                    return None

            results = await asyncio.gather(*[scrape_detail(*u) for u in batch])
            batch_details = [r for r in results if r]
            
            if batch_details and db_ops:
                stored = db_ops.store_details(batch_details)
                logger.info(f"💾 Batch {batch_start//concurrent_jobs + 1}: {stored} details stored")
                detail_models.extend(batch_details)
                logger.info(f"📈 Progress: {len(detail_models)}/{len(unscraped)} jobs scraped")

            await asyncio.sleep(2.0)

    return detail_models
