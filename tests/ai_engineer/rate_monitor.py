"""Rate limiting monitor for scraping operations"""
import time
from typing import Any
import pandas as pd
from jobspy import scrape_jobs


def scrape_with_monitoring(
    role: str, 
    limit: int = 1000, 
    batch_size: int = 50
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Scrape jobs in batches with rate limit monitoring"""
    all_jobs = []
    rate_metrics: dict[str, Any] = {
        "batches": [],
        "total_time": 0,
        "rate_limit_hits": 0,
        "avg_delay": 0
    }
    
    start_time = time.time()
    
    for batch_num in range(0, limit, batch_size):
        batch_start = time.time()
        actual_limit = min(batch_size, limit - batch_num)
        
        print(f"\n📦 Batch {batch_num//batch_size + 1}: Scraping {actual_limit} jobs...")
        
        try:
            jobs = scrape_jobs(
                site_name=["linkedin"],
                search_term=role,
                location="United States",
                results_wanted=actual_limit,
                hours_old=72,
                country_indeed="USA"
            )
            
            batch_time = time.time() - batch_start
            jobs_count = len(jobs) if jobs is not None else 0
            
            rate_metrics["batches"].append({
                "batch": batch_num//batch_size + 1,
                "jobs": jobs_count,
                "time_sec": round(batch_time, 2),
                "rate_sec_per_job": round(batch_time / max(jobs_count, 1), 2)
            })
            
            if jobs is not None and len(jobs) > 0:
                all_jobs.append(jobs)
                print(f"✅ Got {len(jobs)} jobs in {batch_time:.1f}s")
            else:
                print(f"⚠️  No jobs - possible rate limit")
                rate_metrics["rate_limit_hits"] += 1
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            rate_metrics["rate_limit_hits"] += 1
            time.sleep(5)
    
    rate_metrics["total_time"] = time.time() - start_time
    
    if all_jobs:
        return pd.concat(all_jobs, ignore_index=True), rate_metrics
    return pd.DataFrame(), rate_metrics
