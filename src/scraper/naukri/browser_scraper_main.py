#!/usr/bin/env python3
# Main Naukri browser scraper - refactored for EMD compliance
# EMD Compliance: ≤80 lines

import logging
from typing import List

from src.scraper.base.base_scraper import BaseJobScraper
from .extractors.card_extractor import NaukriCardExtractor
from .extractors.job_detail_fetcher import NaukriJobDetailFetcher
from .extractors.api_parser import NaukriAPIParser
from src.scraper.base.skill_validator import SkillValidator
from src.models import JobModel
from .types import BatchConfig
from .browser_manager import BrowserManager
from .batch_processor import BatchProcessor

logger = logging.getLogger(__name__)


class NaukriBrowserScraper(BaseJobScraper):
    """EMD-compliant Naukri.com browser-based job scraper."""
    
    BASE_URL: str = "https://www.naukri.com"
    
    def __init__(self, browser_manager: BrowserManager) -> None:
        self.browser_manager = browser_manager
        self.card_extractor = NaukriCardExtractor()
        self.skill_validator = SkillValidator()
        self.job_detail_fetcher = NaukriJobDetailFetcher()
        self.api_parser = NaukriAPIParser()
        
        batch_config: BatchConfig = {
            "batch_size": 20,
            "max_retries": 3,
            "timeout_seconds": 30,
            "memory_cleanup_threshold": 100
        }
        self.batch_processor = BatchProcessor(batch_config)
    
    def _build_search_url(self, job_role: str, location: str = "") -> str:
        """Build Naukri search URL with encoded parameters."""
        base_url = f"{self.BASE_URL}/jobs"
        encoded_role = job_role.replace(" ", "%20")
        if location:
            encoded_location = location.replace(" ", "%20")
            return f"{base_url}?q={encoded_role}&l={encoded_location}"
        return f"{base_url}?q={encoded_role}"
    
    async def scrape_jobs(
        self,
        job_role: str,
        target_count: int,
        location: str = ""
    ) -> List[JobModel]:
        """Main scraping method using batch processing."""
        logger.info(f"[NAUKRI] Starting batch scraping for '{job_role}'")
        
        self.browser_manager.setup_driver_pool()
        driver = self.browser_manager.get_driver()
        
        if not driver:
            logger.error("[NAUKRI] Failed to get driver")
            return []
        
        try:
            # Build search URL for Naukri
            search_url = self._build_search_url(job_role, location)
            logger.info(f"[NAUKRI] Navigating to: {search_url}")
            
            driver.get(search_url)
            all_jobs: List[JobModel] = []
            
            # Focus: Extract job cards and process them for description + companyDetails
            from selenium.webdriver.common.by import By
            
            # Use hardcoded selectors from memory for 2025 Naukri structure  
            JOB_CARD_SELECTORS = [
                "article.jobTuple",
                ".cust-job-tuple", 
                "article[data-job-id]",
                ".list article"
            ]
            
            # Find job cards using configured selectors
            job_cards = []
            for selector in JOB_CARD_SELECTORS:
                try:
                    logger.info(f"[NAUKRI] Trying job card selector: {selector}")
                    cards = driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        job_cards = cards
                        logger.info(f"[NAUKRI] Found {len(job_cards)} job cards with selector: {selector}")
                        break
                except Exception as selector_error:
                    logger.warning(f"[NAUKRI] Selector failed {selector}: {selector_error}")
                    continue
            
            # Extract data from each job card
            for i, card in enumerate(job_cards[:target_count]):
                try:
                    logger.info(f"[NAUKRI] Processing job card {i+1}/{min(len(job_cards), target_count)}")
                    job_data = self.card_extractor.extract_job_data(card, driver)
                    if job_data and job_data.job_role != "Error: Unable to extract":
                        all_jobs.append(job_data)
                        logger.info(f"[NAUKRI] ✓ Extracted: {job_data.job_role} at {job_data.company}")
                except Exception as detail_error:
                    logger.warning(f"[NAUKRI] Failed to extract job card {i+1}: {detail_error}")
                    continue
            
            logger.info(f"[NAUKRI] Scraped {len(all_jobs)} jobs with description+companyDetails")
            return all_jobs
            
        except Exception as error:
            logger.error(f"[NAUKRI] Scraping failed: {error}")
            return []
        finally:
            self.browser_manager.return_driver(driver)
