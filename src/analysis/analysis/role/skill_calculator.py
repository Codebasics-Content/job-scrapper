# Skill Percentage Calculator Component - EMD Compliance: ≤80 lines
# Calculates skill demand percentages from job data

import logging
from collections import Counter
from src.models import JobModel

logger = logging.getLogger(__name__)


class SkillPercentageCalculator:
    """
    Calculates skill demand percentages from job listings.
    Provides statistical analysis of skill requirements.
    """
    
    def __init__(self):
        """Initialize the skill percentage calculator."""
        self.calculation_cache: dict[str, dict[str, float]] = {}
        
    def calculate_skill_percentages(self, jobs: list[JobModel]) -> dict[str, float]:
        """
        Calculate percentage demand for each skill across job listings.
        
        Args:
            jobs: list of job models to analyze
            
        Returns:
            dictionary mapping skills to their percentage demand
        """
        if not jobs:
            logger.warning("No jobs provided for skill calculation")
            return {}
            
        # Check cache first
        cache_key = f"skills_{len(jobs)}"
        if cache_key in self.calculation_cache:
            logger.debug("Using cached skill percentages")
            return self.calculation_cache[cache_key]
            
        all_skills = self._extract_all_skills(jobs)
        if not all_skills:
            logger.warning("No skills found in job listings")
            return {}
            
        skill_counts = Counter(all_skills)
        total_jobs = len(jobs)
        
        skill_percentages = {}
        for skill, count in skill_counts.items():
            if skill and skill.strip():  # Ensure valid skill
                percentage = (count / total_jobs) * 100
                skill_percentages[skill] = round(percentage, 1)
        
        # Cache results
        self.calculation_cache[cache_key] = skill_percentages
        
        logger.debug(f"Calculated percentages for {len(skill_percentages)} skills")
        return skill_percentages
        
    def _extract_all_skills(self, jobs: list[JobModel]) -> list[str]:
        """
        Extract all skills from job listings.
        
        Args:
            jobs: list of job models
            
        Returns:
            list of all skills found
        """
        all_skills = []
        
        for job in jobs:
            job_skills = self._get_job_skills(job)
            all_skills.extend(job_skills)
            
        return all_skills
        
    def _get_job_skills(self, job: JobModel) -> list[str]:
        """
        Get skills from a single job model.
        
        Args:
            job: Job model to extract skills from
            
        Returns:
            list of skills for the job
        """
        if hasattr(job, 'normalized_skills') and job.normalized_skills:
            return job.normalized_skills
        elif hasattr(job, 'skills_list') and job.skills_list:
            return [skill.lower() for skill in job.skills_list]
        elif hasattr(job, 'skills') and job.skills:
            return [skill.strip().lower() for skill in job.skills.split(',') 
                   if skill.strip()]
        
        return []
        
    def clear_cache(self) -> None:
        """Clear the calculation cache."""
        self.calculation_cache.clear()
        logger.debug("Skill calculation cache cleared")
