"""Retry helper with exponential backoff for Playwright operations"""
import asyncio
import logging
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 2.0,
    operation_name: str = "operation"
) -> tuple[Any | None, bool]:
    """Execute async function with exponential backoff retry
    
    Args:
        func: Async function to execute
        max_retries: Maximum retry attempts (default 3)
        base_delay: Base delay in seconds (default 2.0)
        operation_name: Name for logging
        
    Returns:
        (result, success): Tuple of result and success boolean
    """
    for attempt in range(max_retries):
        try:
            result = await func()
            return result, True
        except Exception as error:
            if attempt == max_retries - 1:
                logger.error(
                    f"❌ {operation_name} failed after {max_retries} attempts: {error}"
                )
                return None, False
            
            delay = base_delay * (2 ** attempt)  # Exponential: 2s, 4s, 8s
            logger.warning(
                f"⚠️  {operation_name} attempt {attempt + 1} failed, "
                f"retrying in {delay}s: {error}"
            )
            await asyncio.sleep(delay)
    
    return None, False
