#!/usr/bin/env python3
# Progress tracking with ETA calculation
# EMD Compliance: ≤80 lines

import time
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Track scraping progress with ETA"""
    
    def __init__(self, total_jobs: int):
        self.total_jobs = total_jobs
        self.jobs_collected = 0
        self.start_time = time.time()
        self.last_log_time = time.time()
    
    def update(self, jobs_collected: int) -> None:
        """Update progress and log if needed"""
        self.jobs_collected = jobs_collected
        current_time = time.time()
        
        # Log every 5 seconds
        if current_time - self.last_log_time >= 5.0:
            self._log_progress()
            self.last_log_time = current_time
    
    def _log_progress(self) -> None:
        """Log detailed progress information"""
        elapsed = time.time() - self.start_time
        progress_pct = (self.jobs_collected / self.total_jobs) * 100
        
        # Calculate ETA
        if self.jobs_collected > 0:
            rate = self.jobs_collected / elapsed
            remaining = self.total_jobs - self.jobs_collected
            eta_seconds = remaining / rate if rate > 0 else 0
            eta = str(timedelta(seconds=int(eta_seconds)))
        else:
            eta = "calculating..."
            rate = 0.0
        
        logger.info(
            f"\n{'='*60}\n"
            f"📊 SCRAPING PROGRESS\n"
            f"{'='*60}\n"
            f"Progress: {self.jobs_collected:,}/{self.total_jobs:,} jobs "
            f"({progress_pct:.1f}%)\n"
            f"Rate: {rate:.1f} jobs/sec\n"
            f"Elapsed: {timedelta(seconds=int(elapsed))}\n"
            f"ETA: {eta}\n"
            f"{'='*60}"
        )
    
    def finalize(self) -> None:
        """Log final statistics"""
        total_time = time.time() - self.start_time
        avg_rate = self.jobs_collected / total_time if total_time > 0 else 0
        
        logger.info(
            f"\n{'='*60}\n"
            f"✅ SCRAPING COMPLETE\n"
            f"{'='*60}\n"
            f"Total Jobs: {self.jobs_collected:,}\n"
            f"Total Time: {timedelta(seconds=int(total_time))}\n"
            f"Avg Rate: {avg_rate:.2f} jobs/sec\n"
            f"{'='*60}"
        )
