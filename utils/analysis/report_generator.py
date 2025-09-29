#!/usr/bin/env python3
"""
Skill Analysis Report Generator - EMD Compliant Module

Generates formatted skill analysis reports with percentage statistics.
Supports platform-specific and general skill reporting.

DDO consolidation of report generation functionality.
EMD Compliance: ≤80 lines, focused responsibility.

Author: Job Scrapper Team
Created: 2024
"""

import logging
from models.job import JobModel
from .skill_calculator import calculate_multiple_skills, calculate_platform_skills
from .skill_extractor import extract_all_skills

logger = logging.getLogger(__name__)

def generate_skill_report(
    jobs: list[JobModel], 
    target_skills: list[str] | None = None,
    top_n: int = 20
) -> dict[str, float]:
    """Generate comprehensive skill percentage report"""
    
    if not jobs:
        logger.warning("No jobs provided for skill report generation")
        return {}
    
    # Use target skills or extract top skills from jobs
    if target_skills:
        skills_to_analyze = target_skills
    else:
        all_skills = extract_all_skills(jobs)
        # Get top N most frequent skills
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = sum(
                1 for job in jobs 
                if skill.lower() in [s.lower() for s in (
                    job.normalized_skills if hasattr(job, 'normalized_skills') and job.normalized_skills
                    else job.skills.split(',') if hasattr(job, 'skills') and job.skills
                    else []
                )]
            )
        
        skills_to_analyze = sorted(skill_counts.keys(), key=skill_counts.get, reverse=True)[:top_n]
    
    # Calculate percentages for selected skills
    skill_percentages = calculate_multiple_skills(skills_to_analyze, jobs)
    
    # Sort by percentage (descending)
    sorted_results = dict(sorted(skill_percentages.items(), key=lambda x: x[1], reverse=True))
    
    logger.info(f"Generated skill report for {len(sorted_results)} skills from {len(jobs)} jobs")
    return sorted_results

def generate_platform_report(
    jobs: list[JobModel], 
    platform: str,
    target_skills: list[str] | None = None,
    top_n: int = 15
) -> dict[str, float]:
    """Generate platform-specific skill analysis report"""
    
    platform_percentages = calculate_platform_skills(jobs, platform, target_skills)
    
    if not platform_percentages:
        logger.warning(f"No data available for platform: {platform}")
        return {}
    
    # Limit to top N results
    sorted_results = dict(
        sorted(platform_percentages.items(), key=lambda x: x[1], reverse=True)[:top_n]
    )
    
    logger.info(f"Generated {platform} platform report with {len(sorted_results)} skills")
    return sorted_results
