"""Parse job cards from Naukri search results page"""

import logging
from bs4 import Tag

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
    """Extract job URL from card - matches test_playwright_detail_pages.py approach"""
    # Primary: Extract from title link (2025 Naukri structure)
    title_elem = card.select_one(".title")
    if title_elem:
        href_val = title_elem.get("href")
        if href_val and isinstance(href_val, str):
            job_url = href_val if href_val.startswith("http") else f"https://www.naukri.com{href_val}"
            return job_url
    
    # Fallback: Try data-job-id attribute
    job_id = card.get("data-job-id")
    if job_id and isinstance(job_id, str):
        return f"https://www.naukri.com/job-listings-{job_id}"
    
    # Last resort: Try other title selectors
    for sel in ["a.title-text", "a[title]"]:
        elem = card.select_one(sel)
        if elem:
            href_val = elem.get("href")
            if href_val and isinstance(href_val, str):
                return href_val if href_val.startswith("http") else f"https://www.naukri.com{href_val}"
    
    logger.warning("Could not extract job URL from card")
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
