"""Test: 3-platform scraping (1000 jobs each) with detailed logging (≤80 lines)"""
from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.jobspy import scrape_multi_platform, proxy_status

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tests/test_output.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def test_3_platforms_with_logs() -> pd.DataFrame:
    """Scrape 1000 jobs from each platform with detailed logging"""
    logger.info("="*80)
    logger.info("🚀 3-PLATFORM TEST: 1000 JOBS EACH (HEADLESS=FALSE)")
    logger.info("="*80)
    
    # Show proxy configuration
    logger.info("\n📊 Proxy Status Check:")
    status = proxy_status()
    for platform, has_proxy in status.items():
        if platform != "brightdata_configured":
            emoji = "🌐" if has_proxy else "🆓"
            logger.info(f"   {emoji} {platform.capitalize()}: {'Proxy' if has_proxy else 'Direct'}")
    
    # Test configuration
    platforms = ["linkedin", "indeed", "naukri"]
    search_term = "AI Engineer"
    location = ""  # Empty for worldwide search without country barriers
    jobs_per_platform = 1000
    
    logger.info(f"\n🔍 Configuration:")
    logger.info(f"   Search Term: {search_term}")
    logger.info(f"   Location: {location}")
    logger.info(f"   Jobs per Platform: {jobs_per_platform}")
    logger.info(f"   Total Target: {jobs_per_platform * 3}")
    logger.info(f"   Headless: FALSE (visible browser)")
    
    logger.info("\n" + "="*80)
    logger.info("📥 SCRAPING STARTED")
    logger.info("="*80)
    
    start_time = datetime.now()
    logger.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scrape with detailed progress
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
    logger.info("\n" + "="*80)
    logger.info("✅ SCRAPING COMPLETE")
    logger.info("="*80)
    logger.info(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Total Jobs: {len(jobs_df)}")
    logger.info(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    logger.info(f"Rate: {len(jobs_df)/duration:.2f} jobs/second")
    
    return jobs_df


if __name__ == "__main__":
    result_df = test_3_platforms_with_logs()
