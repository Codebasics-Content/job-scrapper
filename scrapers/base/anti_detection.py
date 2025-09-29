# Anti-Detection Driver Factory - Chrome WebDriver Configuration
# EMD Compliance: ≤80 lines for anti-bot measures and driver creation

import undetected_chromedriver as uc
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

class AntiDetectionDriverFactory:
    """Factory for creating anti-detection Chrome WebDrivers with evasion techniques"""
    
    def __init__(self):
        self.user_agent: UserAgent = UserAgent()
        
    def create_driver(self) -> uc.Chrome | None:
        """Create configured Chrome WebDriver with comprehensive anti-bot measures"""
        try:
            options = self._configure_chrome_options()
            driver = uc.Chrome(options=options)
            self._apply_javascript_evasions(driver)
            
            logger.info("Anti-detection WebDriver created successfully")
            return driver
            
        except Exception as error:
            error_type = type(error).__name__
            logger.error(f"WebDriver creation failed - {error_type}: {error}")
            logger.debug(f"Failed at driver initialization stage")
            return None
    
    def _configure_chrome_options(self) -> uc.ChromeOptions:
        """Configure Chrome options for visible GUI mode with anti-detection"""
        options = uc.ChromeOptions()
        
        # Basic Chrome arguments for visible mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={self.user_agent.random}")
        
        # GUI mode configuration - browser stays visible
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        
        # Chrome preferences for popup handling
        options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        })
        
        return options
    
    def _apply_javascript_evasions(self, driver: uc.Chrome) -> None:
        """Apply JavaScript-based detection evasions"""
        # Remove webdriver property
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        # Override navigator properties
        driver.execute_script(
            "Object.defineProperty(navigator, 'languages', "
            "{get: () => ['en-US', 'en']})"
        )
        
        # Override permissions API
        driver.execute_script(
            "Object.defineProperty(navigator, 'permissions', "
            "{get: () => ({query: () => Promise.resolve({state: 'granted'})})})"
        )
        
        # Override plugins length
        driver.execute_script(
            "Object.defineProperty(navigator, 'plugins', "
            "{get: () => ({length: 3})})"
        )
        
        logger.debug("JavaScript evasions applied successfully")
