#!/usr/bin/env python3
# Indeed job data extractor
# EMD Compliance: ≤80 lines

import time
import logging
from typing import Optional
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from models.job import JobModel
from scrapers.base.skill_extractor import extract_skills_from_description, format_skills_as_string

logger = logging.getLogger(__name__)

def extract_job_from_card(card: WebElement, job_role: str) -> Optional[JobModel]:
    """Extract job information from Indeed job card"""
    
    try:
        # Extract job ID from data attribute or generate unique ID
        job_id_attr = card.get_attribute("data-jk") or str(int(time.time()))
        job_id = job_id_attr if job_id_attr else f"indeed_{int(time.time())}"
        
        # Extract job title
        title_el = _safe_find_element(card, "[data-testid='job-title'] a, .jobTitle a")
        title = _safe_text(title_el) or job_role
        
        # Extract company name
        company_el = _safe_find_element(card, "[data-testid='company-name'], .companyName")
        company = _safe_text(company_el) or "Unknown Company"
        
        # Extract location
        location_el = _safe_find_element(card, "[data-testid='job-location'], .companyLocation")
        location = _safe_text(location_el) or ""
        
        # Extract job description/snippet
        description = get_job_description_from_card(card)
        full_jd = f"{title} at {company} - {location}. {description}".strip()
        
        # Extract skills using existing skill extractor
        extracted_skills = extract_skills_from_description(description)
        skills_str = format_skills_as_string(extracted_skills, job_role)
        
        return JobModel(
            job_id=f"indeed_{job_id}",
            job_role=title,
            company=company,
            experience="Not specified",
            skills=skills_str,
            jd=full_jd,
            platform="indeed",
            location=location,
        )
        
    except Exception as e:
        logger.warning(f"Failed to extract job from Indeed card: {str(e)}")
        return None

def get_job_description_from_card(card: WebElement) -> str:
    """Extract job description snippet from Indeed job card"""
    
    description_parts = []
    description_selectors = [
        "[data-testid='job-snippet']",
        ".job-snippet",
        ".summary",
        ".jobSnippet"
    ]
    
    for selector in description_selectors:
        try:
            elements = card.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                text = element.text.strip()
                if text and len(text) > 10:
                    description_parts.append(text)
        except NoSuchElementException:
            continue
    
    full_description = ' '.join(description_parts)
    logger.debug(f"Indeed description extracted: {full_description[:100]}...")
    return full_description

def _safe_find_element(parent: WebElement, selector: str) -> Optional[WebElement]:
    """Safely find element using CSS selector"""
    try:
        return parent.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None

def _safe_text(element: Optional[WebElement]) -> str:
    """Safely extract text from element"""
    return element.text.strip() if element else ""
