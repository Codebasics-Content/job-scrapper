"""Quick integration test with authenticated Luminati + HeadlessX"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure HeadlessX (running on Docker port 3000)
os.environ["HEADLESSX_BASE_URL"] = "http://localhost:3000"
os.environ["HEADLESSX_TOKEN"] = "test-token"  # Default for local dev

from src.db.operations import JobStorageOperations
from src.analysis.skill_statistics import calculate_skill_percentages
from src.scraper.services.browserless_adapter import BrowserlessAdapter
from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs_unified


def quick_integration_test() -> None:
    """Quick validation: LinkedIn scraping → DB → Analysis"""
    print("="*60)
    print("🚀 QUICK INTEGRATION TEST")
    print("="*60)
    
    # Test parameters
    keyword = "Data Analyst"
    limit = 5
    
    print(f"\n[1/3] 🔍 Scraping {limit} {keyword} jobs from LinkedIn...")
    print(f"Proxy: US residential (24000)")
    
    try:
        import asyncio
        jobs = asyncio.run(scrape_linkedin_jobs_unified(
            keyword=keyword,
            location="United States",
            limit=limit
        ))
        
        print(f"✅ Scraped {len(jobs)} jobs")
        
        if len(jobs) == 0:
            print("❌ No jobs scraped - check HeadlessX and proxy")
            return
            
        # Step 2: Store in database
        print(f"\n[2/3] 💾 Storing jobs in database...")
        db = JobStorageOperations("quick_test.db")
        stored = db.store_jobs(jobs)
        print(f"✅ Stored {stored} jobs")
        
        # Step 3: Analyze skills
        print(f"\n[3/3] 📊 Analyzing skill statistics...")
        percentages = calculate_skill_percentages(jobs)
        
        print(f"\n📈 Top 5 Skills:")
        for i, (skill, pct) in enumerate(list(percentages.items())[:5], 1):
            print(f"  {i}. {skill}: {pct:.1f}%")
        
        print("\n" + "="*60)
        print("✅ INTEGRATION TEST COMPLETE")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    quick_integration_test()
