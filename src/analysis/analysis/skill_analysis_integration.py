# Skill Analysis Integration - Database to Analysis Pipeline
import logging
from src.db.connection import ConnectionManager
from src.db.operations import JobRetrieval
from src.analysis.analysis.skill_analyzer import SkillAnalysisEngine

logger = logging.getLogger(__name__)

class SkillAnalysisIntegration:
    """Integrates database retrieval with skill analysis engine."""
    
    def __init__(self, db_path: str = "data/jobs.db"):
        self.db_path: str = db_path
        self.conn_manager: ConnectionManager = ConnectionManager(db_path)
        self.job_retrieval: JobRetrieval = JobRetrieval()
        self.analyzer: SkillAnalysisEngine = SkillAnalysisEngine()
        
    def analyze_all_jobs(self) -> dict[str, float]:
        """Analyze skills from all jobs in database."""
        
        try:
            with self.conn_manager.get_connection() as conn:
                jobs = self.job_retrieval.retrieve_all_jobs(conn)
            
            if not jobs:
                logger.warning("No jobs found in database for skill analysis")
                return {}
                
            logger.info(f"Analyzing skills from {len(jobs)} total jobs")
            skill_percentages = self.analyzer.analyze_job_skills(
                jobs, 
                target_role="all"
            )
            
            return skill_percentages
            
        except Exception as e:
            logger.error(f"Error analyzing all jobs: {e}")
            return {}
            
    def analyze_by_role(self, job_role: str) -> dict[str, float]:
        """Analyze skills for specific job role."""
        
        try:
            with self.conn_manager.get_connection() as conn:
                jobs = self.job_retrieval.retrieve_jobs_by_role(conn, job_role)
            
            if not jobs:
                logger.warning(f"No jobs found for role: {job_role}")
                return {}
                
            logger.info(f"Analyzing skills from {len(jobs)} {job_role} jobs")
            skill_percentages = self.analyzer.analyze_job_skills(
                jobs,
                target_role=job_role
            )
            
            return skill_percentages
            
        except Exception as e:
            logger.error(f"Error analyzing jobs for role {job_role}: {e}")
            return {}
            
    def get_total_jobs_count(self) -> int:
        """Get total number of jobs in database."""
        
        try:
            with self.conn_manager.get_connection() as conn:
                count = self.job_retrieval.get_job_count(conn)
            logger.info(f"Total jobs in database: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error getting total jobs count: {e}")
            return 0
