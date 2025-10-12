"""Indeed unified scraper module"""

from .url_scraper import scrape_indeed_urls
from .detail_scraper import scrape_indeed_details
from .parser import create_job_detail_model

__all__ = ["scrape_indeed_urls", "scrape_indeed_details", "create_job_detail_model"]
