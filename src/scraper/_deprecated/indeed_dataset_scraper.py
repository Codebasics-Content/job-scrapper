"""Indeed scraper using BrightData Datasets API (FASTEST METHOD).

This uses BrightData's pre-collected Indeed job data via their Datasets API.
Much faster than browser scraping:
- Browser: 60-90s for 20 jobs
- Datasets API: 1-2s total for 50 jobs

No rate limits when using your API token correctly.
"""

from typing import List
from datetime import datetime

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from src.scraper.brightdata.clients.indeed import IndeedClient


def scrape_indeed_jobs_dataset(
    query: str,
    location: str = "United States",
    limit: int = 50
) -> List[JobModel]:
    """Scrape Indeed jobs using BrightData Datasets API (FASTEST).
    
    Args:
        query: Job search query (e.g., "Data Scientist")
        location: Location filter (e.g., "Seattle, WA")
        limit: Maximum number of jobs to scrape (up to 50K!)
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"\n🚀 Indeed Datasets API Scraper (FASTEST)")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize clients
    client = IndeedClient()
    skills_parser = SkillsParser()
    
    # Discover jobs via BrightData Datasets API
    print(f"\n📡 Fetching from BrightData Datasets API...")
    raw_jobs = client.discover_jobs(
        query=query,
        location=location,
        days_back=7,
        limit=limit
    )
    
    print(f"📥 Received {len(raw_jobs)} jobs from BrightData")
    
    # Convert to JobModel with skills extraction
    job_models = []
    for idx, raw_job in enumerate(raw_jobs, 1):
        try:
            # Extract fields from BrightData response
            job_title = raw_job.get("job_title", "Unknown")
            company_name = raw_job.get("company_name", "Unknown")
            job_location = raw_job.get("location", "Unknown")
            job_url = raw_job.get("url", "")
            job_id = raw_job.get("jobid") or raw_job.get("id") or job_url
            
            # Get full job description (try both fields)
            job_description = raw_job.get("description_text") or raw_job.get("description", "")
            
            # Extract skills from description
            skills_list = skills_parser.extract_from_text(job_description)
            
            # Also extract from qualifications array if available
            qualifications = raw_job.get("qualifications", [])
            if qualifications:
                quals_text = " ".join(qualifications)
                quals_skills = skills_parser.extract_from_text(quals_text)
                skills_list = list(set(skills_list + quals_skills))
            
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            # Log first 2 jobs for debugging
            if idx <= 2:
                print(f"\n📝 Job #{idx}:")
                print(f"   Title: {job_title}")
                print(f"   Company: {company_name}")
                print(f"   Description Length: {len(job_description)} chars")
                print(f"   Extracted Skills ({len(skills_list)}): {skills_list[:10]}")
            
            # Create JobModel
            job = JobModel(
                job_id=f"indeed_{job_id}",
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
            print(f"      ❌ Failed to process job #{idx}: {e}")
            continue
    
    print(f"\n✅ Successfully scraped {len(job_models)} Indeed jobs with skills")
    return job_models


# Test function
if __name__ == "__main__":
    print("Testing Indeed Datasets API scraper...")
    jobs = scrape_indeed_jobs_dataset(
        query="Python Developer",
        location="Seattle, WA",
        limit=5
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        print(f"\n   - {job.Job_Role} at {job.Company}")
        print(f"     Skills ({len(job.skills_list)}): {', '.join(job.skills_list[:10])}")
        print(f"     URL: {job.url}")
