# JobSpy-based LinkedIn scraper
from .linkedin_scraper import scrape_linkedin_jobs
from .multi_platform_scraper import scrape_multi_platform
from .proxy_config import get_proxy_for_platform, proxy_status

__all__ = [
    "scrape_linkedin_jobs",
    "scrape_multi_platform",
    "get_proxy_for_platform",
    "proxy_status",
]
