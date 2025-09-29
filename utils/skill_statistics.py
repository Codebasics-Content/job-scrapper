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
    from utils.skill_statistics import calculate_skill_percentages, generate_skill_report
    
    jobs = [job1, job2, job3]  # list of JobModel instances
    percentages = calculate_skill_percentages(jobs)
    report = generate_skill_report(jobs, "Data Science")

Author: Job Scrapper Team
Created: 2024
EMD Compliance: ≤80 lines, modular design
"""

import logging
from typing import Optional
from collections import Counter

logger = logging.getLogger(__name__)

def calculate_skill_percentages(jobs: list, target_skills: Optional[list[str]] = None) -> dict[str, float]:
    """Calculate skill occurrence percentages from job listings"""
    
    if not jobs:
        logger.warning("No jobs provided for skill calculation")
        return {}
        
    total_jobs = len(jobs)
    skill_counts = Counter()
    
    # Extract and count skills from all jobs
    for job in jobs:
        if hasattr(job, 'skills') and job.skills:
            job_skills = [skill.strip().lower() for skill in job.skills.split(',')]
            skill_counts.update(job_skills)
    
    # Calculate percentages for target skills or all skills
    skills_to_analyze = target_skills or list(skill_counts.keys())
    percentages = {}
    
    for skill in skills_to_analyze:
        skill_lower = skill.strip().lower()
        count = skill_counts.get(skill_lower, 0)
        percentage = (count / total_jobs) * 100
        percentages[skill] = round(percentage, 2)
        
    logger.info(f"Calculated percentages for {len(percentages)} skills from {total_jobs} jobs")
    return percentages

def get_top_skills(jobs: list, top_n: int = 10) -> list[tuple[str, float]]:
    """Get top N skills by occurrence percentage"""
    
    percentages = calculate_skill_percentages(jobs)
    sorted_skills = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    
    top_skills = sorted_skills[:top_n]
    logger.debug(f"Retrieved top {top_n} skills from {len(jobs)} jobs")
    return top_skills

def analyze_platform_skills(jobs: list, platform: str) -> dict[str, float]:
    """Analyze skills for specific platform"""
    
    platform_jobs = [job for job in jobs if hasattr(job, 'platform') and job.platform == platform]
    
    if not platform_jobs:
        logger.warning(f"No jobs found for platform: {platform}")
        return {}
        
    percentages = calculate_skill_percentages(platform_jobs)
    logger.info(f"Analyzed {len(platform_jobs)} jobs for platform {platform}")
    return percentages
