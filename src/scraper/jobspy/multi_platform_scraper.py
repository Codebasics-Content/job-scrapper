"""Multi-platform JobSpy scraper with selective proxy usage (≤80 lines EMD)"""
from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd
from jobspy import scrape_jobs

from .proxy_config import get_proxy_for_platform

logger = logging.getLogger(__name__)


def scrape_multi_platform(
    platforms: list[str],
    search_term: str,
    location: str = "United States",
    results_wanted: int = 100,
    hours_old: int = 72,
    linkedin_fetch_description: bool = True,
) -> pd.DataFrame:
    """
    Scrape jobs from 3 supported platforms with selective proxy usage
    
    Supported platforms:
    - LinkedIn: BrightData proxy (for >100 jobs)
    - Indeed: Direct scraping (no proxy, unlimited)
    - Naukri: Direct scraping (no proxy, unlimited + native skills)
    
    Args:
        platforms: List of platforms - only "linkedin", "indeed", "naukri" supported
        search_term: Job search keyword
        location: Location filter
        results_wanted: Jobs to scrape per platform
        hours_old: Filter by posting age
        linkedin_fetch_description: Fetch full LinkedIn descriptions
    
    Returns:
        Combined DataFrame from all platforms
    """
    all_results = []
    
    for platform in platforms:
        start_time = datetime.now()
        msg = f"\n{'='*60}\n🔍 SCRAPING {platform.upper()}\n{'='*60}"
        print(msg)
        logger.info(msg)
        
        # Get proxy only for LinkedIn
        proxies = get_proxy_for_platform(platform)
        
        proxy_msg = f"   {'🌐 Proxy' if proxies else '🆓 Direct'} | Target: {results_wanted} jobs"
        print(proxy_msg)
        logger.info(proxy_msg)
        
        print(f"   ⏳ Starting at {start_time.strftime('%H:%M:%S')}...")
        logger.info(f"Starting {platform} scrape")
        
        try:
            jobs_df = scrape_jobs(
                site_name=[platform],
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                linkedin_fetch_description=linkedin_fetch_description,
                proxies=proxies,
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if jobs_df is not None and len(jobs_df) > 0:
                all_results.append(jobs_df)
                success_msg = f"   ✅ SUCCESS: {len(jobs_df)} jobs in {duration:.1f}s ({len(jobs_df)/duration:.1f} jobs/sec)"
                print(success_msg)
                logger.info(success_msg)
            else:
                warn_msg = f"   ⚠️  No jobs found after {duration:.1f}s"
                print(warn_msg)
                logger.warning(warn_msg)
                
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            error_msg = f"   ❌ ERROR after {duration:.1f}s: {e}"
            print(error_msg)
            logger.error(error_msg)
    
    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
