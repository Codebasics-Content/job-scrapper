# Base HeadlessX Client - EMD Architecture
# Common functionality shared by HeadlessX clients

import asyncio
from typing import Optional
from types import TracebackType
import httpx

from .config import RetryConfig, CircuitBreakerConfig
from .circuit_breaker import CircuitBreaker, HeadlessXError
from .retry_handler import RetryHandler
from .render_methods import render_multiple_urls


class BaseHeadlessXClient:
    """Base client with common HeadlessX functionality"""
    
    def __init__(
        self,
        base_url: str,
        token: str,
        max_concurrent: int = 5,
        retry_config: Optional[RetryConfig] = None,
        circuit_config: Optional[CircuitBreakerConfig] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.token = token
        
        # Initialize components
        self.circuit_breaker = CircuitBreaker(circuit_config)
        self.retry_handler = RetryHandler(retry_config)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # HTTP client will be initialized in derived classes
        self.client: Optional[httpx.AsyncClient] = None
    
    def get_token(self) -> str:
        """Get authentication token for HeadlessX API"""
        return self.token
    
    async def make_request_with_retry(
        self,
        method: str,
        url: str,
        json: dict[str, str | float] | None = None,
        headers: dict[str, str] | None = None
    ) -> httpx.Response:
        """Make HTTP request with circuit breaker and retry logic"""
        if not self.client:
            raise HeadlessXError("HTTP client not initialized")
        
        async with self.semaphore:
            self.circuit_breaker.check_state()
            
            for attempt in range(self.retry_handler.config.max_attempts):
                try:
                    response = await self.client.request(
                        method, url, json=json, headers=headers
                    )
                    self.circuit_breaker.record_success()
                    return response
                    
                except Exception as e:
                    self.circuit_breaker.record_failure()
                    
                    if attempt == self.retry_handler.config.max_attempts - 1:
                        raise HeadlessXError(f"Request failed after retries: {e}") from e
                    
                    await self.retry_handler.sleep_with_backoff(attempt)
            
            # This should never be reached due to the raise above
            raise HeadlessXError("Unexpected retry loop completion")
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        """Async context manager exit with cleanup"""
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
        """Render single URL with retry and circuit breaker"""
        # Browserless/chrome uses token as query parameter
        endpoint = f"{self.base_url}/content?token={self.get_token()}"
        response = await self.make_request_with_retry(
            "POST",
            endpoint,
            json={"url": url},
            headers={"Content-Type": "application/json"}
        )
        # Browserless returns HTML directly as text, not JSON
        return response.text
    
    async def render_urls_concurrent(
        self,
        urls: list[str],
        timeout: float = 30.0
    ) -> list[tuple[str, dict[str, str | bool]]]:
        """Render multiple URLs concurrently"""
        if not self.client:
            raise HeadlessXError("Client not initialized")
        return await render_multiple_urls(
            self.client,
            self.base_url,
            self.get_token(),
            urls,
            timeout,
            self.semaphore
        )
