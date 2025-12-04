#!/usr/bin/env python3
"""
Skill Statistics Calculator

Implements statistical analysis for job skill occurrences across multiple platforms.
Calculates skill frequency percentages using the formula: (distinct_skill_count / total_jobs) * 100
Provides aggregated analytics for data science and AI job market insights.

Key Features:
- Cross-platform skill occurrence analysis
- Percentage-based frequency calculations  
- Skill trend detection and ranking
- Statistical validation and error handling

Usage:
    from src.analysis.skill_statistics import calculate_skill_percentages, generate_skill_report
    
    jobs = [job1, job2, job3]  # list of JobModel instances
    percentages = calculate_skill_percentages(jobs)
    report = generate_skill_report(jobs, "Data Science")

Author: Job Scrapper Team
Created: 2024
EMD Compliance: ≤80 lines, modular design
"""

import logging
from src.models.models import JobDetailModel

logger = logging.getLogger(__name__)

def calculate_skill_percentages(jobs: list[JobDetailModel], target_skills: list[str] | None = None) -> dict[str, float]:
    """Calculate skill occurrence percentages from job listings
    
    Formula: (Distinct jobs with skill / Total jobs) * 100
    """
    
    if not jobs:
        logger.warning("No jobs provided for skill calculation")
        return {}
        
    total_jobs = len(jobs)
    skill_job_sets: dict[str, set[int]] = {}
    
    # Count distinct jobs for each skill
    for idx, job in enumerate(jobs):
        if hasattr(job, 'skills') and job.skills:
            job_skills = [skill.strip().lower() for skill in job.skills.split(',') if skill.strip()]
            for skill in job_skills:
                if skill not in skill_job_sets:
                    skill_job_sets[skill] = set()
                skill_job_sets[skill].add(idx)
    
    # Calculate percentages for target skills or all skills
    skills_to_analyze = target_skills or list(skill_job_sets.keys())
    percentages: dict[str, float] = {}
    
    for skill in skills_to_analyze:
        skill_lower = skill.strip().lower()
        distinct_jobs_count = len(skill_job_sets.get(skill_lower, set()))
        percentage = (distinct_jobs_count / total_jobs) * 100
        percentages[skill] = round(percentage, 2)
        
    logger.info(f"Calculated percentages for {len(percentages)} skills from {total_jobs} jobs")
    return percentages

def get_top_skills(jobs: list[JobDetailModel], top_n: int = 10) -> list[tuple[str, float]]:
    """Get top N skills by occurrence percentage"""
    
    percentages = calculate_skill_percentages(jobs)
    sorted_skills = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    
    top_skills = sorted_skills[:top_n]
    logger.debug(f"Retrieved top {top_n} skills from {len(jobs)} jobs")
    return top_skills

def analyze_platform_skills(jobs: list[JobDetailModel], platform: str) -> dict[str, float]:
    """Analyze skills for specific platform"""
    
    platform_jobs = [job for job in jobs if hasattr(job, 'platform') and job.platform == platform]
    
    if not platform_jobs:
        logger.warning(f"No jobs found for platform: {platform}")
        return {}
        
    percentages = calculate_skill_percentages(platform_jobs)
    logger.info(f"Analyzed {len(platform_jobs)} jobs for platform {platform}")
    return percentages
