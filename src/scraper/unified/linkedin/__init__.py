"""LinkedIn Playwright Scraper Module
n+5 Rolling Window + Complete Workflow (≤80 lines EMD)
"""
from .playwright_url_scraper import scrape_linkedin_urls_playwright
from .rolling_window_scraper import rolling_window_n_plus_5
from .complete_workflow import complete_linkedin_workflow
from .sequential_detail_scraper import scrape_job_details_sequential
from .selector_config import SEARCH_SELECTORS, DETAIL_SELECTORS

__all__ = [
    "scrape_linkedin_urls_playwright",
    "rolling_window_n_plus_5",
    "complete_linkedin_workflow",
    "scrape_job_details_sequential",
    "SEARCH_SELECTORS",
    "DETAIL_SELECTORS",
]
