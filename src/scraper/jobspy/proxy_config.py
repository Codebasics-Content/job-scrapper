"""BrightData proxy configuration for LinkedIn scraping (≤80 lines EMD)"""
from __future__ import annotations

import os
import logging

logger = logging.getLogger(__name__)


def get_brightdata_proxy() -> str | None:
    """
    Get BrightData proxy for JobSpy (converts wss:// to http:// format)
    
    Handles both formats:
    1. wss://brd-customer-hl_xxx-zone-scraping_browser2:pass@brd.superproxy.io:9222
    2. http://brd-customer-hl_xxx-zone-residential:pass@brd.superproxy.io:22225
    
    Returns:
        Proxy in format: user:pass@host:port (NO http:// prefix)
        or None if not configured
    """
    proxy_url = os.getenv("PROXY_URL")
    if not proxy_url:
        logger.debug("PROXY_URL environment variable not set")
        return None
    
    logger.info(f"Raw PROXY_URL: {proxy_url[:50]}...")
    
    # Handle WebSocket format (convert to HTTP proxy)
    if proxy_url.startswith("wss://"):
        # Extract: wss://username:password@host:port
        proxy_url = proxy_url.replace("wss://", "")
        
        # Replace scraping_browser zone with residential (or use BRIGHTDATA_ZONE)
        zone = os.getenv("BRIGHTDATA_ZONE", "residential")
        proxy_url = proxy_url.replace("-zone-scraping_browser1", f"-zone-{zone}")
        proxy_url = proxy_url.replace("-zone-scraping_browser2", f"-zone-{zone}")
        
        # Replace CDP port 9222 with proxy port 22225
        proxy_url = proxy_url.replace(":9222", ":22225")
        
        return proxy_url
    
    # Handle HTTP format (remove http:// prefix)
    if proxy_url.startswith("http://") or proxy_url.startswith("https://"):
        return proxy_url.replace("http://", "").replace("https://", "")
    
    # Already in correct format
    return proxy_url


def get_proxy_for_platform(platform: str) -> list[str] | None:
    """
    Get proxy list based on platform requirements
    
    Args:
        platform: Platform name (linkedin, indeed, naukri, etc.)
    
    Returns:
        List of proxy URLs for platforms that need it, None otherwise
    """
    # Only LinkedIn needs proxies due to aggressive rate limiting
    if platform.lower() == "linkedin":
        proxy = get_brightdata_proxy()
        return [proxy] if proxy else None
    
    # Indeed, Naukri, ZipRecruiter work fine without proxies
    return None


def proxy_status() -> dict[str, bool]:
    """Check proxy availability for supported platforms (linkedin, indeed, naukri)"""
    brightdata = get_brightdata_proxy()
    
    return {
        "linkedin": brightdata is not None,  # Proxy for rate limits
        "indeed": False,  # Direct scraping (unlimited)
        "naukri": False,  # Direct scraping (unlimited + native skills)
        "brightdata_configured": brightdata is not None,
    }
