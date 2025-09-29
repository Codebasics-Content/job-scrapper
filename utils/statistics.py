# Statistics Calculation Utility - Consolidated Implementation
# DDO: Consolidated duplicate functions, imports from analysis modules
# EMD Compliance: ≤80 lines, delegation to specialized modules

from typing import List, Dict, Set, Tuple
import logging
from collections import Counter
from models.job import JobModel

# Import consolidated implementations from analysis modules
from utils.analysis.skill_calculator import (
    calculate_skill_percentage,
    calculate_multiple_skills,
    calculate_platform_skills
)
from utils.analysis.skill_extractor import extract_all_skills

logger = logging.getLogger(__name__)

def get_top_skills(jobs: List[JobModel], top_n: int = 20) -> List[Tuple[str, float]]:
    """Get top N skills by frequency with percentages"""
    if not jobs:
        return []
    
    all_skills = extract_all_skills(jobs)
    skill_percentages = []
    
    for skill in all_skills:
        percentage = calculate_skill_percentage(skill, jobs)
        skill_percentages.append((skill, percentage))
    
    # Sort by percentage descending
    top_skills = sorted(skill_percentages, key=lambda x: x[1], reverse=True)[:top_n]
    
    logger.info(f"Top {len(top_skills)} skills calculated from {len(all_skills)} total skills")
    return top_skills

def get_platform_statistics(jobs: List[JobModel]) -> Dict[str, int]:
    """Get job count statistics by platform"""
    platform_counts = Counter(job.platform for job in jobs)
    
    stats = dict(platform_counts)
    logger.info(f"Platform statistics: {stats}")
    
    return stats

def generate_skill_report(jobs: List[JobModel], min_percentage: float = 1.0) -> Dict[str, any]:
    """Generate comprehensive skill analysis report"""
    if not jobs:
        return {"error": "No jobs provided for analysis"}
    
    all_skills = extract_all_skills(jobs)
    skill_analysis = {}
    
    for skill in all_skills:
        percentage = calculate_skill_percentage(skill, jobs)
        if percentage >= min_percentage:
            skill_analysis[skill] = {
                "percentage": round(percentage, 2),
                "job_count": int((percentage / 100) * len(jobs))
            }
    
    # Sort by percentage
    sorted_skills = dict(sorted(skill_analysis.items(), 
                               key=lambda x: x[1]["percentage"], reverse=True))
    
    report = {
        "total_jobs": len(jobs),
        "total_skills": len(all_skills),
        "analyzed_skills": len(sorted_skills),
        "platform_distribution": get_platform_statistics(jobs),
        "skill_analysis": sorted_skills
    }
    
    logger.info(f"Generated skill report: {len(sorted_skills)} skills above {min_percentage}% threshold")
    return report
