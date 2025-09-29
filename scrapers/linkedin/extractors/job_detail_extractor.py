#!/usr/bin/env python3
# LinkedIn job detail page extraction
# EMD Compliance: ≤80 lines

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

# Job description selectors (with fallbacks)
JD_SELECTORS: list[str] = [
    "div.description__text",
    "div.show-more-less-html__markup",
    "div.jobs-description__content",
    "div.job-details",
    "article.jobs-description"
]

def extract_job_description(driver: WebDriver) -> str:
    """Extract full job description from LinkedIn job detail page
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        Job description text or empty string
    """
    try:
        # Click "Show more" button if exists
        try:
            show_more = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "button.show-more-less-html__button--more"
                ))
            )
            show_more.click()
            logger.debug("Clicked 'Show more' button")
        except (TimeoutException, NoSuchElementException):
            logger.debug("No 'Show more' button found")
        
        # Try multiple selectors for job description
        for selector in JD_SELECTORS:
            try:
                jd_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                jd_text = jd_element.text.strip()
                if jd_text and len(jd_text) > 50:  # Minimum length check
                    logger.info(f"Extracted JD: {len(jd_text)} chars using {selector}")
                    return jd_text
            except (TimeoutException, NoSuchElementException):
                continue
        
        logger.warning("Could not extract job description with any selector")
        return ""
        
    except Exception as error:
        logger.error(f"Job description extraction failed: {error}")
        return ""


def extract_criteria_items(driver: WebDriver) -> dict[str, str]:
    """Extract job criteria like experience, employment type, etc.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        Dictionary of criteria items
    """
    criteria: dict[str, str] = {}
    
    try:
        criteria_items = driver.find_elements(
            By.CSS_SELECTOR,
            "li.jobs-unified-top-card__job-insight"
        )
        
        for item in criteria_items:
            try:
                text = item.text.strip()
                if text:
                    parts = text.split("\n")
                    if len(parts) >= 2:
                        key = parts[0].lower().replace(" ", "_")
                        criteria[key] = parts[1]
            except Exception:
                continue
                
    except Exception as error:
        logger.debug(f"Could not extract criteria: {error}")
    
    return criteria
