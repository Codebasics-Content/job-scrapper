#!/usr/bin/env python3
# Parallel country scraping coordinator
# EMD Compliance: ≤80 lines

import asyncio
import logging
from typing import Callable
from selenium.webdriver.remote.webdriver import WebDriver

from .country_scraper import scrape_country_jobs
from models.job import JobModel

logger = logging.getLogger(__name__)

class ParallelCoordinator:
    """Coordinates parallel scraping across multiple countries"""
    
    target_count: int
    jobs: list[JobModel]
    processed_ids: set[str]
    lock: asyncio.Lock
    stop_event: asyncio.Event
    
    def __init__(self, target_count: int):
        self.target_count = target_count
        self.jobs = []
        self.processed_ids = set()
        self.lock = asyncio.Lock()
        self.stop_event = asyncio.Event()
        
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
    
    async def scrape_country_parallel(
        self,
        get_driver: Callable[[str], WebDriver | None],
        close_window: Callable[[str], None],
        base_url: str,
        job_role: str,
        country: dict[str, str],
        semaphore: asyncio.Semaphore
    ) -> None:
        """Scrape a single country in parallel with semaphore control"""
        from ..config.concurrency import get_task_start_delay
        
        country_name = country['name']
        
        if self.should_stop():
            logger.info(f"[{country_name}] Stopping - target already reached")
            close_window(country_name)
            return
        
        # Humanized delay before task start
        task_delay = get_task_start_delay()
        await asyncio.sleep(task_delay)
        
        async with semaphore:
            logger.info(f"[{country_name}] Starting scrape (delay: {task_delay:.1f}s)")
            
            if self.should_stop():
                logger.info(f"[{country_name}] Stopping - target reached during delay")
                close_window(country_name)
                return
            
            driver = get_driver(country_name)
            if not driver:
                logger.error(f"[{country_name}] Failed to get driver")
                return
            
            try:
                remaining = max(1, self.target_count - len(self.jobs))
                logger.info(f"[{country_name}] Need {remaining} jobs")
                
                country_jobs = await scrape_country_jobs(
                    driver=driver,
                    base_url=base_url,
                    job_role=job_role,
                    country=country,
                    target_count=remaining,
                    processed_ids=self.processed_ids,
                    should_stop_callback=self.should_stop
                )
                
                target_reached = await self.add_jobs(country_jobs)
                logger.info(f"[{country_name}] Collected {len(country_jobs)} jobs")
                
                if target_reached:
                    logger.info(f"[{country_name}] TARGET REACHED - closing window")
                
            except Exception as error:
                logger.error(f"[{country_name}] Scraping failed: {error}")
            finally:
                # Always close window when done
                close_window(country_name)
                logger.info(f"[{country_name}] Window closed")
