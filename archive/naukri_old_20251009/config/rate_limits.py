#!/usr/bin/env python3
# Naukri API Rate Limiting Configuration
# EMD Compliance: ≤80 lines

from typing import Final
from dataclasses import dataclass

# Rate Limiting Tiers
@dataclass(frozen=True)
class RateLimitTier:
    """Rate limit configuration for different scales"""
    delay: float  # Seconds between requests
    max_concurrent: int  # Max concurrent requests
    retry_attempts: int  # Max retry attempts on 429
    backoff_base: float  # Exponential backoff base (seconds)

# Conservative tier for safety (10k-20k jobs)
CONSERVATIVE: Final[RateLimitTier] = RateLimitTier(
    delay=2.0,
    max_concurrent=2,
    retry_attempts=5,
    backoff_base=2.0
)

# Balanced tier for medium scale (20k-40k jobs)
BALANCED: Final[RateLimitTier] = RateLimitTier(
    delay=1.5,
    max_concurrent=3,
    retry_attempts=5,
    backoff_base=1.5
)

# Aggressive tier for maximum speed (40k-50k jobs)
AGGRESSIVE: Final[RateLimitTier] = RateLimitTier(
    delay=1.0,
    max_concurrent=5,
    retry_attempts=7,
    backoff_base=1.0
)

# Default tier (start conservative, scale up if no issues)
DEFAULT_TIER: Final[RateLimitTier] = CONSERVATIVE

# HTTP Status Codes
RATE_LIMIT_STATUS: Final[int] = 429
TOO_MANY_REQUESTS: Final[int] = 429
SUCCESS_STATUS: Final[int] = 200

# Backoff multipliers
MAX_BACKOFF_DELAY: Final[float] = 60.0  # Max 60 seconds wait
MIN_BACKOFF_DELAY: Final[float] = 1.0   # Min 1 second wait

# Progress logging intervals
LOG_EVERY_N_REQUESTS: Final[int] = 100  # Log progress every 100 requests
ETA_UPDATE_INTERVAL: Final[int] = 50    # Update ETA every 50 requests
