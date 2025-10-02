#!/usr/bin/env python3
# Phase 1: Collect job IDs with pagination
# EMD Compliance: ≤80 lines

import asyncio
import logging
import urllib.parse
from collections.abc import Callable
from selenium.webdriver.remote.webdriver import WebDriver

from .job_id_extractor import extract_job_ids_from_page
from .scroll_handler import scroll_to_load_jobs

logger = logging.getLogger(__name__)

async def collect_job_ids(
    driver: WebDriver,
    base_url: str,
    job_role: str,
    location_name: str,
    target_count: int,
    processed_ids: set[str],
    should_stop_callback: Callable[[], bool],
    geo_id: str | None = None
) -> list[str]:
    """Phase 1: Collect job IDs with pagination (no detail fetching)
    
    Args:
        driver: Selenium WebDriver instance
        base_url: LinkedIn jobs search base URL
        job_role: Job role to search for
        location_name: Location name for logging
        target_count: Target number of unique IDs to collect
        processed_ids: Global set of processed job IDs
        should_stop_callback: Function to check if global target reached
        geo_id: Optional geoId for location filtering
        
    Returns:
        List of unique job IDs collected
    """
    logger.info(f"[{location_name}] 🔍 Phase 1: Collecting job IDs (target: {target_count})")
    
    collected_ids: list[str] = []
    
    # Build URL with optional geoId
    params = {
        'keywords': job_role,
        'f_TPR': 'r2592000',
        'start': 0
    }
    
    if geo_id:
        params['geoId'] = geo_id
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        driver.get(url)
        await asyncio.sleep(3)
        
        # Pagination loop - collect IDs only
        while len(collected_ids) < target_count:
            if should_stop_callback():
                logger.info(f"[{location_name}] ⏹️ Stopping - global target reached")
                break
            
            # Extract IDs from current page
            page_ids = extract_job_ids_from_page(driver)
            logger.info(f"[{location_name}] Found {len(page_ids)} IDs on page")
            
            # Add unique IDs (stop at target)
            for job_id in page_ids:
                if len(collected_ids) >= target_count:
                    break  # Stop once target reached
                if job_id not in processed_ids and job_id not in collected_ids:
                    collected_ids.append(job_id)
                    processed_ids.add(job_id)
            
            logger.info(f"[{location_name}] 📊 Collected {len(collected_ids)}/{target_count} unique IDs")
            
            if len(collected_ids) >= target_count:
                break
            
            # Scroll to load more jobs
            has_more = await asyncio.get_event_loop().run_in_executor(
                None, scroll_to_load_jobs, driver, target_count, len(collected_ids)
            )
            
            if not has_more:
                logger.info(f"[{location_name}] ⚠️ No more jobs to load")
                break
            
            await asyncio.sleep(2)
    
    except Exception as error:
        logger.error(f"[{location_name}] ❌ ID collection failed: {error}")
    
    logger.info(f"[{location_name}] ✅ Phase 1 complete: {len(collected_ids)} IDs collected")
    return collected_ids
