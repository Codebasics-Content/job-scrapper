#!/usr/bin/env python3
# Batch Operations - Efficient Bulk Database Operations
# EMD Compliance: ≤80 lines

import sqlite3
from typing import Any
import logging
import json
from datetime import datetime

from models.job import JobModel

logger = logging.getLogger(__name__)

class BatchOperations:
    """
    Handles efficient batch database operations with proper error handling
    """
    
    def batch_store_jobs(self, conn: sqlite3.Connection, jobs: list[JobModel]) -> int:
        """Store multiple jobs efficiently using batch operations"""
        if not jobs:
            logger.warning("[DB STORAGE] No jobs to store")
            return 0
        
        logger.info(f"[DB STORAGE] Preparing to store {len(jobs)} jobs...")
        batch_data = []
        for job in jobs:
            job_data = self._prepare_job_data(job)
            batch_data.append(job_data)
        
        logger.info(f"[DB STORAGE] Batch data prepared, inserting into database...")
        try:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR IGNORE INTO jobs (
                    job_id, job_role, company, experience, skills, jd,
                    platform, url, location, salary, posted_date, scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch_data)
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.commit()
            
            logger.info(f"[DB STORAGE] ✅ Successfully stored {rows_affected} new jobs")
            logger.info(f"[DB STORAGE] Duplicates skipped: {len(jobs) - rows_affected}")
            return rows_affected
            
        except Exception as error:
            logger.error(f"[DB STORAGE] ❌ Batch store failed: {error}")
            logger.exception("Full error traceback:")
            conn.rollback()
            return 0
    
    def _prepare_job_data(self, job: JobModel) -> tuple[Any, ...]:
        """Prepare job data for batch insertion"""
        return (
            job.job_id or f"{job.job_role}_{job.company}_{job.platform}",
            job.job_role or "",
            job.company or "",
            job.experience or "",
            json.dumps(job.normalized_skills) if job.normalized_skills else "[]",
            job.jd or "",
            job.platform or "",
            job.url,
            job.location,
            job.salary,
            job.posted_date.isoformat() if job.posted_date else None,
            job.scraped_at.isoformat() if job.scraped_at else datetime.now().isoformat()
        )
