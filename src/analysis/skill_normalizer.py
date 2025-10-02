#!/usr/bin/env python3
"""Skill Normalization Module - EMD Compliant
Parses and normalizes comma-separated skills from database
"""
import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)

def normalize_skills_from_string(skills_str: str) -> list[str]:
    """Parse comma-separated skills string into normalized list
    
    Args:
        skills_str: Comma-separated skills string from database
        
    Returns:
        List of normalized, unique skills
    """
    if not skills_str:
        return []
    
    # Split by comma and clean each skill
    skills: list[str] = [
        skill.strip().lower() 
        for skill in skills_str.split(',') 
        if skill.strip()
    ]
    
    # Return unique skills only
    return list(set(skills))

def normalize_jobs_skills(
    jobs: Sequence[dict[str, object]]
) -> list[dict[str, object]]:
    """Add normalized_skills field to job dictionaries
    
    Args:
        jobs: List of job dictionaries with 'skills' field
        
    Returns:
        Jobs with added 'normalized_skills' field
    """
    normalized_jobs: list[dict[str, object]] = []
    
    for job in jobs:
        job_copy: dict[str, object] = dict(job)
        skills_value: object = job.get('skills', '')
        skills_str: str = str(skills_value) if skills_value else ''
        job_copy['normalized_skills'] = normalize_skills_from_string(skills_str)
        normalized_jobs.append(job_copy)
    
    logger.info(f"Normalized skills for {len(normalized_jobs)} jobs")
    return normalized_jobs
