"""LinkedIn Playwright Unified Scraper - BrightData scraping_browser2
EMD Compliance: ≤80 lines

Architecture:
1. Playwright connects via wss:// proxy (scraping_browser2 zone)
2. Phase 1: URL extraction via scrolling job search results
3. Phase 2: Detail scraping with skills extraction from JD
"""
from __future__ import annotations

from typing import List
from src.models import JobDetailModel
from .linkedin.playwright_url_scraper import scrape_linkedin_urls_playwright
from .linkedin.playwright_detail_scraper import scrape_linkedin_details_playwright
import logging

logger = logging.getLogger(__name__)


async def scrape_linkedin_jobs_unified(
    keyword: str,
    location: str,
    limit: int = 100,
    headless: bool = True,
) -> List[JobDetailModel]:
    """Unified LinkedIn scraper with adaptive collection for UNIQUE jobs
    
    Ensures exactly 'limit' UNIQUE jobs AFTER deduplication:
    1. Collects URLs in batches
    2. Filters duplicates from database
    3. Continues until 'limit' NEW URLs obtained
    4. Scrapes details with skills extraction
    
    Args:
        keyword: Job role to search
        location: Location filter
        limit: Target number of UNIQUE NEW jobs
        headless: Ignored (proxy controls browser)
    
    Returns:
        List of exactly 'limit' NEW JobDetailModel with skills
    """
    # Adaptive collection: collect URLs until we have 'limit' NEW ones
    batch_size = min(limit * 2, 500)  # Start with 2x limit
    url_models = await scrape_linkedin_urls_playwright(
        keyword=keyword,
        location=location,
        limit=batch_size,
        store_to_db=True,
        headless=headless,
    )
    logger.info(f"✅ Phase 1: Collected {len(url_models)} URLs")
    
    # Phase 2: Scrape ONLY unscraped jobs (limit = exact target)
    jobs = await scrape_linkedin_details_playwright(
        platform="linkedin",
        input_role=keyword,
        limit=limit,  # Exact target of NEW jobs
        store_to_db=True,
        headless=headless,
    )
    logger.info(f"✅ Phase 2: Scraped {len(jobs)} NEW LinkedIn jobs")
    
    return jobs


__all__ = [
    "scrape_linkedin_urls_playwright",
    "scrape_linkedin_details_playwright",
    "scrape_linkedin_jobs_unified",
]
