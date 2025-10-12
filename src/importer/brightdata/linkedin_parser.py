# BrightData LinkedIn Response Parser - EMD Component
# Parses BrightData JSON format to JobDetailModel

import logging
from datetime import datetime
from src.models import JobDetailModel, JobUrlModel

logger = logging.getLogger(__name__)

def parse_brightdata_response(data: dict[str, object]) -> JobDetailModel | None:
    """Parse single BrightData LinkedIn job entry to JobDetailModel
    
    Expected BrightData fields:
    - url: Job posting URL
    - title: Job title
    - company: Company name
    - description: Full job description
    - posted_date: Posting date (optional)
    - location: Job location (optional)
    """
    try:
        url_raw = data.get("url", "")
        title_raw = data.get("title", "")
        
        # Type narrow to str
        url = str(url_raw) if url_raw else ""
        title = str(title_raw) if title_raw else ""
        
        if not url or not title:
            logger.warning("Missing required fields: url or title")
            return None
        
        # Generate job_id using existing utility
        job_id = JobUrlModel.generate_job_id("linkedin", url)
        
        # Parse posted date if available
        posted_date = None
        if raw_date := data.get("posted_date"):
            try:
                posted_date = datetime.fromisoformat(str(raw_date))
            except (ValueError, TypeError):
                logger.debug(f"Could not parse date: {raw_date}")
        
        return JobDetailModel(
            job_id=job_id,
            platform="linkedin",
            actual_role=title,
            url=url,
            job_description=str(data.get("description", "")),
            skills="",  # Will be populated by skills extraction
            company_name=str(data.get("company", "")),
            company_detail=str(data.get("company_detail", "")),
            posted_date=posted_date,
            scraped_at=datetime.now()
        )
    
    except Exception as error:
        logger.error(f"Failed to parse BrightData entry: {error}")
        return None


def parse_brightdata_batch(response: list[dict[str, object]]) -> list[JobDetailModel]:
    """Parse batch of BrightData LinkedIn jobs"""
    jobs = []
    for entry in response:
        if job := parse_brightdata_response(entry):
            jobs.append(job)
    
    logger.info(f"Parsed {len(jobs)}/{len(response)} jobs from BrightData")
    return jobs
