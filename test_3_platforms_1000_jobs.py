"""Test: Scrape 1000 jobs from each platform (LinkedIn, Indeed, Naukri) - ≤80 lines"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from src.scraper.jobspy import scrape_multi_platform, proxy_status


def test_3_platforms():
    """
    Scrape 1000 jobs from each of the 3 supported platforms
    
    Platforms:
    - LinkedIn: BrightData proxy (if configured)
    - Indeed: Direct scraping (no proxy)
    - Naukri: Direct scraping (no proxy)
    """
    print("\n" + "=" * 80)
    print("🚀 JOBSPY 3-PLATFORM TEST: 1000 JOBS EACH")
    print("=" * 80)
    
    # Check proxy status
    print("\n📊 Proxy Configuration:")
    status = proxy_status()
    for platform, has_proxy in status.items():
        if platform != "brightdata_configured":
            emoji = "🌐" if has_proxy else "🆓"
            print(f"   {emoji} {platform.capitalize()}: {'Proxy' if has_proxy else 'Direct'}")
    
    # Scrape configuration
    platforms = ["linkedin", "indeed", "naukri"]
    search_term = "AI Engineer"
    location = "United States"
    jobs_per_platform = 1000
    
    print(f"\n🔍 Search Configuration:")
    print(f"   Keywords: {search_term}")
    print(f"   Location: {location}")
    print(f"   Jobs per platform: {jobs_per_platform}")
    print(f"   Total target: {jobs_per_platform * len(platforms)} jobs")
    
    # Start scraping
    print("\n" + "=" * 80)
    print("📥 SCRAPING STARTED")
    print("=" * 80)
    
    start_time = datetime.now()
    
    jobs_df = scrape_multi_platform(
        platforms=platforms,
        search_term=search_term,
        location=location,
        results_wanted=jobs_per_platform,
        hours_old=72,
        linkedin_fetch_description=True,
    )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Results summary
    print("\n" + "=" * 80)
    print("✅ SCRAPING COMPLETE")
    print("=" * 80)
    print(f"   Total jobs scraped: {len(jobs_df)}")
    print(f"   Duration: {duration:.1f} seconds")
    print(f"   Rate: {len(jobs_df) / duration:.1f} jobs/second")
    
    # Save results
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"jobs_3platforms_{timestamp}.csv"
    
    jobs_df.to_csv(output_file, index=False)
    print(f"\n💾 Results saved: {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")
    
    return jobs_df


if __name__ == "__main__":
    test_3_platforms()
