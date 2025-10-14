"""BrightData Proxy configuration for LinkedIn scraping.

Provides BrightData proxy classes for LinkedIn rate-limit avoidance.
Used by JobSpy for LinkedIn scraping with rotating residential IPs.

Note: This module is deprecated. Use JobSpy's built-in proxy support.
      Kept for reference and manual LinkedIn proxy configuration.
"""

from .config import BrightDataProxy, ProxyConfig, ProxyPool, ProxySession

__all__ = [
    "BrightDataProxy",
    "ProxyConfig",
    "ProxyPool",
    "ProxySession",
]
