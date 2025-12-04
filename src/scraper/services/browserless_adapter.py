"""Browserless.io API Adapter - EMD compliant
Adapts browserless/chrome Docker API to our HeadlessX interface
"""
from __future__ import annotations

import os
from typing import Optional
from types import TracebackType
import httpx

from .base import BaseHeadlessXClient, RetryConfig, CircuitBreakerConfig, HeadlessXError


class BrowserlessAdapter(BaseHeadlessXClient):
    """Adapter for browserless/chrome container API"""
    
    def __init__(
        self,
        retry_config: Optional[RetryConfig] = None,
        circuit_config: Optional[CircuitBreakerConfig] = None,
        max_concurrent: int = 5
    ):
        base_url = os.getenv("HEADLESSX_BASE_URL", "http://localhost:3000").rstrip("/")
        token = os.getenv("HEADLESSX_TOKEN", "test-token")
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
        if self.client:
            await self.client.aclose()
    
    async def render_url(
        self,
        url: str,
        proxy_url: str | None = None,
        profile: str | None = None,
        stealth_mode: str | None = None,
        timeout: float = 30.0
    ) -> str:
        """Render URL using browserless /content API"""
        # Note: proxy_url, profile, stealth_mode, timeout are accepted for API compatibility
        # but browserless uses a simpler payload format
        response = await self.make_request_with_retry(
            "POST",
            f"{self.base_url}/content",
            json={"url": url, "waitFor": "networkidle"}
        )

        if response.status_code != 200:
            raise HeadlessXError(f"Browserless API error: {response.status_code}")

        return response.text
