"""Job validation logic for LinkedIn scraped data"""
from typing import Tuple
from src.models.models import JobDetailModel
import logging

logger = logging.getLogger(__name__)


class JobValidator:
    """Validates job detail data for quality and completeness"""
    
    def __init__(self, min_description_length: int = 50, max_skills: int = 50):
        self.min_description_length = min_description_length
        self.max_skills = max_skills
    
    def validate_job(self, job: JobDetailModel) -> Tuple[bool, str]:
        """Validate single job - returns (is_valid, reason)"""
        
        # Check 1: Required fields present
        if not job.actual_role or not job.company_name:
            return False, "Missing required fields (actual_role/company_name)"
        
        # Check 2: Description quality
        if not job.job_description or len(job.job_description) < self.min_description_length:
            return False, f"Description too short (min {self.min_description_length} chars)"
        
        # Check 3: URL validity
        if not job.url or not job.url.startswith('https://'):
            return False, "Invalid URL format"
        
        # Check 4: Skills extraction (flexible - allow 0 skills for manual review)
        skills = job.skills.split(',') if job.skills else []
        if len(skills) > self.max_skills:
            return False, f"Excessive skills ({len(skills)})"
        
        # Check 5: Job ID validity
        if not job.job_id or not job.job_id.startswith('linkedin_'):
            return False, "Invalid job ID format"
        
        # All checks passed
        return True, "Valid job"
    
    def batch_validate(
        self, jobs: list[JobDetailModel]
    ) -> Tuple[list[JobDetailModel], list[dict[str, str]]]:
        """Validate batch of jobs - returns (valid_jobs, rejected_jobs)"""
        valid_jobs: list[JobDetailModel] = []
        rejected_jobs: list[dict[str, str]] = []
        
        for idx, job in enumerate(jobs, 1):
            is_valid, reason = self.validate_job(job)
            
            if is_valid:
                valid_jobs.append(job)
                logger.info(f"✅ Job {idx}: VALID")
            else:
                rejected_jobs.append({
                    "job_id": job.job_id,
                    "job_title": job.actual_role or "Unknown",
                    "company": job.company_name or "Unknown",
                    "reason": reason
                })
                logger.warning(msg=f"❌ Job {idx}: REJECTED - {reason}")
        
        logger.info(f"📊 Validation: {len(valid_jobs)} valid, {len(rejected_jobs)} rejected")
        return valid_jobs, rejected_jobs
