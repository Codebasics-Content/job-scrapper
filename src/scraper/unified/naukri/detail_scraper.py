# Phase 2: Naukri Detail Scraping - Only unscraped jobs
# EMD Compliance: ≤80 lines, Optimized deduplication via LEFT JOIN
from __future__ import annotations

import logging
import asyncio
from datetime import datetime

from src.models import JobDetailModel, JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.db.operations import JobStorageOperations
from .parser import create_job_model

logger = logging.getLogger(__name__)


async def scrape_naukri_details(
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

    # Query unscraped URLs (LEFT JOIN deduplication)
    unscraped = db_ops.get_unscraped_urls(platform, input_role, limit)
    if not unscraped:
        logger.info(f"No unscraped URLs for {platform}/{input_role}")
        return detail_models

    logger.info(f"Found {len(unscraped)} unscraped URLs, processing...")

    async with PlaywrightBrowser(headless=headless) as browser:
        concurrent_jobs = 5

        for batch_start in range(0, len(unscraped), concurrent_jobs):
            batch = unscraped[batch_start:batch_start + concurrent_jobs]

            async def scrape_detail(job_id: str, job_url: str) -> JobDetailModel | None:
                try:
                    detail_html = await browser.render_url(job_url, wait_seconds=3.0)
                    job_model = create_job_model(job_url, detail_html)

                    detail = JobDetailModel(
                        job_id=job_id,
                        platform=platform,
                        actual_role=job_model.job_role,
                        url=job_url,
                        job_description=job_model.jd[:2000],
                        skills=job_model.skills[:500],
                        company_name=job_model.company[:200],
                        company_detail=job_model.company_detail[:500],
                        posted_date=job_model.posted_date,
                        scraped_at=datetime.now(),
                    )
                    return detail
                except Exception as e:
                    logger.error(f"❌ Error {job_url}: {e}")
                    return None

            batch_results = await asyncio.gather(*[scrape_detail(jid, url) for jid, url in batch])
            batch_details = [d for d in batch_results if d]

            detail_models.extend(batch_details)

            if db_ops and batch_details:
                stored = db_ops.store_details(batch_details)
                logger.info(f"💾 Batch {batch_start // concurrent_jobs + 1}: {stored} details stored")

            await asyncio.sleep(1.5)
            logger.info(f"📈 Progress: {len(detail_models)}/{len(unscraped)} jobs scraped")

    return detail_models
