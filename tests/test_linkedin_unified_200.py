"""Test LinkedIn Unified Scraper with BrightData Proxy - 200 AI Engineer Jobs"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs_unified
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_linkedin_unified():
    """Test LinkedIn Unified Scraper (Playwright + BrightData)"""
    
    print("\n" + "="*70)
    print("🧪 TESTING: LinkedIn Unified Scraper - 1000 Jobs at Scale")
    print("="*70)
    
    print(f"\n🎯 Target: 1000 UNIQUE LinkedIn jobs (after deduplication)")
    print(f"🔍 Search: 'AI Engineer'")
    print(f"📍 Location: '' (worldwide)")
    print(f"🌐 Method: Playwright with BrightData residential proxy")
    print(f"⚡ Adaptive collection: will gather ~500 URLs (max)")
    
    try:
        # Scrape using unified Playwright scraper
        jobs = await scrape_linkedin_jobs_unified(
            keyword="AI Engineer",
            location="",  # Worldwide
            limit=1000,  # 1000 UNIQUE jobs after deduplication
            headless=False  # Visible browser for debugging
        )
        
        print(f"\n" + "="*70)
        print(f"✅ SCRAPING COMPLETED")
        print(f"="*70)
        print(f"📦 Total UNIQUE jobs scraped: {len(jobs)}")
        print(f"📝 Jobs stored in database: jobs.db")
        
        # Show sample
        if len(jobs) > 0:
            first_job = jobs[0]
            print(f"\n📋 Sample job (first result):")
            print(f"   Role: {first_job.actual_role}")
            print(f"   Company: {first_job.company_name}")
            print(f"   URL: {first_job.url[:60]}...")
            print(f"   Skills: {first_job.skills[:100]}..." if first_job.skills else "   Skills: None")
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_linkedin_unified())
