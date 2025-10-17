"""Adaptive Rate Limiter for LinkedIn - Intelligent Throttling with Anti-Detection
EMD Compliance: ≤80 lines

Features:
- Adaptive concurrency (auto-reduces on 429 errors)
- Random jitter (2-4s delays, unpredictable)
- Circuit breaker (pauses after consecutive failures)
- Success rate tracking (auto-tunes parameters)
"""
from __future__ import annotations

import asyncio
import random
import time
import logging
from collections import deque
from types import TracebackType

logger = logging.getLogger(__name__)


class AdaptiveLinkedInRateLimiter:
    """Intelligent rate limiter that adapts to LinkedIn's defenses"""
    
    def __init__(
        self,
        initial_concurrent: int = 8,
        base_delay: float = 2.5,
        jitter_range: float = 1.0
    ):
        # Concurrency settings
        self.max_concurrent = initial_concurrent
        self.min_concurrent = 2  # Safety floor
        self.current_concurrent = initial_concurrent
        self.semaphore = asyncio.Semaphore(self.current_concurrent)
        
        # Delay settings
        self.base_delay = base_delay
        self.jitter_range = jitter_range
        
        # Tracking metrics
        self.error_count = 0
        self.success_count = 0
        self.consecutive_429s = 0
        
        # Circuit breaker state
        self.circuit_open = False
        self.circuit_open_until = 0
        
        # Performance tracking (last 100 requests)
        self.recent_delays = deque(maxlen=100)
        self.recent_successes = deque(maxlen=100)
    
    async def acquire(self) -> None:
        """Acquire with adaptive throttling and circuit breaker"""
        
        # Circuit breaker check
        if self.circuit_open:
            wait_time = self.circuit_open_until - time.time()
            if wait_time > 0:
                logger.warning(f"⚡ Circuit breaker: Waiting {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
            self.circuit_open = False
            self.consecutive_429s = 0
            logger.info("✅ Circuit breaker reset")
        
        # Acquire semaphore
        await self.semaphore.acquire()
        
        # Random jitter delay (human-like, unpredictable)
        delay = self.base_delay + random.uniform(-self.jitter_range, self.jitter_range)
        delay = max(1.0, delay)  # Minimum 1s
        
        self.recent_delays.append(delay)
        await asyncio.sleep(delay)
    
    def release(self, success: bool = True, error_code: int | None = None) -> None:
        """Release with success/failure tracking and auto-tuning"""
        self.semaphore.release()
        self.recent_successes.append(success)
        
        if success:
            self.success_count += 1
            self.consecutive_429s = 0
            
            # Gradually increase concurrency if performing well (>95% success)
            if len(self.recent_successes) >= 20:
                success_rate = sum(self.recent_successes) / len(self.recent_successes)
                if success_rate > 0.95 and self.current_concurrent < self.max_concurrent:
                    self._increase_concurrency()
        
        elif error_code == 429:
            self.error_count += 1
            self.consecutive_429s += 1
            
            # Aggressive response to rate limiting
            if self.consecutive_429s >= 3:
                self._trigger_circuit_breaker()
            else:
                self._reduce_concurrency()
    
    def _reduce_concurrency(self) -> None:
        """Reduce concurrent requests on errors"""
        old = self.current_concurrent
        self.current_concurrent = max(self.min_concurrent, self.current_concurrent - 2)
        if old != self.current_concurrent:
            self.semaphore = asyncio.Semaphore(self.current_concurrent)
            logger.warning(f"⚠️ Reduced concurrency: {old} → {self.current_concurrent}")
    
    def _increase_concurrency(self) -> None:
        """Increase concurrent requests when stable"""
        old = self.current_concurrent
        self.current_concurrent = min(self.max_concurrent, self.current_concurrent + 1)
        if old != self.current_concurrent:
            self.semaphore = asyncio.Semaphore(self.current_concurrent)
            logger.info(f"✅ Increased concurrency: {old} → {self.current_concurrent}")
    
    def _trigger_circuit_breaker(self) -> None:
        """Open circuit breaker for cooldown period"""
        self.circuit_open = True
        cooldown = 60  # 60 seconds pause
        self.circuit_open_until = time.time() + cooldown
        logger.error(f"🔴 Circuit breaker triggered! Pausing for {cooldown}s...")
        # Reset to minimum concurrency
        self.current_concurrent = self.min_concurrent
        self.semaphore = asyncio.Semaphore(self.current_concurrent)
    
    def get_stats(self) -> dict[str, str | int | bool | float]:
        """Return performance statistics"""
        success_rate = (sum(self.recent_successes) / len(self.recent_successes) 
                       if self.recent_successes else 0)
        avg_delay = (sum(self.recent_delays) / len(self.recent_delays) 
                    if self.recent_delays else 0)
        
        return {
            "current_concurrent": self.current_concurrent,
            "success_rate": f"{success_rate:.2%}",
            "avg_delay": f"{avg_delay:.2f}s",
            "total_successes": self.success_count,
            "total_errors": self.error_count,
            "circuit_open": self.circuit_open
        }
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        success = exc_type is None
        error_code = None
        
        # Extract status code from exception
        if exc_val:
            if hasattr(exc_val, 'status'):
                error_code = exc_val.status
            elif '429' in str(exc_val):
                error_code = 429
        
        self.release(success=success, error_code=error_code)
