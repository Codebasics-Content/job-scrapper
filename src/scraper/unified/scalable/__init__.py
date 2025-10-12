"""Scalable scraping components for rate limiting and batch processing

Platform-specific rate limiters based on real-world constraints (2025 research).
"""
from .rate_limiters import (
    IndeedRateLimiter,
    LinkedInRateLimiter,
    NaukriRateLimiter,
    get_rate_limiter,
)

__all__ = [
    "IndeedRateLimiter",
    "LinkedInRateLimiter",
    "NaukriRateLimiter",
    "get_rate_limiter",
]
