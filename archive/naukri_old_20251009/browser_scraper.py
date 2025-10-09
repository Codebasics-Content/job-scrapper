#!/usr/bin/env python3
# Backward compatibility wrapper for refactored browser scraper
# EMD Compliance: ≤80 lines

# Re-export main classes for backward compatibility
from .browser_scraper_main import NaukriBrowserScraper
from .types import (
    CompanyDetail,
    BulkJobData, 
    JobCardHTML,
    ScrapingMetrics,
    BatchConfig
)
from .browser_manager import BrowserManager, NaukriBrowserManager
from .batch_processor import BatchProcessor

# Make imports available at module level
__all__ = [
    'NaukriBrowserScraper',
    'CompanyDetail', 
    'BulkJobData',
    'JobCardHTML',
    'ScrapingMetrics',
    'BatchConfig',
    'BrowserManager',
    'NaukriBrowserManager',
    'BatchProcessor'
]
