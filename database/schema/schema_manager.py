# Database Schema Manager - Table Creation and Indexing
# EMD Compliance: ≤80 lines for schema operations

import logging
from typing import Any
from database.connection.db_connection import DatabaseConnection

logger = logging.getLogger(__name__)

class SchemaManager:
    """
    Handles database schema creation and optimization
    """
    
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
    
    def create_jobs_table(self) -> None:
        """Create jobs table with optimized schema"""
        with self.connection.get_connection_context() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_role TEXT NOT NULL,
                    company TEXT NOT NULL,
                    experience TEXT,
                    skills TEXT,  -- JSON array of normalized skills
                    jd TEXT,      -- Job description  
                    platform TEXT NOT NULL,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(job_role, company, platform)
                )
            """)
            conn.commit()
            
        logger.info("Jobs table created successfully")
    
    def create_indexes(self) -> None:
        """Create optimized indexes for job queries"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_skills ON jobs(skills)",
            "CREATE INDEX IF NOT EXISTS idx_platform ON jobs(platform)",
            "CREATE INDEX IF NOT EXISTS idx_job_role ON jobs(job_role)",
            "CREATE INDEX IF NOT EXISTS idx_company ON jobs(company)",
            "CREATE INDEX IF NOT EXISTS idx_scraped_at ON jobs(scraped_at)"
        ]
        
        with self.connection.get_connection_context() as conn:
            for index_sql in indexes:
                conn.execute(index_sql)
            conn.commit()
            
        logger.info(f"Created {len(indexes)} database indexes")
    
    def initialize_schema(self) -> None:
        """Initialize complete database schema"""
        self.create_jobs_table()
        self.create_indexes()
        logger.info("Database schema initialization completed")
