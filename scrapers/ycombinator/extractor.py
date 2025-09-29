#!/usr/bin/env python3
# YCombinator job data extractor
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
    """Extract job information from YCombinator company/job card"""
    
    try:
        # Extract company ID from data attribute or generate unique ID
        job_id_attr = card.get_attribute("data-company-id") or str(int(time.time()))
        job_id = job_id_attr if job_id_attr else f"yc_{int(time.time())}"
        
        # Extract company name (YC focuses on startups, so company is primary)
        company_el = _safe_find_element(card, ".company-name, .startup-name, h3, .name")
        company = _safe_text(company_el) or "YCombinator Startup"
        
        # Extract job title/role (often generic for startups)
        title_el = _safe_find_element(card, ".position, .role, .job-title")
        title = _safe_text(title_el) or job_role
        
        # Extract location
        location_el = _safe_find_element(card, ".location, .city, .headquarters")
        location = _safe_text(location_el) or "Remote/Various"
        
        # Extract experience/stage info
        exp_el = _safe_find_element(card, ".stage, .experience, .funding")
        experience = _safe_text(exp_el) or "Startup Stage"
        
        # Extract company description/job description
        description = get_job_description_from_card(card)
        full_jd = f"{title} at {company} (YCombinator) - {location}. {description}".strip()
        
        # Extract skills using existing skill extractor
        extracted_skills = extract_skills_from_description(description)
        skills_str = format_skills_as_string(extracted_skills, job_role)
        
        return JobModel(
            job_id=f"ycombinator_{job_id}",
            job_role=title,
            company=company,
            experience=experience,
            skills=skills_str,
            jd=full_jd,
            platform="ycombinator",
            location=location,
        )
        
    except Exception as e:
        logger.warning(f"Failed to extract job from YCombinator card: {str(e)}")
        return None

def get_job_description_from_card(card: WebElement) -> str:
    """Extract job/company description from YCombinator card"""
    
    description_parts = []
    description_selectors = [
        ".description",
        ".company-description", 
        ".about",
        ".summary",
        ".pitch",
        "p"
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
    logger.debug(f"YCombinator description extracted: {full_description[:100]}...")
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
