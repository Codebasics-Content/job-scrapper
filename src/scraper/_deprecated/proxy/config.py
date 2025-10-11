"""BrightData Proxy configuration for job scraping.

This module provides a lightweight proxy system using BrightData's proxy network
instead of their Scraping Browser. Benefits:
- Much faster than Scraping Browser (direct HTTP vs CDP)
- Rotating residential/datacenter/ISP/mobile IPs
- Session management with sticky IPs
- Automatic geo-targeting and retry logic

BrightData Proxy Format:
  http://brd-customer-{customer_id}-zone-{zone_name}:{password}@brd.superproxy.io:22225
  
For sessions (sticky IP):
  http://brd-customer-{customer_id}-zone-{zone_name}-session-{session_id}:{password}@brd.superproxy.io:22225
"""

import random
import uuid
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import urlparse
import httpx
import os


@dataclass
class BrightDataProxy:
    """BrightData proxy configuration."""
    customer_id: str
    zone_name: str
    password: str
    host: str = "brd.superproxy.io"
    port: int = 22225
    protocol: str = "http"
    session_id: Optional[str] = None  # For sticky sessions
    country: Optional[str] = None  # For geo-targeting (e.g., 'us', 'in')
    
    @property
    def username(self) -> str:
        """Generate BrightData username with zone and optional parameters.
        
        Format: brd-customer-{customer_id}-zone-{zone_name}[-session-{session_id}][-country-{country}]
        """
        parts = [f"brd-customer-{self.customer_id}", f"zone-{self.zone_name}"]
        
        if self.session_id:
            parts.append(f"session-{self.session_id}")
        
        if self.country:
            parts.append(f"country-{self.country}")
        
        return "-".join(parts)
    
    @property
    def url(self) -> str:
        """Generate full proxy URL."""
        return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
    
    @property
    def auth_dict(self) -> dict:
        """Return proxy dict for httpx/requests."""
        return {
            "http://": self.url,
            "https://": self.url
        }
    
    def with_session(self, session_id: Optional[str] = None) -> "BrightDataProxy":
        """Create a new proxy instance with sticky session.
        
        Args:
            session_id: Session ID for sticky IP. If None, generates random UUID.
        
        Returns:
            New BrightDataProxy instance with session enabled
        """
        return BrightDataProxy(
            customer_id=self.customer_id,
            zone_name=self.zone_name,
            password=self.password,
            host=self.host,
            port=self.port,
            protocol=self.protocol,
            session_id=session_id or str(uuid.uuid4()),
            country=self.country
        )
    
    def with_country(self, country_code: str) -> "BrightDataProxy":
        """Create a new proxy instance with geo-targeting.
        
        Args:
            country_code: Two-letter country code (e.g., 'us', 'in', 'uk')
        
        Returns:
            New BrightDataProxy instance with country targeting
        """
        return BrightDataProxy(
            customer_id=self.customer_id,
            zone_name=self.zone_name,
            password=self.password,
            host=self.host,
            port=self.port,
            protocol=self.protocol,
            session_id=self.session_id,
            country=country_code.lower()
        )
    
    @classmethod
    def from_env(cls) -> "BrightDataProxy":
        """Create BrightData proxy from environment variables.
        
        Supports two methods:
        
        Method 1: Direct proxy credentials (Recommended)
            BRIGHTDATA_CUSTOMER_ID: Your customer ID
            BRIGHTDATA_ZONE: Zone name (e.g., 'residential', 'datacenter')
            BRIGHTDATA_PASSWORD: Zone password
        
        Method 2: Extract from Browser URL (Auto-detect)
            BRIGHTDATA_BROWSER_URL: wss://brd-customer-hl_xxx-zone-xxx:password@...
            
        Optional:
            BRIGHTDATA_PROXY_HOST: Proxy host (default: brd.superproxy.io)
            BRIGHTDATA_PROXY_PORT: Proxy port (default: 22225)
        """
        # Try Method 1: Direct credentials
        customer_id = os.getenv("BRIGHTDATA_CUSTOMER_ID")
        zone_name = os.getenv("BRIGHTDATA_ZONE")
        password = os.getenv("BRIGHTDATA_PASSWORD")
        
        # Method 2: Extract from Browser URL if direct credentials not available
        if not all([customer_id, zone_name, password]):
            browser_url = os.getenv("BRIGHTDATA_BROWSER_URL")
            
            if not browser_url:
                raise ValueError(
                    "Missing BrightData credentials. Provide either:\n"
                    "  Method 1: BRIGHTDATA_CUSTOMER_ID, BRIGHTDATA_ZONE, BRIGHTDATA_PASSWORD\n"
                    "  Method 2: BRIGHTDATA_BROWSER_URL (will auto-extract credentials)"
                )
            
            # Parse Browser URL: wss://brd-customer-hl_xxx-zone-xxx:password@host:port
            import re
            match = re.search(
                r'brd-customer-(\w+)-zone-([^:]+):(\w+)@',
                browser_url
            )
            
            if not match:
                raise ValueError(
                    f"Could not parse BrightData credentials from BRIGHTDATA_BROWSER_URL.\n"
                    f"Expected format: wss://brd-customer-{{id}}-zone-{{name}}:{{password}}@host:port\n"
                    f"Got: {browser_url[:50]}..."
                )
            
            customer_id, zone_name, password = match.groups()
            
            # Convert scraping_browser zone to residential for proxy use
            # Scraping Browser uses special zones, we'll use the base customer account
            if "scraping_browser" in zone_name:
                zone_name = "residential"  # Default to residential proxies
                print(f"ℹ️  Extracted credentials from Browser URL, using 'residential' zone for proxies")
            
            print(f"✅ Auto-detected BrightData credentials from BRIGHTDATA_BROWSER_URL")
            print(f"   Customer ID: {customer_id}")
            print(f"   Zone: {zone_name}")
        
        return cls(
            customer_id=customer_id,
            zone_name=zone_name,
            password=password,
            host=os.getenv("BRIGHTDATA_PROXY_HOST", "brd.superproxy.io"),
            port=int(os.getenv("BRIGHTDATA_PROXY_PORT", "22225"))
        )


