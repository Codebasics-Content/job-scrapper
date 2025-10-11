"""Local proxy scraping using BrightData Proxy Manager + Playwright.

This module uses:
- BrightData Proxy Manager running locally (luminati-proxy)
- Playwright for browser automation
- Local proxy server at localhost:24000 (US) and localhost:24001 (India)

Much faster than cloud browser scraping!
"""

from .linkedin_scraper import scrape_linkedin_jobs_local_proxy
from .indeed_scraper import scrape_indeed_jobs_local_proxy
from .naukri_scraper import scrape_naukri_jobs_local_proxy

__all__ = [
    "scrape_linkedin_jobs_local_proxy",
    "scrape_indeed_jobs_local_proxy",
    "scrape_naukri_jobs_local_proxy",
]
