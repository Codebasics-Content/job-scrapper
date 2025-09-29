#!/usr/bin/env python3
# YCombinator job scraping operations
# EMD Compliance: ≤80 lines for scraping logic

import asyncio
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from models.job import JobModel
from ..extractor import extract_job_from_card

logger = logging.getLogger(__name__)

class YCJobScraper:
    """Handle YCombinator job scraping operations"""
    
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
    
    async def scrape_jobs(self, job_role: str, max_jobs: int = 20) -> list[JobModel]:
        """Scrape YCombinator jobs with rate limiting"""
        jobs = []
        search_url = self._build_search_url(job_role)
        
        try:
            logger.info(f"Scraping YCombinator jobs for: {job_role}")
            self.driver.get(search_url)
            
            job_cards = await self._wait_and_find_cards()
            logger.info(f"Found {len(job_cards)} YCombinator cards")
            
            jobs = await self._extract_jobs_from_cards(job_cards, job_role, max_jobs)
            
        except TimeoutException:
            logger.error("Timeout waiting for YCombinator page to load")
        except Exception as error:
            logger.error(f"Error during YCombinator scraping: {str(error)}")
        
        logger.info(f"Successfully scraped {len(jobs)} YCombinator jobs")
        return jobs
    
    def _build_search_url(self, job_role: str) -> str:
        """Build search URL for YCombinator job board"""
        base_url = "https://www.worklist.fyi/companies?q="
        return f"{base_url}{job_role.replace(' ', '+')}"
    
    async def _wait_and_find_cards(self) -> list:
        """Wait for and locate job cards on the page"""
        wait = WebDriverWait(self.driver, self.timeout)
        selector = ".company-card, .job-card, [data-testid='company-card']"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
        return self.driver.find_elements(
            By.CSS_SELECTOR, 
            ".company-card, .job-card, [data-testid='company-card'], .company-item"
        )
    
    async def _extract_jobs_from_cards(
        self, 
        cards: list, 
        job_role: str, 
        max_jobs: int
    ) -> list[JobModel]:
        """Extract job data from cards with rate limiting"""
        jobs = []
        
        for index, card in enumerate(cards[:max_jobs]):
            try:
                if index > 0:
                    await asyncio.sleep(2)  # Rate limiting
                
                job = extract_job_from_card(card, job_role)
                if job:
                    jobs.append(job)
                    logger.debug(f"Extracted: {job.job_role} at {job.company}")
                    
            except Exception as error:
                logger.warning(f"Failed to extract job from card {index}: {str(error)}")
                continue
        
        return jobs
