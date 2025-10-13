"""Indeed job data parsing logic"""

import re
from datetime import datetime
from bs4 import BeautifulSoup

from src.models import JobDetailModel
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
from .selectors import DESC_SELECTORS_CSS


def extract_job_id(url: str) -> str:
    """Extract job ID from Indeed URL"""
    m = re.search(r"jk=([A-Za-z0-9]+)", url)
    return f"indeed_{m.group(1)}" if m else url


def extract_description(soup: BeautifulSoup) -> str:
    """Extract job description from detail page HTML"""
    # Primary selector for Indeed detail pages
    desc_div = soup.select_one("div#jobDescriptionText")
    if desc_div:
        return desc_div.get_text(" ", strip=True)
    
    # Fallback selectors
    for sel in DESC_SELECTORS_CSS:
        node = soup.select_one(sel)
        if node:
            text = node.get_text(" ", strip=True)
            if text and len(text) > 100:
                return text
    
    return ""


def create_job_detail_model(
    job_id: str,
    platform: str,
    actual_role: str,
    url: str,
    html: str
) -> JobDetailModel | None:
    """Parse HTML and create JobDetailModel for two-table architecture"""
    soup = BeautifulSoup(html, "html.parser")
    desc = extract_description(soup)
    
    if not desc:
        return None
    
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    skills_list = extractor.extract(desc)
    skills_str = ", ".join(skills_list) if skills_list else ""
    
    return JobDetailModel(
        job_id=job_id,
        platform=platform,
        actual_role=actual_role,
        url=url,
        job_description=desc,
        skills=skills_str,
        company_name="",
        company_detail="",
        posted_date=datetime.now()
    )
