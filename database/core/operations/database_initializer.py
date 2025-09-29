#!/usr/bin/env python3
# Database Initialization - WAL Mode Setup and Schema Creation
# EMD Compliance: ≤80 lines

import sqlite3
import logging

logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """
    Handles database initialization with WAL mode and schema creation
    """
    
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
    
    def initialize_database(self, db_path: str) -> None:
        """Initialize database with WAL mode and create tables"""
        with self.connection_manager.get_connection() as conn:
            self._configure_database(conn)
            self._create_tables(conn)
            self._create_indexes(conn)
            conn.commit()
            
        logger.info(f"Database initialized at {db_path} with WAL mode")
    
    def _configure_database(self, conn: sqlite3.Connection) -> None:
        """Configure database with optimal settings"""
        optimizations = [
            "PRAGMA journal_mode=WAL",
            "PRAGMA synchronous=NORMAL", 
            "PRAGMA cache_size=10000",
            "PRAGMA temp_store=memory"
        ]
        
        for pragma in optimizations:
            cursor = conn.execute(pragma)
            cursor.close()
    
    def _create_tables(self, conn: sqlite3.Connection) -> None:
        """Create jobs table with optimized schema"""
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
    
    def _create_indexes(self, conn: sqlite3.Connection) -> None:
        """Create indexes for faster queries"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_skills ON jobs(skills)",
            "CREATE INDEX IF NOT EXISTS idx_platform ON jobs(platform)"
        ]
        
        for index_sql in indexes:
            cursor = conn.execute(index_sql)
            cursor.close()
