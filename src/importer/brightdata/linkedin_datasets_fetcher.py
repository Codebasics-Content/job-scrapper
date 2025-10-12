# BrightData LinkedIn Web Datasets Fetcher - EMD Component
# Uses pre-collected dataset API instead of real-time scraping

import logging
from .datasets_client import BrightDataDatasetsClient

logger = logging.getLogger(__name__)

async def fetch_linkedin_jobs_from_datasets(
    keyword: str,
    limit: int = 50,
    location: str = "Worldwide",
    api_token: str | None = None
) -> list[dict[str, object]]:
    """Fetch LinkedIn jobs from BrightData Web Datasets
    
    This uses pre-collected data via REST API, much faster
    than real-time scraping.
    
    Args:
        keyword: Job search keyword
        limit: Maximum jobs to fetch
        location: Job location filter
        api_token: Optional API token override
    
    Returns:
        List of job data dicts compatible with parser
    """
    logger.info(f"Fetching from LinkedIn Web Datasets: {keyword}")
    
    client = BrightDataDatasetsClient(api_token)
    jobs = await client.fetch_linkedin_jobs(keyword, location, limit)
    
    # Normalize to parser-compatible format
    normalized_jobs = _normalize_dataset_response(jobs)
    
    logger.info(f"Normalized {len(normalized_jobs)} jobs from dataset")
    return normalized_jobs


def _normalize_dataset_response(
    raw_jobs: list[dict[str, object]]
) -> list[dict[str, object]]:
    """Normalize Web Datasets response to parser format"""
    normalized: list[dict[str, object]] = []
    
    for job in raw_jobs:
        # Map dataset fields to parser-expected fields
        normalized_job = {
            "title": job.get("title", job.get("job_title", "")),
            "company": job.get("company", job.get("company_name", "")),
            "url": job.get("url", job.get("job_url", job.get("link", ""))),
            "description": job.get("description", job.get("job_description", "")),
            "location": job.get("location", ""),
            "posted_date": job.get("posted_date", job.get("posted_at", "")),
            "company_detail": job.get("company_detail", ""),
        }
        
        normalized.append(normalized_job)
    
    return normalized
