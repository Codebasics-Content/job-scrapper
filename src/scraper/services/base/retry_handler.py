# Retry Handler Logic - EMD Architecture  
# Handles exponential backoff retry strategy for HeadlessX clients

import asyncio
import random
from typing import Optional

from .config import RetryConfig


class RetryHandler:
    """Retry handler with exponential backoff and jitter"""
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter"""
        delay = min(
            self.config.base_delay * (self.config.exponential_factor ** attempt),
            self.config.max_delay
        )
        
        if self.config.jitter:
            # Add ±25% jitter to prevent thundering herd
            jitter_range = delay * 0.25
            delay += random.uniform(-jitter_range, jitter_range)
        
        return max(0, delay)
    
    async def sleep_with_backoff(self, attempt: int) -> None:
        """Sleep with calculated exponential backoff delay"""
        delay = self.calculate_delay(attempt)
        await asyncio.sleep(delay)
