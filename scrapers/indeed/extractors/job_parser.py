#!/usr/bin/env python3
# Indeed job data parser - minimalistic extraction
# EMD Compliance: ≤80 lines

import time
import logging
from typing import Optional
from selenium.webdriver.remote.webelement import WebElement

from .dom_utils import safe_find_element, safe_text, safe_attribute

logger = logging.getLogger(__name__)

def extract_job_id(card: WebElement) -> str:
    """Extract job ID from Indeed card"""
    job_id_attr = safe_attribute(card, "data-jk")
    if job_id_attr:
        return f"indeed_{job_id_attr}"
    return f"indeed_{int(time.time())}"

def extract_job_title(card: WebElement, fallback_role: str) -> str:
    """Extract job title from Indeed card"""
    selectors = [
        "[data-testid='job-title'] a",
        ".jobTitle a",
        "h2 a[data-jk]"
    ]
    
    for selector in selectors:
        title_el = safe_find_element(card, selector)
        title = safe_text(title_el)
        if title:
            return title
    
    return fallback_role

def extract_company_name(card: WebElement) -> str:
    """Extract company name from Indeed card"""
    selectors = [
        "[data-testid='company-name']",
        ".companyName",
        "span[title]"
    ]
    
    for selector in selectors:
        company_el = safe_find_element(card, selector)
        company = safe_text(company_el)
        if company:
            return company
    
    return "Unknown Company"

def extract_location(card: WebElement) -> str:
    """Extract location from Indeed card"""
    selectors = [
        "[data-testid='job-location']",
        ".companyLocation",
        "[data-testid='job-location'] div"
    ]
    
    for selector in selectors:
        location_el = safe_find_element(card, selector)
        location = safe_text(location_el)
        if location:
            return location
    
    return ""
