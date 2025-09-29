# Exponential Backoff Retry Handler - Anti-detection resilience
# EMD Compliance: ≤80 lines for retry logic

import asyncio
import logging
import time
from typing import Callable, TypeVar
from collections.abc import Awaitable

T = TypeVar('T')

logger = logging.getLogger(__name__)

class ExponentialBackoffRetry:
    """
    Exponential backoff retry mechanism for web scraping resilience
    """
    
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 8.0):
        self.max_attempts: int = max_attempts
        self.base_delay: float = base_delay
        self.max_delay: float = max_delay
    
    def retry_sync(self, func: Callable[[], T], operation_name: str = "operation") -> T:
        """Synchronous retry with exponential backoff"""
        last_exception: Exception | None = None
        
        for attempt in range(self.max_attempts):
            try:
                result = func()
                if attempt > 0:
                    logger.info(f"{operation_name} succeeded on attempt {attempt + 1}")
                return result
                
            except Exception as error:
                last_exception = error
                if attempt < self.max_attempts - 1:
                    delay: float = min(self.base_delay * (2 ** attempt), self.max_delay)
                    logger.warning(f"{operation_name} attempt {attempt + 1} failed: {error}. Retrying in {delay}s")
                    time.sleep(delay)
                else:
                    logger.error(f"{operation_name} failed after {self.max_attempts} attempts")
        
        if last_exception is not None:
            raise last_exception
        raise RuntimeError(f"{operation_name} failed without exception")
    
    async def retry_async(self, func: Callable[[], Awaitable[T]], operation_name: str = "operation") -> T:
        """Asynchronous retry with exponential backoff"""
        last_exception: Exception | None = None
        
        for attempt in range(self.max_attempts):
            try:
                result = await func()
                if attempt > 0:
                    logger.info(f"{operation_name} succeeded on attempt {attempt + 1}")
                return result
                
            except Exception as error:
                last_exception = error
                if attempt < self.max_attempts - 1:
                    delay: float = min(self.base_delay * (2 ** attempt), self.max_delay)
                    logger.warning(f"{operation_name} attempt {attempt + 1} failed: {error}. Retrying in {delay}s")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"{operation_name} failed after {self.max_attempts} attempts")
        
        if last_exception is not None:
            raise last_exception
        raise RuntimeError(f"{operation_name} failed without exception")
