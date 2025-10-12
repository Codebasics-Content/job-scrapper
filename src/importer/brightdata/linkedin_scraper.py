# BrightData LinkedIn End-to-End Scraper - EMD Component
# Uses Web Datasets API for pre-collected LinkedIn data

import logging
from .linkedin_datasets_fetcher import fetch_linkedin_jobs_from_datasets
from .linkedin_importer import import_linkedin_jobs

logger = logging.getLogger(__name__)

async def scrape_and_import_linkedin_jobs(
    keyword: str,
    limit: int = 50,
    location: str = "Worldwide",
    db_path: str = "jobs.db"
) -> tuple[int, int]:
    """Complete workflow: Fetch → Parse → Extract Skills → Store
    
    Args:
        keyword: Job search keyword
        limit: Maximum jobs to fetch
        location: Job location filter
        db_path: Database path for storage
    
    Returns:
        (stored_count, duplicate_count)
    """
    logger.info(f"Starting LinkedIn dataset fetch: {keyword} (limit={limit})")
    
    # Step 1: Fetch pre-collected data from Web Datasets API
    brightdata_response = await fetch_linkedin_jobs_from_datasets(
        keyword, limit, location
    )
    
    if not brightdata_response:
        logger.warning("No jobs fetched from Web Datasets")
        return 0, 0
    
    # Step 2: Parse, extract skills, and store
    stored, duplicates = import_linkedin_jobs(brightdata_response, db_path)
    
    logger.info(
        f"✅ LinkedIn dataset fetch complete: {stored} stored, {duplicates} duplicates"
    )
    
    return stored, duplicates
