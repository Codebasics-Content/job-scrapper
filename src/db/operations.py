# Database Operations - Thread-Safe Job Storage
# EMD Compliance: ≤80 lines, ZUV compliant

import logging
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import JobModel

from src.db.connection import DatabaseConnection
from src.db.schema import SchemaManager

logger = logging.getLogger(__name__)

class JobStorageOperations:
    """Thread-safe job storage with batch processing"""
    
    connection: DatabaseConnection
    schema_manager: SchemaManager
    lock: threading.RLock
    
    def __init__(self, db_path: str = "jobs.db") -> None:
        self.connection = DatabaseConnection(db_path)
        self.schema_manager = SchemaManager(self.connection)
        self.lock = threading.RLock()
        self._initialize_storage()
    
    def _initialize_storage(self) -> None:
        """Initialize database schema for job storage"""
        self.schema_manager.initialize_schema()
        logger.info("Job storage operations initialized")
    
    def store_jobs(self, jobs: list["JobModel"]) -> int:
        """Store jobs with thread-safe batch operations"""
        if not jobs:
            return 0
            
        with self.lock, self.connection.get_connection_context() as conn:
            stored_count = 0
            for job in jobs:
                try:
                    cursor = conn.execute("""
                        INSERT OR REPLACE INTO jobs 
                        (job_id, job_role, company, experience, skills, 
                         jd, platform, url, location, salary, posted_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        job.job_id, job.job_role, job.company,
                        job.experience, job.skills, job.jd,
                        job.platform, job.url, job.location,
                        job.salary, job.posted_date
                    ))
                    if cursor:
                        stored_count += 1
                except Exception as error:
                    logger.warning(f"Failed to store job {job.job_id}: {error}")
            
            conn.commit()
            logger.info(f"Stored {stored_count}/{len(jobs)} jobs successfully")
            return stored_count
    
    def get_jobs_by_role(self, job_role: str) -> list[dict[str, object]]:
        """Retrieve jobs by role with efficient querying"""
        with self.connection.get_connection_context() as conn:
            cursor = conn.execute("""
                SELECT * FROM jobs 
                WHERE job_role LIKE ? 
                ORDER BY scraped_at DESC
            """, (f"%{job_role}%",))
            
            if cursor.description is None:
                return []
            
            columns: list[str] = [str(desc[0]) for desc in cursor.description]
            rows = cursor.fetchall()
            
            result: list[dict[str, object]] = []
            for row in rows:
                row_dict: dict[str, object] = {}
                for i, column in enumerate(columns):
                    value: object = row[i]
                    row_dict[column] = value if value is not None else ""
                result.append(row_dict)
            
            return result
