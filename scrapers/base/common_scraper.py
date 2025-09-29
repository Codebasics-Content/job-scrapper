# Common HTTP Scraper Base - EMD Component
import logging
import requests

logger = logging.getLogger(__name__)

class CommonHTTPScraper:
    """Common base class for HTTP-based job scrapers with shared patterns."""
    
    def __init__(self, platform: str, base_url: str, location: str = "Remote"):
        self.platform: str = platform
        self.base_url: str = base_url
        self.location: str = location
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def build_params(self, job_role: str, page: int = 0) -> dict[str, str | int]:
        """Build query parameters for job search. Override in subclasses."""
        return {
            'q': job_role,
            'l': self.location,
            'start': page
        }
    
    def get_max_pages(self, target_count: int) -> int:
        """Calculate maximum pages to scrape based on target count."""
        return min(target_count, 1000) // 10
        
    async def make_request(self, params: dict[str, str | int]) -> requests.Response | None:
        """Make HTTP request with error handling."""
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response
            logger.warning(f"HTTP {response.status_code} for {self.platform}")
            return None
        except Exception as error:
            logger.error(f"{self.platform} request failed: {error}")
            return None
            
    def log_scraping_start(self, job_role: str, target_count: int) -> None:
        """Log scraping start message."""
        logger.info(f"Scraping {target_count} {job_role} jobs from {self.platform}")
        
    def log_scraping_complete(self, jobs_count: int) -> None:
        """Log scraping completion message."""
        logger.info(f"{self.platform} scraping completed: {jobs_count} jobs collected")
