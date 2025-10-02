#!/usr/bin/env python3
"""
Role-Based Job Analysis System - EMD Compliant Module

Analyzes job requirements for specific roles and calculates skill percentages.
Matches requirements like: RAG 89%, Langchain 62%, Crew AI 41%

EMD Compliance: ≤80 lines, single responsibility principle.
"""

import logging
from src.models import JobModel
from .role.job_filter import JobRoleFilter
from .role.skill_calculator import SkillPercentageCalculator

logger = logging.getLogger(__name__)


class RoleAnalyzer:
    """
    Analyzes job roles and calculates skill demand percentages.
    Uses EMD-compliant components for modular functionality.
    """
    
    def __init__(self) -> None:
        """Initialize the role analyzer with EMD components."""
        self.job_filter: JobRoleFilter = JobRoleFilter()
        self.skill_calculator: SkillPercentageCalculator = SkillPercentageCalculator()
        
    def analyze_role_skills(self, jobs: list[JobModel], role: str) -> dict[str, float]:
        """
        Analyze skills for a specific role and return percentage breakdown.
        
        Args:
            jobs: list of job models to analyze
            role: Target role to analyze
            
        Returns:
            dictionary mapping skills to their percentage demand for the role
        """
        if not jobs or not role:
            logger.warning("Empty jobs list or role provided")
            return {}
            
        # Filter jobs by role using EMD component
        role_jobs = self.job_filter.filter_jobs_by_role(jobs, role)
        if not role_jobs:
            logger.warning(f"No jobs found for role: {role}")
            return {}
            
        # Calculate skill percentages using EMD component
        skill_percentages = self.skill_calculator.calculate_skill_percentages(role_jobs)
        
        logger.info(f"Analyzed {len(role_jobs)} jobs for role: {role}")
        logger.info(f"Found {len(skill_percentages)} unique skills")
        return skill_percentages
        
    def get_top_skills(self, jobs: list[JobModel], role: str, limit: int = 10) -> dict[str, float]:
        """
        Get top N skills for a specific role by demand percentage.
        
        Args:
            jobs: list of job models to analyze
            role: Target role to analyze
            limit: Maximum number of skills to return
            
        Returns:
            dictionary of top skills with their percentages
        """
        all_skills = self.analyze_role_skills(jobs, role)
        if not all_skills:
            return {}
            
        # Sort by percentage and limit results
        sorted_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)
        top_skills = dict(sorted_skills[:limit])
        
        logger.debug(f"Retrieved top {len(top_skills)} skills for role: {role}")
        return top_skills
        
    def clear_cache(self) -> None:
        """Clear all component caches."""
        self.job_filter.clear_cache()
        self.skill_calculator.clear_cache()
        logger.debug("All role analysis caches cleared")
