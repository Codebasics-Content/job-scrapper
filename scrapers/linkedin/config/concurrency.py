#!/usr/bin/env python3
# Concurrency and humanized scraping configuration
# EMD Compliance: ≤80 lines

import random

# Maximum concurrent browser windows to prevent resource exhaustion
MAX_CONCURRENT_WINDOWS = 8

# Maximum concurrent scraping tasks (reduced to avoid rate limiting)
MAX_CONCURRENT_SCRAPERS = 2

# Humanized delays (seconds) - increased to avoid rate limiting
WINDOW_CREATION_DELAY_MIN = 3.0
WINDOW_CREATION_DELAY_MAX = 6.0

# Task start delays (seconds) - stagger parallel tasks
TASK_START_DELAY_MIN = 2.0
TASK_START_DELAY_MAX = 5.0

def get_window_creation_delay() -> float:
    """Get randomized delay for window creation (2-4 seconds)"""
    return random.uniform(WINDOW_CREATION_DELAY_MIN, WINDOW_CREATION_DELAY_MAX)

def get_task_start_delay() -> float:
    """Get randomized delay for task start (1-3 seconds)"""
    return random.uniform(TASK_START_DELAY_MIN, TASK_START_DELAY_MAX)
