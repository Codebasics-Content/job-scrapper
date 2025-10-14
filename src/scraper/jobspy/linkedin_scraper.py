# JobSpy LinkedIn Scraper - EMD Component
# Free, unlimited LinkedIn scraping with BrightData proxy support
# No browser automation, pure HTTP requests

import os
import logging
from typing import Optional
from jobspy import scrape_jobs
import pandas as pd

logger = logging.getLogger(__name__)


def scrape_linkedin_jobs(
    keyword: str,
    location: str = "Worldwide",
    limit: int = 100,
    hours_old: Optional[int] = None,
    job_type: Optional[str] = None,
    is_remote: bool = False,
    fetch_description: bool = True
) -> list[dict[str, object]]:
    """Scrape LinkedIn jobs using JobSpy library
    
    Args:
        keyword: Job search keyword/title
        location: Job location (city, state, country)
        limit: Maximum number of jobs to scrape
        hours_old: Filter by job age in hours
        job_type: fulltime, parttime, internship, contract
        is_remote: Filter for remote jobs only
        fetch_description: Get full description (slower but more complete)
    
    Returns:
        List of job dictionaries with standardized schema
    
    Example:
        jobs = scrape_linkedin_jobs("Data Scientist", "United States", 50)
    """
    # Get BrightData proxy from environment (Luminati proxy manager)
    proxy_url = os.getenv("PROXY_URL")
    proxies = [proxy_url] if proxy_url else None
    
    print("\n" + "="*60)
    print("🔐 PROXY STATUS CHECK")
    print("="*60)
    if proxies:
        print(f"✅ BrightData Proxy: CONFIGURED")
        print(f"🌐 Proxy URL: {proxy_url[:50]}..." if len(proxy_url) > 50 else f"🌐 Proxy URL: {proxy_url}")
        logger.info(f"Using BrightData proxy: {proxy_url}")
    else:
        print(f"❌ BrightData Proxy: NOT CONFIGURED")
        print(f"⚠️  WARNING: LinkedIn may rate limit without proxy!")
        logger.warning("No proxy configured - LinkedIn may rate limit")
    print("="*60 + "\n")
    
    try:
        print(f"🚀 JobSpy API Call Starting...")
        print(f"📍 Search: '{keyword}' in '{location}'")
        print(f"🎯 Target: {limit} jobs\n")
        logger.info(
            f"Scraping LinkedIn: {keyword} in {location} "
            f"(limit={limit}, proxy={bool(proxies)})"
        )
        
        # Call JobSpy
        df = scrape_jobs(
            site_name=["linkedin"],
            search_term=keyword,
            location=location,
            results_wanted=limit,
            hours_old=hours_old,
            job_type=job_type,
            is_remote=is_remote,
            linkedin_fetch_description=fetch_description,
            proxies=proxies,
            country_indeed='USA'  # Not used for LinkedIn
        )
        
        if df is None or df.empty:
            print(f"❌ JobSpy returned 0 jobs")
            logger.warning("No jobs found")
            return []
        
        print(f"✅ JobSpy returned {len(df)} jobs")
        print(f"📊 DataFrame shape: {df.shape}")
        logger.info(f"Successfully scraped {len(df)} LinkedIn jobs")
        
        # Convert DataFrame to list of dicts
        jobs = df.to_dict('records')
        print(f"✅ Converted to {len(jobs)} job dictionaries\n")
        return jobs
        
    except Exception as e:
        logger.error(f"JobSpy scraping failed: {e}")
        return []
