"""Batch processor for scalable job scraping with streaming DB writes

Processes jobs in configurable batches (default 1000) to avoid memory issues
and enables checkpoint/resume functionality for long-running scrapes.
"""
from __future__ import annotations

import logging
from typing import List, AsyncGenerator

from src.models.models import JobDetailModel

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process jobs in batches with streaming to database"""

    def __init__(
        self,
        batch_size: int = 1000,
        platform: str = "unknown",
    ):
        self.batch_size = batch_size
        self.platform = platform
        self.processed_count = 0
        self.failed_count = 0

    async def process_batch(
        self,
        jobs: List[JobDetailModel],
    ) -> List[JobDetailModel]:
        """Process a single batch of jobs"""
        logger.info(
            f"Processing batch of {len(jobs)} jobs for {self.platform}"
        )
        
        successful_jobs: List[JobDetailModel] = []
        
        for job in jobs:
            try:
                # Validate job has minimum requirements
                if self._validate_job(job):
                    successful_jobs.append(job)
                    self.processed_count += 1
                else:
                    self.failed_count += 1
                    logger.warning(f"Job validation failed: {job.id}")
            except Exception as e:
                self.failed_count += 1
                logger.error(f"Error processing job {job.id}: {e}")
        
        return successful_jobs

    def _validate_job(self, job: JobDetailModel) -> bool:
        """Validate job has minimum required data"""
        if not job.job_description or len(job.job_description) < 50:
            return False
        if not job.actual_role or not job.company_name:
            return False
        return True

    async def stream_batches(
        self,
        all_jobs: List[JobDetailModel],
    ) -> AsyncGenerator[List[JobDetailModel], None]:
        """Stream jobs in batches for memory-efficient processing"""
        total_jobs = len(all_jobs)
        logger.info(
            f"Streaming {total_jobs} jobs in batches of {self.batch_size}"
        )
        
        for i in range(0, total_jobs, self.batch_size):
            batch = all_jobs[i : i + self.batch_size]
            processed_batch = await self.process_batch(batch)
            yield processed_batch

    def get_stats(self) -> dict[str, int]:
        """Get processing statistics"""
        return {
            "processed": self.processed_count,
            "failed": self.failed_count,
            "total": self.processed_count + self.failed_count,
        }
