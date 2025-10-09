# Database Schema Management - LinkedIn Jobs Table
# EMD Compliance: ≤80 lines, ZUV compliant

"""Database schema management module"""
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.db.connection import DatabaseConnection

logger = logging.getLogger(__name__)

class SchemaManager:
    """Manages database schema and indexes"""
    
    connection: "DatabaseConnection"
    
    def __init__(self, connection: "DatabaseConnection") -> None:
        self.connection = connection
    
    def create_jobs_table(self) -> None:
        """Create jobs table optimized for LinkedIn data"""
        with self.connection.get_connection_context() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'"
            )
            table_exists = cursor.fetchone() is not None
            
            if not table_exists:
                cursor = conn.execute("""
                    CREATE TABLE jobs (
                        job_id TEXT PRIMARY KEY,
                        job_role TEXT NOT NULL,
                        company TEXT NOT NULL,
                        experience TEXT,
                        skills TEXT,
                        jd TEXT,
                        company_detail TEXT,
                        platform TEXT NOT NULL,
                        url TEXT,
                        location TEXT,
                        salary TEXT,
                        posted_date TEXT,
                        scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(job_role, company, platform)
                    )
                """)
                if cursor:
                    logger.info("Created jobs table successfully")
                else:
                    logger.info("Failed to create jobs table")
                conn.commit()
            else:
                logger.info("Jobs table already exists")
    
    def create_indexes(self) -> None:
        """Create performance indexes for common queries"""
        indexes = [
            ("idx_skills", "skills"),
            ("idx_platform", "platform"),
            ("idx_job_role", "job_role"),
            ("idx_company", "company"),
            ("idx_scraped_at", "scraped_at")
        ]
        
        with self.connection.get_connection_context() as conn:
            for index_name, column in indexes:
                cursor = conn.execute(
                    f"CREATE INDEX IF NOT EXISTS {index_name} ON jobs ({column})"
                )
                if cursor:
                    logger.info(f"Created index {index_name} successfully")
            conn.commit()
            
        logger.info(f"Created {len(indexes)} database indexes")
    
    def initialize_schema(self) -> None:
        """Initialize complete database schema with indexes"""
        self.create_jobs_table()
        self.create_indexes()
        logger.info("Database schema initialization complete")
