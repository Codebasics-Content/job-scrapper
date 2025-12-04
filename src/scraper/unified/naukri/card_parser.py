"""Parse job cards from Naukri search results page"""

import logging
from bs4 import Tag
from .selectors import TITLE_SELECTORS_CSS

logger = logging.getLogger(__name__)


def extract_title_from_card(card: Tag) -> str:
    """Extract job title from card"""
    for sel in ["a.title", "a.title-text", "a[title]", ".title"]:
        elem = card.select_one(sel)
        if elem:
            title = elem.get_text(strip=True)
            if title:
                return title
    return ""


def extract_company_from_card(card: Tag) -> str:
    """Extract company name from card"""
    for sel in [".comp-name", ".companyInfo", "a.comp-name"]:
        elem = card.select_one(sel)
        if elem:
            company = elem.get_text(strip=True)
            if company:
                return company
    return ""


def extract_experience_from_card(card: Tag) -> str:
    """Extract experience requirement from card"""
    for sel in [".exp", ".experience", ".expwdth"]:
        elem = card.select_one(sel)
        if elem:
            exp = elem.get_text(strip=True)
            if exp:
                return exp
    return ""


def extract_location_from_card(card: Tag) -> str:
    """Extract location from card"""
    for sel in [".locWdth", ".location", ".loc"]:
        elem = card.select_one(sel)
        if elem:
            loc = elem.get_text(strip=True)
            if loc:
                return loc
    return ""


def extract_job_url_from_card(card: Tag) -> str | None:
    """Extract job URL from card using selectors from selectors.py (2025 Naukri)"""
    # First check for data-job-id on the card itself (most reliable)
    job_id = card.get("data-job-id")
    if job_id and isinstance(job_id, str):
        fallback_url = f"https://www.naukri.com/job-listings-{job_id}"
        logger.debug(f"✅ Using data-job-id: {fallback_url}")
        return fallback_url
    
    # Try to find link with href attribute
    for sel in TITLE_SELECTORS_CSS:
        elem = card.select_one(sel)
        if elem:
            href_val = elem.get("href")
            if href_val and isinstance(href_val, str):
                job_url = href_val if href_val.startswith("http") else f"https://www.naukri.com{href_val}"
                logger.debug(f"✅ Found URL with selector '{sel}': {job_url[:80]}")
                return job_url
    
    # If card is .cust-job-tuple, try parent for data-job-id
    parent = card.parent
    if parent:
        parent_job_id = parent.get("data-job-id")
        if parent_job_id and isinstance(parent_job_id, str):
            fallback_url = f"https://www.naukri.com/job-listings-{parent_job_id}"
            logger.debug(f"✅ Using parent data-job-id: {fallback_url}")
            return fallback_url
    
    logger.error(f"❌ URL extraction failed. Card: {card.get('class')}")
    return None


def parse_search_card(card: Tag) -> dict[str, str]:
    """Parse all metadata from a single job card"""
    return {
        "title": extract_title_from_card(card),
        "company": extract_company_from_card(card),
        "experience": extract_experience_from_card(card),
        "location": extract_location_from_card(card),
        "url": extract_job_url_from_card(card) or "",
    }
