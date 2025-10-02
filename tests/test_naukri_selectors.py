#!/usr/bin/env python3
"""Test script to find correct Naukri selectors"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def test_selectors():
    """Test various selectors to find job cards"""
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = uc.Chrome(options=options)
    
    try:
        url = "https://www.naukri.com/ai-engineer-jobs?k=AI+Engineer"
        print(f"Loading: {url}")
        driver.get(url)
        time.sleep(3)
        
        # Test various possible selectors
        selectors = [
            ("article.jobTuple", By.CSS_SELECTOR),
            (".jobTuple", By.CSS_SELECTOR),
            (".cust-job-tuple", By.CLASS_NAME),
            ("article[data-job-id]", By.CSS_SELECTOR),
            (".list > article", By.CSS_SELECTOR),
            (".jobTupleWrapper", By.CLASS_NAME),
            (".srp-jobtuple-wrapper", By.CLASS_NAME),  # Old selector
            ("div[data-testid='job-card']", By.CSS_SELECTOR),
            ("article", By.TAG_NAME)
        ]
        
        for selector, by_type in selectors:
            try:
                elements = driver.find_elements(by_type, selector)
                if elements:
                    print(f"✓ Found {len(elements)} elements with selector: {selector}")
                    # Check first element's classes
                    if elements[0].get_attribute("class"):
                        print(f"  Classes: {elements[0].get_attribute('class')}")
            except Exception as e:
                print(f"✗ Error with selector {selector}: {e}")
        
        # Check page source for hints
        if "jobTuple" in driver.page_source:
            print("\n'jobTuple' found in page source")
        if "srp-jobtuple" in driver.page_source:
            print("'srp-jobtuple' found in page source")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_selectors()
