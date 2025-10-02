#!/usr/bin/env python3
# Phase 2: Fetch job details in parallel
# EMD Compliance: ≤80 lines

import asyncio
import logging
from collections.abc import Callable, Awaitable

from .api_job_fetcher import fetch_job_via_api
from src.models import JobModel
from src.scraper.config.delays import BATCH_SIZE, BATCH_DELAY

logger = logging.getLogger(__name__)

async def fetch_job_details_batch(
    job_ids: list[str],
    job_role: str,
    location_name: str,
    add_job_callback: Callable[[JobModel], Awaitable[bool]],
    should_stop_callback: Callable[[], bool],
    semaphore: asyncio.Semaphore,
    global_target: int = 0
) -> int:
    """Phase 2: Fetch job details for a batch of IDs in parallel
    
    Args:
        job_ids: List of job IDs to fetch details for
        job_role: Job role for API requests
        location_name: Location name for logging
        add_job_callback: Callback to add job to global list (returns True if target reached)
        should_stop_callback: Function to check if global target reached
        semaphore: Semaphore to limit concurrent workers
        
    Returns:
        Number of jobs successfully fetched
    """
    target_info = f" (target: {global_target})" if global_target > 0 else ""
    logger.info(f"[{location_name}] 🚀 Phase 2: Fetching details for {len(job_ids)} jobs{target_info}")
    
    fetched_count = 0
    job_counter = 0
    
    async def fetch_single_job(job_id: str) -> None:
        nonlocal fetched_count, job_counter
        
        if should_stop_callback():
            return
        
        async with semaphore:
            try:
                job_counter += 1
                current_job_num = job_counter
                
                # Fetch job details via API with progress tracking
                job = await fetch_job_via_api(
                    job_id, 
                    job_role,
                    job_number=current_job_num,
                    total_target=global_target
                )
                
                if job:
                    # Add to global job list
                    target_reached = await add_job_callback(job)
                    fetched_count += 1
                    
                    if target_reached:
                        logger.info(f"[{location_name}] 🎯 Target reached!")
                        return
                    
                    logger.debug(f"[{location_name}] ✅ Fetched job {job_id}")
                else:
                    logger.warning(f"[{location_name}] ⚠️ Failed to fetch job {job_id}")
                
            except Exception as error:
                logger.error(f"[{location_name}] ❌ Error fetching job {job_id}: {error}")
    
    # Process jobs in batches to avoid rate limiting
    total_batches = (len(job_ids) + BATCH_SIZE - 1) // BATCH_SIZE
    logger.info(f"[{location_name}] Processing {len(job_ids)} jobs in {total_batches} batches of {BATCH_SIZE}")
    
    all_results = []
    for batch_num in range(total_batches):
        if should_stop_callback():
            break
            
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(job_ids))
        batch_ids = job_ids[start_idx:end_idx]
        
        logger.info(f"[{location_name}] Batch {batch_num + 1}/{total_batches}: Processing {len(batch_ids)} jobs")
        
        # Create tasks for current batch only
        batch_tasks = [asyncio.create_task(fetch_single_job(job_id)) for job_id in batch_ids]
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        all_results.extend(batch_results)
        
        # Delay between batches to avoid rate limiting (except for last batch)
        if batch_num < total_batches - 1:
            logger.info(f"[{location_name}] Waiting {BATCH_DELAY}s before next batch...")
            await asyncio.sleep(BATCH_DELAY)
    
    # Log any exceptions that occurred during fetching
    exception_count = sum(1 for r in all_results if isinstance(r, Exception))
    if exception_count > 0:
        logger.warning(f"[{location_name}] ⚠️ {exception_count} tasks failed with exceptions")
    
    if global_target > 0:
        logger.info(f"[{location_name}] ✅ Phase 2 complete: {fetched_count} jobs scraped (target: {global_target})")
    else:
        logger.info(f"[{location_name}] ✅ Phase 2 complete: {fetched_count}/{len(job_ids)} jobs fetched")
    return fetched_count
