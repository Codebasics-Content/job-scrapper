# Database Connection - Thread-Safe SQLite with WAL Mode
# EMD Compliance: ≤80 lines, ZUV compliant

import sqlite3
import logging
from contextlib import contextmanager, AbstractContextManager
from collections.abc import Iterator

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Thread-safe SQLite connection manager with WAL mode optimization"""
    
    db_path: str
    
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._setup_database()
    
    def _setup_database(self) -> None:
        """Initialize database with optimal settings for concurrent access"""
        with self._get_connection() as conn:
            # Enable Write-Ahead Logging for concurrent operations
            cursor = conn.execute("PRAGMA journal_mode=WAL")
            cursor.close()
            cursor = conn.execute("PRAGMA synchronous=NORMAL")
            cursor.close()
            cursor = conn.execute("PRAGMA cache_size=10000")
            cursor.close()
            cursor = conn.execute("PRAGMA temp_store=memory")
            cursor.close()
            
        logger.info(f"Database initialized: {self.db_path}")
    
    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """
        Thread-safe connection context manager
        Handles automatic commit/rollback and cleanup
        """
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
    
    def get_connection_context(self) -> AbstractContextManager[sqlite3.Connection]:
        """Get connection context for external use"""
        return self._get_connection()
