"""Naukri API-Based Scraper - Session Transfer Architecture

Phase 1: URL extraction via API (5 concurrent, captcha bypass)
Phase 2: Detail scraping via API (5 concurrent, deduplication)
"""

from __future__ import annotations

import logging
from typing import List

from src.models.models import JobDetailModel

from .naukri.api_detail_scraper import scrape_naukri_details_api
from .naukri.api_url_scraper import scrape_naukri_urls_api

logger = logging.getLogger(__name__)


async def scrape_naukri_jobs_unified(
    keyword: str,
    location: str,
    limit: int = 100,
    headless: bool = False,  # Always visible browser to avoid rate limits
) -> List[JobDetailModel]:
    """Unified API-based Naukri scraper

    Architecture:
    1. Playwright establishes session (bypass captcha)
    2. Extract cookies for API authentication
    3. Phase 1: API URL extraction (5 concurrent pages)
    4. Phase 2: API detail scraping (5 concurrent jobs)
    """

    # Phase 1: API-based URL extraction
    url_models = await scrape_naukri_urls_api(
        keyword=keyword,
        location=location,
        limit=limit,
        headless=headless,
        store_to_db=True,
    )
    logger.info(f"✅ Phase 1 (API): Collected {len(url_models)} URLs")

    # Phase 2: API-based detail scraping with deduplication
    jobs = await scrape_naukri_details_api(
        platform="naukri",
        input_role=keyword,
        limit=limit,
        headless=headless,
        store_to_db=True,
    )
    logger.info(f"✅ Phase 2 (API): Scraped {len(jobs)} details")

    return jobs


__all__ = [
    "scrape_naukri_urls_api",
    "scrape_naukri_details_api",
    "scrape_naukri_jobs_unified",
]
