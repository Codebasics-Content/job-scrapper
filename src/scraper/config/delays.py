#!/usr/bin/env python3
# Shared anti-bot detection delay configuration
# EMD Compliance: ≤80 lines

import random

# Page interaction delays (in seconds)
PAGE_LOAD_DELAY: float = 2.0  # Fast 2-second page load
MIN_SCROLL_DELAY: float = 1.0
MAX_SCROLL_DELAY: float = 2.0

# LinkedIn API Rate Limiting (Optimized for speed while avoiding 429 errors)
API_REQUEST_DELAY: float = 1.0  # 1.0s delay for ~60 req/min (optimized rate)
MIN_API_DELAY: float = 0.5  # Minimum delay between API requests (optimized)
MAX_API_DELAY: float = 1.5  # Maximum delay for randomization (optimized)
BATCH_SIZE: int = 10  # Process 10 jobs per batch to avoid bulk detection
BATCH_DELAY: float = 1.5  # 1.5s delay between batches (optimized)

TAB_SWITCH_DELAY: float = 0.5
ERROR_RETRY_DELAY: float = 5.0  # Increased from 3.0 for better recovery
API_TIMEOUT: float = 10.0  # 10s timeout for API responses (increased for stability)

def get_scroll_delay() -> float:
    """Get randomized scroll delay (1-2 seconds)"""
    return random.uniform(MIN_SCROLL_DELAY, MAX_SCROLL_DELAY)

def get_api_delay() -> float:
    """Get randomized API delay (1-2.5 seconds) to mimic human behavior"""
    return random.uniform(MIN_API_DELAY, MAX_API_DELAY)
