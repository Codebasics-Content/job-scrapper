#!/usr/bin/env python3
"""
YCombinator Scraper Package

This module provides scraping capabilities for YCombinator job listings and startup profiles.
YCombinator focuses on early-stage startups, so job data extraction emphasizes company information
and startup-specific roles rather than traditional corporate job structures.

Key Features:
- Async scraping with Selenium WebDriver
- Startup-focused job extraction and skill analysis
- Rate limiting and anti-detection measures
- Integration with centralized skill extraction pipeline

Usage:
    from scrapers.ycombinator import YCombinatorScraper
    from scrapers.ycombinator.extractor import extract_job_from_card
    
    async with YCombinatorScraper() as scraper:
        jobs = await scraper.scrape_jobs("ai engineer", max_jobs=20)

Components:
- YCombinatorScraper: Main async scraper class with WebDriver management
- extract_job_from_card: Extracts job data from YCombinator company/job cards
- get_job_description_from_card: Extracts startup descriptions for skill analysis

Author: Job Scrapper Team
Created: 2024
EMD Compliance: ≤80 lines, modular architecture
"""

from .scraper import YCombinatorScraper
from .extractor import extract_job_from_card, get_job_description_from_card

__all__ = [
    "YCombinatorScraper",
    "extract_job_from_card", 
    "get_job_description_from_card"
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Job Scrapper Team"
__description__ = "YCombinator startup job scraping with skill extraction"
