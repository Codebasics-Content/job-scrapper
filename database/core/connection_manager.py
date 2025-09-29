#!/usr/bin/env python3
# SQLite Connection Manager - Thread-Safe Context Management
# EMD Compliance: ≤80 lines

import sqlite3
from typing import Generator
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    Thread-safe SQLite connection manager with WAL mode support
    """
    
    def __init__(self, db_path: str) -> None:
        self.db_path: str = db_path
        
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Thread-safe database connection context manager"""
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path, 
                check_same_thread=False,
                timeout=30.0
            )
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except Exception as error:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {error}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_pragma(self, conn: sqlite3.Connection, pragma: str) -> None:
        """Execute PRAGMA statement and properly close cursor"""
        cursor = conn.execute(pragma)
        cursor.close()
    
    def execute_ddl(self, conn: sqlite3.Connection, sql: str) -> None:
        """Execute DDL statement and properly close cursor"""
        cursor = conn.execute(sql)
        cursor.close()
    
    def test_connection(self) -> bool:
        """Test database connection health"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result is not None
        except Exception as error:
            logger.error(f"Connection test failed: {error}")
            return False
