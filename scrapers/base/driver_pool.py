# Tab-Based Browser Management - Single Browser with Multiple Tabs
# EMD Compliance: ≤80 lines for tab management

import logging
import threading
import time
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import WebDriver
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .anti_detection import AntiDetectionDriverFactory

logger = logging.getLogger(__name__)

class WebDriverPool:
    """Single browser instance with multiple tabs for different platforms"""
    
    # Shared browser instance across all platforms  
    _shared_browser: uc.Chrome | None = None
    _platform_tabs: dict[str, str] = {}  # platform_name -> window_handle
    _initialized: bool = False
    _creation_lock: threading.Lock = threading.Lock()
    
    def __init__(self, platform_name: str, pool_size: int = 1):
        self.platform_name: str = platform_name
        self.tab_handle: str | None = None
        
    def initialize_pool(self, driver_factory: 'AntiDetectionDriverFactory') -> None:
        """Initialize shared browser and create tab for platform (thread-safe)"""
        with WebDriverPool._creation_lock:
            # Check if tab already exists
            if self.platform_name in WebDriverPool._platform_tabs:
                self.tab_handle = WebDriverPool._platform_tabs[self.platform_name]
                logger.info(f"Using existing tab for {self.platform_name}")
                return
            
            # Create shared browser if not exists
            if WebDriverPool._shared_browser is None:
                logger.info("Creating shared browser instance")
                WebDriverPool._shared_browser = driver_factory.create_driver()
                if WebDriverPool._shared_browser is None:
                    raise RuntimeError("Failed to create shared browser")
            
            # Create new tab for this platform with anti-bot delay
            browser = WebDriverPool._shared_browser
            time.sleep(0.5)  # Anti-bot delay before tab creation
            browser.execute_script("window.open('about:blank', '_blank');")
            time.sleep(0.3)  # Anti-bot delay after tab creation
            
            # Switch to the newly created tab
            all_handles = browser.window_handles
            browser.switch_to.window(all_handles[-1])
            
            self.tab_handle = browser.current_window_handle
            WebDriverPool._platform_tabs[self.platform_name] = self.tab_handle
            WebDriverPool._initialized = True
            
            logger.info(f"Tab created for {self.platform_name} (Handle: {self.tab_handle[:8]}..., Total tabs: {len(all_handles)})")
    
    def get_driver(self) -> uc.Chrome | None:
        """Get shared browser and switch to platform's tab with anti-bot delay"""
        if WebDriverPool._shared_browser is None or self.tab_handle is None:
            return None
        
        time.sleep(0.5)  # Anti-bot delay before tab switch
        WebDriverPool._shared_browser.switch_to.window(self.tab_handle)
        return WebDriverPool._shared_browser
    
    def return_driver(self, driver: WebDriver | None) -> None:
        """No-op for tab-based system (driver stays alive, accepts any WebDriver)"""
        if driver:
            logger.debug(f"Driver returned for {self.platform_name} (tab remains active)")
    
    def cleanup_pool(self) -> None:
        """Close platform's tab"""
        if WebDriverPool._shared_browser and self.tab_handle:
            try:
                WebDriverPool._shared_browser.switch_to.window(self.tab_handle)
                WebDriverPool._shared_browser.close()
                removed_handle = WebDriverPool._platform_tabs.pop(self.platform_name, None)
                logger.info(f"Tab closed for {self.platform_name} (handle: {removed_handle})")
            except Exception as e:
                logger.warning(f"Error closing tab for {self.platform_name}: {e}")
    
    @classmethod
    def cleanup_shared_browser(cls) -> None:
        """Cleanup shared browser instance completely"""
        if cls._shared_browser:
            try:
                cls._shared_browser.quit()
                logger.info("Shared browser closed successfully")
            except Exception as e:
                logger.warning(f"Error closing shared browser: {e}")
            finally:
                cls._shared_browser = None
                cls._platform_tabs.clear()
                cls._initialized = False
    
    @property
    def is_initialized(self) -> bool:
        """Check if tab is initialized"""
        return self.platform_name in WebDriverPool._platform_tabs
