# EMD-Compliant Base Job Scraper - Import from Modular Components
# EMD Architecture: Original file replaced with imports from base/ module

# Import all components from the EMD-compliant base module
from .base import (
    BaseJobScraper,
    WebDriverPool,
    AntiDetectionDriverFactory,
    DEFAULT_POOL_SIZE,
    DEFAULT_MAX_WORKERS,
    DEFAULT_DRIVER_TIMEOUT
)

# Re-export for backwards compatibility
__all__ = [
    "BaseJobScraper",
    "WebDriverPool", 
    "AntiDetectionDriverFactory",
    "DEFAULT_POOL_SIZE",
    "DEFAULT_MAX_WORKERS",
    "DEFAULT_DRIVER_TIMEOUT"
]

# Legacy compatibility - maintain original interface
BaseJobScraper = BaseJobScraper
