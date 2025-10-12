"""Actual implementation test with 100 jobs - find real gaps"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.linkedin_unified import scrape_linkedin_jobs_unified
from src.db.connection import DatabaseConnection
from src.db.operations import JobStorageOperations


async def test_actual_scraping():
    """Test actual LinkedIn scraping with 100 jobs target"""
    print("🚀 Starting actual scraping test - Target: 100 jobs")
    print("=" * 60)
    
    # Test configuration
    keyword = "Data Analyst"
    location = "United States"
    target_jobs = 100
    
    try:
        # 1. Scrape jobs
        print(f"\n📊 Scraping LinkedIn: '{keyword}' in '{location}'")
        print(f"   Target: {target_jobs} jobs\n")
        
        jobs = await scrape_linkedin_jobs_unified(
            keyword=keyword,
            location=location,
            limit=target_jobs
        )
        
        print(f"\n✅ Scraping complete: {len(jobs)} jobs retrieved")
        
        # 2. Analyze results
        print("\n📈 Analysis:")
        print(f"   • Jobs with descriptions: {sum(1 for j in jobs if j.description)}")
        print(f"   • Jobs with skills: {sum(1 for j in jobs if j.skills_list)}")
        print(f"   • Average description length: {sum(len(j.description or '') for j in jobs) // max(len(jobs), 1)} chars")
        
        # 3. Store in database
        print("\n💾 Storing in database...")
        db_path = "jobs.db"
        
        with DatabaseConnection(db_path) as conn:
            storage = JobStorageOperations(conn)
            stored = storage.bulk_insert_jobs(jobs)
            print(f"   ✅ Stored {stored} jobs")
        
        # 4. Identify gaps
        print("\n🔍 Gap Analysis:")
        missing_desc = [j.job_id for j in jobs if not j.description]
        missing_skills = [j.job_id for j in jobs if not j.skills_list]
        
        if missing_desc:
            print(f"   ⚠️  {len(missing_desc)} jobs missing descriptions")
        if missing_skills:
            print(f"   ⚠️  {len(missing_skills)} jobs missing skills")
        
        if not missing_desc and not missing_skills:
            print("   ✅ No gaps found - all jobs have descriptions and skills!")
        
        # 5. Sample output
        if jobs:
            print(f"\n📋 Sample Job:")
            sample = jobs[0]
            print(f"   • ID: {sample.job_id}")
            print(f"   • Title: {sample.title}")
            print(f"   • Description: {sample.description[:100]}...")
            print(f"   • Skills: {sample.skills_list[:5] if sample.skills_list else 'None'}")
        
        return len(jobs), len(missing_desc), len(missing_skills)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 0, 0, 0


if __name__ == "__main__":
    scraped, missing_desc, missing_skills = asyncio.run(test_actual_scraping())
    print(f"\n{'='*60}")
    print(f"Final Results: {scraped} jobs | {missing_desc} gaps (desc) | {missing_skills} gaps (skills)")
