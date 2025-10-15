"""Test JobSpy with BrightData residential proxy - 200 LinkedIn jobs"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.jobspy.multi_platform_scraper import scrape_multi_platform
from src.scraper.jobspy.proxy_config import proxy_status
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_linkedin_200_with_proxy():
    """Test scraping 200 LinkedIn jobs with BrightData residential proxy"""
    
    print("\n" + "="*70)
    print("🧪 TESTING: JobSpy + BrightData Residential Proxy")
    print("="*70)
    
    # Check proxy configuration
    status = proxy_status()
    print(f"\n📊 Proxy Status:")
    for key, value in status.items():
        icon = "✅" if value else "❌"
        print(f"   {icon} {key}: {value}")
    
    if not status["brightdata_configured"]:
        print("\n❌ ERROR: BrightData proxy not configured in .env")
        print("   Please set PROXY_URL environment variable")
        return
    
    print(f"\n🎯 Target: 200 LinkedIn jobs")
    print(f"🔍 Search: 'AI Engineer'")
    print(f"📍 Location: '' (worldwide)")
    print(f"⏰ Max age: 72 hours")
    
    try:
        # Scrape with proxy (will be capped at 100 by multi_platform_scraper)
        results_df = scrape_multi_platform(
            platforms=["linkedin"],
            search_term="AI Engineer",
            location="",  # Worldwide
            results_wanted=200,  # Note: Will be capped at 100 internally
            hours_old=72,
            linkedin_fetch_description=True,
            store_to_db=True
        )
        
        print(f"\n" + "="*70)
        print(f"✅ SCRAPING COMPLETED")
        print(f"="*70)
        print(f"📦 Total jobs scraped: {len(results_df)}")
        print(f"📝 Jobs stored in database: jobs.db")
        
        # Show sample
        if len(results_df) > 0:
            print(f"\n📋 Sample job (first result):")
            first_job = results_df.iloc[0]
            print(f"   Title: {first_job.get('title', 'N/A')}")
            print(f"   Company: {first_job.get('company', 'N/A')}")
            print(f"   Location: {first_job.get('location', 'N/A')}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_linkedin_200_with_proxy()
