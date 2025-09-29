#!/usr/bin/env python3
# LinkedIn scraper module initialization
# EMD Compliance: ≤80 lines

from .scraper import LinkedInScraper
from .extractor import extract_job_from_url

__all__ = [
    'LinkedInScraper',
    'extract_job_from_url'
]
