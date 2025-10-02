"""Shared scraper configuration module for all platforms"""
from .concurrency import (
    MAX_CONCURRENT_WINDOWS,
    MAX_CONCURRENT_SCRAPERS,
    get_window_creation_delay,
    get_task_start_delay
)
from .delays import (
    MIN_SCROLL_DELAY,
    MAX_SCROLL_DELAY,
    get_scroll_delay
)

__all__ = [
    "MAX_CONCURRENT_WINDOWS",
    "MAX_CONCURRENT_SCRAPERS",
    "get_window_creation_delay",
    "get_task_start_delay",
    "MIN_SCROLL_DELAY",
    "MAX_SCROLL_DELAY",
    "get_scroll_delay",
]
