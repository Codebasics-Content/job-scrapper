#!/usr/bin/env python3
# LinkedIn infinite scroll handler
# EMD Compliance: ≤80 lines

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

def scroll_to_load_jobs(
    driver: WebDriver, 
    target_count: int,
    current_count: int
) -> bool:
    """Scroll page to trigger infinite loading
    
    Args:
        driver: Selenium WebDriver instance
        target_count: Total jobs needed
        current_count: Jobs already extracted
        
    Returns:
        True if more jobs loaded, False otherwise
    """
    try:
        # Get initial job count
        initial_cards = len(driver.find_elements(
            By.CSS_SELECTOR,
            "div.base-card[data-entity-urn]"
        ))
        
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for load
        
        # Check if new jobs loaded
        new_cards = len(driver.find_elements(
            By.CSS_SELECTOR,
            "div.base-card[data-entity-urn]"
        ))
        
        if new_cards > initial_cards:
            logger.info(f"Scroll loaded {new_cards - initial_cards} new jobs")
            return True
            
        # Check for "See More Jobs" button
        if current_count < target_count:
            return click_see_more_button(driver)
            
        return False
        
    except Exception as error:
        logger.error(f"Scroll failed: {error}")
        return False

def click_see_more_button(driver: WebDriver) -> bool:
    """Click 'See More Jobs' button if present
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        True if button clicked, False otherwise
    """
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "button.infinite-scroller__show-more-button"
            ))
        )
        
        button.click()
        logger.info("Clicked 'See More Jobs' button")
        time.sleep(3)  # Wait for jobs to load
        return True
        
    except (TimeoutException, NoSuchElementException):
        logger.debug("'See More Jobs' button not found")
        return False