@dataclass
class ProxyConfig:
    """Generic proxy configuration (for non-BrightData proxies)."""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"
    
    @property
    def url(self) -> str:
        """Generate proxy URL in format: http://username:password@host:port"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    @property
    def auth_dict(self) -> dict:
        """Return proxy dict for httpx/requests."""
        return {
            "http://": self.url,
            "https://": self.url
        }


class ProxyPool:
    """Manages a pool of rotating proxies for web scraping."""
    
    def __init__(self, proxies: List[ProxyConfig], max_retries: int = 3):
        """Initialize proxy pool.
        
        Args:
            proxies: List of ProxyConfig objects
            max_retries: Maximum number of proxies to try before giving up
        """
        self.proxies = proxies
        self.max_retries = max_retries
        self.current_index = 0
        self._failed_proxies = set()
    
    def get_next_proxy(self) -> Optional[ProxyConfig]:
        """Get next available proxy from pool using round-robin."""
        if not self.proxies:
            return None
        
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            
            if proxy.url not in self._failed_proxies:
                return proxy
            
            attempts += 1
        
        return None  # All proxies failed
    
    def mark_failed(self, proxy: ProxyConfig):
        """Mark a proxy as failed (temporarily)."""
        self._failed_proxies.add(proxy.url)
    
    def reset_failures(self):
        """Reset all failed proxy markers."""
        self._failed_proxies.clear()
    
    @classmethod
    def from_env(cls, proxy_list_str: str) -> "ProxyPool":
        """Create ProxyPool from environment variable string.
        
        Format: host1:port1:user1:pass1,host2:port2:user2:pass2
        Or simple: host1:port1,host2:port2
        
        Example:
            PROXY_LIST=proxy1.com:8080:user1:pass1,proxy2.com:8080:user2:pass2
        """
        proxies = []
        
        for proxy_str in proxy_list_str.split(","):
            parts = proxy_str.strip().split(":")
            
            if len(parts) == 2:
                # Simple format: host:port
                host, port = parts
                proxies.append(ProxyConfig(host=host, port=int(port)))
            
            elif len(parts) == 4:
                # Auth format: host:port:user:pass
                host, port, user, password = parts
                proxies.append(ProxyConfig(
                    host=host,
                    port=int(port),
                    username=user,
                    password=password
                ))
        
        return cls(proxies)


class ProxySession:
    """HTTP client with automatic proxy rotation and retry logic."""
    
    def __init__(
        self,
        proxy_pool: Optional[ProxyPool] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize proxy session.
        
        Args:
            proxy_pool: ProxyPool instance, None for no proxy
            timeout: Request timeout in seconds
            max_retries: Max retry attempts per request
        """
        self.proxy_pool = proxy_pool
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None
        self._current_proxy: Optional[ProxyConfig] = None
    
    async def get(self, url: str, proxies: dict = None, **kwargs) -> httpx.Response:
        """Perform GET request with automatic proxy rotation on failure.
        
        Args:
            url: Target URL
            proxies: Dict with proxy URLs (e.g., from BrightDataProxy.auth_dict)
            **kwargs: Additional arguments passed to httpx.get()
        
        Returns:
            httpx.Response object
        
        Raises:
            httpx.HTTPError: If all retry attempts fail
        """
        for attempt in range(self.max_retries):
            try:
                # Get next proxy if available from pool
                if self.proxy_pool:
                    self._current_proxy = self.proxy_pool.get_next_proxy()
                    if not self._current_proxy:
                        raise RuntimeError("No available proxies in pool")
                
                # Create client with proxy
                client_kwargs = {
                    "timeout": self.timeout,
                    "follow_redirects": True,
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                }
                
                # Use proxies from parameter or from pool
                # httpx uses 'proxy' parameter with the proxy URL string
                if proxies:
                    # proxies dict has format {"http://": url, "https://": url}
                    # httpx wants just the URL for both protocols
                    proxy_url = proxies.get("https://") or proxies.get("http://")
                    if proxy_url:
                        client_kwargs["proxy"] = proxy_url
                elif self._current_proxy:
                    client_kwargs["proxy"] = self._current_proxy.url
                
                async with httpx.AsyncClient(**client_kwargs) as client:
                    response = await client.get(url, **kwargs)
                    response.raise_for_status()
                    return response
            
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                print(f"⚠️  Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                
                # Mark proxy as failed if used
                if self._current_proxy and self.proxy_pool:
                    self.proxy_pool.mark_failed(self._current_proxy)
                
                # Retry with next proxy
                if attempt < self.max_retries - 1:
                    continue
                else:
                    raise
    
    async def post(self, url: str, proxies: dict = None, **kwargs) -> httpx.Response:
        """Perform POST request with automatic proxy rotation on failure.
        
        Args:
            url: Target URL
            proxies: Dict with proxy URLs (e.g., from BrightDataProxy.auth_dict)
            **kwargs: Additional arguments passed to httpx.post()
        """
        for attempt in range(self.max_retries):
            try:
                if self.proxy_pool:
                    self._current_proxy = self.proxy_pool.get_next_proxy()
                    if not self._current_proxy:
                        raise RuntimeError("No available proxies in pool")
                
                client_kwargs = {
                    "timeout": self.timeout,
                    "follow_redirects": True,
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                }
                
                # Use proxies from parameter or from pool
                # httpx uses 'proxy' parameter with the proxy URL string
                if proxies:
                    # proxies dict has format {"http://": url, "https://": url}
                    # httpx wants just the URL for both protocols
                    proxy_url = proxies.get("https://") or proxies.get("http://")
                    if proxy_url:
                        client_kwargs["proxy"] = proxy_url
                elif self._current_proxy:
                    client_kwargs["proxy"] = self._current_proxy.url
                
                async with httpx.AsyncClient(**client_kwargs) as client:
                    response = await client.post(url, **kwargs)
                    response.raise_for_status()
                    return response
            
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                print(f"⚠️  Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                
                if self._current_proxy and self.proxy_pool:
                    self.proxy_pool.mark_failed(self._current_proxy)
                
                if attempt < self.max_retries - 1:
                    continue
                else:
                    raise


# Example usage and testing functions
async def test_proxy_config():
    """Test proxy configuration with a sample request."""
    # Example: Using free proxy for testing
    proxy = ProxyConfig(
        host="proxy.example.com",
        port=8080,
        username="user",
        password="pass"
    )
    
    print(f"Proxy URL: {proxy.url}")
    print(f"Proxy Dict: {proxy.auth_dict}")


async def test_proxy_session():
    """Test proxy session with actual request."""
    # Example without proxy (direct connection)
    session = ProxySession()
    
    try:
        response = await session.get("https://httpbin.org/ip")
        print(f"Response: {response.status_code}")
        print(f"IP: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import asyncio
    
    print("Testing Proxy Configuration...")
    asyncio.run(test_proxy_config())
    
    print("\nTesting Proxy Session...")
    asyncio.run(test_proxy_session())
