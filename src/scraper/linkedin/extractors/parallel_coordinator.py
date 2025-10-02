#!/usr/bin/env python3
# Parallel country scraping coordinator
# EMD Compliance: ≤80 lines

import asyncio
import logging
from typing import Callable
from selenium.webdriver.remote.webdriver import WebDriver

from .id_collector import collect_job_ids
from .round_robin_collector import collect_one_id_from_country
from .detail_fetcher import fetch_job_details_batch
from src.models import JobModel

logger = logging.getLogger(__name__)

class ParallelCoordinator:
    """Coordinates parallel global scraping across browser windows"""
    
    target_count: int
    jobs: list[JobModel]
    processed_ids: set[str]
    lock: asyncio.Lock
    stop_event: asyncio.Event
    country_counts: dict[str, int]
    
    def __init__(self, target_count: int):
        self.target_count = target_count
        self.jobs = []
        self.processed_ids = set()
        self.lock = asyncio.Lock()
        self.stop_event = asyncio.Event()
        self.country_counts = {}
        
    async def add_jobs(self, new_jobs: list[JobModel]) -> bool:
        """Add jobs with deduplication, return True if target reached"""
        async with self.lock:
            for job in new_jobs:
                if len(self.jobs) >= self.target_count:
                    self.stop_event.set()
                    return True
                    
                if job.job_id not in self.processed_ids:
                    self.jobs.append(job)
                    self.processed_ids.add(job.job_id)
                    
            if len(self.jobs) >= self.target_count:
                self.stop_event.set()
                return True
                
        return False
    
    def should_stop(self) -> bool:
        """Check if scraping should stop"""
        return self.stop_event.is_set()
    
    async def collect_ids_from_country(
        self,
        get_driver: Callable[[str], WebDriver | None],
        close_window: Callable[[str], None],
        base_url: str,
        job_role: str,
        country: dict[str, str],
        semaphore: asyncio.Semaphore
    ) -> list[str]:
        """Phase 1: Collect job IDs from a country"""
        from src.scraper.config.concurrency import get_task_start_delay
        
        country_code = country['name']
        geo_id = country.get('geoId', '')
        
        task_delay = get_task_start_delay()
        await asyncio.sleep(task_delay)
        
        async with semaphore:
            logger.info(f"[{country_code}] Phase 1: Starting ID collection")
            
            driver = get_driver(country_code)
            if not driver:
                logger.error(f"[{country_code}] Failed to get driver")
                return []
            
            try:
                collected_ids = await collect_job_ids(
                    driver=driver,
                    base_url=base_url,
                    job_role=job_role,
                    location_name=country_code,
                    target_count=self.target_count,
                    processed_ids=self.processed_ids,
                    should_stop_callback=self.should_stop,
                    geo_id=geo_id if geo_id else None
                )
                
                logger.info(f"[{country_code}] Phase 1 complete: {len(collected_ids)} IDs")
                return collected_ids
                
            except Exception as error:
                logger.error(f"[{country_code}] ID collection failed: {error}")
                return []
            finally:
                close_window(f"LinkedIn-{country_code}")
    
    async def scrape_round_robin(
        self,
        get_driver: Callable[[str], WebDriver | None],
        base_url: str,
        job_role: str,
        countries: list[dict[str, str]]
    ) -> None:
        """Round-robin: 1 ID from each country in rotation"""
        logger.info(f"🔄 Starting round-robin collection: {self.target_count} jobs")
        
        page_cache: dict[str, list[str]] = {}
        country_drivers: dict[str, WebDriver] = {}
        
        # Get drivers for all countries
        for country in countries:
            driver = get_driver(country['name'])
            if driver:
                country_drivers[country['name']] = driver
        
        all_ids: list[str] = []
        country_idx = 0
        failed_attempts = 0
        max_failed = len(countries) * 3  # Allow 3 failures per country before stopping
        
        while len(all_ids) < self.target_count and failed_attempts < max_failed:
            country = countries[country_idx % len(countries)]
            driver = get_driver(country['name'])
            
            if not driver:
                logger.warning(f"[{country['name']}] No driver available")
                failed_attempts += 1
                country_idx += 1
                continue
            
            job_id = await collect_one_id_from_country(
                driver=driver,
                base_url=base_url,
                job_role=job_role,
                location_name=country['name'],
                geo_id=country.get('geoId'),
                processed_ids=self.processed_ids,
                page_cache=page_cache
            )
            
            if job_id:
                all_ids.append(job_id)
                self.processed_ids.add(job_id)
                failed_attempts = 0  # Reset on success
                logger.info(
                    f"[{country['name']}] Job {len(all_ids)} (country) | "
                    f"Global: {len(all_ids)}/{self.target_count}"
                )
            else:
                failed_attempts += 1
            
            country_idx += 1
        
        logger.info(f"✅ Round-robin complete: {len(all_ids)} IDs collected")
        
        # Phase 2: Fetch details
        if all_ids:
            logger.info(f"🚀 Fetching details for {len(all_ids)} jobs...")
            await fetch_job_details_batch(
                job_ids=all_ids,
                job_role=job_role,
                location_name="Global",
                add_job_callback=self.add_single_job,
                should_stop_callback=self.should_stop,
                semaphore=asyncio.Semaphore(15),  # 15 workers to respect LinkedIn rate limits
                global_target=self.target_count
            )
    
    async def scrape_two_phase(
        self,
        get_driver: Callable[[str], WebDriver | None],
        close_window: Callable[[str], None],
        base_url: str,
        job_role: str,
        countries: list[dict[str, str]],
        id_semaphore: asyncio.Semaphore,
        detail_semaphore: asyncio.Semaphore
    ) -> None:
        """Two-phase scraping: Phase 1 collects IDs, Phase 2 fetches details"""
        # Phase 1: Collect all job IDs from countries in parallel
        logger.info("🔍 PHASE 1: Collecting job IDs from all countries...")
        
        id_tasks = [
            self.collect_ids_from_country(
                get_driver, close_window, base_url, job_role, country, id_semaphore
            )
            for country in countries
        ]
        
        all_country_ids = await asyncio.gather(*id_tasks)
        all_ids = [job_id for country_ids in all_country_ids for job_id in country_ids]
        
        logger.info(f"✅ Phase 1 complete: {len(all_ids)} unique job IDs collected")
        
        if not all_ids:
            logger.warning("No job IDs collected - exiting")
            return
        
        # Phase 2: Fetch job details with 15 workers (balanced speed + rate limit safety)
        logger.info(f"🚀 PHASE 2: Fetching details for {len(all_ids)} jobs with 15 concurrent workers...")
        
        detail_semaphore = asyncio.Semaphore(15)  # 15 workers for optimal speed + safety
        
        fetched_count: int = await fetch_job_details_batch(
            job_ids=all_ids,
            job_role=job_role,
            location_name="Global",
            add_job_callback=self.add_single_job,
            should_stop_callback=self.should_stop,
            semaphore=detail_semaphore,
            global_target=self.target_count
        )
        
        logger.info(f"✅ SCRAPING COMPLETE: {fetched_count} jobs scraped (target: {self.target_count})")
    
    async def add_single_job(self, job: JobModel) -> bool:
        """Add single job with deduplication, return True if target reached"""
        async with self.lock:
            if len(self.jobs) >= self.target_count:
                self.stop_event.set()
                return True
            
            if job.job_id not in self.processed_ids:
                self.jobs.append(job)
                self.processed_ids.add(job.job_id)
            
            if len(self.jobs) >= self.target_count:
                self.stop_event.set()
                return True
        
        return False
