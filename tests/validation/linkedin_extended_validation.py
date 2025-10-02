"""LinkedIn Extended Validation - 500+ Jobs Test
Tests scraper at scale across multiple countries.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
import time
import logging
from datetime import datetime
from src.scraper.linkedin.scraper import LinkedInScraper
from src.db import JobStorageOperations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def validate_linkedin_scale():
    """Test LinkedIn scraper with 500+ jobs across multiple countries."""
    
    # Test configuration
    job_role = "Data Scientist"
    countries = ["India", "United States", "United Kingdom"]
    target_jobs = 500
    
    logger.info(f"Starting extended validation: {target_jobs}+ jobs")
    logger.info(f"Countries: {', '.join(countries)}")
    
    start_time = time.time()
    total_scraped = 0
    total_stored = 0
    errors = []
    
    storage = JobStorageOperations("jobs.db")
    
    for country in countries:
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Testing {country}...")
            logger.info(f"{'='*60}")
            
            country_start = time.time()
            
            scraper = LinkedInScraper(job_role=job_role, country=country)
            jobs = await scraper.scrape_jobs(target_count=200)
            
            country_time = time.time() - country_start
            
            # Store jobs
            stored = storage.store_jobs_batch(jobs)
            
            total_scraped += len(jobs)
            total_stored += stored
            
            logger.info(f"✓ {country}: {len(jobs)} scraped, {stored} stored")
            logger.info(f"  Time: {country_time:.1f}s")
            logger.info(f"  Rate: {len(jobs)/(country_time/60):.1f} jobs/min")
            
        except Exception as e:
            error_msg = f"{country}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"✗ {error_msg}")
    
    # Final results
    total_time = time.time() - start_time
    
    logger.info(f"\n{'='*60}")
    logger.info(f"VALIDATION COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Total Scraped: {total_scraped} jobs")
    logger.info(f"Total Stored: {total_stored} jobs")
    logger.info(f"Duplicates: {total_scraped - total_stored}")
    logger.info(f"Total Time: {total_time:.1f}s ({total_time/60:.1f}min)")
    logger.info(f"Overall Rate: {total_scraped/(total_time/60):.1f} jobs/min")
    logger.info(f"Errors: {len(errors)}")
    
    if errors:
        logger.error("\nErrors encountered:")
        for error in errors:
            logger.error(f"  - {error}")
    
    # Performance assessment
    if total_scraped >= target_jobs:
        logger.info("\n✓ VALIDATION PASSED: Target reached")
    else:
        logger.warning(f"\n⚠ VALIDATION PARTIAL: {total_scraped}/{target_jobs}")
    
    return {
        "total_scraped": total_scraped,
        "total_stored": total_stored,
        "duplicates": total_scraped - total_stored,
        "total_time_seconds": total_time,
        "rate_jobs_per_minute": total_scraped/(total_time/60),
        "errors": errors,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    results = asyncio.run(validate_linkedin_scale())
    print(f"\nValidation Results: {results}")
