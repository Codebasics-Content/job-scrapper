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
            # Batch scraping for real-time progress (10 jobs per batch)
            batch_size = 10
            num_batches = (results_wanted + batch_size - 1) // batch_size
            platform_results = []
            
            for batch_num in range(1, num_batches + 1):
                batch_start = datetime.now()
                current_batch = min(batch_size, results_wanted - (batch_num - 1) * batch_size)
                
                batch_msg = f"   📦 Batch {batch_num}/{num_batches} (target: {current_batch} jobs)..."
                print(batch_msg)
                logger.info(batch_msg)
                
                batch_df = scrape_jobs(
                    site_name=[platform],
                    search_term=search_term,
                    location=location,
                    results_wanted=current_batch,
                    hours_old=hours_old,
                    linkedin_fetch_description=linkedin_fetch_description,
                    proxies=proxies,
                )
                
                batch_end = datetime.now()
                batch_duration = (batch_end - batch_start).total_seconds()
                
                if batch_df is not None and len(batch_df) > 0:
                    platform_results.append(batch_df)
                    total_so_far = sum(len(df) for df in platform_results)
                    elapsed = (batch_end - start_time).total_seconds()
                    rate = total_so_far / elapsed if elapsed > 0 else 0
                    
                    progress_msg = f"   ✅ Batch {batch_num} done: {len(batch_df)} jobs | Total: {total_so_far}/{results_wanted} | {batch_duration:.1f}s | Rate: {rate:.1f} jobs/s"
                    print(progress_msg)
                    logger.info(progress_msg)
                else:
                    warn_msg = f"   ⚠️  Batch {batch_num} returned 0 jobs"
                    print(warn_msg)
                    logger.warning(warn_msg)
            
            # Combine all batches
            if platform_results:
                combined_df = pd.concat(platform_results, ignore_index=True)
                all_results.append(combined_df)
                
                end_time = datetime.now()
                total_duration = (end_time - start_time).total_seconds()
                final_msg = f"   🎉 {platform.upper()} COMPLETE: {len(combined_df)} jobs in {total_duration:.1f}s ({len(combined_df)/total_duration:.1f} jobs/sec)"
                print(final_msg)
                logger.info(final_msg)
            else:
                warn_msg = f"   ⚠️  No jobs found for {platform}"
                print(warn_msg)
                logger.warning(warn_msg)
                
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            error_msg = f"   ❌ ERROR after {duration:.1f}s: {e}"
            print(error_msg)
            logger.error(error_msg)
    
    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
