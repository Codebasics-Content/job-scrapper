#!/usr/bin/env python3
# Job Retrieval - Database Query Operations for Job Data
# EMD Compliance: ≤80 lines

import sqlite3
import logging
from typing import Optional
from models.job import JobModel
from database.core.data_converter import DataConverter

logger = logging.getLogger(__name__)

class JobRetrieval:
    """Retrieve jobs from database with filtering and conversion"""
    
    def __init__(self):
        self.converter = DataConverter()
    
    def retrieve_all_jobs(self, conn: sqlite3.Connection) -> list[JobModel]:
        """Retrieve all jobs from database"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs")
            rows = cursor.fetchall()
            
            jobs: list[JobModel] = []
            for row in rows:
                row_dict = dict(zip([col[0] for col in cursor.description], row))
                job_data = self.converter.convert_row_to_job_data(row_dict)
                jobs.append(JobModel(**job_data))
            
            logger.info(f"Retrieved {len(jobs)} jobs from database")
            return jobs
            
        except sqlite3.DatabaseError as error:
            logger.error(f"Failed to retrieve jobs: {error}")
            return []
    
    def retrieve_jobs_by_role(
        self, 
        conn: sqlite3.Connection, 
        role: str
    ) -> list[JobModel]:
        """Retrieve jobs filtered by job role"""
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM jobs WHERE job_role LIKE ?",
                (f"%{role}%",)
            )
            rows = cursor.fetchall()
            
            jobs: list[JobModel] = []
            for row in rows:
                row_dict = dict(zip([col[0] for col in cursor.description], row))
                job_data = self.converter.convert_row_to_job_data(row_dict)
                jobs.append(JobModel(**job_data))
            
            logger.info(f"Retrieved {len(jobs)} jobs for role '{role}'")
            return jobs
            
        except sqlite3.DatabaseError as error:
            logger.error(f"Failed to retrieve jobs by role: {error}")
            return []
    
    def get_job_count(self, conn: sqlite3.Connection) -> int:
        """Get total count of jobs in database"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM jobs")
            count_result = cursor.fetchone()
            count: int = count_result[0] if count_result else 0
            return count
        except sqlite3.DatabaseError as error:
            logger.error(f"Failed to get job count: {error}")
            return 0
