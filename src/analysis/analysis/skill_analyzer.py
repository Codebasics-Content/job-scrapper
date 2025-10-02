# Skill Analysis Engine - Core Analytics
import logging
from src.models import JobModel
from src.analysis.skill_statistics import calculate_skill_percentages

logger = logging.getLogger(__name__)

class SkillAnalysisEngine:
    """Core engine for analyzing job market skill requirements."""
    
    def __init__(self):
        self.skill_synonyms: dict[str, list[str]] = {
            'machine learning': ['ml', 'machinelearning'],
            'artificial intelligence': ['ai', 'artificialintelligence'],
            'python': ['py'],
            'javascript': ['js'],
            'react': ['reactjs', 'react.js'],
            'node': ['nodejs', 'node.js'],
            'sql': ['mysql', 'postgresql', 'sqlite'],
            'aws': ['amazon web services'],
            'gcp': ['google cloud platform']
        }
        
    def analyze_job_skills(self, jobs: list[JobModel], target_role: str) -> dict[str, float]:
        """Analyze skills from job listings for specific role"""
        
        if not jobs:
            logger.warning(f"No jobs provided for skill analysis of {target_role}")
            return {}
            
        # Normalize and extract skills
        normalized_jobs = self._normalize_job_skills(jobs)
        
        # Calculate skill percentages
        skill_percentages = calculate_skill_percentages(normalized_jobs)
        
        # Apply skill synonyms mapping
        consolidated_skills = self._consolidate_synonyms(skill_percentages)
        
        logger.info(f"Analyzed {len(jobs)} jobs for {target_role}, found {len(consolidated_skills)} unique skills")
        return consolidated_skills
        
    def _normalize_job_skills(self, jobs: list[JobModel]) -> list[JobModel]:
        """Normalize job skills for consistent analysis"""
        
        for job in jobs:
            if hasattr(job, 'skills') and job.skills:
                # Extract and clean skills
                skills_list = [skill.strip().lower() for skill in job.skills.split(',')]
                job.skills_list = skills_list
                job.normalized_skills = skills_list
                
        return jobs
        
    def _consolidate_synonyms(self, skill_percentages: dict[str, float]) -> dict[str, float]:
        """Consolidate similar skills using synonym mapping"""
        
        consolidated = {}
        
        for skill, percentage in skill_percentages.items():
            # Find canonical name for skill
            canonical_skill = self._get_canonical_skill(skill.lower())
            
            if canonical_skill in consolidated:
                consolidated[canonical_skill] += percentage
            else:
                consolidated[canonical_skill] = percentage
                
        return consolidated
        
    def _get_canonical_skill(self, skill: str) -> str:
        """Get canonical skill name from synonyms"""
        
        for canonical, synonyms in self.skill_synonyms.items():
            if skill == canonical or skill in synonyms:
                return canonical
                
        return skill
