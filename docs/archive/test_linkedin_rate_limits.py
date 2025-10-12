#!/usr/bin/env python3
"""Test LinkedIn rate limits with JobSpy to determine optimal delays for large-scale scraping"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from python_jobspy import scrape_jobs

load_dotenv()

# Remove proxy for free scraping
os.environ.pop("PROXY_URL", None)

def test_rate_limits(batch_size=50, delay_seconds=2):
    """
    Test LinkedIn rate limiting by scraping in batches with delays
    
    Args:
        batch_size: Number of jobs per batch
        delay_seconds: Delay between batches
    """
    print("=" * 70)
    print("LinkedIn Rate Limit Test")
    print("=" * 70)
    print(f"Batch size: {batch_size}")
    print(f"Delay: {delay_seconds}s between batches")
    print()
    
    total_scraped = 0
    batch_num = 1
    errors = []
    
    try:
        while total_scraped < 200:  # Test up to 200 jobs
            print(f"\n📦 Batch {batch_num} - Scraping {batch_size} jobs...")
            start_time = time.time()
            
            try:
                jobs = scrape_jobs(
                    site_name=["linkedin"],
                    search_term="Software Engineer",
                    location="United States",
                    results_wanted=batch_size,
                    hours_old=72,
                    country_indeed="USA"
                )
                
                elapsed = time.time() - start_time
                scraped = len(jobs) if jobs is not None else 0
                total_scraped += scraped
                
                print(f"✅ Scraped {scraped} jobs in {elapsed:.1f}s")
                print(f"📊 Total: {total_scraped} jobs")
                
                if scraped < batch_size:
                    print(f"⚠️  Got less than requested ({scraped}/{batch_size})")
                
            except Exception as e:
                error_msg = str(e)
                errors.append({
                    'batch': batch_num,
                    'time': datetime.now(),
                    'error': error_msg
                })
                print(f"❌ Error: {error_msg}")
                
                if "429" in error_msg or "rate" in error_msg.lower():
                    print("🚫 RATE LIMIT HIT!")
                    break
            
            batch_num += 1
            
            if total_scraped < 200:
                print(f"⏳ Waiting {delay_seconds}s before next batch...")
                time.sleep(delay_seconds)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Test stopped by user")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total jobs scraped: {total_scraped}")
    print(f"Batches completed: {batch_num - 1}")
    print(f"Errors encountered: {len(errors)}")
    
    if errors:
        print("\n❌ Errors:")
        for err in errors:
            print(f"  Batch {err['batch']}: {err['error']}")
    
    return total_scraped, errors

if __name__ == "__main__":
    # Test different delay strategies
    print("🧪 Testing with 2-second delays...")
    test_rate_limits(batch_size=50, delay_seconds=2)
