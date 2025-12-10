"""Network response monitoring for LinkedIn scraping (≤80 lines EMD)"""
import logging
from collections import defaultdict
from playwright.async_api import Response

logger = logging.getLogger(__name__)

class NetworkMonitor:
    """Monitor network responses to detect rate limiting and blocking"""
    
    def __init__(self):
        self.response_codes: defaultdict[int, int] = defaultdict(int)
        self.failed_requests = 0
        self.total_requests = 0
        self.rate_limited = False
    
    async def handle_response(self, response: Response) -> None:
        """Track all network responses"""
        try:
            url = response.url
            status = response.status
            
            # Only track LinkedIn API/job requests
            if "linkedin.com" in url and ("jobs" in url or "voyager" in url):
                self.total_requests += 1
                self.response_codes[status] += 1
                
                # Detect rate limiting
                if status in [429, 403, 503]:
                    self.failed_requests += 1
                    self.rate_limited = True
                    logger.warning(f"⚠️  Rate limit detected: {status} - {url[:80]}")
                elif status != 200:
                    self.failed_requests += 1
                    logger.debug(f"Non-200 response: {status} - {url[:80]}")
        except Exception as e:
            logger.debug(f"Network monitor error: {e}")
    
    def get_status(self) -> dict[str, int | bool | float]:
        """Get current network status"""
        return {
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "rate_limited": self.rate_limited,
            "success_rate": (
                (self.total_requests - self.failed_requests) / self.total_requests * 100
                if self.total_requests > 0 else 100.0
            )
        }
    
    def print_summary(self) -> None:
        """Print network response summary"""
        if self.total_requests > 0:
            print(f"\n🌐 NETWORK SUMMARY:")
            print(f"   ├─ Total requests: {self.total_requests}")
            print(f"   ├─ Failed: {self.failed_requests}")
            for code, count in sorted(self.response_codes.items()):
                emoji = "✅" if code == 200 else "⚠️" if code < 500 else "❌"
                print(f"   ├─ {emoji} HTTP {code}: {count}")
            print(f"   └─ Success rate: {self.get_status()['success_rate']:.1f}%")
            
            if self.rate_limited:
                print(f"\n⚠️  WARNING: LinkedIn is rate limiting requests!")
                print(f"   Recommendation: Add delays or use proxy rotation")
