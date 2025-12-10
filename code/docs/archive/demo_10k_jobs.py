#!/usr/bin/env python3
"""Demo: Scrape 10,000 LinkedIn jobs with rate limiting"""
import os
from dotenv import load_dotenv
from src.importer.jobspy.batch_scraper import scrape_jobs_batch

load_dotenv()

# Remove proxy for free scraping
os.environ.pop("PROXY_URL", None)

def main():
    """Scrape 10,000 jobs with optimal rate limiting"""
    
    print("=" * 70)
    print("LinkedIn Large-Scale Scraping Demo")
    print("=" * 70)
    print()
    print("🎯 Strategy:")
    print("   • Batch size: 100 jobs")
    print("   • Delay: 3-5 seconds (random)")
    print("   • Estimated time: ~15 minutes")
    print("   • Cost: $0 (no proxy needed)")
    print()
    
    # Scrape 10,000 jobs
    jobs_df = scrape_jobs_batch(
        search_term="Software Engineer",
        location="United States",
        total_jobs=10000,
        batch_size=100,
        base_delay=3.0,
        random_jitter=2.0
    )
    
    # Save results
    if len(jobs_df) > 0:
        output_file = "linkedin_10k_jobs.csv"
        jobs_df.to_csv(output_file, index=False)
        
        print()
        print("=" * 70)
        print("✅ SUCCESS")
        print("=" * 70)
        print(f"📊 Total jobs scraped: {len(jobs_df)}")
        print(f"💾 Saved to: {output_file}")
        print()
        print("📋 Sample job:")
        print(jobs_df[['title', 'company', 'location']].head(1))
    else:
        print("\n❌ No jobs scraped")

if __name__ == "__main__":
    main()
