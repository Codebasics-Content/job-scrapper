"""HeadlessX rendering methods with timeout handling - EMD Architecture"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx

from .circuit_breaker import HeadlessXError


async def render_single_url(
    client: httpx.AsyncClient,
    base_url: str,
    token: str,
    url: str,
    timeout: float,
    proxy_url: str | None = None,
    profile: str | None = None,
    stealth_mode: str | None = None
) -> str:
    """Render a single URL with timeout handling"""
    payload: dict[str, str | float] = {"url": url, "timeout": timeout}
    
    if proxy_url:
        payload["proxy_url"] = proxy_url
    if profile:
        payload["profile"] = profile
    if stealth_mode:
        payload["stealth_mode"] = stealth_mode
    
    # Browserless/chrome uses token as query parameter
    endpoint = f"{base_url}/content?token={token}"
    
    try:
        response = await client.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("html", "")
    except Exception as e:
        raise HeadlessXError(f"Render failed for {url}: {e}") from e


async def render_multiple_urls(
    client: httpx.AsyncClient,
    base_url: str,
    token: str,
    urls: list[str],
    timeout: float,
    semaphore: asyncio.Semaphore
) -> list[tuple[str, dict[str, str | bool]]]:
    """Render multiple URLs concurrently with error isolation"""
    
    async def render_with_isolation(url: str) -> tuple[str, dict[str, str | bool]]:
        """Render URL with error isolation"""
        async with semaphore:
            try:
                html = await render_single_url(
                    client, base_url, token, url, timeout
                )
                return (url, {"success": True, "html": html})
            except Exception as e:
                return (url, {"success": False, "error": str(e)})
    
    tasks = [render_with_isolation(url) for url in urls]
    return await asyncio.gather(*tasks)
