"""LinkedIn Playwright Scraper Module
n+5 Rolling Window + Complete Workflow (≤80 lines EMD)
"""

from .complete_workflow import complete_linkedin_workflow
from .playwright_url_scraper import scrape_linkedin_urls_playwright
from .queue_based_scraper import scrape_job_details_queue_based
from .rolling_window_scraper import rolling_window_n_plus_5
from .selector_config import DETAIL_SELECTORS, SEARCH_SELECTORS
from .sequential_detail_scraper import scrape_job_details_sequential
from .staggered_queue_scraper import scrape_job_details_staggered

__all__ = [
    "scrape_linkedin_urls_playwright",
    "rolling_window_n_plus_5",
    "complete_linkedin_workflow",
    "scrape_job_details_sequential",
    "scrape_job_details_queue_based",
    "scrape_job_details_staggered",
    "SEARCH_SELECTORS",
    "DETAIL_SELECTORS",
]
