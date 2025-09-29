#!/usr/bin/env python3
# YCombinator startup job scraper
# EMD Compliance: ≤80 lines

import asyncio
import logging
from typing import TYPE_CHECKING, override
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

from ..base.base_scraper import BaseJobScraper
from models.job import JobModel
from .extractor import extract_job_from_card

logger = logging.getLogger(__name__)

class YCombinatorScraper(BaseJobScraper):
    """YCombinator job board scraper with async support and rate limiting"""
    
    def __init__(self):
        super().__init__(platform_name="YCombinator")
        self.base_url: str = "https://www.worklist.fyi/companies?q="
    
    @override
    async def scrape_jobs(self, job_role: str, target_count: int, location: str = "") -> list[JobModel]:
        """Scrape YCombinator jobs with rate limiting and error handling"""
        
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
            
            search_url = f"{self.base_url}{job_role.replace(' ', '+')}"
            logger.info(f"Starting YCombinator scrape for: {job_role}")
            driver.get(search_url)
            
            # Wait for job cards to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".company-card, .job-card, [data-testid='company-card']")
            ))
            
            # Find job/company cards
            job_cards = driver.find_elements(
                By.CSS_SELECTOR, 
                ".company-card, .job-card, [data-testid='company-card'], .company-item"
            )
            logger.info(f"Found {len(job_cards)} YCombinator cards")
            
            for i, card in enumerate(job_cards[:target_count]):
                try:
                    if i > 0:
                        await asyncio.sleep(2)  # Rate limiting
                    
                    job = extract_job_from_card(card, job_role)
                    if job:
                        jobs.append(job)
                        logger.debug(f"Extracted job: {job.job_role} at {job.company}")
                        
                        if len(jobs) >= target_count:
                            break
                except Exception as e:
                    logger.warning(f"Failed to extract job from card {i}: {str(e)}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from YCombinator")
            
        except TimeoutException:
            logger.error("Timeout waiting for YCombinator page elements")
        except Exception as e:
            logger.error(f"Error scraping YCombinator jobs: {str(e)}")
        finally:
            if driver:
                self.return_driver(driver)
        
        return jobs
