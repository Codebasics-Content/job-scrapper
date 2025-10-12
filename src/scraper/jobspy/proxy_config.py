"""BrightData proxy configuration for LinkedIn scraping (≤80 lines EMD)"""
from __future__ import annotations

import os
from typing import Optional


def get_brightdata_proxy() -> Optional[str]:
    """
    Get BrightData proxy URL from environment
    
    Returns:
        Proxy URL in format: wss://brd-customer-{ID}-zone-{ZONE}:{PASS}@...
        or None if not configured
    """
    proxy_url = os.getenv("BRIGHTDATA_BROWSER_URL")
    
    if proxy_url and proxy_url.startswith("wss://brd-customer-"):
        return proxy_url
    
    return None


def get_proxy_for_platform(platform: str) -> Optional[list[str]]:
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
