#!/usr/bin/env python3
"""
Core Skill Percentage Calculator - EMD Compliant Module

Implements the fundamental skill percentage calculation formula:
percentage = (jobs_with_skill / total_jobs) * 100

Optimized DDO consolidation of duplicated statistics functionality.
EMD Compliance: ≤80 lines, single responsibility principle.

Author: Job Scrapper Team
Created: 2024
"""

import logging
from typing import List, Dict, Optional, Union
from src.models import JobModel

logger = logging.getLogger(__name__)

def calculate_skill_percentage(skill: str, jobs: List[JobModel]) -> float:
    """Calculate percentage of jobs containing a specific skill"""
    
    if not jobs:
        logger.warning("No jobs provided for skill percentage calculation")
        return 0.0
    
    skill_lower = skill.lower().strip()
    jobs_with_skill = 0
    total_jobs = len(jobs)
    
    for job in jobs:
        # Support both normalized_skills and comma-separated skills attributes
        job_skills = []
        if hasattr(job, 'normalized_skills') and job.normalized_skills:
            job_skills = [s.lower().strip() for s in job.normalized_skills]
        elif hasattr(job, 'skills') and job.skills:
            job_skills = [s.lower().strip() for s in job.skills.split(',')]
        
        if skill_lower in job_skills:
            jobs_with_skill += 1
    
    percentage = (jobs_with_skill / total_jobs) * 100
    logger.debug(f"Skill '{skill}': {jobs_with_skill}/{total_jobs} = {percentage:.2f}%")
    
    return round(percentage, 2)

def calculate_multiple_skills(
    skills: List[str], 
    jobs: List[JobModel]
) -> Dict[str, float]:
    """Calculate percentages for multiple skills efficiently"""
    
    if not skills or not jobs:
        logger.warning("No skills or jobs provided for calculation")
        return {}
    
    results = {}
    for skill in skills:
        results[skill] = calculate_skill_percentage(skill, jobs)
    
    logger.info(f"Calculated percentages for {len(results)} skills from {len(jobs)} jobs")
    return results

def calculate_platform_skills(
    jobs: List[JobModel], 
    platform: str,
    skills: Optional[List[str]] = None
) -> Dict[str, float]:
    """Calculate skill percentages for specific platform"""
    
    platform_jobs = [
        job for job in jobs 
        if hasattr(job, 'platform') and job.platform == platform
    ]
    
    if not platform_jobs:
        logger.warning(f"No jobs found for platform: {platform}")
        return {}
    
    if skills:
        return calculate_multiple_skills(skills, platform_jobs)
    
    # If no specific skills provided, extract all skills from platform jobs
    from .skill_extractor import extract_all_skills
    all_skills = extract_all_skills(platform_jobs)
    
    return calculate_multiple_skills(list(all_skills), platform_jobs)
