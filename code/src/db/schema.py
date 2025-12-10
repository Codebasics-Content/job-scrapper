# Two-Table Schema - Optimized for URL Collection + Detail Scraping
# EMD Compliance: ≤80 lines, Two-phase scraping architecture
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.db.connection import DatabaseConnection

logger = logging.getLogger(__name__)

class SchemaManager:
    """Manages two-table database schema for optimized scraping"""
    
    connection: "DatabaseConnection"
    
    def __init__(self, connection: "DatabaseConnection") -> None:
        self.connection = connection
    
    def create_job_urls_table(self) -> None:
        """Table 1: Lightweight URL collection with scraped tracking"""
        with self.connection.get_connection_context() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_urls (
                    job_id TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    input_role TEXT NOT NULL,
                    actual_role TEXT NOT NULL,
                    url TEXT NOT NULL,
                    scraped INTEGER DEFAULT 0,
                    UNIQUE(platform, url)
                )
            """)
            # Migration: Add scraped column to existing tables
            try:
                conn.execute("ALTER TABLE job_urls ADD COLUMN scraped INTEGER DEFAULT 0")
                logger.info("Added 'scraped' column to existing job_urls table")
            except Exception:
                pass  # Column already exists
            conn.commit()
            logger.info("Created/verified job_urls table with scraped tracking")
    
    def create_jobs_table(self) -> None:
        """Table 2: Full job details with foreign key"""
        with self.connection.get_connection_context() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    input_role TEXT,
                    actual_role TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    job_description TEXT,
                    skills TEXT,
                    company_name TEXT,
                    posted_date TEXT,
                    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES job_urls(job_id)
                )
            """)
            # Migration: Add input_role column to existing tables
            try:
                conn.execute("ALTER TABLE jobs ADD COLUMN input_role TEXT")
                logger.info("Added 'input_role' column to existing jobs table")
            except Exception:
                pass  # Column already exists
            conn.commit()
            logger.info("Created/verified jobs table with input_role")
    
    def create_indexes(self) -> None:
        """Create indexes for fast querying and deduplication"""
        with self.connection.get_connection_context() as conn:
            conn.execute("CREATE INDEX IF NOT EXISTS idx_urls_platform_role ON job_urls(platform, input_role)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_urls_url ON job_urls(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_urls_scraped ON job_urls(scraped)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_platform ON jobs(platform)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_url ON jobs(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_input_role ON jobs(input_role)")
            conn.commit()
            logger.info("Created all indexes with input_role tracking")
    
    def initialize_schema(self) -> None:
        """Initialize two-table schema with indexes"""
        self.create_job_urls_table()
        self.create_jobs_table()
        self.create_indexes()
        logger.info("Two-table schema initialization complete")
