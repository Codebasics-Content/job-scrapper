#!/usr/bin/env python3
# Naukri.com job scraper (API-based with headers only)
# EMD Compliance: ≤80 lines

import logging
import asyncio
from src.models import JobModel
from .extractors.api_fetcher import NaukriAPIFetcher
from .extractors.api_parser import NaukriAPIParser
from .extractors.job_detail_fetcher import NaukriJobDetailFetcher
from .config.rate_limits import RateLimitTier, CONSERVATIVE
from .utils.progress_tracker import ProgressTracker

logger = logging.getLogger(__name__)

class NaukriScraper:
    """Main Naukri scraper using API with headers only"""
    
    def __init__(self, tier: RateLimitTier = CONSERVATIVE):
        self.api_fetcher = NaukriAPIFetcher(tier)
        self.api_parser = NaukriAPIParser()
        self.job_detail_fetcher = NaukriJobDetailFetcher()
        self.tier = tier
    
    async def scrape_jobs(
        self,
        keyword: str,
        num_jobs: int = 10
    ) -> list[JobModel]:
        """Scrape jobs from Naukri via API with bulk support"""
        jobs: list[JobModel] = []
        page_no = 1
        max_pages = (num_jobs // 20) + 1
        
        # Initialize progress tracker
        tracker = ProgressTracker(num_jobs)
        
        logger.info(
            f"\n🚀 STARTING NAUKRI SCRAPE\n"
            f"Keyword: '{keyword}'\n"
            f"Target: {num_jobs:,} jobs (~{max_pages} pages)\n"
            f"Rate Tier: {self.tier.delay}s delay, "
            f"{self.tier.max_concurrent} concurrent\n"
            f"{'='*60}"
        )
        
        while len(jobs) < num_jobs:
            # Fetch page data
            page_data = await asyncio.to_thread(
                self.api_fetcher.fetch_jobs_page,
                keyword,
                page_no
            )
            
            if not page_data:
                logger.warning(f"[STOP] No data at page {page_no}")
                break
            
            # Parse jobs from page
            page_jobs = self.api_parser.parse_jobs(page_data)
            jobs.extend(page_jobs)
            
            # Update progress
            tracker.update(len(jobs))
            
            # Stop if no more jobs
            if not page_jobs:
                break
            
            page_no += 1
        
        # Finalize and log statistics
        tracker.finalize()
        stats = self.api_fetcher.rate_limiter.get_stats()
        logger.info(
            f"\n📈 RATE LIMIT STATS\n"
            f"Total Requests: {stats['total_requests']}\n"
            f"Rate Limit Hits: {stats['rate_limit_hits']}\n"
            f"Total Backoff Time: {stats['total_backoff_time']}s\n"
            f"{'='*60}"
        )
        
        return jobs[:num_jobs]
    
    async def _enrich_job(self, job: JobModel) -> JobModel:
        """Enrich job with full details from API"""
        try:
            if not job.url:
                return job
            
            api_data = await self.job_detail_fetcher.fetch_job_details(job.url)
            if api_data:
                return self.api_parser.parse_api_response(api_data, job)
        except Exception as e:
            logger.debug(f"[NAUKRI] Enrichment failed: {e}")
        return job
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        self.api_fetcher.close()
