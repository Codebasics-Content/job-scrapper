#!/usr/bin/env python3
# Indeed scraper module initialization
# EMD Compliance: ≤80 lines

from .scraper import IndeedScraper
from .extractor import extract_job_from_card, get_job_description_from_card

__all__ = [
    'IndeedScraper',
    'extract_job_from_card', 
    'get_job_description_from_card'
]
