#!/usr/bin/env python3
"""Single Platform Job Scraper Test - Streamlit Integration Focus"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import logging
import pytest
from scrapers.linkedin import LinkedInScraper
from scrapers.indeed import IndeedScraper
from scrapers.naukri import NaukriScraper
from scrapers.ycombinator import YCombinatorScraper
from scrapers.base.driver_pool import WebDriverPool
from database.core.sqlite_manager import SQLiteManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_single_platform() -> None:
    """Test single platform scraper with database storage"""
    # Default test parameters
    platform = "LinkedIn"
    job_role = "AI Engineer"
    num_jobs = 10
    
    logger.info(f"Testing {platform} scraper for {num_jobs} {job_role} jobs")
    
    try:
        # Initialize database first
        db_manager = SQLiteManager("jobs.db")
        logger.info("Database initialized")
        
        scraper_map = {
            "LinkedIn": LinkedInScraper,
            "Indeed": IndeedScraper,
            "Naukri": NaukriScraper,
            "YCombinator": YCombinatorScraper
        }
        
        scraper_class = scraper_map.get(platform)
        if not scraper_class:
            logger.error(f"Platform {platform} not supported")
            return
        
        with scraper_class() as scraper:
            jobs = await scraper.scrape_jobs(job_role, num_jobs)
            logger.info(f"✅ Scraped {len(jobs)} jobs from {platform}")
            
            # Use database manager to store jobs
            stored = db_manager.store_jobs(jobs)
            logger.info(f"✅ Stored {stored} jobs in database")
        
    except Exception as error:
        logger.error(f"Test failed: {error}")
        WebDriverPool.cleanup_shared_browser()

if __name__ == "__main__":
    print("\n🧪 Testing LinkedIn scraper")
    print("Job Role: AI Engineer")
    print("Target Jobs: 10\n")
    
    asyncio.run(test_single_platform())
