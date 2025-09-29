#!/usr/bin/env python3
# Indeed job scraper for Codebasics Job Scrapper
# EMD Compliance: ≤80 lines

import asyncio
import logging
from typing import TYPE_CHECKING, override
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

from ..base.base_scraper import BaseJobScraper
from .extractor import extract_job_from_card
from models.job import JobModel


logger = logging.getLogger(__name__)

class IndeedScraper(BaseJobScraper):
    """Indeed job scraper with rate limiting and error handling"""
    
    def __init__(self):
        super().__init__(platform_name="Indeed")
        self.base_url: str = "https://www.indeed.com"
        self.search_url: str = f"{self.base_url}/jobs"
    
    @override
    async def scrape_jobs(self, job_role: str, target_count: int, location: str = "") -> list[JobModel]:
        """Scrape jobs from Indeed for given job role"""
        
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
                
            search_query = f"{self.search_url}?q={job_role.replace(' ', '+')}"
            
            logger.info(f"Starting Indeed scrape for: {job_role}")
            driver.get(search_query)
            
            # Wait for job cards to load and get them
            self.wait_for_element(driver, ".job_seen_beacon", timeout=10)
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".job_seen_beacon")
            logger.info(f"Found {len(job_cards)} job cards on Indeed")
            
            for i, card in enumerate(job_cards[:target_count]):
                if i > 0 and i % 5 == 0:
                    await asyncio.sleep(2)  # Rate limiting
                
                job = extract_job_from_card(card, job_role)
                if job:
                    jobs.append(job)
                    logger.debug(f"Extracted job: {job.job_role} at {job.company}")
                    
                    if len(jobs) >= target_count:
                        break
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from Indeed")
            
        except TimeoutException:
            logger.error("Timeout waiting for Indeed page elements")
        except Exception as e:
            logger.error(f"Error scraping Indeed jobs: {str(e)}")
        finally:
            if driver:
                self.return_driver(driver)
        
        return jobs

    def wait_for_element(self, driver: 'WebDriver', selector: str, timeout: int = 10) -> None:
        """Wait for element to be present"""
        try:
            element_found = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if element_found:
                logger.debug(f"Element {selector} found successfully")
        except TimeoutException:
            logger.warning(f"Element {selector} not found within {timeout}s")
            raise
