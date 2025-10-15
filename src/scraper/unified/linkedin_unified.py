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
    """Unified LinkedIn Playwright scraper with BrightData proxy
    
    Architecture:
    1. Connect via wss:// scraping_browser2 proxy
    2. Phase 1: Scroll job search, extract URLs (100 URLs in ~30s)
    3. Phase 2: Navigate to each job, extract JD + skills (~90s for 50 jobs)
    
    Args:
        keyword: Job role to search
        location: Location filter
        limit: Max jobs to scrape
        headless: Ignored (proxy controls browser)
    
    Returns:
        List of JobDetailModel with skills extracted from descriptions
    """
    
    # Phase 1: URL collection via Playwright scrolling
    url_models = await scrape_linkedin_urls_playwright(
        keyword=keyword,
        location=location,
        limit=limit,
        store_to_db=True,
    )
    logger.info(f"✅ Phase 1 (Playwright): Collected {len(url_models)} LinkedIn URLs")
    
    # Phase 2: Detail scraping with skills extraction
    jobs = await scrape_linkedin_details_playwright(
        platform="linkedin",
        input_role=keyword,
        limit=limit,
        store_to_db=True,
    )
    logger.info(f"✅ Phase 2 (Playwright): Scraped {len(jobs)} LinkedIn jobs with skills")
    
    return jobs


__all__ = [
    "scrape_linkedin_urls_playwright",
    "scrape_linkedin_details_playwright",
    "scrape_linkedin_jobs_unified",
]
