#!/usr/bin/env python3
"""Test JobSpy LinkedIn scraping with BrightData proxy"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from importer.jobspy import scrape_linkedin_jobs


def test_linkedin_scraping():
    """Test LinkedIn scraping with small batch"""
    
    print("=" * 60)
    print("JobSpy LinkedIn Scraper Test")
    print("=" * 60)
    
    # Check proxy configuration
    proxy = os.getenv("PROXY_URL")
    print(f"\n✓ BrightData Proxy: {proxy if proxy else '❌ Not configured'}")
    
    # Use WITHOUT proxy for 100% free LinkedIn scraping
    # JobSpy works perfectly without BrightData proxies
    os.environ.pop("PROXY_URL", None)
    print("⚠️  Running in FREE mode (no proxy, no BrightData costs)")
    
    # Test parameters
    keyword = "Python Developer"
    location = "United States"
    limit = 10  # Small test batch
    
    print(f"\n📊 Search Parameters:")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    print(f"   Fetch descriptions: True")
    
    print(f"\n🚀 Starting scrape...")
    
    # Scrape jobs
    jobs = scrape_linkedin_jobs(
        keyword=keyword,
        location=location,
        limit=limit,
        fetch_description=True
    )
    
    # Results
    print(f"\n✅ Results: {len(jobs)} jobs scraped")
    
    if jobs:
        print(f"\n📋 Sample Job:")
        job = jobs[0]
        print(f"   Title: {job.get('title', 'N/A')}")
        print(f"   Company: {job.get('company', 'N/A')}")
        print(f"   Location: {job.get('location', 'N/A')}")
        print(f"   Job Type: {job.get('job_type', 'N/A')}")
        print(f"   URL: {job.get('job_url', 'N/A')[:60]}...")
        
        desc = job.get('description', '')
        if desc:
            print(f"   Description: {desc[:100]}...")
    
    print(f"\n" + "=" * 60)
    return jobs


if __name__ == "__main__":
    test_linkedin_scraping()
