#!/usr/bin/env python3
# Naukri browser-based scraper
# EMD Compliance: ≤80 lines

import logging
import asyncio
import time
from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.models import JobModel
from src.scraper.base.base_scraper import BaseJobScraper
from .extractors.card_extractor import NaukriCardExtractor
from .extractors.job_detail_fetcher import NaukriJobDetailFetcher
from .extractors.api_parser import NaukriAPIParser
from .config.selectors import JOB_CARD_SELECTORS

logger = logging.getLogger(__name__)

class NaukriBrowserScraper(BaseJobScraper):
    """Naukri.com browser-based job scraper"""
    
    BASE_URL = "https://www.naukri.com"
    
    def __init__(self):
        super().__init__(platform_name="naukri", max_workers=2, pool_size=2)
        self.card_extractor = NaukriCardExtractor()
        self.job_detail_fetcher = NaukriJobDetailFetcher()
        self.api_parser = NaukriAPIParser()
    
    async def scrape_jobs(
        self,
        job_role: str,
        target_count: int,
        location: str = ""
    ) -> list[JobModel]:
        """Scrape jobs using browser automation"""
        logger.info(f"[NAUKRI START] Browser scraping {target_count} jobs for '{job_role}'")
        
        self.setup_driver_pool()
        driver = self.get_driver()
        
        if not driver:
            logger.error("[NAUKRI] Failed to get driver from pool")
            return []
        
        try:
            all_jobs: list[JobModel] = []
            keyword_slug = job_role.replace(' ', '-').lower()
            keyword_param = job_role.replace(' ', '+')
            
            # Calculate pages needed (20 jobs per page)
            jobs_per_page = 20
            total_pages = (target_count // jobs_per_page) + 1
            
            logger.info(f"[NAUKRI] Scraping {total_pages} pages for {target_count} jobs")
            
            for page_num in range(1, total_pages + 1):
                if len(all_jobs) >= target_count:
                    break
                
                # Build pagination URL
                if page_num == 1:
                    page_url = f"{self.BASE_URL}/{keyword_slug}-jobs?k={keyword_param}"
                else:
                    page_url = f"{self.BASE_URL}/{keyword_slug}-jobs-{page_num}?k={keyword_param}"
                
                logger.info(f"[NAUKRI] Page {page_num}/{total_pages}: {page_url}")
                driver.get(page_url)
                
                # Special handling for first page - needs more time to load
                if page_num == 1:
                    time.sleep(5)  # Longer initial wait for first page
                else:
                    time.sleep(3)  # Standard wait
                page_title = driver.title
                current_url = driver.current_url
                logger.info(f"[NAUKRI DEBUG] Page title: {page_title}")
                logger.info(f"[NAUKRI DEBUG] Current URL: {current_url}")
                
                # Check page source for debugging
                page_source = driver.page_source
                if "jobTuple" in page_source:
                    logger.info("[NAUKRI DEBUG] Found 'jobTuple' in page source")
                if "srp-jobtuple" in page_source:
                    logger.info("[NAUKRI DEBUG] Found 'srp-jobtuple' in page source")
                if "cust-job-tuple" in page_source:
                    logger.info("[NAUKRI DEBUG] Found 'cust-job-tuple' in page source")
                if "No jobs found" in page_source or "0 Jobs" in page_source:
                    logger.warning("[NAUKRI DEBUG] Page indicates no jobs found")
                # More specific captcha detection to avoid false positives
                if "g-recaptcha" in page_source or "captcha-box" in page_source:
                    logger.error("[NAUKRI DEBUG] Captcha detected in page")
                    logger.warning("[NAUKRI] Stopping due to captcha detection")
                    break
                    
                # Save page source for debugging
                try:
                    source_path = f"/tmp/naukri_page_{page_num}.html"
                    with open(source_path, 'w', encoding='utf-8') as f:
                        f.write(page_source[:5000])  # First 5000 chars
                    logger.info(f"[NAUKRI DEBUG] Page source saved to {source_path}")
                except Exception as e:
                    logger.warning(f"[NAUKRI DEBUG] Could not save page source: {e}")
                
                # Save screenshot for debugging
                try:
                    screenshot_path = f"/tmp/naukri_page_{page_num}.png"
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"[NAUKRI DEBUG] Screenshot saved to {screenshot_path}")
                except Exception as e:
                    logger.warning(f"[NAUKRI DEBUG] Could not save screenshot: {e}")
                
                # Wait for any of the job card selectors to appear
                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ", ".join(JOB_CARD_SELECTORS)))
                    )
                    logger.info("[NAUKRI DEBUG] Job cards detected on page")
                except Exception as e:
                    logger.warning(f"[NAUKRI DEBUG] Timeout waiting for job cards: {e}")
                    # Check if we got redirected or blocked
                    if "captcha" in current_url.lower() or "verify" in current_url.lower():
                        logger.error("[NAUKRI] Captcha or verification detected!")
                    
                await asyncio.sleep(2)  # Additional wait for dynamic content
                
                # Extract all job cards on current page using multiple selectors
                job_cards = []
                # For first page, try with a retry mechanism
                retry_count = 3 if page_num == 1 else 1
                
                for attempt in range(retry_count):
                    if attempt > 0:
                        logger.info(f"[NAUKRI] Retry attempt {attempt} for page {page_num}")
                        time.sleep(2)
                        
                for selector in JOB_CARD_SELECTORS:
                    try:
                        if selector.startswith("."):
                            cards = driver.find_elements(By.CLASS_NAME, selector[1:])
                        else:
                            cards = driver.find_elements(By.CSS_SELECTOR, selector)
                        if cards:
                            job_cards = cards
                            logger.info(f"[NAUKRI] Found {len(cards)} jobs using selector: {selector}")
                            break
                        else:
                            logger.debug(f"[NAUKRI DEBUG] No elements found with selector: {selector}")
                    except Exception as e:
                        logger.debug(f"[NAUKRI DEBUG] Error with selector {selector}: {e}")
                        continue
                
                if not job_cards:
                    logger.info(f"[NAUKRI] Found 0 jobs on page {page_num}")
                    # Try to find ANY article elements as a last resort
                    articles = driver.find_elements(By.TAG_NAME, "article")
                    if articles:
                        logger.info(f"[NAUKRI DEBUG] Found {len(articles)} article elements on page")
                        # Log first article's attributes for debugging
                        if articles:
                            first = articles[0]
                            logger.info(f"[NAUKRI DEBUG] First article class: {first.get_attribute('class') or ''}")
                            outer_html = first.get_attribute('outerHTML') or ''
                            logger.info(f"[NAUKRI DEBUG] First article HTML: {outer_html[:200]}")
                    else:
                        logger.warning("[NAUKRI DEBUG] No article elements found at all")
                
                # Early exit if no jobs found (end of results)
                if len(job_cards) == 0:
                    logger.warning(f"[NAUKRI] No jobs on page {page_num} - reached end of available jobs")
                    break
                
                for card in job_cards:
                    if len(all_jobs) >= target_count:
                        break
                    
                    try:
                        job = self._extract_job_from_card(card, job_role)
                        if job:
                            enriched_job = await self._enrich_with_api_data(job)
                            all_jobs.append(enriched_job)
                            logger.info(f"[NAUKRI] Progress: {len(all_jobs)}/{target_count}")
                    except Exception as e:
                        logger.debug(f"[NAUKRI] Error extracting job: {e}")
                        continue
            
            # Log completion with clarity
            if len(all_jobs) < target_count:
                logger.warning(
                    f"[NAUKRI COMPLETE] Scraped {len(all_jobs)}/{target_count} jobs "
                    f"(only {len(all_jobs)} available on Naukri)"
                )
            else:
                logger.info(f"[NAUKRI COMPLETE] Scraped {len(all_jobs)} jobs")
            return all_jobs
            
        finally:
            # Immediate cleanup - browser closes instantly after scraping
            self.cleanup_pool()
            logger.info("[NAUKRI] Browser cleanup complete")
    
    def _extract_job_from_card(self, card: Any, job_role: str) -> JobModel | None:
        """Extract job data from a job card element (card is Selenium WebElement)"""
        return self.card_extractor.extract_job_data(card, job_role)
    
    async def _enrich_with_api_data(self, job: JobModel) -> JobModel:
        """Enrich job with full description and skills from API"""
        try:
            if not job.url:
                return job
            
            api_data = await self.job_detail_fetcher.fetch_job_details(job.url)
            if api_data:
                return self.api_parser.parse_api_response(api_data, job)
        except Exception as e:
            logger.debug(f"[NAUKRI] API enrichment failed: {e}")
        return job
