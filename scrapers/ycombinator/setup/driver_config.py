#!/usr/bin/env python3
# YCombinator WebDriver configuration module
# EMD Compliance: ≤80 lines for driver setup

import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger(__name__)

class YCDriverConfig:
    """Configure and initialize Chrome WebDriver for YCombinator scraping"""
    
    def __init__(self, headless: bool = True, timeout: int = 10):
        self.headless = headless
        self.timeout = timeout
        self.driver: Optional[webdriver.Chrome] = None
    
    def create_chrome_options(self) -> Options:
        """Create optimized Chrome options for YCombinator"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        return chrome_options
    
    async def initialize_driver(self) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with optimized settings"""
        try:
            chrome_options = self.create_chrome_options()
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(self.timeout)
            
            logger.info("YCombinator scraper driver initialized successfully")
            return self.driver
            
        except WebDriverException as error:
            logger.error(f"Failed to initialize Chrome driver: {str(error)}")
            raise
    
    async def close_driver(self) -> None:
        """Clean up WebDriver resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("YCombinator scraper driver closed successfully")
            except Exception as error:
                logger.warning(f"Error closing YCombinator driver: {str(error)}")
            finally:
                self.driver = None
