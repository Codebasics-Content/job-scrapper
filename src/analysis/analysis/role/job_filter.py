# Job Role Filter Component - EMD Compliance: ≤80 lines
# Handles job filtering by role with fuzzy matching

import logging
from src.models import JobModel

logger = logging.getLogger(__name__)


class JobRoleFilter:
    """
    Filters jobs based on role matching criteria.
    Uses fuzzy string matching for role identification.
    """
    
    def __init__(self):
        """Initialize the job role filter."""
        self.filter_cache: dict[str, list[JobModel]] = {}
        
    def filter_jobs_by_role(self, jobs: list[JobModel], role: str) -> list[JobModel]:
        """
        Filter jobs that match the specified role.
        
        Args:
            jobs: list of job models to filter
            role: Target role to filter for
            
        Returns:
            list of jobs matching the role criteria
        """
        if not jobs or not role:
            logger.warning("Empty jobs list or role provided")
            return []
            
        # Check cache first
        cache_key = f"{role}_{len(jobs)}"
        if cache_key in self.filter_cache:
            logger.debug(f"Using cached results for role: {role}")
            return self.filter_cache[cache_key]
            
        role_lower = role.lower().strip()
        filtered_jobs: list[JobModel] = []
        
        for job in jobs:
            if self._matches_role(job, role_lower):
                filtered_jobs.append(job)
        
        # Cache results
        self.filter_cache[cache_key] = filtered_jobs
        
        logger.debug(f"Filtered {len(filtered_jobs)}/{len(jobs)} jobs for role: {role}")
        return filtered_jobs
        
    def _matches_role(self, job: JobModel, target_role: str) -> bool:
        """
        Check if a job matches the target role using fuzzy matching.
        
        Args:
            job: Job model to check
            target_role: Target role (already lowercase and stripped)
            
        Returns:
            True if job matches the role criteria
        """
        if not hasattr(job, 'job_role') or not job.job_role:
            return False
            
        job_role_lower = job.job_role.lower().strip()
        
        # Exact match or partial match in either direction
        return (target_role in job_role_lower or 
                job_role_lower in target_role)
                
    def clear_cache(self) -> None:
        """Clear the filter cache."""
        self.filter_cache.clear()
        logger.debug("Job filter cache cleared")
