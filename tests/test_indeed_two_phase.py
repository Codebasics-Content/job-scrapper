"""Test Indeed Two-Phase Scraper (URL → Details)"""
import asyncio
import logging
from src.scraper.unified.indeed import scrape_indeed_urls, scrape_indeed_details
from src.db.operations import JobStorageOperations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_indeed_two_phase() -> None:
    """Test Phase 1 (URLs) then Phase 2 (Details) for Indeed"""
    keyword = "AI Engineer"
    limit = 10
    
    # Phase 1: Scrape URLs
    logger.info(f"🔍 Phase 1: Scraping {limit} Indeed job URLs for '{keyword}'")
    url_models = await scrape_indeed_urls(
        keyword=keyword,
        location="United States",
        limit=limit,
        headless=False,
        store_to_db=True
    )
    logger.info(f"✅ Phase 1 Complete: {len(url_models)} URLs collected")
    
    # Phase 2: Scrape Details
    logger.info(f"📄 Phase 2: Scraping job details for unscraped URLs")
    detail_models = await scrape_indeed_details(
        platform="Indeed",
        input_role=keyword,
        limit=limit,
        headless=False,
        store_to_db=True
    )
    logger.info(f"✅ Phase 2 Complete: {len(detail_models)} job details scraped")
    
    # Verify data
    db_ops = JobStorageOperations()
    for job in detail_models[:3]:
        logger.info(f"\n📋 Sample Job:")
        logger.info(f"  Role: {job.actual_role}")
        logger.info(f"  Company: {job.company_name}")
        logger.info(f"  Skills: {job.skills[:100]}...")
        logger.info(f"  Description: {job.job_description[:150]}...")


if __name__ == "__main__":
    asyncio.run(test_indeed_two_phase())
