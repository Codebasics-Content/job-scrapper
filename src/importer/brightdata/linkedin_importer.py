# BrightData LinkedIn Importer - EMD Component
# Batch import with duplicate checking and skills extraction

import logging
from src.analysis.skill_extraction import extract_skills_from_text, load_skill_patterns
from src.db.operations import JobStorageOperations
from .linkedin_parser import parse_brightdata_batch

logger = logging.getLogger(__name__)

def import_linkedin_jobs(
    brightdata_response: list[dict[str, object]],
    db_path: str = "jobs.db"
) -> tuple[int, int]:
    """Import LinkedIn jobs from BrightData with skills extraction
    
    Process:
    1. Parse BrightData JSON response
    2. Extract skills from job descriptions
    3. Check for duplicates using existing job_id
    4. Store only new jobs to jobs table
    
    Returns:
        (stored_count, duplicate_count)
    """
    logger.info(f"Starting BrightData LinkedIn import: {len(brightdata_response)} jobs")
    
    # Parse BrightData response
    jobs = parse_brightdata_batch(brightdata_response)
    if not jobs:
        logger.warning("No valid jobs parsed from BrightData response")
        return 0, 0
    
    # Load skill patterns once for batch processing
    skill_patterns = load_skill_patterns()
    
    # Extract skills for each job
    for job in jobs:
        if job.job_description:
            skills = extract_skills_from_text(job.job_description, skill_patterns)
            job.skills = ','.join(skills) if skills else ''
    
    # Store to database with duplicate checking
    db_ops = JobStorageOperations(db_path)
    stored = db_ops.store_details(jobs)
    duplicates = len(jobs) - stored
    
    logger.info(
        f"✅ Import complete: {stored} stored, {duplicates} duplicates skipped"
    )
    
    return stored, duplicates


def import_from_json_file(json_path: str, db_path: str = "jobs.db") -> tuple[int, int]:
    """Import LinkedIn jobs from BrightData JSON file"""
    import json
    
    with open(json_path, 'r', encoding='utf-8') as file:
        raw_data: object = json.load(file)
    
    # Extract jobs list from response
    jobs_data: list[dict[str, object]]
    if isinstance(raw_data, dict) and 'results' in raw_data:
        jobs_data = raw_data['results']  # type: ignore[assignment]
    elif isinstance(raw_data, list):
        jobs_data = raw_data  # type: ignore[assignment]
    else:
        raise ValueError("Invalid JSON format. Expected array or object with 'results' key")
    
    return import_linkedin_jobs(jobs_data, db_path)
