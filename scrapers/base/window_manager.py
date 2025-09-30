#!/usr/bin/env python3
# Multi-Window Browser Manager for parallel scraping
# EMD Compliance: ≤80 lines

import logging
from typing import Callable
import undetected_chromedriver as uc

logger = logging.getLogger(__name__)

class WindowManager:
    """Manages separate browser windows for parallel scraping"""
    
    active_windows: dict[str, uc.Chrome]
    driver_factory: Callable[[], uc.Chrome | None]
    
    def __init__(self, driver_factory: Callable[[], uc.Chrome | None]):
        self.active_windows = {}
        self.driver_factory = driver_factory
        
    def create_window(self, window_id: str) -> uc.Chrome | None:
        """Create new browser window for specific country"""
        if window_id in self.active_windows:
            logger.warning(f"Window {window_id} already exists")
            return self.active_windows[window_id]
            
        driver = self.driver_factory()
        if driver:
            self.active_windows[window_id] = driver
            logger.info(f"Created browser window for {window_id}")
            return driver
        
        logger.error(f"Failed to create window for {window_id}")
        return None
    
    def get_window(self, window_id: str) -> uc.Chrome | None:
        """Get existing browser window"""
        return self.active_windows.get(window_id)
    
    def close_window(self, window_id: str) -> None:
        """Close specific browser window"""
        if window_id in self.active_windows:
            try:
                self.active_windows[window_id].quit()
                del self.active_windows[window_id]
                logger.info(f"Closed window {window_id}")
            except Exception as error:
                logger.error(f"Error closing window {window_id}: {error}")
    
    def close_all(self) -> None:
        """Close all browser windows"""
        for window_id in list(self.active_windows.keys()):
            self.close_window(window_id)
        
        logger.info("All browser windows closed")
    
    def window_count(self) -> int:
        """Get number of active windows"""
        return len(self.active_windows)
