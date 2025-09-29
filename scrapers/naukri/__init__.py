#!/usr/bin/env python3
# Naukri.com scraper package initialization
# EMD Compliance: ≤80 lines

"""
Naukri.com scraper package providing job scraping and data extraction functionality.

This package includes:
- NaukriScraper: Main scraper class for Naukri.com job listings
- extract_job_from_card: Function to extract job data from Naukri job cards
- get_job_description_from_card: Function to extract job descriptions

Usage:
    from scrapers.naukri import NaukriScraper, extract_job_from_card
    
    scraper = NaukriScraper()
    jobs = await scraper.scrape_jobs("Python Developer", max_jobs=20)
"""

from .scraper import NaukriScraper
from .extractor import extract_job_from_card, get_job_description_from_card

__all__ = [
    "NaukriScraper",
    "extract_job_from_card", 
    "get_job_description_from_card"
]

__version__ = "1.0.0"
__author__ = "Codebasics Job Scrapper Team"
__description__ = "Naukri.com job scraping and extraction module"
