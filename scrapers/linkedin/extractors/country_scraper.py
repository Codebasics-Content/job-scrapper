#!/usr/bin/env python3
# Country-specific LinkedIn scraper
# EMD Compliance: ≤80 lines

import asyncio
import logging
import urllib.parse
from collections.abc import Callable
from selenium.webdriver.remote.webdriver import WebDriver

from .job_id_extractor import extract_job_ids_from_page
from .api_job_fetcher import fetch_job_via_api
from .scroll_handler import scroll_to_load_jobs
from models.job import JobModel

logger = logging.getLogger(__name__)

async def scrape_country_jobs(
    driver: WebDriver,
    base_url: str,
    job_role: str,
    country: dict[str, str],
    target_count: int,
    processed_ids: set[str],
    should_stop_callback: Callable[[], bool]
) -> list[JobModel]:
    """Scrape jobs from specific country using geoId
    
    Args:
        driver: Selenium WebDriver instance
        base_url: LinkedIn jobs search base URL
        job_role: Job role to search for
        country: Country dict with name and geoId
        target_count: Number of jobs to scrape for this country
        processed_ids: Global set of already processed job IDs
        should_stop_callback: Function to check if global target reached
        
    Returns:
        List of scraped jobs from this country
    """
    logger.info(f"Scraping {country['name']} for {job_role}")
    
    jobs: list[JobModel] = []
    
    # Build URL with geoId
    params = {
        'keywords': job_role,
        'f_TPR': 'r2592000',  # Last month
        'start': 0
    }
    
    # Add geoId only if not empty (empty = worldwide)
    if country['geoId']:
        params['geoId'] = country['geoId']
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        driver.get(url)
        await asyncio.sleep(3)  # Wait for page load
        
        # Scraping loop
        while len(jobs) < target_count:
            # Check if global target reached by other countries
            if should_stop_callback():
                logger.info(f"{country['name']}: Stopping - global target reached")
                break
            
            job_ids = extract_job_ids_from_page(driver)
            logger.info(f"[{country['name']}] Processing {len(job_ids)} job IDs...")
            
            for job_id in job_ids:
                if len(jobs) >= target_count or should_stop_callback():
                    break
                    
                if job_id in processed_ids:
                    logger.debug(f"[{country['name']}] Skipping duplicate job ID: {job_id}")
                    continue
                    
                processed_ids.add(job_id)
                logger.info(f"[{country['name']}] 🔍 Fetching job details for ID: {job_id}")
                
                job = await asyncio.get_event_loop().run_in_executor(
                    None, fetch_job_via_api, job_id, job_role
                )
                
                if job:
                    jobs.append(job)
                    logger.info(f"[{country['name']}] ✅ Job added ({len(jobs)}/{target_count})")
                else:
                    logger.warning(f"[{country['name']}] ⚠️ Failed to fetch job {job_id}")
                    
                await asyncio.sleep(0.5)
            
            if len(jobs) >= target_count:
                break
                
            has_more = await asyncio.get_event_loop().run_in_executor(
                None, scroll_to_load_jobs, driver, target_count, len(jobs)
            )
            
            if not has_more:
                break
                
            await asyncio.sleep(2)
    
    except Exception as error:
        logger.error(f"Country {country['name']} scraping failed: {error}")
    
    return jobs
