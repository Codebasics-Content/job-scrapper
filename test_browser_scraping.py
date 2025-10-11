#!/usr/bin/env python3
"""Test BrightData Browser scraping with LinkedIn."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scraper.brightdata.linkedin_browser_scraper import scrape_linkedin_jobs_browser

print("="*60)
print("BrightData Browser Scraping Test")
print("="*60)
print("\n🔍 Testing LinkedIn real-time scraping...")
print("This will connect to BrightData's Scraping Browser\n")

try:
    # Test with small limit
    jobs = scrape_linkedin_jobs_browser(
        keyword="Python Developer",
        location="United States",
        limit=5  # Just 5 jobs for testing
    )
    
    print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
    print("\n" + "="*60)
    print("Sample Jobs:")
    print("="*60)
    
    for idx, job in enumerate(jobs[:3], 1):
        print(f"\n{idx}. {job.job_title}")
        print(f"   Company: {job.company_name}")
        print(f"   Location: {job.location}")
        print(f"   Skills: {', '.join(job.skills[:5]) if job.skills else 'None'}")
        print(f"   URL: {job.job_url[:80] if job.job_url else 'N/A'}...")
    
    print("\n" + "="*60)
    print("✅ Test completed successfully!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
