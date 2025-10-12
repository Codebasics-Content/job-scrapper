"""Progress tracker with realistic ETA calculations for scraping operations

Calculates accurate ETAs based on actual throughput and platform constraints.
"""
from __future__ import annotations

import logging
import time
from typing import TypedDict

logger = logging.getLogger(__name__)


class ProgressStats(TypedDict):
    """Progress statistics structure"""
    processed: int
    failed: int
    remaining: int
    eta_seconds: float
    throughput: float


class ProgressTracker:
    """Track scraping progress with realistic ETA"""

    def __init__(self, total_jobs: int, platform: str = "unknown"):
        self.total_jobs = total_jobs
        self.platform = platform
        self.processed_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        # Track throughput samples for moving average
        self.throughput_samples: list[float] = []
        self.last_sample_time = self.start_time

    def update_progress(self, processed: int, failed: int) -> None:
        """Update progress counts and calculate throughput"""
        self.processed_count = processed
        self.failed_count = failed
        
        # Sample throughput every 10 jobs
        if processed % 10 == 0 and processed > 0:
            current_time = time.time()
            elapsed = current_time - self.last_sample_time
            if elapsed > 0:
                sample_throughput = 10 / elapsed
                self.throughput_samples.append(sample_throughput)
                # Keep last 10 samples for moving average
                if len(self.throughput_samples) > 10:
                    self.throughput_samples.pop(0)
                self.last_sample_time = current_time

    def get_stats(self) -> ProgressStats:
        """Get current progress statistics with ETA"""
        total_processed = self.processed_count + self.failed_count
        remaining = max(0, self.total_jobs - total_processed)
        
        # Calculate throughput (jobs/second)
        if self.throughput_samples:
            throughput = sum(self.throughput_samples) / len(self.throughput_samples)
        else:
            elapsed = time.time() - self.start_time
            throughput = total_processed / elapsed if elapsed > 0 else 0
        
        # Calculate ETA
        eta_seconds = remaining / throughput if throughput > 0 else 0
        
        return {
            "processed": self.processed_count,
            "failed": self.failed_count,
            "remaining": remaining,
            "eta_seconds": eta_seconds,
            "throughput": throughput,
        }

    def log_progress(self) -> None:
        """Log current progress to console"""
        stats = self.get_stats()
        eta_mins = stats["eta_seconds"] / 60
        logger.info(
            f"{self.platform}: {stats['processed']}/{self.total_jobs} jobs "
            f"({stats['throughput']:.2f} jobs/s, ETA: {eta_mins:.1f}m)"
        )
