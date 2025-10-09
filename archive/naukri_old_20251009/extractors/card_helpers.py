#!/usr/bin/env python3
# Naukri card fallback helper methods
# EMD Compliance: ≤80 lines

import logging
from typing import Any
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)

def extract_card_company_info(job_card: WebElement) -> str:
    """Company details extraction removed - rely on API response only"""
    logger.info("[COMPANY INFO] Using API-only extraction - no fallback needed")
    return ""

def extract_card_skills(card: Any) -> str:
    """Skills extraction removed - rely on API response only"""
    logger.info("[SKILLS] Using API-only extraction - no fallback needed")
    return ""

def extract_card_experience(card: Any) -> str:
    """Extract experience from job card"""
    try:
        exp_selectors = [
            ".exp",
            ".experience", 
            "[data-experience]",
            ".yrs-exp"
        ]
        
        for selector in exp_selectors:
            try:
                exp_element = card.find_element(By.CSS_SELECTOR, selector)
                experience = exp_element.text.strip()
                if experience:
                    return experience
            except NoSuchElementException:
                continue
                
    except Exception as e:
        logger.debug(f"[CARD FALLBACK] Experience extraction failed: {e}")
        
    return ""

def extract_card_salary(card: Any) -> str:
    """Extract salary from job card"""
    try:
        salary_selectors = [
            ".sal",
            ".salary",
            "[data-salary]", 
            ".package"
        ]
        
        for selector in salary_selectors:
            try:
                salary_element = card.find_element(By.CSS_SELECTOR, selector)
                salary = salary_element.text.strip()
                if salary:
                    return salary
            except NoSuchElementException:
                continue
                
    except Exception as e:
        logger.debug(f"[CARD FALLBACK] Salary extraction failed: {e}")
        
    return ""
