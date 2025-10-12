"""Parse job cards from Indeed search results page"""

import logging
import re
from bs4 import Tag

logger = logging.getLogger(__name__)


def extract_title_from_card(card: Tag) -> str:
    """Extract job title from card"""
    for sel in [".jobTitle", "h2.jobTitle", "a[data-jk]"]:
        elem = card.select_one(sel)
        if elem:
            title = elem.get_text(strip=True)
            if title:
                return title
    return ""


def extract_company_from_card(card: Tag) -> str:
    """Extract company name from card"""
    for sel in [".companyName", "span.companyName", "[data-testid='company-name']"]:
        elem = card.select_one(sel)
        if elem:
            company = elem.get_text(strip=True)
            if company:
                return company
    return ""


def extract_location_from_card(card: Tag) -> str:
    """Extract location from card"""
    for sel in [".companyLocation", "div.companyLocation", "[data-testid='text-location']"]:
        elem = card.select_one(sel)
        if elem:
            loc = elem.get_text(strip=True)
            if loc:
                return loc
    return ""


def extract_job_url_from_card(card: Tag) -> str | None:
    """Extract job URL from card - build from job key"""
    # Try data-jk attribute (job key)
    job_key = card.get("data-jk")
    if job_key and isinstance(job_key, str):
        return f"https://www.indeed.com/viewjob?jk={job_key}"
    
    # Look for data-jk in child elements
    elem_with_jk = card.select_one("[data-jk]")
    if elem_with_jk:
        job_key = elem_with_jk.get("data-jk")
        if job_key and isinstance(job_key, str):
            return f"https://www.indeed.com/viewjob?jk={job_key}"
    
    # Extract from href
    for sel in [".jobTitle a", "h2.jobTitle a", "a[href*='jk=']"]:
        elem = card.select_one(sel)
        if elem:
            href = elem.get("href")
            if href and isinstance(href, str):
                match = re.search(r'jk=([a-f0-9]+)', href)
                if match:
                    return f"https://www.indeed.com/viewjob?jk={match.group(1)}"
    
    logger.warning("Could not extract job URL from Indeed card")
    return None


def parse_search_card(card: Tag) -> dict[str, str]:
    """Parse all metadata from a single job card"""
    return {
        "title": extract_title_from_card(card),
        "company": extract_company_from_card(card),
        "experience": "",  # Indeed doesn't show experience in cards
        "location": extract_location_from_card(card),
        "url": extract_job_url_from_card(card) or "",
    }
