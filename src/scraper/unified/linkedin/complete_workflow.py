"""Complete LinkedIn Workflow: URL Collection → n+5 Rolling Window
Phase 1: Collect 1000+ URLs (5 concurrent tabs)
Phase 2: Process with n+5 rolling window (5 concurrent tabs)
"""
from __future__ import annotations

import logging
from typing import List
from src.models.models import JobDetailModel
from .playwright_url_scraper import scrape_linkedin_urls_playwright
from .rolling_window_scraper import rolling_window_n_plus_5

logger = logging.getLogger(__name__)


async def complete_linkedin_workflow(
    keyword: str = "AI Engineer",
    location: str = "",
    target_jobs: int = 1000,
    window_size: int = 5,
    headless: bool = False,
) -> List[JobDetailModel]:
    """Complete workflow: URLs → Rolling Window Processing
    
    Phase 1: 5 tabs collect 1000+ URLs
    Phase 2: n+5 rolling window processes all URLs
    """
    logger.info("="*80)
    logger.info("🚀 COMPLETE LINKEDIN WORKFLOW")
    logger.info("="*80)
    
    # Phase 1: Collect URLs
    logger.info("\n📍 PHASE 1: URL Collection (5 concurrent tabs)")
    logger.info(f"   Target: {target_jobs} URLs")
    
    url_models = await scrape_linkedin_urls_playwright(
        keyword=keyword,
        location=location,
        limit=target_jobs,
        store_to_db=True,
        headless=headless,
    )
    logger.info(f"✅ Phase 1 Complete: {len(url_models)} URLs collected")
    
    # Phase 2: n+5 Rolling Window
    logger.info("\n📍 PHASE 2: n+5 Rolling Window Detail Scraping")
    logger.info(f"   Pattern: Job n → Job n+5")
    logger.info(f"   Window Size: {window_size} concurrent")
    
    jobs = await rolling_window_n_plus_5(
        platform="linkedin",
        input_role=keyword,
        total_jobs=target_jobs,
        window_size=window_size,
        headless=headless,
    )
    
    logger.info("\n✅ WORKFLOW COMPLETE")
    logger.info(f"   URLs Collected: {len(url_models)}")
    logger.info(f"   Jobs Processed: {len(jobs)}")
    logger.info(f"   Success Rate: {(len(jobs)/len(url_models))*100:.1f}%")
    
    return jobs
