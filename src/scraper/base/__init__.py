# Base Scraper Module Exports - EMD-Compliant Architecture
# EMD Compliance: ≤80 lines for module organization and exports

from .base_scraper import BaseJobScraper
from .driver_pool import WebDriverPool
from .anti_detection import AntiDetectionDriverFactory

__all__ = [
    "BaseJobScraper",
    "WebDriverPool", 
    "AntiDetectionDriverFactory"
]

# Module version and metadata
__version__ = "1.0.0"
__author__ = "Job Scrapper Team"
__description__ = "EMD-compliant base scraper architecture with thread-safe WebDriver pools"

# Module configuration constants
DEFAULT_POOL_SIZE = 3
DEFAULT_MAX_WORKERS = 2
DEFAULT_DRIVER_TIMEOUT = 30

# Export configuration constants
__all__.extend([
    "DEFAULT_POOL_SIZE",
    "DEFAULT_MAX_WORKERS", 
    "DEFAULT_DRIVER_TIMEOUT"
])
