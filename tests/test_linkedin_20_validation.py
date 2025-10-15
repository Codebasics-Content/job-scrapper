"""LinkedIn 200-job scale test - Playwright Unified Scraper
Tests: Job descriptions, skill extraction, DB storage, BrightData proxy
RL: +10 if all pass, -15 if failures
"""
import asyncio
from datetime import datetime
from pathlib import Path
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs_unified


async def test_linkedin_200_jobs():
    """Test LinkedIn Playwright scraping: 200 AI Engineer jobs with descriptions + skills"""
    print("🧪 LinkedIn 200-Job Playwright Scale Test")
    print("=" * 60)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Target: 200 AI Engineer jobs from LinkedIn (Worldwide)")
    print("🔧 Platform: Playwright + BrightData scraping_browser2")
    print("⚡ Concurrency: 5 concurrent tabs (Naukri pattern)\n")
    
    db_path = Path(__file__).parent.parent / "jobs.db"
    print(f"💾 Database: {db_path}\n")
    
    # Scrape 200 LinkedIn jobs via Playwright
    print("🚀 Starting Playwright scrape with BrightData proxy...")
    print("📋 Phase 1: URL Collection (scroll job search)")
    print("📋 Phase 2: Detail Scraping (navigate + extract JD + skills)\n")
    start = datetime.now()
    jobs = await scrape_linkedin_jobs_unified(
        keyword="AI Engineer",
        location="",  # Worldwide search
        limit=200,
        headless=True  # Proxy controls browser, this param ignored
    )
    duration = (datetime.now() - start).total_seconds()
    print(f"\n⏱️  Scraping completed in {duration:.1f}s ({duration/60:.1f} min)")
    
    # Validation
    print(f"\n📊 Validating {len(jobs)} jobs...")
    print(f"📋 Checking: Job descriptions (>50 chars) + Skills extraction")
    print(f"📦 Batch Size: 10 jobs per batch\n")
    
    passed = 0
    failed = 0
    batch_start = datetime.now()
    
    for idx, job in enumerate(jobs, 1):
        has_desc = bool(job.job_description and len(job.job_description) > 50)
        has_skills = bool(job.skills and len(job.skills) > 0)
        
        if has_desc and has_skills:
            passed += 1
        else:
            failed += 1
            print(f"  ❌ Job {idx}: desc={len(job.job_description) if job.job_description else 0}, skills={job.skills}")
        
        # Batch logging every 10 jobs
        if idx % 10 == 0:
            batch_time = (datetime.now() - batch_start).total_seconds()
            print(f"\n  📦 BATCH {idx//10}: Jobs {idx-9}-{idx}")
            print(f"     ✅ Passed in batch: {passed - (passed - 10 if idx > 10 else 0)}")
            print(f"     ⏱️  Batch time: {batch_time:.2f}s")
            print(f"     📊 Total progress: {idx}/{len(jobs)} ({idx/len(jobs)*100:.1f}%)")
            print(f"     ✅ Cumulative passed: {passed}")
            print(f"     ❌ Cumulative failed: {failed}\n")
            batch_start = datetime.now()
    
    # Results
    print("\n" + "="*60)
    print("📈 RESULTS SUMMARY")
    print("="*60)
    
    if len(jobs) == 0:
        print("⚠️  No jobs scraped (all were duplicates or LinkedIn has no new jobs)")
        print(f"💡 Suggestion: Clear database OR use different search keyword")
        print(f"⏱️  Total Time: {duration:.1f}s ({duration/60:.1f} min)")
        print(f"💾 Database: {db_path}")
        return
    
    print(f"✅ Passed: {passed}/{len(jobs)} ({passed/len(jobs)*100:.1f}%)")
    print(f"❌ Failed: {failed}/{len(jobs)} ({failed/len(jobs)*100:.1f}%)")
    print(f"⏱️  Total Time: {duration:.1f}s ({duration/60:.1f} min)")
    print(f"💾 Database: {db_path}")
    print(f"⚡ Speed: {len(jobs)/duration:.2f} jobs/sec")
    print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # RL scoring
    if failed == 0:
        print(f"🎉 RL REWARD: +10 (100% success)")
        return {"reward": 10, "passed": passed, "failed": 0}
    else:
        print(f"⚠️  RL PENALTY: -15 ({failed} failures)")
        return {"penalty": -15, "passed": passed, "failed": failed}


if __name__ == "__main__":
    result = asyncio.run(test_linkedin_200_jobs())
    sys.exit(0 if result and result.get("failed", 0) == 0 else 1)
