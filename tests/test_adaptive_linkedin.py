"""Test script for adaptive LinkedIn scraper
Run with: python test_adaptive_linkedin.py
"""
import asyncio
import logging
from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs_unified

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_adaptive_scraper():
    """Test adaptive scraper with 100 jobs"""
    print("🚀 Testing Adaptive LinkedIn Scraper")
    print("=" * 60)
    print("Configuration:")
    print("  - Concurrent workers: 8 (adaptive 2-8)")
    print("  - Base delay: 2.5s ±1s jitter")
    print("  - User agents: 11 variants (rotating)")
    print("  - Circuit breaker: 60s after 3x 429s")
    print("  - Expected speed: ~160 jobs/min")
    print("=" * 60)
    
    # Test with small batch first
    results = await scrape_linkedin_jobs_unified(
        keyword="Python Developer",
        location="United States",
        limit=100,
        headless=False  # Set True for production
    )
    
    print("\n" + "=" * 60)
    print(f"✅ Test completed!")
    print(f"📊 Results: {len(results)} jobs scraped")
    print("=" * 60)
    
    if results:
        sample = results[0]
        print("\n📋 Sample job:")
        print(f"  Title: {sample.actual_role}")
        print(f"  Company: {sample.company_name}")
        print(f"  Skills: {sample.skills[:100]}...")
        print(f"  URL: {sample.url[:60]}...")

if __name__ == "__main__":
    asyncio.run(test_adaptive_scraper())
