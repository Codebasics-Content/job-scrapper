# Retry Logic - Exponential backoff utility for robust web scraping
# EMD Compliance: ≤80 lines for retry mechanisms with exponential backoff

import asyncio
import logging
import time
from typing import Callable, TypeVar, ParamSpec, cast
from functools import wraps
from collections.abc import Awaitable

logger = logging.getLogger(__name__)

class ExponentialBackoffRetry:
    """Exponential backoff retry mechanism for web scraping operations"""
    
    max_retries: int
    base_delay: float
    max_delay: float
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff + jitter"""
        exponential_delay: float = self.base_delay * float(pow(2, attempt))
        capped_delay: float = min(exponential_delay, self.max_delay)
        # Add jitter to prevent thundering herd
        jitter: float = capped_delay * 0.1 * (time.time() % 1)
        final_delay: float = capped_delay + jitter
        logger.debug(f"Retry attempt {attempt}: delay={final_delay:.2f}s")
        return final_delay
    
    def retry_sync(self, operation: Callable[[], object], operation_name: str = "operation") -> object:
        """Synchronous retry with exponential backoff"""
        last_exception: Exception | None = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = operation()
                if attempt > 0:
                    logger.info(f"{operation_name}: Success on retry attempt {attempt}")
                return result
                
            except Exception as error:
                last_exception = error
                
                if attempt < self.max_retries:
                    delay = self.calculate_delay(attempt)
                    logger.warning(f"{operation_name} failed (attempt {attempt + 1}): {error}")
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"{operation_name}: All {self.max_retries + 1} attempts failed")
        
        # All retries exhausted - last_exception must be set if we reach here
        if last_exception is None:
            raise RuntimeError(f"{operation_name}: No exception captured during retry")
        raise last_exception
    
    async def retry_async(self, operation: Callable[[], Awaitable[object]], operation_name: str = "operation") -> object:
        """Asynchronous retry with exponential backoff"""
        last_exception: Exception | None = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(operation):
                    result = await operation()
                else:
                    result = operation()
                    
                if attempt > 0:
                    logger.info(f"{operation_name}: Success on retry attempt {attempt}")
                return result
                
            except Exception as error:
                last_exception = error
                
                if attempt < self.max_retries:
                    delay = self.calculate_delay(attempt)
                    logger.warning(f"{operation_name} failed (attempt {attempt + 1}): {error}")
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"{operation_name}: All {self.max_retries + 1} attempts failed")
        
        # All retries exhausted - last_exception must be set if we reach here
        if last_exception is None:
            raise RuntimeError(f"{operation_name}: No exception captured during retry")
        raise last_exception

# Type variables for decorator
P = ParamSpec('P')
T = TypeVar('T')

# Convenience decorator for quick retry operations
def retry_on_failure(max_retries: int = 3, base_delay: float = 1.0) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator for automatic retry with exponential backoff"""
    retry_handler = ExponentialBackoffRetry(max_retries, base_delay)
    
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            operation: Callable[[], object] = lambda: func(*args, **kwargs)
            result = retry_handler.retry_sync(operation, func.__name__)
            return cast(T, result)
        return cast(Callable[P, T], wrapper)
    return decorator
