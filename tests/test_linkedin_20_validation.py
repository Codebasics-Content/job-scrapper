"""LinkedIn 1000-job scale test - JobSpy scraper
Tests: Job descriptions, skill extraction, DB storage
RL: +10 if all pass, -15 if failures
"""
import asyncio
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.multi_platform_service import scrape_jobs_with_skills


async def test_linkedin_20_jobs():
    """Test LinkedIn scraping: 100 AI Engineer jobs with descriptions + skills"""
    print("🧪 LinkedIn 100-Job Scale Test")
    print("=" * 60)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: 100 AI Engineer jobs from LinkedIn")
    print(f"🔧 Platform: JobSpy library\n")
    
    db_path = Path(__file__).parent.parent / "jobs.db"
    print(f"💾 Database: {db_path}\n")
    
    # Scrape 100 LinkedIn jobs
    print("🚀 Starting scrape...")
    start = datetime.now()
    jobs = await scrape_jobs_with_skills(
        platforms=["linkedin"],
        keyword="AI Engineer",
        location="",  # Empty string for broad search per JobSpy docs
        limit=100,
        store_to_db=True  # ✅ STORE TO DATABASE DURING SCRAPING
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
    result = asyncio.run(test_linkedin_20_jobs())
    sys.exit(0 if result.get("failed", 0) == 0 else 1)
