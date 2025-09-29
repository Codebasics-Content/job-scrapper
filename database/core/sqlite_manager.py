#!/usr/bin/env python3
# SQLite Database Manager - Thread-Safe WAL Mode Operations
# EMD Compliance: ≤80 lines

import sqlite3
import threading
from contextlib import contextmanager
import logging
from datetime import datetime

from models.job import JobModel
from .connection_manager import ConnectionManager
from .data_converter import DataConverter

logger = logging.getLogger(__name__)

class SQLiteManager:
    """
    Thread-safe SQLite database manager with WAL mode for parallel operations
    """
    
    def __init__(self, db_path: str = "jobs.db") -> None:
        self.db_path: str = db_path
        self.lock: threading.RLock = threading.RLock()
        self.connection_manager = ConnectionManager(db_path)
        self.data_converter = DataConverter()
        self._initialize_database()
        
    def _initialize_database(self) -> None:
        """Initialize database with WAL mode and create tables"""
        with self.connection_manager.get_connection() as conn:
            # Enable WAL mode for concurrent read/write operations
            cursor = conn.execute("PRAGMA journal_mode=WAL")
            cursor.close()
            cursor = conn.execute("PRAGMA synchronous=NORMAL") 
            cursor.close()
            cursor = conn.execute("PRAGMA cache_size=10000")
            cursor.close()
            cursor = conn.execute("PRAGMA temp_store=memory")
            cursor.close()
            
            # Create jobs table with optimized schema
            cursor = conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_role TEXT NOT NULL,
                    company TEXT NOT NULL,
                    experience TEXT,
                    skills TEXT,  -- JSON array of normalized skills
                    jd TEXT,      -- Job description
                    platform TEXT NOT NULL,
                    url TEXT,
                    location TEXT,
                    salary TEXT,
                    posted_date TEXT,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(job_role, company, platform)
                )
            """)
            cursor.close()
            
            # Create index for faster skill queries
            cursor = conn.execute("CREATE INDEX IF NOT EXISTS idx_skills ON jobs(skills)")
            cursor.close()
            cursor = conn.execute("CREATE INDEX IF NOT EXISTS idx_platform ON jobs(platform)")
            cursor.close()
            conn.commit()
            
        logger.info(f"Database initialized at {self.db_path} with WAL mode")
    
    def store_jobs(self, jobs: list[JobModel]) -> int:
        """Store jobs with thread-safe batch operations"""
        if not jobs:
            return 0
            
        from .batch_operations import BatchOperations
        batch_ops = BatchOperations()
        
        with self.lock, self.connection_manager.get_connection() as conn:
            return batch_ops.batch_store_jobs(conn, jobs)
    
    def get_all_jobs(self) -> list[JobModel]:
        """Retrieve all jobs from database with proper row handling"""
        jobs = []
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM jobs")
                
                # Get column names from cursor description
                columns = [desc[0] for desc in cursor.description]
                
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    job_data = self.data_converter.convert_row_to_job_data(row_dict)
                    job_model = JobModel(**job_data)
                    jobs.append(job_model)
                    
            logger.info(f"Retrieved {len(jobs)} jobs from database")
            return jobs
            
        except Exception as error:
            logger.error(f"Error retrieving jobs: {error}")
            return []
