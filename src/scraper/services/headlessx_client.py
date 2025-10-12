"""Standard HeadlessX client using base architecture.

Provides a clean HeadlessX client that inherits from BaseHeadlessXClient.
Eliminates code duplication by leveraging existing base modules.
"""
from __future__ import annotations

import os
from typing import Optional
from types import TracebackType
import httpx

from .base import (
    BaseHeadlessXClient,
    RetryConfig, 
    CircuitBreakerConfig,
    HeadlessXError
)


class HeadlessXClient(BaseHeadlessXClient):
    """Standard HeadlessX client with base functionality"""
    
    def __init__(
        self,
        retry_config: Optional[RetryConfig] = None,
        circuit_config: Optional[CircuitBreakerConfig] = None,
        max_concurrent: int = 5,
        rate_limit_per_second: float = 2.0
    ):
        base_url = os.getenv("HEADLESSX_BASE_URL", "http://localhost:3000").rstrip("/")
        token = os.getenv("HEADLESSX_TOKEN", "test-token")
        if not base_url:
            raise HeadlessXError("HEADLESSX_BASE_URL is required")
        
        super().__init__(base_url, token, max_concurrent, retry_config, circuit_config)
    
    async def __aenter__(self):
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=5.0)
        
        self.client = httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            http2=True,
            follow_redirects=True
        )
        return self
    
    async def __aexit__(
        self, 
        exc_type: type[BaseException] | None, 
        exc_val: BaseException | None, 
        exc_tb: TracebackType | None
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)


# Backward compatibility - use the standard class
EnhancedHeadlessXClient = HeadlessXClient


# Backward compatibility function
async def render_url(
    url: str,
    *,
    proxy_url: str | None = None,
    profile: str | None = None,
    stealth_mode: str | None = None,
    timeout: float = 30.0,
) -> str:
    """Legacy function for backward compatibility"""
    async with HeadlessXClient() as client:
        return await client.render_url(
            url,
            proxy_url=proxy_url,
            profile=profile,
            stealth_mode=stealth_mode,
            timeout=timeout
        )
