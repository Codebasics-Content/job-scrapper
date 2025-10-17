"""LinkedIn Unified Scraper - PARALLEL Producer-Consumer Architecture
EMD Compliance: ≤80 lines

Parallel Architecture (2 Windows Simultaneously):
1. Window 1 (Producer): Infinite scroll → store URLs to database (continuous)
2. Window 2 (Consumer): Read URLs from database → 5-concurrent detail scraping
3. Both run in parallel using asyncio.gather()
"""
from __future__ import annotations

import asyncio
import logging
from typing import List
from src.models.models import JobDetailModel
from .linkedin.infinite_scroll_scraper import scrape_linkedin_urls_infinite_scroll
from .linkedin.sequential_detail_scraper import scrape_job_details_sequential
from src.db.operations import JobStorageOperations

logger = logging.getLogger(__name__)


async def producer_task(
    keyword: str, 
    location: str, 
    limit: int, 
    headless: bool,
    producer_done: asyncio.Event
) -> None:
    """Window 1: Continuously scroll and produce URLs to database"""
    logger.info("🪟 Window 1 (Producer): Starting infinite scroll URL collection...")
    db_ops = JobStorageOperations()
    
    try:
        new_urls = await scrape_linkedin_urls_infinite_scroll(
            keyword=keyword,
            location=location,
            limit=limit,
            headless=headless
        )
        
        if new_urls:
            stored = db_ops.store_urls(new_urls)
            logger.info(f"✅ Window 1: Produced {stored} NEW URLs")
    finally:
        # Signal consumer that producer is done
        producer_done.set()
        logger.info("🚩 Window 1: Producer finished, signaling consumer to shutdown")


async def consumer_task(
    keyword: str, 
    limit: int, 
    headless: bool,
    producer_done: asyncio.Event
) -> List[JobDetailModel]:
    """Window 2: Keep window open, continuously consume URLs from database"""
    from playwright.async_api import async_playwright
    
    logger.info("🪟 Window 2 (Consumer): Starting 5-concurrent detail scraping...")
    db_ops = JobStorageOperations()
    job_details: List[JobDetailModel] = []
    
    # Give producer time to populate first batch
    await asyncio.sleep(5)
    
    # Create browser ONCE for reuse (prevents memory leak)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        logger.info("✅ Browser instance created (will be reused across all batches)")
        
        # KEEP WINDOW OPEN - continuous polling (FIFO queue behavior)
        while True:
            unscraped_urls = db_ops.get_unscraped_urls("linkedin", keyword, 5)  # Get 5 at a time
            details: List[JobDetailModel] = []
            
            if unscraped_urls:
                logger.info(f"📊 Window 2: Processing {len(unscraped_urls)} URLs (FIFO queue)")
                # Pass full tuples (url, job_id, platform, actual_role)
                details = await scrape_job_details_sequential(
                    urls=unscraped_urls,
                    headless=headless,
                    browser=browser,
                    context=context,
                    prefetch_size=5  # Keep 5 jobs in queue
                )
                
                # Store valid jobs (automatically marks them as scraped=1)
                stored_urls = set()
                if details:
                    stored = db_ops.store_details(details)
                    job_details.extend(details)
                    stored_urls = {d.url for d in details}
                    logger.info(f"✅ Window 2: Stored {stored} valid jobs (auto-marked scraped=1)")
                
                # Mark ONLY invalid/skipped URLs as scraped=1 (to avoid re-processing)
                all_urls = [u[0] for u in unscraped_urls]  # Extract URLs (index 0)
                skipped_urls = [url for url in all_urls if url not in stored_urls]
                if skipped_urls:
                    db_ops.mark_urls_scraped(skipped_urls)
                    logger.info(f"⏭️ Window 2: Marked {len(skipped_urls)} invalid/skipped URLs as scraped=1")
            else:
                # No URLs available - check if producer is done
                if producer_done.is_set():
                    logger.info("✅ Window 2: Producer finished and no more URLs - shutting down gracefully")
                    break
                # Producer still running - wait and poll again
                await asyncio.sleep(3)
    
    return job_details


async def scrape_linkedin_jobs_unified(
    keyword: str,
    location: str,
    limit: int = 200,
    headless: bool = False
) -> List[JobDetailModel]:
    """2-Window Parallel Scraper: Producer-Consumer Pattern with Shutdown Coordination"""
    logger.info("🚀 Starting PARALLEL scraping (2 windows simultaneously)")
    
    # Create shutdown coordination event
    producer_done = asyncio.Event()
    
    # Run both windows in parallel with shared event
    producer = asyncio.create_task(producer_task(keyword, location, limit, headless, producer_done))
    consumer = asyncio.create_task(consumer_task(keyword, limit, headless, producer_done))
    
    # Wait for both to complete gracefully
    results = await asyncio.gather(producer, consumer)
    
    logger.info("✅ Both windows completed - scraping finished")
    return results[1]  # Return consumer results


__all__ = [
    "scrape_linkedin_jobs_unified",
    "scrape_job_details_sequential",
    "scrape_linkedin_urls_infinite_scroll",
]
