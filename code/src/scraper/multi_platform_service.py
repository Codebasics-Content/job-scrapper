# Multi-Platform Job Scraper Service - Centralized Skill Extraction
# 2-Platform Architecture: LinkedIn (JobSpy) + Naukri (Playwright)
from __future__ import annotations

import logging
from typing import List

from src.models.models import JobDetailModel
from .unified.linkedin_unified import scrape_linkedin_jobs_unified
from .unified.naukri_unified import scrape_naukri_jobs_unified

logger = logging.getLogger(__name__)


async def scrape_jobs_with_skills(
    platforms: list[str],
    keyword: str,
    location: str = "United States",
    limit: int = 100,
    headless: bool = False,
    store_to_db: bool = True,
) -> List[JobDetailModel]:
    """2-Platform scraper with Playwright unified architecture
    
    Platforms:
        - linkedin: Playwright unified (URL collection + detail scraping with skills)
        - naukri: Playwright unified (headless=False for anti-detection)
    
    Returns:
        List of JobDetailModel with skills extracted and stored
    """
    all_jobs: List[JobDetailModel] = []
    linkedin_requested = "linkedin" in platforms
    naukri_requested = "naukri" in platforms
    
    # Scrape LinkedIn via unified Playwright scraper
    if linkedin_requested:
        logger.info("Scraping LinkedIn via unified Playwright (2-phase: URLs + Details + Skills)...")
        linkedin_jobs = await scrape_linkedin_jobs_unified(
            keyword=keyword,
            location=location,
            limit=limit,
            headless=headless,
        )
        logger.info(f"✅ LinkedIn: Collected {len(linkedin_jobs)} jobs with skills")
        all_jobs.extend(linkedin_jobs)
    
    # Scrape Naukri via unified Playwright scraper
    if naukri_requested:
        logger.info("Scraping Naukri via unified Playwright (headless=False, visible browser)...")
        naukri_jobs = await scrape_naukri_jobs_unified(
            keyword=keyword,
            location=location,
            limit=limit,
            headless=False,
        )
        logger.info(f"✅ Naukri: Collected {len(naukri_jobs)} jobs with skills")
        all_jobs.extend(naukri_jobs)
    
    logger.info(f"Total jobs scraped: {len(all_jobs)} with skills extracted")
    if store_to_db:
        logger.info(f"✅ All {len(all_jobs)} jobs stored to database in batches")
    
    return all_jobs
