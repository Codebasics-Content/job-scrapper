# Refactored Base Job Scraper - Abstract Interface for Platform Scrapers

import logging
from abc import ABC, abstractmethod
from types import TracebackType
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import WebDriver
from models.job import JobModel
from .driver_pool import WebDriverPool
from .anti_detection import AntiDetectionDriverFactory

logger = logging.getLogger(__name__)

class BaseJobScraper(ABC):
    """
    Abstract base class for platform-specific job scrapers with EMD-compliant architecture
    """
    
    def __init__(self, platform_name: str, max_workers: int = 2, pool_size: int = 3):
        self.platform_name: str = platform_name
        self.max_workers: int = max_workers
        self.driver_pool: WebDriverPool = WebDriverPool(platform_name, pool_size)
        self.driver_factory: AntiDetectionDriverFactory = AntiDetectionDriverFactory()
        
    def setup_driver_pool(self) -> None:
        """Initialize WebDriver pool using anti-detection factory"""
        if not self.driver_pool.is_initialized:
            self.driver_pool.initialize_pool(self.driver_factory)
            logger.info(f"Driver pool setup completed for {self.platform_name}")
    
    def get_driver(self) -> uc.Chrome | None:
        """Get WebDriver from pool (thread-safe)"""
        return self.driver_pool.get_driver()
    
    def return_driver(self, driver: WebDriver) -> None:
        """Return WebDriver to pool (accepts any WebDriver subclass)"""
        self.driver_pool.return_driver(driver)
    
    def cleanup_pool(self) -> None:
        """Clean up WebDriver pool"""
        self.driver_pool.cleanup_pool()
        logger.info(f"Pool cleanup completed for {self.platform_name}")
    
    @property
    def pool_status(self) -> dict[str, str | bool | int]:
        """Get current pool status information"""
        return {
            "platform": self.platform_name,
            "initialized": self.driver_pool.is_initialized,
            "max_workers": self.max_workers
        }
    
    @abstractmethod
    async def scrape_jobs(
        self, 
        job_role: str, 
        target_count: int,
        location: str = ""
    ) -> list[JobModel]:
        """
        Abstract method to be implemented by each platform scraper
        
        Args:
            job_role: Job role to search for
            target_count: Number of jobs to scrape
            location: Location filter (empty for worldwide, configurable via Streamlit)
            
        Returns:
            List of validated JobModel instances
        """
        pass
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_driver_pool()
        return self
    
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        """Context manager exit with cleanup"""
        self.cleanup_pool()
        # Cleanup shared browser if this is the last scraper
        if len(WebDriverPool._platform_tabs) == 0:
            WebDriverPool.cleanup_shared_browser()
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.setup_driver_pool()
        return self
    
    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        """Async context manager exit with cleanup"""
        self.cleanup_pool()
        # Cleanup shared browser if this is the last scraper
        if len(WebDriverPool._platform_tabs) == 0:
            WebDriverPool.cleanup_shared_browser()
