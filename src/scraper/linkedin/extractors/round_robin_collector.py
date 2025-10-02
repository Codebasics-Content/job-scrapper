#!/usr/bin/env python3
# Round-robin job ID collector
# EMD Compliance: ≤80 lines

import asyncio
import logging
from selenium.webdriver.remote.webdriver import WebDriver

from .job_id_extractor import extract_job_ids_from_page

logger = logging.getLogger(__name__)

async def collect_one_id_from_country(
    driver: WebDriver,
    base_url: str,
    job_role: str,
    location_name: str,
    geo_id: str | None,
    processed_ids: set[str],
    page_cache: dict[str, list[str]]
) -> str | None:
    """Collect one job ID from a country
    
    Returns:
        Single job ID or None if no more available
    """
    cache_key = f"{location_name}_{geo_id or 'no_geo'}"
    
    # Use cached IDs first
    if cache_key in page_cache and page_cache[cache_key]:
        while page_cache[cache_key]:
            job_id = page_cache[cache_key].pop(0)
            if job_id not in processed_ids:
                processed_ids.add(job_id)
                return job_id
    
    # Load new page if cache empty
    try:
        import urllib.parse
        params = {
            'keywords': job_role,
            'f_TPR': 'r2592000',
            'start': 0
        }
        if geo_id:
            params['geoId'] = geo_id
        
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        driver.get(url)
        await asyncio.sleep(2)  # Fast 2-second load
        
        page_ids = extract_job_ids_from_page(driver)
        logger.info(f"[{location_name}] Loaded {len(page_ids)} new IDs")
        
        # Cache and return first unique
        page_cache[cache_key] = page_ids
        
        while page_cache[cache_key]:
            job_id = page_cache[cache_key].pop(0)
            if job_id not in processed_ids:
                processed_ids.add(job_id)
                return job_id
                
    except Exception as error:
        logger.error(f"[{location_name}] Failed to load IDs: {error}")
    
    return None
