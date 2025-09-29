#!/usr/bin/env python3
# Job Retrieval Operations - Database Query Management
# EMD Compliance: ≤80 lines

import logging
from typing import List
from models.job import JobModel

logger = logging.getLogger(__name__)

class JobRetriever:
    """
    Handles job retrieval operations from database
    """
    
    def __init__(self, connection_manager, data_converter):
        self.connection_manager = connection_manager
        self.data_converter = data_converter
    
    def get_all_jobs(self) -> List[JobModel]:
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
    
    def get_job_by_id(self, job_id: str) -> JobModel:
        """Retrieve specific job by ID"""
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
                
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    row_dict = dict(zip(columns, row))
                    job_data = self.data_converter.convert_row_to_job_data(row_dict)
                    return JobModel(**job_data)
                
            return None
            
        except Exception as error:
            logger.error(f"Error retrieving job {job_id}: {error}")
            return None
    
    def get_jobs_by_platform(self, platform: str) -> List[JobModel]:
        """Retrieve jobs filtered by platform"""
        jobs = []
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM jobs WHERE platform = ?", (platform,))
                
                columns = [desc[0] for desc in cursor.description]
                
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    job_data = self.data_converter.convert_row_to_job_data(row_dict)
                    job_model = JobModel(**job_data)
                    jobs.append(job_model)
                    
            logger.info(f"Retrieved {len(jobs)} jobs for platform {platform}")
            return jobs
            
        except Exception as error:
            logger.error(f"Error retrieving jobs for platform {platform}: {error}")
            return []
