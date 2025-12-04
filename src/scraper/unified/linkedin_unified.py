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

from src.db.operations import JobStorageOperations
from src.models.models import JobDetailModel

from .linkedin.infinite_scroll_scraper import scrape_linkedin_urls_infinite_scroll
from .linkedin.queue_based_scraper import scrape_job_details_queue_based
from .linkedin.sequential_detail_scraper import scrape_job_details_sequential
from .linkedin.staggered_queue_scraper import scrape_job_details_staggered

logger = logging.getLogger(__name__)


async def producer_task(
    keyword: str,
    location: str,
    limit: int,
    headless: bool,
    producer_done: asyncio.Event,
) -> None:
    """Window 1: Continuously scroll and produce URLs to database"""
    logger.info("🪟 Window 1 (Producer): Starting infinite scroll URL collection...")
    db_ops = JobStorageOperations()

    try:
        new_urls = await scrape_linkedin_urls_infinite_scroll(
            keyword=keyword, location=location, limit=limit, headless=headless
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
    producer_done: asyncio.Event,
    num_workers: int = 10,
    stagger_delay: float = 2.0,
) -> List[JobDetailModel]:
    """Window 2: Staggered queue-based 10-worker parallel scraping

    DSA Architecture:
    - Workers launch with staggered delays (0s, 2s, 4s, 6s... 18s)
    - FIFO Queue for pending jobs
    - Priority Queue (heapq) for 429 retry with exponential backoff
    - When worker finishes, immediately pulls next job from queue
    """

    logger.info(
        f"🪟 Window 2 (Consumer): Starting {num_workers}-worker STAGGERED scraping..."
    )
    logger.info(
        f"   Stagger pattern: Worker 0 at 0s, Worker 1 at {stagger_delay}s, Worker 2 at {stagger_delay * 2}s..."
    )

    db_ops = JobStorageOperations()
    job_details: List[JobDetailModel] = []

    # Give producer time to populate first batch
    await asyncio.sleep(5)

    # KEEP WINDOW OPEN - continuous polling (FIFO queue behavior)
    while True:
        # Get batch of URLs for staggered queue processing
        unscraped_urls = db_ops.get_unscraped_urls(
            "linkedin", keyword, 50
        )  # Get 50 at a time for queue
        details: List[JobDetailModel] = []

        if unscraped_urls:
            logger.info(
                f"📊 Window 2: Processing {len(unscraped_urls)} URLs with {num_workers} STAGGERED workers"
            )
            # Use STAGGERED queue scraper with DSA-optimized distribution
            details = await scrape_job_details_staggered(
                urls=unscraped_urls,
                headless=headless,
                num_workers=num_workers,
                stagger_delay=stagger_delay,
            )

            if details:
                job_details.extend(details)
                logger.info(f"✅ Window 2: Scraped {len(details)} jobs in this batch")

            # Mark all processed URLs as scraped
            stored_urls = {d.url for d in details} if details else set()
            all_urls = [u[0] for u in unscraped_urls]  # Extract URLs (index 0)
            skipped_urls = [url for url in all_urls if url not in stored_urls]
            if skipped_urls:
                await asyncio.to_thread(db_ops.mark_urls_scraped, skipped_urls)
                logger.info(
                    f"⏭️ Window 2: Marked {len(skipped_urls)} skipped URLs as scraped"
                )
        else:
            # No URLs available - check if producer is done
            if producer_done.is_set():
                logger.info(
                    "✅ Window 2: Producer finished and no more URLs - shutting down gracefully"
                )
                break
            # Producer still running - wait and poll again
            await asyncio.sleep(3)

    return job_details


async def scrape_linkedin_jobs_unified(
    keyword: str, location: str, limit: int = 200, headless: bool = False
) -> List[JobDetailModel]:
    """2-Window Parallel Scraper: Producer-Consumer Pattern with Shutdown Coordination"""
    logger.info("🚀 Starting PARALLEL scraping (2 windows simultaneously)")

    # Create shutdown coordination event
    producer_done = asyncio.Event()

    # Run both windows in parallel with shared event
    producer = asyncio.create_task(
        producer_task(keyword, location, limit, headless, producer_done)
    )
    consumer = asyncio.create_task(
        consumer_task(keyword, limit, headless, producer_done)
    )

    # Wait for both to complete gracefully
    results = await asyncio.gather(producer, consumer)

    logger.info("✅ Both windows completed - scraping finished")
    return results[1]  # Return consumer results


__all__ = [
    "scrape_linkedin_jobs_unified",
    "scrape_job_details_sequential",
    "scrape_job_details_queue_based",
    "scrape_job_details_staggered",
    "scrape_linkedin_urls_infinite_scroll",
]
