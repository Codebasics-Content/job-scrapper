#!/usr/bin/env python3
"""
Skill Extraction and Normalization Module - EMD Compliant

Handles extraction and normalization of skills from JobModel instances.
Supports both normalized_skills and comma-separated skills attributes.

DDO consolidation of skill extraction functionality.
EMD Compliance: ≤80 lines, focused responsibility.

Author: Job Scrapper Team
Created: 2024
"""

import logging
from src.models import JobModel

logger = logging.getLogger(__name__)

def extract_all_skills(jobs: list[JobModel]) -> set[str]:
    """Extract unique skills from all job listings"""
    
    if not jobs:
        logger.warning("No jobs provided for skill extraction")
        return set()
    
    all_skills: set[str] = set()
    
    for job in jobs:
        job_skills = extract_job_skills(job)
        all_skills.update(job_skills)
    
    logger.info(f"Extracted {len(all_skills)} unique skills from {len(jobs)} jobs")
    return all_skills

def extract_job_skills(job: JobModel) -> list[str]:
    """Extract skills from a single job instance"""
    
    skills: list[str] = []
    
    # Support both normalized_skills and comma-separated skills attributes
    if hasattr(job, 'normalized_skills') and job.normalized_skills:
        skills = [skill.strip() for skill in job.normalized_skills if skill.strip()]
    elif hasattr(job, 'skills') and job.skills:
        skills = [skill.strip() for skill in job.skills.split(',') if skill.strip()]
    
    return skills

def normalize_skills_from_jobs(jobs: list[JobModel]) -> list[JobModel]:
    """Normalize skills format for consistency across job instances"""
    
    if not jobs:
        logger.warning("No jobs provided for skills normalization")
        return []
    
    normalized_jobs: list[JobModel] = []
    
    for job in jobs:
        job_skills = extract_job_skills(job)
        
        # Ensure consistent normalized_skills attribute
        if not hasattr(job, 'normalized_skills') or not job.normalized_skills:
            job.normalized_skills = job_skills
        
        normalized_jobs.append(job)
    
    logger.info(f"Normalized skills for {len(normalized_jobs)} jobs")
    return normalized_jobs

def get_skill_frequency_map(jobs: list[JobModel]) -> dict[str, int]:
    """Generate frequency map of skills across all jobs"""
    
    all_skills = extract_all_skills(jobs)
    frequency_map: dict[str, int] = {}
    
    for skill in all_skills:
        skill_count = sum(1 for job in jobs if skill.lower() in 
                         [s.lower() for s in extract_job_skills(job)])
        frequency_map[skill] = skill_count
    
    return frequency_map
