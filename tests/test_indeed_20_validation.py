"""Indeed 20-job validation test - JobSpy scraper
Tests: Job descriptions, skill extraction, DB storage
RL: +10 if all pass, -15 if failures
"""
import asyncio
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.multi_platform_service import scrape_jobs_with_skills
from src.db.operations import JobStorageOperations


async def test_indeed_20_jobs():
    """Test Indeed scraping: 20 jobs with descriptions + skills"""
    print("🧪 Indeed 20-Job Validation Test")
    print("=" * 60)
    
    db_path = Path(__file__).parent.parent / "jobs.db"
    db_ops = JobStorageOperations(str(db_path))
    
    # Scrape 20 Indeed jobs
    start = datetime.now()
    jobs = await scrape_jobs_with_skills(
        platforms=["indeed"],
        keyword="Python Developer",
        location="",  # Empty string for broad search per JobSpy docs
        limit=20,
        store_to_db=False
    )
    
    duration = (datetime.now() - start).total_seconds()
    
    # Validation
    passed = 0
    failed = 0
    
    print(f"\n✅ Scraped {len(jobs)} jobs in {duration:.1f}s")
    
    for idx, job in enumerate(jobs, 1):
        has_desc = bool(job.job_description and len(job.job_description) > 50)
        has_skills = bool(job.skills and len(job.skills) > 0)
        
        if has_desc and has_skills:
            passed += 1
            print(f"  ✅ Job {idx}: {len(job.job_description)} chars, {len(job.skills.split(','))} skills")
        else:
            failed += 1
            print(f"  ❌ Job {idx}: desc={len(job.job_description) if job.job_description else 0}, skills={job.skills}")
    
    # Store to DB
    stored = db_ops.store_details(jobs)
    
    # Results
    print(f"\n{'='*60}")
    print(f"✅ Passed: {passed}/{len(jobs)}")
    print(f"❌ Failed: {failed}/{len(jobs)}")
    print(f"💾 Stored: {stored} jobs to DB")
    
    # RL scoring
    if failed == 0:
        print(f"🎉 RL REWARD: +10 (100% success)")
        return {"reward": 10, "passed": passed, "failed": 0}
    else:
        print(f"⚠️  RL PENALTY: -15 ({failed} failures)")
        return {"penalty": -15, "passed": passed, "failed": failed}


if __name__ == "__main__":
    result = asyncio.run(test_indeed_20_jobs())
    sys.exit(0 if result.get("failed", 0) == 0 else 1)
