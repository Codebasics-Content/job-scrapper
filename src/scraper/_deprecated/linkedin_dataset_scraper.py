"""LinkedIn scraper using BrightData Datasets API (FASTEST METHOD).

This uses BrightData's pre-collected LinkedIn job data via their Datasets API.
Much faster than browser scraping:
- Browser: 60-90s for 20 jobs
- Datasets API: 1-2s total for 50 jobs

No rate limits when using your API token correctly.
"""

from typing import List
from datetime import datetime

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from src.scraper.brightdata.clients.linkedin import LinkedInClient


def scrape_linkedin_jobs_dataset(
    keyword: str,
    location: str = "United States",
    limit: int = 50
) -> List[JobModel]:
    """Scrape LinkedIn jobs using BrightData Datasets API (FASTEST).
    
    Args:
        keyword: Job search keyword (e.g., "Machine Learning Engineer")
        location: Location filter (e.g., "United States", "San Francisco, CA")
        limit: Maximum number of jobs to scrape (up to 50K!)
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"\n🚀 LinkedIn Datasets API Scraper (FASTEST)")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize clients
    client = LinkedInClient()
    skills_parser = SkillsParser()
    
    # Discover jobs via BrightData Datasets API
    print(f"\n📡 Fetching from BrightData Datasets API...")
    raw_jobs = client.discover_jobs(
        keyword=keyword,
        location=location,
        time_range="past_week",
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
            job_location = raw_job.get("job_location", "Unknown")
            job_url = raw_job.get("url", "")
            job_id = raw_job.get("job_posting_id") or raw_job.get("id") or job_url
            
            # Get full job description
            job_description = raw_job.get("job_summary", "") or raw_job.get("description", "")
            
            # Extract skills from description
            skills_list = skills_parser.extract_from_text(job_description)
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            # Log first 2 jobs for debugging
            if idx <= 2:
                print(f"\n📝 Job #{idx}:")
                print(f"   Title: {job_title}")
                print(f"   Company: {company_name}")
                print(f"   Description Length: {len(job_description)} chars")
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
                job_id=f"linkedin_{job_id}",
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
            print(f"      ❌ Failed to process job #{idx}: {e}")
            continue
    
    print(f"\n✅ Successfully scraped {len(job_models)} LinkedIn jobs with skills")
    return job_models


# Test function
if __name__ == "__main__":
    print("Testing LinkedIn Datasets API scraper...")
    jobs = scrape_linkedin_jobs_dataset(
        keyword="Python Developer",
        location="United States",
        limit=5
    )
    
    print(f"\n📊 Results: {len(jobs)} jobs")
    for job in jobs[:3]:
        print(f"\n   - {job.Job_Role} at {job.Company}")
        print(f"     Skills ({len(job.skills_list)}): {', '.join(job.skills_list[:10])}")
        print(f"     URL: {job.url}")
