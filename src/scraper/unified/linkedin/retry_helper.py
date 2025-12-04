"""Retry helper with exponential backoff for Playwright operations"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

logger = logging.getLogger(__name__)


class JobExpiredError(Exception):
    """Exception for expired/removed job postings (404) - should not be retried"""

    pass


class Job404Error(Exception):
    """Exception for HTTP 404 Not Found - job page doesn't exist, delete from DB"""

    pass


class Job503Error(Exception):
    """Exception for HTTP 503 Service Unavailable - retry with backoff"""

    pass


T = TypeVar("T")


async def retry_with_backoff(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    base_delay: float = 2.0,
    operation_name: str = "operation",
) -> tuple[T | str | None, bool]:
    """Execute async function with exponential backoff retry

    Args:
        func: Async function to execute
        max_retries: Maximum retry attempts (default 3)
        base_delay: Base delay in seconds (default 2.0)
        operation_name: Name for logging

    Returns:
        (result_or_error, success): Tuple of result (or error message on failure) and success boolean
    """
    last_error: str | None = None
    for attempt in range(max_retries):
        try:
            result: T = await func()
            return result, True
        except JobExpiredError as error:
            # Don't retry expired/404 jobs - fail immediately (silent)
            logger.debug(f"{operation_name} - job expired/removed, skipping retries")
            return str(error), False
        except Job404Error as error:
            # HTTP 404 - job doesn't exist, don't retry
            logger.debug(f"{operation_name} - HTTP 404 Not Found, skipping retries")
            return f"404:{error}", False
        except Job503Error as error:
            # HTTP 503 - server temporarily unavailable, DO retry with longer backoff
            last_error = f"503:{error}"
            if attempt == max_retries - 1:
                logger.error(
                    f"{operation_name} - HTTP 503 after {max_retries} attempts"
                )
                return last_error, False
            delay: float = base_delay * (3**attempt)  # Longer backoff for 503: 2s, 6s, 18s
            logger.warning(f"{operation_name} - HTTP 503, retrying in {delay}s...")
            await asyncio.sleep(delay)
            continue
        except Exception as error:
            last_error = str(error)
            if attempt == max_retries - 1:
                logger.error(
                    f"{operation_name} failed after {max_retries} attempts: {error}"
                )
                return last_error, False

            delay = base_delay * (2**attempt)  # Exponential: 2s, 4s, 8s
            logger.warning(
                f"{operation_name} attempt {attempt + 1} failed, "
                f"retrying in {delay}s: {error}"
            )
            await asyncio.sleep(delay)

    return last_error, False
