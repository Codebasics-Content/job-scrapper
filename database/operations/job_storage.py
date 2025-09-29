# Job Storage Operations - Thread-Safe Batch Job Storage
# EMD Compliance: ≤80 lines for job storage operations

import threading
import logging
from typing import List
from database.connection.db_connection import DatabaseConnection
from database.schema.schema_manager import SchemaManager
from models.job import JobModel

logger = logging.getLogger(__name__)

class JobStorageOperations:
    """
    Thread-safe job storage operations with batch processing
    """
    
    def __init__(self, db_path: str = "jobs.db"):
        self.connection = DatabaseConnection(db_path)
        self.schema_manager = SchemaManager(self.connection)
        self.lock = threading.RLock()
        self._initialize_storage()
    
    def _initialize_storage(self) -> None:
        """Initialize database schema for job storage"""
        self.schema_manager.initialize_schema()
        logger.info("Job storage operations initialized")
    
    def store_jobs(self, jobs: List[JobModel]) -> int:
        """Store jobs with thread-safe batch operations"""
        if not jobs:
            return 0
            
        with self.lock, self.connection.get_connection_context() as conn:
            stored_count = 0
            for job in jobs:
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO jobs 
                        (job_id, job_role, company, experience, skills, jd, platform)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        job.job_id, job.job_role, job.company, 
                        job.experience, job.skills, job.jd, job.platform
                    ))
                    stored_count += 1
                except Exception as error:
                    logger.warning(f"Failed to store job {job.job_id}: {error}")
            
            conn.commit()
            logger.info(f"Stored {stored_count}/{len(jobs)} jobs successfully")
            return stored_count
    
    def get_jobs_by_role(self, job_role: str) -> List[dict]:
        """Retrieve jobs by role with efficient querying"""
        with self.connection.get_connection_context() as conn:
            cursor = conn.execute("""
                SELECT * FROM jobs WHERE job_role LIKE ? ORDER BY scraped_at DESC
            """, (f"%{job_role}%",))
            return [dict(row) for row in cursor.fetchall()]
