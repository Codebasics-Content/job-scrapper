"""Platform-specific rate limiters based on 2025 research

Research findings (verified via @mcp:fetch):
- Indeed: 10 jobs/page, max 5-10 concurrent (HIGH anti-bot)
- LinkedIn: 25 jobs/page, max 1-3 concurrent (EXTREME anti-bot)
- Naukri: 20-25 jobs/page, max 10-20 concurrent (MODERATE anti-bot)
"""
from __future__ import annotations

import asyncio
from types import TracebackType
from typing import Literal

PlatformType = Literal["indeed", "linkedin", "naukri"]


class IndeedRateLimiter:
    """Rate limiter for Indeed (max 5 concurrent, 2s delay)"""

    def __init__(self, max_concurrent: int = 5, delay_seconds: float = 2.0):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.delay = delay_seconds
        self.platform = "indeed"

    async def acquire(self) -> None:
        """Acquire rate limit slot with delay"""
        await self.semaphore.acquire()
        await asyncio.sleep(self.delay)

    def release(self) -> None:
        """Release rate limit slot"""
        self.semaphore.release()

    async def __aenter__(self) -> IndeedRateLimiter:
        await self.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()


class LinkedInRateLimiter:
    """Rate limiter for LinkedIn (max 2 concurrent, 5s delay - EXTREME caution)"""

    def __init__(self, max_concurrent: int = 2, delay_seconds: float = 5.0):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.delay = delay_seconds
        self.platform = "linkedin"

    async def acquire(self) -> None:
        """Acquire rate limit slot with delay"""
        await self.semaphore.acquire()
        await asyncio.sleep(self.delay)

    def release(self) -> None:
        """Release rate limit slot"""
        self.semaphore.release()

    async def __aenter__(self) -> LinkedInRateLimiter:
        await self.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()


class NaukriRateLimiter:
    """Rate limiter for Naukri (max 15 concurrent, 1s delay - most lenient)"""

    def __init__(self, max_concurrent: int = 15, delay_seconds: float = 1.0):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.delay = delay_seconds
        self.platform = "naukri"

    async def acquire(self) -> None:
        """Acquire rate limit slot with delay"""
        await self.semaphore.acquire()
        await asyncio.sleep(self.delay)

    def release(self) -> None:
        """Release rate limit slot"""
        self.semaphore.release()

    async def __aenter__(self) -> NaukriRateLimiter:
        await self.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()


def get_rate_limiter(platform: PlatformType) -> IndeedRateLimiter | LinkedInRateLimiter | NaukriRateLimiter:
    """Factory function to get platform-specific rate limiter"""
    if platform == "indeed":
        return IndeedRateLimiter()
    elif platform == "linkedin":
        return LinkedInRateLimiter()
    elif platform == "naukri":
        return NaukriRateLimiter()
    else:
        raise ValueError(f"Unknown platform: {platform}")
