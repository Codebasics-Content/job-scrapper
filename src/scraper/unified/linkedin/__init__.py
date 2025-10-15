"""LinkedIn Playwright Scraper Module
BrightData scraping_browser2 integration (≤80 lines EMD)
"""
from .playwright_url_scraper import scrape_linkedin_urls_playwright
from .playwright_detail_scraper import scrape_linkedin_details_playwright
from .selector_config import SEARCH_SELECTORS, DETAIL_SELECTORS

__all__ = [
    "scrape_linkedin_urls_playwright",
    "scrape_linkedin_details_playwright",
    "SEARCH_SELECTORS",
    "DETAIL_SELECTORS",
]
