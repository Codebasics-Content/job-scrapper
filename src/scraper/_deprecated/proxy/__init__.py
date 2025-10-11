"""Proxy-based scraping module for job sites.

This module provides lightweight HTTP proxy scraping using BrightData's proxy
network instead of Scraping Browser. Benefits:
- 3x faster (direct HTTP vs browser automation)
- Simpler setup (just 3 env vars)
- Lower cost (proxy credits vs browser credits)
- Focus on skills extraction only

Usage:
    from src.scraper.proxy import scrape_linkedin_jobs, BrightDataProxy
    
    # Simple usage (auto-loads from .env)
    jobs = await scrape_linkedin_jobs("Python Developer", limit=50)
    
    # Advanced usage with custom proxy config
    proxy = BrightDataProxy.from_env().with_country("us").with_session()
    jobs = await scrape_linkedin_jobs("Data Scientist", proxy=proxy)
"""

from .config import BrightDataProxy, ProxyConfig, ProxyPool, ProxySession
from .linkedin_scraper import scrape_linkedin_jobs
from .indeed_scraper import scrape_indeed_jobs
from .naukri_scraper import scrape_naukri_jobs

__all__ = [
    # Config classes
    "BrightDataProxy",
    "ProxyConfig",
    "ProxyPool",
    "ProxySession",
    # Scraper functions
    "scrape_linkedin_jobs",
    "scrape_indeed_jobs",
    "scrape_naukri_jobs",
]
