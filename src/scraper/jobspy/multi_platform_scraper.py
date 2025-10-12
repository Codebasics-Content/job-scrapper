"""Multi-platform JobSpy scraper with selective proxy usage (≤80 lines EMD)"""
from __future__ import annotations

import pandas as pd
from jobspy import scrape_jobs

from .proxy_config import get_proxy_for_platform


def scrape_multi_platform(
    platforms: list[str],
    search_term: str,
    location: str = "United States",
    results_wanted: int = 100,
    hours_old: int = 72,
    linkedin_fetch_description: bool = True,
) -> pd.DataFrame:
    """
    Scrape jobs from multiple platforms with selective proxy usage
    
    LinkedIn: Uses BrightData proxy (if configured)
    Indeed/Naukri: No proxy (unlimited free scraping)
    
    Args:
        platforms: List of platforms ["linkedin", "indeed", "naukri"]
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
        print(f"\n🔍 Scraping {platform.upper()}...")
        
        # Get proxy only for LinkedIn
        proxies = get_proxy_for_platform(platform)
        
        if proxies:
            print(f"   🌐 Using BrightData proxy")
        else:
            print(f"   🆓 Free scraping (no proxy)")
        
        try:
            jobs_df = scrape_jobs(
                site_name=[platform],
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                linkedin_fetch_description=linkedin_fetch_description,
                proxies=proxies,  # LinkedIn gets proxy, others get None
            )
            
            if jobs_df is not None and len(jobs_df) > 0:
                all_results.append(jobs_df)
                print(f"   ✅ Found {len(jobs_df)} jobs")
            else:
                print(f"   ⚠️  No jobs found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
