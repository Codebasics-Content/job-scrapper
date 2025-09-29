#!/usr/bin/env python3
# Indeed job extractor - JobModel aligned extraction
# EMD Compliance: ≤80 lines

import logging
from selenium.webdriver.remote.webelement import WebElement

from models.job import JobModel
from .job_parser import extract_job_id, extract_job_title, extract_company_name, extract_location
from .description_extractor import get_combined_job_description, format_description_for_skills

logger = logging.getLogger(__name__)

def extract_job_from_card(card: WebElement, fallback_role: str = "AI Engineer") -> JobModel:
    """Extract complete job data from Indeed card element - JobModel aligned"""
    
    try:
        # Extract basic job information
        job_id = extract_job_id(card)
        job_role = extract_job_title(card, fallback_role)
        company = extract_company_name(card)
        location = extract_location(card)
        
        # Get combined description
        jd = get_combined_job_description(card, job_role, company, location)
        
        # Format for skill extraction (keep concise)
        formatted_jd = format_description_for_skills(jd, 400)
        
        # Create JobModel object with correct field mapping
        job_data = {
            'job_id': job_id,
            'job_role': job_role,        # Correct field name
            'company': company,
            'experience': "Not specified",  # Default for Indeed cards
            'skills': "",               # Empty string, will be populated by skill extraction
            'jd': formatted_jd,         # Correct field name for job description
            'platform': "Indeed",
            'location': location,
            'url': "",                  # Will be set by scraper
        }
        
        logger.debug(f"Extracted job: {job_role} at {company}")
        return JobModel(**job_data)
        
    except Exception as e:
        logger.error(f"Error extracting job from card: {e}")
        
        # Return minimal fallback job with JobModel schema
        fallback_data = {
            'job_id': f"indeed_fallback_{id(card)}",
            'job_role': fallback_role,
            'company': "Unknown Company",
            'experience': "Not specified",
            'skills': "",
            'jd': f"{fallback_role} position available.",
            'platform': "Indeed",
            'location': "",
            'url': "",
        }
        
        return JobModel(**fallback_data)

def extract_jobs_from_cards(cards: list, fallback_role: str = "AI Engineer") -> list:
    """Extract jobs from multiple Indeed cards"""
    
    jobs = []
    for card in cards:
        job = extract_job_from_card(card, fallback_role)
        if job:
            jobs.append(job)
    
    logger.info(f"Extracted {len(jobs)} jobs from {len(cards)} cards")
    return jobs
