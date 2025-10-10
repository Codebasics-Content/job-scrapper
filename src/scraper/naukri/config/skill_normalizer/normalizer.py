#!/usr/bin/env python3
"""Skill Normalization Functions - EMD Compliant
Core functions for normalizing and enhancing skills from job data
"""
import json
import logging

from .enhanced_extractor import extract_skills_from_combined_text

logger = logging.getLogger(__name__)

def normalize_skills_from_string(skills_str: str) -> str:
    """Normalize skills from comma-separated string"""
    if not skills_str:
        return ""
    
    # Split by comma and clean
    skills: list[str] = [skill.strip().lower() for skill in skills_str.split(',') if skill.strip()]
    
    # Remove duplicates while preserving order
    unique_skills: list[str] = list(dict.fromkeys(skills))
    
    return ', '.join(unique_skills)

def normalize_jobs_skills_enhanced(jobs: list[dict[str, object]]) -> list[dict[str, object]]:
    """Add enhanced normalized_skills field using job description and company details"""
    normalized_jobs: list[dict[str, object]] = []
    
    for job in jobs:
        normalized_job: dict[str, object] = job.copy()
        
        # Extract existing fields with proper type handling
        existing_skills: str = str(job.get('skills', ''))
        job_description: str = str(job.get('jd', '') or job.get('description', ''))
        company_detail: str = str(job.get('company_detail', ''))
        
        # Use enhanced extraction
        enhanced_skills: list[str] = extract_skills_from_combined_text(
            jd=job_description,
            company_detail=company_detail,
            existing_skills=existing_skills
        )
        
        # Convert to comma-separated string and normalize
        skills_string: str = ', '.join(enhanced_skills)
        normalized_job['normalized_skills'] = normalize_skills_from_string(skills_string)
        
        normalized_jobs.append(normalized_job)
    
    return normalized_jobs

def normalize_jobs_skills(jobs: list[dict[str, object]]) -> list[dict[str, object]]:
    """Add normalized_skills field to jobs (legacy method)"""
    normalized_jobs: list[dict[str, object]] = []
    
    for job in jobs:
        normalized_job: dict[str, object] = job.copy()
        skills: str = str(job.get('skills', ''))
        normalized_job['normalized_skills'] = normalize_skills_from_string(skills)
        normalized_jobs.append(normalized_job)
    
    return normalized_jobs

def load_skill_normalizer_config() -> dict[str, object]:
    """Load skill normalizer configuration"""
    try:
        with open('skill_db_relax_20.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Skill normalizer config not found")
        return {}
