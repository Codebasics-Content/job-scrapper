"""Large-scale LinkedIn job scraper with rate limiting (≤80 lines EMD)"""
import time
import random
import pandas as pd
from jobspy import scrape_jobs


def scrape_jobs_batch(
    search_term: str,
    location: str = "United States",
    total_jobs: int = 10000,
    batch_size: int = 100,
    base_delay: float = 3.0,
    random_jitter: float = 2.0,
) -> pd.DataFrame:
    """
    Scrape LinkedIn jobs in batches with delays to avoid rate limiting
    
    Args:
        search_term: Job search keyword
        location: Location filter
        total_jobs: Total jobs to scrape
        batch_size: Jobs per batch (recommended: 50-100)
        base_delay: Base delay between batches in seconds
        random_jitter: Random delay variation (0 to this value)
    
    Returns:
        DataFrame with all scraped jobs
    """
    all_jobs = []
    batches_needed = (total_jobs + batch_size - 1) // batch_size
    
    print(f"🎯 Target: {total_jobs} jobs")
    print(f"📦 {batches_needed} batches of {batch_size} jobs")
    print(f"⏱️  Delay: {base_delay}s + random(0-{random_jitter}s)")
    print()
    
    for batch_num in range(1, batches_needed + 1):
        jobs_remaining = total_jobs - len(all_jobs)
        current_batch_size = min(batch_size, jobs_remaining)
        
        print(f"📦 Batch {batch_num}/{batches_needed}: Scraping {current_batch_size} jobs...")
        start_time = time.time()
        
        try:
            jobs_df = scrape_jobs(
                site_name=["linkedin"],
                search_term=search_term,
                location=location,
                results_wanted=current_batch_size,
                hours_old=72
            )
            
            if jobs_df is not None and len(jobs_df) > 0:
                all_jobs.append(jobs_df)
                elapsed = time.time() - start_time
                print(f"   ✅ {len(jobs_df)} jobs in {elapsed:.1f}s")
                print(f"   📊 Total: {sum(len(df) for df in all_jobs)} jobs")
            else:
                print(f"   ⚠️  No jobs returned")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            if "429" in str(e) or "rate" in str(e).lower():
                print(f"   🚫 Rate limited! Waiting 120s...")
                time.sleep(120)
                continue
        
        if len(all_jobs) >= total_jobs:
            break
            
        # Apply delay with random jitter
        if batch_num < batches_needed:
            delay = base_delay + random.uniform(0, random_jitter)
            print(f"   ⏳ Waiting {delay:.1f}s...\n")
            time.sleep(delay)
    
    return pd.concat(all_jobs, ignore_index=True) if all_jobs else pd.DataFrame()
