#!/usr/bin/env python3
# LinkedIn job scraper using multi-country approach
# EMD Compliance: ≤80 lines

import asyncio
import logging
try:
    from typing import override
except ImportError:
    from typing_extensions import override

from ..base.base_scraper import BaseJobScraper
from ..base.window_manager import WindowManager
from ..base.anti_detection import AntiDetectionDriverFactory
from .config.countries import LINKEDIN_COUNTRIES
from src.models import JobModel
import undetected_chromedriver as uc

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseJobScraper):
    """LinkedIn job scraper with multi-window parallel approach"""
    
    def __init__(self):
        super().__init__(platform_name="LinkedIn")
        self.base_url: str = "https://www.linkedin.com/jobs/search"
        self.driver_factory: AntiDetectionDriverFactory = AntiDetectionDriverFactory()
        self.window_manager: WindowManager = WindowManager(self.driver_factory.create_driver)
        self.setup_driver_pool()  # Initialize main driver pool

    async def initialize_country_windows_async(
        self, 
        country_codes: list[str],
        job_role: str
    ) -> None:
        """Pre-initialize windows with URL parameters and humanized delays"""
        import urllib.parse
        from src.scraper.config.concurrency import (
            MAX_CONCURRENT_WINDOWS,
            get_window_creation_delay
        )
        
        logger.info(f"[WINDOW INIT] Creating {len(country_codes)} windows (max {MAX_CONCURRENT_WINDOWS} concurrent)...")
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_WINDOWS)
        
        async def create_window_with_delay(country_code: str, country_data: dict[str, str]) -> None:
            async with semaphore:
                # Humanized delay before window creation
                delay = get_window_creation_delay()
                await asyncio.sleep(delay)
                
                window_id = f"LinkedIn-{country_code}"
                driver = self.window_manager.create_window(window_id)
                
                if driver:
                    try:
                        # Build URL with parameters: job role, country, 1-month filter
                        params = {
                            'keywords': job_role,
                            'f_TPR': 'r2592000',  # 1 month (30 days)
                            'location': country_data['name'],
                            'start': 0
                        }
                        # Only add geoId if not empty (Worldwide has empty geoId)
                        if country_data['geoId']:
                            params['geoId'] = country_data['geoId']
                        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
                        driver.get(url)
                        logger.info(f"[WINDOW CREATED] {window_id} (delay: {delay:.1f}s)")
                    except Exception as e:
                        logger.error(f"[WINDOW NAV FAILED] {window_id}: {e}")
                else:
                    logger.error(f"[WINDOW FAILED] {window_id}")
        
        # Create country lookup dictionary
        country_lookup = {c['name']: c for c in LINKEDIN_COUNTRIES}
        
        tasks = [
            create_window_with_delay(code, country_lookup[code]) 
            for code in country_codes
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log any creation failures
        failures = [r for r in results if isinstance(r, Exception)]
        if failures:
            logger.warning(f"[WINDOW INIT] {len(failures)} windows failed to create")
        
        logger.info(f"[WINDOW INIT COMPLETE] {self.window_manager.window_count()} windows ready")
    
    def get_driver_for_country(self, country_code: str) -> uc.Chrome | None:
        """Get dedicated window for country"""
        window_id = f"LinkedIn-{country_code}"
        driver = self.window_manager.get_window(window_id)
        
        if not driver:
            logger.warning(f"[WINDOW MISSING] {window_id}, creating new window")
            driver = self.window_manager.create_window(window_id)
        
        return driver
    
    @override
    async def scrape_jobs(
        self, 
        job_role: str, 
        target_count: int,
        location: str = "",
        countries: list[dict[str, str]] | None = None
    ) -> list[JobModel]:
        """Scrape jobs using parallel multi-country approach with global limit
        
        Scrapes all countries in parallel with global target distribution.
        Stops immediately when target count is reached.
        
        Args:
            job_role: Job role to search for
            target_count: Total number of jobs to scrape (distributed globally)
            location: Ignored for LinkedIn (kept for base class compatibility)
            countries: List of countries to scrape (optional, defaults to all)
        """
        from .extractors.parallel_coordinator import ParallelCoordinator
        
        # Use provided countries or default to all
        countries_to_scrape = countries if countries is not None else LINKEDIN_COUNTRIES
    
        logger.info(f"[SCRAPE START] Parallel scrape for {target_count} {job_role} jobs (global limit)")
        logger.info(f"[SCRAPE START] Scraping {len(countries_to_scrape)} countries in parallel")
        logger.info(f"[SCRAPE START] Current windows: {self.window_manager.window_count()}")
        
        try:
            # Pre-initialize all country tabs before parallel execution
            logger.info("[INIT START] Starting country pool initialization...")
            country_codes = [country['name'] for country in countries_to_scrape]
            logger.info(f"[INIT START] Country codes to initialize: {country_codes[:5]}... (showing first 5)")
            logger.info(f"[INIT START] Total codes: {len(country_codes)}")
            
            await self.initialize_country_windows_async(country_codes, job_role)
            logger.info(f"[INIT COMPLETE] Successfully initialized {self.window_manager.window_count()} windows")
        except Exception as e:
            logger.error(f"[INIT FAILED] Failed to initialize country pools: {e}", exc_info=True)
        
        # Round-robin: 1 job from each country in rotation
        coordinator = ParallelCoordinator(target_count=target_count)
        
        await coordinator.scrape_round_robin(
            get_driver=self.get_driver_for_country,
            base_url=self.base_url,
            job_role=job_role,
            countries=countries_to_scrape
        )
        
        logger.info(
            f"Completed: {len(coordinator.jobs)} jobs " +
            f"from {len(coordinator.processed_ids)} unique listings"
        )
        
        # Cleanup all browser windows
        from .cleanup.browser_cleanup import cleanup_browsers
        await cleanup_browsers(self.window_manager)
        
        return coordinator.jobs[:target_count]
    
    
