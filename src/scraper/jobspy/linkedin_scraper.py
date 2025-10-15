# JobSpy LinkedIn Scraper - EMD Component
# Free, unlimited LinkedIn scraping with BrightData proxy support
# No browser automation, pure HTTP requests

import logging
from typing import TypedDict
from jobspy import scrape_jobs

from .proxy_config import get_brightdata_proxy


logger = logging.getLogger(__name__)


class LinkedInJobDict(TypedDict, total=False):
    """Type definition for LinkedIn job dictionary from JobSpy"""
    site: str
    job_url: str
    title: str
    company: str
    location: str
    description: str
    job_type: str
    date_posted: str


def scrape_linkedin_jobs(
    keyword: str,
    location: str = "Worldwide",
    limit: int = 100,
    hours_old: int | None = None,
    job_type: str | None = None,
    is_remote: bool = False,
    fetch_description: bool = True
) -> list[LinkedInJobDict]:
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
    # Get BrightData proxy (auto-converts wss:// to http:// format)
    proxy_url = get_brightdata_proxy()
    
    # CRITICAL: JobSpy expects list of strings in format 'user:pass@host:port'
    # WITHOUT http:// prefix
    proxies: list[str] | None = None
    if proxy_url:
        # Validate proxy format
        if proxy_url.startswith(('http://', 'https://', 'wss://')):
            logger.error(f"PROXY FORMAT ERROR: URL still has protocol prefix: {proxy_url[:30]}")
            print(f"❌ PROXY ERROR: Protocol prefix detected, stripping...")
            proxy_url = proxy_url.replace('http://', '').replace('https://', '').replace('wss://', '')
        
        proxies = [proxy_url]
        print(f"\n{'='*60}")
        print(f"🔐 PROXY CONFIGURED FOR JOBSPY")
        print(f"{'='*60}")
        print(f"✅ Format: {proxy_url[:60]}..." if len(proxy_url) > 60 else f"✅ Format: {proxy_url}")
        print(f"✅ List format: {proxies}")
        print(f"✅ Type check: {type(proxies)} with {len(proxies)} proxy")
        logger.info(f"Proxy configured: {proxy_url[:50]}...")
    else:
        print(f"\n{'='*60}")
        print(f"❌ NO PROXY - LINKEDIN WILL RATE LIMIT")
        print(f"{'='*60}")
        print(f"⚠️  Set PROXY_URL environment variable for scaling")
        logger.warning("No proxy - LinkedIn will rate limit after ~50 jobs")
    print(f"{'='*60}\n")
    
    try:
        print(f"🚀 JobSpy API Call Starting...")
        print(f"📍 Search: '{keyword}' in '{location}'")
        print(f"🎯 Target: {limit} jobs\n")
        logger.info(
            f"Scraping LinkedIn: {keyword} in {location} "
            f"(limit={limit}, proxy={bool(proxies)})"
        )
        
        # Call JobSpy for LinkedIn (no Indeed parameters needed)
        if hours_old is not None:
            df = scrape_jobs(
                site_name=["linkedin"],
                search_term=keyword,
                location=location,
                results_wanted=limit,
                hours_old=hours_old,
                job_type=job_type,
                is_remote=is_remote,
                linkedin_fetch_description=fetch_description,
                proxies=proxies
            )
        else:
            df = scrape_jobs(
                site_name=["linkedin"],
                search_term=keyword,
                location=location,
                results_wanted=limit,
                job_type=job_type,
                is_remote=is_remote,
                linkedin_fetch_description=fetch_description,
                proxies=proxies
            )
        
        if df.empty:
            print(f"❌ JobSpy returned 0 jobs")
            logger.warning("No jobs found")
            return []
        
        print(f"✅ JobSpy returned {len(df)} jobs")
        print(f"📊 DataFrame shape: {df.shape}")
        
        # Check if proxy was actually used (if rate limited, would be 0 or low count)
        if proxies and len(df) < limit * 0.5:
            logger.warning(f"LOW RESULTS WITH PROXY: Got {len(df)}/{limit} - proxy may not be working")
            print(f"⚠️  WARNING: Low results despite proxy - verify BrightData credentials")
        
        logger.info(f"Successfully scraped {len(df)} LinkedIn jobs")
        
        # Convert DataFrame to list of dicts with proper typing
        jobs: list[LinkedInJobDict] = df.to_dict('records')  # type: ignore[assignment]
        print(f"✅ Converted to {len(jobs)} job dictionaries\n")
        return jobs
        
    except Exception as e:
        logger.error(f"JobSpy scraping failed: {e}")
        return []
