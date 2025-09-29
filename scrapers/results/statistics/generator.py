# Job Scrapper - Statistics Generation Module
# EMD Compliance: ≤80 lines for statistics calculation

import logging
from models.job import JobModel
from utils.statistics import calculate_skill_percentage

logger = logging.getLogger(__name__)

class StatisticsGenerator:
    """
    Generates comprehensive skill percentage statistics from job data
    Handles skill analysis and platform metrics
    """
    
    def generate_report(self, jobs: list[JobModel]) -> dict[str, str | int | dict[str, int] | dict[str, float] | list[str] | dict[str, float]]:
        """Generate structured statistics report from jobs"""
        if not jobs:
            logger.warning("No jobs available for statistics generation")
            return {"error": "No jobs to analyze", "total_jobs": 0}
        
        all_skills = self._extract_all_skills(jobs)
        skill_stats = self._calculate_skill_stats(jobs, all_skills)
        platform_counts = self._count_platforms(jobs)
        sorted_skills = dict(sorted(skill_stats.items(), 
                                   key=lambda x: x[1], reverse=True))
        
        return {
            "total_jobs": len(jobs),
            "platforms_scraped": len(platform_counts),
            "platform_distribution": platform_counts,
            "skill_percentages": sorted_skills,
            "top_companies": [job.company for job in jobs[:15]],
            "analysis_summary": self._generate_summary(jobs, skill_stats)
        }
    
    def _extract_all_skills(self, jobs: list[JobModel]) -> set[str]:
        """Extract unique skills from all jobs"""
        all_skills = set()
        for job in jobs:
            all_skills.update(job.normalized_skills)
        logger.info(f"Analyzing {len(all_skills)} unique skills from {len(jobs)} jobs")
        return all_skills
    
    def _calculate_skill_stats(self, jobs: list[JobModel], 
                               all_skills: set[str]) -> dict[str, float]:
        """Calculate percentages for top skills"""
        skill_stats = {}
        top_skills = list(all_skills)[:25]  # Top 25 for performance
        
        for skill in top_skills:
            try:
                percentage = calculate_skill_percentage(skill, jobs)
                skill_stats[skill] = round(percentage, 2)
            except Exception as error:
                logger.error(f"Error calculating for skill '{skill}': {error}")
        
        return skill_stats
    
    def _count_platforms(self, jobs: list[JobModel]) -> dict[str, int]:
        """Generate platform distribution statistics"""
        platform_counts = {}
        for job in jobs:
            platform = job.platform
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        return platform_counts
    
    def _generate_summary(self, jobs: list[JobModel], 
                         skill_stats: dict[str, float]) -> dict[str, float]:
        """Generate analysis summary metrics"""
        return {
            "total_skills_analyzed": len(skill_stats),
            "highest_skill_percentage": max(skill_stats.values()) if skill_stats else 0,
            "average_skills_per_job": sum(len(job.normalized_skills) 
                                         for job in jobs) / len(jobs)
        }
