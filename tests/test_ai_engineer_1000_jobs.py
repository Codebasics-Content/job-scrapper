#!/usr/bin/env python3
"""
Test: Scrape 1000 AI Engineer jobs with rate limiting analysis
Purpose: Monitor LinkedIn rate limits, optimize scraping speed, extract skills
"""
from typing import Any
from tests.ai_engineer import scrape_with_monitoring, extract_and_store_skills


def print_rate_insights(metrics: dict[str, Any], job_count: int) -> None:
    """Print rate limiting analysis and recommendations"""
    print(f"\n{'='*70}")
    print("🎯 Rate Limiting Insights:")
    print(f"{'='*70}")
    print(f"📊 Total jobs: {job_count}")
    print(f"⏱️  Total time: {metrics['total_time']:.1f}s")
    print(f"⚡ Avg speed: {metrics['total_time']/job_count:.2f}s/job")
    print(f"🚨 Rate limit hits: {metrics['rate_limit_hits']}")
    print(f"\n📦 Batch Performance:")
    
    for batch in metrics['batches'][:5]:
        print(
            f"  Batch {batch['batch']}: {batch['jobs']} jobs, "
            f"{batch['time_sec']}s ({batch['rate_sec_per_job']}s/job)"
        )
    
    print(f"\n💡 Optimization Recommendations:")
    print(f"  • Batch size: 50 jobs (balanced)")
    print(f"  • Request delay: {metrics['total_time']/job_count:.1f}s")
    print(f"  • Max concurrent: 2-3 batches")
    print(f"{'='*70}\n")


def main() -> None:
    """Main orchestrator for AI Engineer job scraping test"""
    print(f"\n{'='*70}")
    print("AI Engineer Jobs: 1000-Job Scraping + Rate Analysis")
    print(f"{'='*70}\n")
    
    # Scrape with rate monitoring
    df, metrics = scrape_with_monitoring(
        role="AI Engineer",
        limit=1000,
        batch_size=50
    )
    
    if df.empty:
        print("\n❌ No jobs scraped")
        return
    
    # Extract skills and store
    stored = extract_and_store_skills(df)
    
    # Print insights
    print_rate_insights(metrics, len(df))
    print(f"\n✅ Test Complete: {stored} AI Engineer jobs in database")


if __name__ == "__main__":
    main()
