#!/usr/bin/env python3
# Adaptive rate limiter with exponential backoff
# EMD Compliance: ≤80 lines

import time
import logging
from ..config.rate_limits import (
    RateLimitTier,
    DEFAULT_TIER,
    MAX_BACKOFF_DELAY,
    MIN_BACKOFF_DELAY
)

logger = logging.getLogger(__name__)

class AdaptiveRateLimiter:
    """Adaptive rate limiter with backoff and metrics"""
    
    def __init__(self, tier: RateLimitTier = DEFAULT_TIER):
        self.tier = tier
        self.last_request_time = 0.0
        self.request_count = 0
        self.rate_limit_hits = 0
        self.total_backoff_time = 0.0
    
    def wait(self) -> None:
        """Wait according to rate limit tier"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.tier.delay:
            wait_time = self.tier.delay - elapsed
            time.sleep(wait_time)
        self.last_request_time = time.time()
        self.request_count += 1
    
    def backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay"""
        delay = min(
            self.tier.backoff_base * (2 ** attempt),
            MAX_BACKOFF_DELAY
        )
        delay = max(delay, MIN_BACKOFF_DELAY)
        
        logger.warning(
            f"[RATE LIMIT] Backoff attempt {attempt}: "
            f"Waiting {delay:.1f}s"
        )
        
        time.sleep(delay)
        self.rate_limit_hits += 1
        self.total_backoff_time += delay
        return delay
    
    def get_stats(self) -> dict[str, int | float]:
        """Get rate limiter statistics"""
        return {
            "total_requests": self.request_count,
            "rate_limit_hits": self.rate_limit_hits,
            "total_backoff_time": round(self.total_backoff_time, 2),
            "avg_delay": round(self.tier.delay, 2)
        }
