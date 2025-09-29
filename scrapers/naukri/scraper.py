#!/usr/bin/env python3
# Naukri.com job scraper implementation
# EMD Compliance: ≤80 lines

import asyncio
import logging
from typing import TYPE_CHECKING, override
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

from ..base.base_scraper import BaseJobScraper
from models.job import JobModel
from .extractor import extract_job_from_card

logger = logging.getLogger(__name__)

class NaukriScraper(BaseJobScraper):
    """Async scraper for Naukri.com jobs with rate limiting"""
    
    def __init__(self):
        super().__init__(platform_name="Naukri")
        self.base_url: str = "https://www.naukri.com"

    @override
    async def scrape_jobs(self, job_role: str, target_count: int, location: str = "") -> list[JobModel]:
        """Scrape jobs from Naukri.com with async rate limiting"""
        
        jobs: list[JobModel] = []
        driver: 'WebDriver | None' = None
        
        try:
            # Ensure driver pool is initialized
            if not self.driver_pool.is_initialized:
                self.setup_driver_pool()
            
            driver = self.get_driver()
            if driver is None:
                logger.error("Failed to get driver from pool")
                return jobs
            
            search_url = f"{self.base_url}/{job_role.replace(' ', '-')}-jobs"
            logger.info(f"Starting Naukri scrape for: {job_role}")
            driver.get(search_url)
            
            # Wait for job listings to load
            await asyncio.sleep(3)
            
            # Find all job cards
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".srp-jobtuple-wrapper, .jobTuple")
            logger.info(f"Found {len(job_cards)} job cards on Naukri")
            
            for i, card in enumerate(job_cards[:target_count]):
                if i > 0 and i % 5 == 0:
                    await asyncio.sleep(2)  # Rate limiting
                
                job = extract_job_from_card(card, job_role)
                if job:
                    jobs.append(job)
                    logger.debug(f"Extracted job: {job.job_role} at {job.company}")
                    
                    if len(jobs) >= target_count:
                        break
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from Naukri")
            
        except TimeoutException:
            logger.error("Timeout waiting for Naukri page elements")
        except Exception as e:
            logger.error(f"Error scraping Naukri jobs: {str(e)}")
        finally:
            if driver:
                self.return_driver(driver)
        
        return jobs
