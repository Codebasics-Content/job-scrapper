#!/usr/bin/env python3
# Indeed job description extractor - minimal implementation
# EMD Compliance: ≤80 lines

import logging
from typing import List
from selenium.webdriver.remote.webelement import WebElement

from .dom_utils import find_elements_safe, safe_text

logger = logging.getLogger(__name__)

def extract_job_description(card: WebElement) -> str:
    """Extract job description from Indeed card - minimalistic approach"""
    
    description_parts = []
    
    # Primary selectors for Indeed job descriptions
    selectors = [
        "[data-testid='job-snippet']",
        ".job-snippet",
        ".summary",
        ".jobSnippet"
    ]
    
    # Try each selector and collect text
    for selector in selectors:
        elements = find_elements_safe(card, selector)
        for element in elements:
            text = safe_text(element)
            if text and len(text.strip()) > 10:  # Only meaningful text
                description_parts.append(text.strip())
    
    # Join all description parts
    full_description = ' '.join(description_parts)
    
    # Log for debugging
    if full_description:
        logger.debug(f"Description extracted: {full_description[:100]}...")
    else:
        logger.warning("No job description found")
    
    return full_description.strip()

def get_combined_job_description(card: WebElement, title: str, 
                               company: str, location: str) -> str:
    """Create combined job description with basic info"""
    
    # Get core description
    description = extract_job_description(card)
    
    # Create combined description with context
    if description:
        combined = f"{title} at {company} - {location}. {description}"
    else:
        combined = f"{title} at {company} - {location}. No detailed description available."
    
    return combined.strip()

def format_description_for_skills(description: str, max_length: int = 500) -> str:
    """Format description for skill extraction - keep it concise"""
    
    if not description:
        return ""
    
    # Truncate if too long for skill processing
    if len(description) > max_length:
        truncated = description[:max_length].rsplit(' ', 1)[0]
        return f"{truncated}..."
    
    return description
