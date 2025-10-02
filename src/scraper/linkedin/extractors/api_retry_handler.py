#!/usr/bin/env python3
# API retry handler for LinkedIn rate limiting
# EMD Compliance: ≤80 lines

import logging
import asyncio
from typing import Callable, TypeVar, Awaitable

logger = logging.getLogger(__name__)

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    initial_delay: float = 2.0,
    backoff_factor: float = 2.0
) -> T | None:
    """Retry function with exponential backoff for rate limits
    
    Args:
        func: Async function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay on each retry
        
    Returns:
        Function result or None if all retries failed
    """
    delay = initial_delay
    
    for attempt in range(max_retries + 1):
        try:
            return await func()
            
        except Exception as error:
            error_str = str(error).lower()
            
            # Detect shutdown conditions (don't retry or log)
            is_shutdown = (
                'cannot schedule new futures after shutdown' in error_str or
                'event loop is closed' in error_str or
                'connection refused' in error_str
            )
            
            if is_shutdown:
                return None  # Silently fail during shutdown
            
            # Check if it's a rate limit error (status 429)
            is_rate_limit = hasattr(error, 'status') and getattr(error, 'status', None) == 429
            
            if is_rate_limit:
                if attempt < max_retries:
                    logger.warning(
                        f"⏳ Rate limited (429). "
                        f"Retrying in {delay}s... ({attempt + 1}/{max_retries})"
                    )
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
                else:
                    logger.error(f"❌ Rate limit exceeded after {max_retries} retries")
                    return None
            else:
                # Non-rate-limit error, log and retry if attempts remain
                logger.error(f"Error: {error}")
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
                else:
                    return None
    
    return None
