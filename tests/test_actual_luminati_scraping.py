"""Actual scraping test using Luminati proxy - bypass browser rendering"""
import asyncio
import httpx
from bs4 import BeautifulSoup
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.linkedin.url_builder import build_search_url
from src.scraper.unified.linkedin.selectors import SEARCH_SELECTOR
from src.scraper.unified.linkedin.parser import create_job_model
from src.db.connection import DatabaseConnection
from src.db.operations import JobStorageOperations


async def fetch_with_luminati(url: str, proxy_url: str) -> str:
    """Fetch URL via Luminati proxy"""
    async with httpx.AsyncClient(proxy=proxy_url, timeout=30.0) as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        return response.text


async def test_linkedin_luminati_scraping():
    """Test LinkedIn scraping with Luminati proxy"""
    print("🚀 Actual LinkedIn scraping via Luminati Proxy")
    print("=" * 60)
    
    # Luminati proxy configuration
    proxy_username = "codebasics-gkl7gk6qk7s0"
    proxy_password = "codebasics"
    proxy_url = f"http://{proxy_username}:{proxy_password}@zproxy.lum-superproxy.io:24000"
    
    keyword = "Data Analyst"
    location = "United States"
    target_jobs = 100
    
    print(f"\n📊 Configuration:")
    print(f"   • Keyword: {keyword}")
    print(f"   • Location: {location}")
    print(f"   • Target: {target_jobs} jobs")
    print(f"   • Proxy: Luminati (US zone)")
    
    try:
        # Step 1: Fetch search results
        search_url = build_search_url(keyword, location)
        print(f"\n🔍 Fetching search page...")
        print(f"   URL: {search_url[:80]}...")
        
        html = await fetch_with_luminati(search_url, proxy_url)
        soup = BeautifulSoup(html, "html.parser")
        
        # Step 2: Extract job URLs
        job_urls = []
        for a in soup.select(SEARCH_SELECTOR):
            href = a.get("href")
            if href and href.startswith("http"):
                job_urls.append(href)
            if len(job_urls) >= target_jobs:
                break
        
        print(f"   ✅ Found {len(job_urls)} job URLs")
        
        if not job_urls:
            print("\n⚠️  No job URLs found. Possible issues:")
            print("   • Selector may be outdated")
            print("   • LinkedIn structure changed")
            print("   • Anti-bot detection")
            return 0, 0, 0
        
        # Step 3: Fetch and parse individual jobs
        print(f"\n📥 Fetching job details (first 10 for testing)...")
        jobs = []
        test_limit = min(10, len(job_urls))
        
        for i, job_url in enumerate(job_urls[:test_limit], 1):
            try:
                print(f"   [{i}/{test_limit}] Fetching job...", end="\r")
                job_html = await fetch_with_luminati(job_url, proxy_url)
                job = create_job_model(job_url, job_html)
                if job:
                    jobs.append(job)
                await asyncio.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"\n   ⚠️  Failed to fetch job {i}: {str(e)[:50]}")
        
        print(f"\n   ✅ Successfully parsed {len(jobs)}/{test_limit} jobs")
        
        # Step 4: Analyze results
        print(f"\n📊 Analysis:")
        with_desc = sum(1 for j in jobs if j.description)
        with_skills = sum(1 for j in jobs if j.skills_list)
        avg_desc_len = sum(len(j.description or '') for j in jobs) // max(len(jobs), 1)
        
        print(f"   • Jobs with descriptions: {with_desc}/{len(jobs)}")
        print(f"   • Jobs with skills: {with_skills}/{len(jobs)}")
        print(f"   • Avg description length: {avg_desc_len} chars")
        
        # Step 5: Store in database
        if jobs:
            print(f"\n💾 Storing in database...")
            db_path = "jobs.db"
            
            with DatabaseConnection(db_path) as conn:
                storage = JobStorageOperations(conn)
                stored = storage.bulk_insert_jobs(jobs)
                print(f"   ✅ Stored {stored} jobs")
        
        # Step 6: Identify gaps
        print(f"\n🔍 Gap Analysis:")
        missing_desc = len(jobs) - with_desc
        missing_skills = len(jobs) - with_skills
        
        if missing_desc > 0:
            print(f"   ⚠️  {missing_desc} jobs missing descriptions ({missing_desc/len(jobs)*100:.1f}%)")
        if missing_skills > 0:
            print(f"   ⚠️  {missing_skills} jobs missing skills ({missing_skills/len(jobs)*100:.1f}%)")
        
        if missing_desc == 0 and missing_skills == 0:
            print("   ✅ Perfect! All jobs have descriptions and skills")
        
        # Step 7: Sample output
        if jobs:
            print(f"\n📋 Sample Job:")
            sample = jobs[0]
            print(f"   • Title: {sample.title}")
            print(f"   • Description: {sample.description[:100] if sample.description else 'MISSING'}...")
            print(f"   • Skills: {', '.join(sample.skills_list[:5]) if sample.skills_list else 'MISSING'}")
        
        return len(jobs), missing_desc, missing_skills
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 0, 0, 0


if __name__ == "__main__":
    scraped, missing_desc, missing_skills = asyncio.run(test_linkedin_luminati_scraping())
    print(f"\n{'='*60}")
    print(f"Results: {scraped} jobs | {missing_desc} gaps (desc) | {missing_skills} gaps (skills)")
    
    if scraped > 0:
        success_rate = ((scraped - missing_desc) / scraped * 100) if scraped else 0
        print(f"Success Rate: {success_rate:.1f}% jobs with complete data")
