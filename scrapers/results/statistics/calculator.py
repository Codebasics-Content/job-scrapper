# Statistics Calculator - Computes skill percentages and metrics
# EMD Compliance: ≤80 lines for statistical analysis

import logging
from models.job import JobModel
from utils.statistics import calculate_skill_percentage

logger = logging.getLogger(__name__)

class StatisticsCalculator:
    """
    Calculates statistical metrics from job data
    Generates skill percentages and analysis summaries
    """
    
    def generate_statistics_report(
        self, 
        jobs: list[JobModel],
        all_skills: set,
        platform_counts: dict[str, int]
    ) -> dict:
        """Generate comprehensive statistics report"""
        if not jobs:
            logger.warning("No jobs available for statistics generation")
            return {"error": "No jobs to analyze", "total_jobs": 0}
            
        logger.info(
            f"Analyzing {len(all_skills)} unique skills from {len(jobs)} jobs"
        )
        
        # Calculate skill percentages (top 25 for performance)
        skill_stats = self._calculate_skill_percentages(jobs, all_skills)
        
        # Sort skills by percentage descending
        sorted_skills = dict(
            sorted(skill_stats.items(), key=lambda x: x[1], reverse=True)
        )
        
        return {
            "total_jobs": len(jobs),
            "platforms_scraped": len(platform_counts),
            "platform_distribution": platform_counts,
            "skill_percentages": sorted_skills,
            "top_companies": [job.company for job in jobs[:15]],
            "analysis_summary": self._generate_summary(jobs, skill_stats)
        }
        
    def _calculate_skill_percentages(
        self, 
        jobs: list[JobModel], 
        all_skills: set
    ) -> dict[str, float]:
        """Calculate percentage for top skills"""
        skill_stats = {}
        top_skills = list(all_skills)[:25]
        
        for skill in top_skills:
            try:
                percentage = calculate_skill_percentage(skill, jobs)
                skill_stats[skill] = round(percentage, 2)
            except Exception as error:
                logger.error(
                    f"Error calculating percentage for skill '{skill}': {error}"
                )
        return skill_stats
        
    def _generate_summary(
        self, 
        jobs: list[JobModel], 
        skill_stats: dict
    ) -> dict:
        """Generate analysis summary metrics"""
        total_skills_per_job = sum(
            len(job.normalized_skills) for job in jobs
        )
        avg_skills = total_skills_per_job / len(jobs) if jobs else 0
        
        return {
            "total_skills_analyzed": len(skill_stats),
            "highest_skill_percentage": max(skill_stats.values()) if skill_stats else 0,
            "average_skills_per_job": avg_skills
        }
