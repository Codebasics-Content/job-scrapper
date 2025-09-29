# Database Connection Manager - Thread-Safe Context Management
# EMD Compliance: ≤80 lines for connection handling

try:
    import sqlite3
except ImportError:
    import pysqlite3 as sqlite3
import logging
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    Thread-safe SQLite connection manager with WAL mode
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._setup_database()
    
    def _setup_database(self) -> None:
        """Initialize database with optimal settings"""
        with self._get_connection() as conn:
            # Enable WAL mode for concurrent operations
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL") 
            conn.execute("PRAGMA cache_size=10000")
            conn.execute("PRAGMA temp_store=memory")
            
        logger.info(f"Database connection initialized: {self.db_path}")
    
    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Thread-safe database connection context manager"""
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path, 
                check_same_thread=False,
                timeout=30.0
            )
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as error:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {error}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_connection_context(self):
        """Get connection context for external use"""
        return self._get_connection()
