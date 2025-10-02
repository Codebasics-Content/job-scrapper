#!/usr/bin/env python3
"""Skill Leaderboard Data Generator - EMD Compliant
Calculates and sorts skill percentages for visualization
"""
import logging
from collections import Counter
from collections.abc import Sequence
from src.models import JobModel

logger = logging.getLogger(__name__)

def generate_skill_leaderboard(
    jobs: Sequence[JobModel | dict[str, object]], 
    top_n: int = 20
) -> list[dict[str, str | float | int]]:
    """Generate sorted skill leaderboard with percentages
    
    Args:
        jobs: List of job models with normalized_skills
        top_n: Number of top skills to return
        
    Returns:
        List of dicts with 'skill' and 'percentage' keys, sorted by percentage
    """
    if not jobs:
        logger.warning("No jobs provided for leaderboard generation")
        return []
    
    # Count skill occurrences across all jobs
    skill_counter: Counter[str] = Counter()
    total_jobs = len(jobs)
    
    for job in jobs:
        # Handle both JobModel objects and dict formats
        skills: list[str] | None = None
        if isinstance(job, dict):
            raw_skills = job.get('normalized_skills') or job.get('skills_list')
            if isinstance(raw_skills, list):
                # Convert to strings and filter valid entries
                skills = [str(item) for item in raw_skills if item]
        elif hasattr(job, 'normalized_skills'):
            raw_attr = getattr(job, 'normalized_skills')
            if isinstance(raw_attr, list):
                skills = [str(item) for item in raw_attr if item]
        
        if skills:
            unique_skills = set(skills)
            skill_counter.update(unique_skills)
    
    if not skill_counter:
        logger.warning("No skills found in jobs")
        return []
    
    # Calculate percentages and create leaderboard
    leaderboard = []
    for skill, count in skill_counter.most_common(top_n):
        percentage = round((count / total_jobs) * 100, 2)
        leaderboard.append({
            'skill': skill,
            'percentage': percentage,
            'count': count
        })
    
    logger.info(f"Generated leaderboard with {len(leaderboard)} skills from {total_jobs} jobs")
    return leaderboard

def format_leaderboard_text(leaderboard: list[dict[str, str | float]]) -> str:
    """Format leaderboard as readable text
    
    Returns:
        Formatted string like "Python 89%, Machine Learning 75%, ..."
    """
    if not leaderboard:
        return "No skills available"
    
    skill_strings = [
        f"{item['skill']} {item['percentage']}%" 
        for item in leaderboard[:10]  # Top 10 for text format
    ]
    
    return ", ".join(skill_strings)
