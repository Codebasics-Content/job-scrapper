#!/usr/bin/env python3
# LinkedIn job ID extractor from search results
# EMD Compliance: ≤80 lines

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)

def extract_job_ids_from_page(driver: WebDriver) -> list[str]:
    """Extract job IDs from LinkedIn search results page
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        List of job IDs
    """
    job_ids: list[str] = []
    
    try:
        # Wait for job cards to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.job-search-card"
            ))
        )
        
        # Find all job cards
        job_cards = driver.find_elements(
            By.CSS_SELECTOR,
            "div.base-card[data-entity-urn]"
        )
        
        logger.info(f"Found {len(job_cards)} job cards on page")
        
        for card in job_cards:
            try:
                # Extract job ID from data-entity-urn attribute
                # Format: "urn:li:jobPosting:4308073806"
                urn = card.get_attribute("data-entity-urn")
                
                if urn and "jobPosting:" in urn:
                    job_id = urn.split("jobPosting:")[-1]
                    job_ids.append(job_id)
                    logger.debug(f"Extracted job ID: {job_id}")
                    
            except Exception as error:
                logger.debug(f"Failed to extract job ID from card: {error}")
                continue
        
        logger.info(f"Successfully extracted {len(job_ids)} job IDs")
        return job_ids
        
    except Exception as error:
        logger.error(f"Failed to extract job IDs: {error}")
        return []
