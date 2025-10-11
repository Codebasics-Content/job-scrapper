"""Indeed scraper using BrightData Datasets API (pre-collected data)."""
from typing import List, Optional, Dict, Any
import asyncio
import time
import requests
from datetime import datetime

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from .config.settings import get_settings


async def scrape_indeed_jobs_browser(
    query: str,
    location: Optional[str] = None,
    limit: int = 50
) -> List[JobModel]:
    """Scrape Indeed jobs using BrightData Datasets API (pre-collected data).
    
    Args:
        query: Job search query (e.g., "Data Scientist")
        location: Location filter (e.g., "Seattle, WA")
        limit: Maximum number of jobs to scrape
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"🚀 Starting Indeed Datasets API scraping...")
    print(f"   Query: {query}")
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
        "dataset_id": settings.indeed_dataset_id,
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
    }
    data = {
        "input": [{
            "domain": "indeed.com",
            "keyword_search": query,
            "country": "US",
            "location": location or "",
            "date_posted": "",
            "posted_by": "",
            "location_radius": ""
        }],
        "custom_output_fields": [
            "jobid", "company_name", "job_title", "description_text", "description",
            "qualifications", "job_type", "location", "salary_formatted",
            "url", "date_posted"
        ],
    }
    
    # Call BrightData API in thread pool
    print(f"📡 Calling BrightData Datasets API...")
    
    def _call_brightdata_api() -> List[Dict[str, Any]]:
        # Trigger collection
        response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
        response.raise_for_status()
        trigger_result = response.json()
        snapshot_id = trigger_result.get("snapshot_id")
        
        if not snapshot_id:
            raise RuntimeError(f"No snapshot_id in response: {trigger_result}")
        
        print(f"   Snapshot ID: {snapshot_id}")
        print(f"   Polling for results...")
        
        # Poll for results
        snapshot_url = f"{settings.base_url}{settings.snapshot_endpoint}/{snapshot_id}"
        print(f"   ⏳ BrightData is collecting data in real-time (this may take 2-5 minutes)...")
        
        max_wait = 300  # 5 minutes max
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
            job_location = raw_job.get("location", "Unknown")
            job_url = raw_job.get("url", "")
            job_id = raw_job.get("jobid") or job_url
            
            # Get full job description (try both fields)
            job_description = raw_job.get("description_text") or raw_job.get("description", "")
            
            # Extract skills from description using regex patterns
            skills_list = parser.extract_from_text(job_description)
            
            # Also extract from qualifications array if available
            qualifications = raw_job.get("qualifications", [])
            if qualifications:
                quals_text = " ".join(qualifications)
                quals_skills = parser.extract_from_text(quals_text)
                skills_list = list(set(skills_list + quals_skills))
            
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            # Log first 2 jobs for debugging
            if idx <= 2:
                print(f"\n📝 Indeed Job #{idx}:")
                print(f"   Title: {job_title}")
                print(f"   Company: {company_name}")
                print(f"   Description Length: {len(job_description)} chars")
                print(f"   Description Preview: {job_description[:200]}...")
                print(f"   Extracted Skills ({len(skills_list)}): {skills_list[:10]}")
            
            # Create JobModel
            job = JobModel(
                job_id=str(job_id),
                Job_Role=job_title,
                Company=company_name,
                Experience=raw_job.get("job_type", ""),
                Skills=skills_str,
                jd=job_description,
                company_detail="",
                platform="indeed",
                url=job_url,
                location=job_location,
                salary=raw_job.get("salary_formatted"),
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
