"""LinkedIn scraper using BrightData Datasets API (pre-collected data)."""
from typing import List, Optional, Dict, Any
import asyncio
import time
import requests
from datetime import datetime

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from .config.settings import get_settings


async def scrape_linkedin_jobs_browser(
    keyword: str,
    location: Optional[str] = None,
    limit: int = 50
) -> List[JobModel]:
    """Scrape LinkedIn jobs using BrightData Datasets API (pre-collected data).
    
    Args:
        keyword: Job search keyword (e.g., "Machine Learning Engineer")
        location: Location filter (e.g., "United States", "San Francisco, CA")
        limit: Maximum number of jobs to scrape
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"🚀 Starting LinkedIn Datasets API scraping...")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location or 'United States'}")
    print(f"   Limit: {limit}")
    
    # Initialize parser
    parser = SkillsParser()
    settings = get_settings()
    
    # Prepare BrightData API request
    url = f"{settings.base_url}{settings.trigger_endpoint}"
    headers = {
        "Authorization": settings.api_token if settings.api_token.startswith("Bearer") else f"Bearer {settings.api_token}",
        "Content-Type": "application/json",
    }
    params = {
        "dataset_id": settings.linkedin_dataset_id,
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
    }
    data = {
        "input": [{
            "keyword": keyword,
            "location": location or "United States",
            "country": "",
            "time_range": "Past week",
            "job_type": "",
            "experience_level": "",
            "remote": "",
            "company": "",
            "location_radius": ""
        }],
        "custom_output_fields": [
            "url", "job_posting_id", "job_title", "company_name", "company_id",
            "job_location", "job_summary", "job_seniority_level", "job_function",
            "job_employment_type", "job_industries", "job_base_pay_range",
            "base_salary"
        ],
    }
    
    # Call BrightData API in thread pool
    print(f"📡 Calling BrightData Datasets API...")
    
    def _call_brightdata_api() -> List[Dict[str, Any]]:
        # Trigger collection
        print(f"   POST {url}")
        print(f"   Dataset ID: {params['dataset_id']}")
        response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"   ❌ Error Response: {response.text}")
            response.raise_for_status()
        
        trigger_result = response.json()
        print(f"   Trigger Result: {trigger_result}")
        
        snapshot_id = trigger_result.get("snapshot_id")
        
        if not snapshot_id:
            raise RuntimeError(f"No snapshot_id in response: {trigger_result}")
        
        print(f"   ✅ Snapshot ID: {snapshot_id}")
        print(f"   Polling for results...")
        
        # Poll for results
        snapshot_url = f"{settings.base_url}{settings.snapshot_endpoint}/{snapshot_id}"
        print(f"   Polling URL: {snapshot_url}")
        print(f"   ⏳ BrightData is collecting data in real-time (this may take 2-5 minutes)...")
        
        max_wait = 300  # 5 minutes max (BrightData collections can take time)
        start_time = time.time()
        poll_count = 0
        
        while time.time() - start_time < max_wait:
            poll_response = requests.get(snapshot_url, headers=headers, timeout=30)
            poll_count += 1
            
            # Accept both 200 and 202 status codes
            if poll_response.status_code not in (200, 202):
                print(f"   ❌ Poll Error ({poll_response.status_code}): {poll_response.text}")
                poll_response.raise_for_status()
            
            snapshot_data = poll_response.json()
            status = snapshot_data.get("status", "").lower()
            
            # Show progress every 30 seconds
            if poll_count == 1 or poll_count % 15 == 0:
                elapsed = int(time.time() - start_time)
                print(f"   🔄 Poll #{poll_count} ({elapsed}s elapsed) - Status: {status}")
            
            if status == "ready":
                elapsed = int(time.time() - start_time)
                print(f"   ✅ Data ready after {elapsed}s!")
                return snapshot_data.get("data", [])
            elif status in ("error", "failed"):
                error_msg = snapshot_data.get("error", "Unknown error")
                raise RuntimeError(f"Snapshot failed: {error_msg}")
            
            time.sleep(2)  # Poll every 2 seconds
        
        raise TimeoutError(f"Polling timed out after {max_wait}s - BrightData collection is still running")
    
    raw_jobs = await asyncio.to_thread(_call_brightdata_api)
    
    print(f"📥 Received {len(raw_jobs)} jobs from BrightData Datasets API")
    
    # Convert to JobModel with skills extraction
    job_models = []
    for idx, raw_job in enumerate(raw_jobs, 1):
        try:
            # Extract fields from BrightData Datasets API response
            job_title = raw_job.get("job_title", "Unknown")
            company_name = raw_job.get("company_name", "Unknown")
            job_location = raw_job.get("job_location", "Unknown")
            job_url = raw_job.get("url", "")
            job_id = raw_job.get("job_posting_id") or job_url
            
            # Get full job description from job_summary
            job_description = raw_job.get("job_summary", "")
            
            # Extract skills from description using regex patterns
            skills_list = parser.extract_from_text(job_description)
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            # Log first 2 jobs for debugging
            if idx <= 2:
                print(f"\n📝 LinkedIn Job #{idx}:")
                print(f"   Title: {job_title}")
                print(f"   Company: {company_name}")
                print(f"   Description Length: {len(job_description)} chars")
                print(f"   Description Preview: {job_description[:200]}...")
                print(f"   Extracted Skills ({len(skills_list)}): {skills_list[:10]}")
            
            # Extract salary info
            salary = None
            base_salary = raw_job.get("base_salary", {})
            if base_salary and base_salary.get("min_amount"):
                min_amt = base_salary.get("min_amount", 0)
                max_amt = base_salary.get("max_amount", 0)
                currency = base_salary.get("currency", "USD")
                period = base_salary.get("payment_period", "YEAR")
                salary = f"${min_amt:,} - ${max_amt:,} {currency}/{period}"
            
            # Create JobModel
            job = JobModel(
                job_id=str(job_id),
                Job_Role=job_title,
                Company=company_name,
                Experience=raw_job.get("job_seniority_level", ""),
                Skills=skills_str,
                jd=job_description,
                company_detail=raw_job.get("job_industries", ""),
                platform="linkedin",
                url=job_url,
                location=job_location,
                salary=salary,
                posted_date=datetime.now(),
                skills_list=skills_list,
                normalized_skills=[s.lower() for s in skills_list]
            )
            
            job_models.append(job)
            
        except Exception as e:
            print(f"⚠️  Failed to process job #{idx}: {e}")
            continue
    
    print(f"\n✅ Successfully created {len(job_models)} JobModel objects with skills")
    return job_models
