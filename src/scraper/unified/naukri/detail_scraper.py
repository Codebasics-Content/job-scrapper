# Phase 2: Naukri Detail Scraping - Only unscraped jobs
# EMD Compliance: <=80 lines, Optimized deduplication via LEFT JOIN
from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from src.db.operations import JobStorageOperations
from src.models.models import JobDetailModel, JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser

from .parser import create_job_detail_model

logger = logging.getLogger(__name__)


async def scrape_naukri_details(
    platform: str,
    input_role: str,
    limit: int = 100,
    headless: bool = False,
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
        concurrent_jobs: int = 5

        for batch_start in range(0, len(unscraped), concurrent_jobs):
            batch = unscraped[batch_start:batch_start + concurrent_jobs]

            async def scrape_detail(
                jid: str, jurl: str, plat: str
            ) -> JobDetailModel | None:
                try:
                    detail_html: str = await browser.render_url(
                        jurl, wait_seconds=3.0, timeout_ms=60000, wait_until='networkidle'
                    )
                    job_detail: JobDetailModel | None = create_job_detail_model(
                        job_url=jurl,
                        html=detail_html,
                        title="",
                        company=""
                    )

                    if not job_detail:
                        logger.warning(f"Parser returned None for {jurl}")
                        return None

                    detail = JobDetailModel(
                        job_id=jid,
                        platform=plat,
                        actual_role=job_detail.actual_role,
                        url=jurl,
                        job_description=job_detail.job_description,
                        skills=job_detail.skills,
                        company_name=job_detail.company_name,
                        posted_date=job_detail.posted_date,
                        scraped_at=datetime.now(),
                    )
                    return detail
                except Exception as e:
                    logger.error(f"Error {jurl}: {e}")
                    return None

            batch_results = await asyncio.gather(
                *[scrape_detail(url, job_id, platform) for url, job_id, _, _ in batch]
            )
            batch_details: list[JobDetailModel] = [d for d in batch_results if d is not None]

            detail_models.extend(batch_details)

            if db_ops and batch_details:
                stored: int = await asyncio.to_thread(db_ops.store_details, batch_details)
                logger.info(f"Batch {batch_start // concurrent_jobs + 1}: {stored} details stored")

            await asyncio.sleep(1.5)
            logger.info(f"Progress: {len(detail_models)}/{len(unscraped)} jobs scraped")

    return detail_models
