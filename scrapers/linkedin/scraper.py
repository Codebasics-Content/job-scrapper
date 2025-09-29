#!/usr/bin/env python3
# LinkedIn job scraper using API-based approach
# EMD Compliance: ≤80 lines

import asyncio
import logging
import urllib.parse
try:
    from typing import override
except ImportError:
    from typing_extensions import override

from ..base.base_scraper import BaseJobScraper
from .extractors.job_id_extractor import extract_job_ids_from_page
from .extractors.api_job_fetcher import fetch_job_via_api
from .extractors.scroll_handler import scroll_to_load_jobs
from models.job import JobModel

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseJobScraper):
    """LinkedIn job scraper using API endpoint for job details"""
    
    def __init__(self):
        super().__init__(platform_name="LinkedIn")
        self.base_url: str = "https://www.linkedin.com/jobs/search"
        self.setup_driver_pool()  # Initialize driver pool on creation

    @override
    async def scrape_jobs(
        self, 
        job_role: str, 
        target_count: int,
        location: str = ""
    ) -> list[JobModel]:
        """Scrape jobs using API-based approach
        
        Args:
            job_role: Job role to search for
            target_count: Number of jobs to scrape
            location: Location filter (empty for worldwide search)
        """
        logger.info(f"Starting API-based LinkedIn scrape for {target_count} {job_role} jobs")
        if location:
            logger.info(f"Location filter: {location}")
        
        jobs: list[JobModel] = []
        processed_ids: set[str] = set()  # Track all extracted IDs
        
        params = {
            'keywords': job_role,
            'f_TPR': 'r86400',
            'start': 0
        }
        
        # Only add location if provided
        if location:
            params['location'] = location
        
        # Build initial URL
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            # Get driver and load initial page
            driver = self.get_driver()
            if not driver:
                logger.error("Failed to get driver")
                return []
            
            try:
                driver.get(url)
                
                # Main scraping loop with scroll
                while len(jobs) < target_count:
                    # Extract job IDs from current page state
                    job_ids = extract_job_ids_from_page(driver)
                    
                    # Fetch details for new jobs
                    for job_id in job_ids:
                        if len(jobs) >= target_count:
                            break
                        
                        # Skip if already processed
                        if job_id in processed_ids:
                            continue
                        
                        processed_ids.add(job_id)
                        
                        job = await asyncio.get_event_loop().run_in_executor(
                            None, fetch_job_via_api, job_id, job_role
                        )
                        
                        if job:
                            jobs.append(job)
                            logger.info(f"Fetched job {len(jobs)}/{target_count}: {job.job_role}")
                        
                        await asyncio.sleep(0.5)
                    
                    # Break if target reached
                    if len(jobs) >= target_count:
                        break
                    
                    # Scroll to load more jobs
                    has_more = await asyncio.get_event_loop().run_in_executor(
                        None, scroll_to_load_jobs, driver, target_count, len(jobs)
                    )
                    
                    if not has_more:
                        logger.info("No more jobs available")
                        break
                    
                    await asyncio.sleep(2)
            finally:
                self.return_driver(driver)
                
        except Exception as error:
            logger.error(f"LinkedIn API scraping failed: {error}")
            
        logger.info(f"Completed: {len(jobs)} jobs with NLP-extracted skills")
        return jobs[:target_count]
    
