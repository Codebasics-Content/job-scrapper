"""Naukri 20-job validation test - Playwright scraper
Tests: Job descriptions, skill extraction, DB storage
RL: +10 if all pass, -15 if failures
"""
import asyncio
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.naukri.browser_scraper import scrape_naukri_jobs_browser
from src.db.operations import JobStorageOperations


async def test_naukri_20_jobs():
    """Test Naukri scraping: 1000 AI Engineer jobs with descriptions + skills"""
    print("🧪 Naukri 1000-Job Scale Test")
    print("=" * 60)
    
    db_path = Path(__file__).parent.parent / "jobs.db"
    db_ops = JobStorageOperations(str(db_path))
    
    # Scrape 20 Naukri jobs
    start = datetime.now()
    jobs = await scrape_naukri_jobs_browser(
        keyword="AI Engineer",
        location="",
        limit=100000,
        headless=False
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
    if len(jobs) == 0:
        print(f"❌ RL PENALTY: -20 (0 jobs scraped - scraper broken)")
        return {"penalty": -20, "passed": 0, "failed": 0}
    elif failed == 0:
        print(f"🎉 RL REWARD: +10 (100% success)")
        return {"reward": 10, "passed": passed, "failed": 0}
    else:
        print(f"⚠️  RL PENALTY: -15 ({failed} failures)")
        return {"penalty": -15, "passed": passed, "failed": failed}


if __name__ == "__main__":
    result = asyncio.run(test_naukri_20_jobs())
    sys.exit(0 if result.get("failed", 0) == 0 else 1)
