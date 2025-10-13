#!/usr/bin/env python3
"""
Batch Skill Extraction for Multiple Jobs - Performance Optimized
Loads patterns once, processes all jobs in single pass

Author: Job Scrapper Team  
Created: 2025-10-11
EMD Compliance: ≤80 lines
"""

from typing import Any
from .extractor import AdvancedSkillExtractor

def extract_skills_batch(job_descriptions: list[str]) -> list[list[str]]:
    """
    Extract skills from multiple job descriptions efficiently
    
    Loads regex patterns ONCE, then processes all jobs
    ~100x faster than loading patterns per job
    
    Args:
        job_descriptions: List of job description texts
    
    Returns:
        List of skill lists (one per job)
    """
    
    if not job_descriptions:
        return []
    
    # Initialize extractor once for entire batch
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    
    # Process all jobs with same extractor instance
    results: list[list[str]] = [
        extractor.extract(jd)
        for jd in job_descriptions
    ]
    
    return results

def extract_skills_from_jobs(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Extract skills from list of job dicts (with 'jd' or 'description' field)
    
    Args:
        jobs: List of job dicts with description field
    
    Returns:
        Same job dicts with added 'skills' field
    """
    
    if not jobs:
        return []
    
    # Extract descriptions
    descriptions = [
        job.get('jd') or job.get('description') or job.get('job_description', '')
        for job in jobs
    ]
    
    # Batch extract skills
    skills_lists = extract_skills_batch(descriptions)
    
    # Add skills to job dicts
    for job, skills in zip(jobs, skills_lists):
        job['skills'] = ','.join(skills) if skills else ''
    
    return jobs
