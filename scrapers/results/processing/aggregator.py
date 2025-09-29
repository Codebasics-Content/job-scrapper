# Job Aggregator - Processes and stores job results
# EMD Compliance: ≤80 lines for job collection management

import logging
from models.job import JobModel

logger = logging.getLogger(__name__)

class JobAggregator:
    """
    Aggregates and stores processed job results
    Maintains collection for statistical analysis
    """
    
    def __init__(self):
        self.processed_jobs: list[JobModel] = []
        
    def process_job_results(self, jobs: list[JobModel]) -> None:
        """Process and store job results for analysis"""
        self.processed_jobs = jobs
        logger.info(f"Processed {len(jobs)} job results for analysis")
        
    def get_all_jobs(self) -> list[JobModel]:
        """Return all processed jobs"""
        return self.processed_jobs
        
    def get_job_count(self) -> int:
        """Return total number of processed jobs"""
        return len(self.processed_jobs)
        
    def has_jobs(self) -> bool:
        """Check if any jobs have been processed"""
        return len(self.processed_jobs) > 0
        
    def get_unique_skills(self) -> set:
        """Extract unique skills from all processed jobs"""
        all_skills = set()
        for job in self.processed_jobs:
            all_skills.update(job.normalized_skills)
        return all_skills
        
    def get_platform_distribution(self) -> dict[str, int]:
        """Calculate job distribution across platforms"""
        platform_counts = {}
        for job in self.processed_jobs:
            platform = job.platform
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        return platform_counts
