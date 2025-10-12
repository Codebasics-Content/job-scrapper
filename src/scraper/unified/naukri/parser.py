"""Naukri job data parsing logic"""

from datetime import datetime
from bs4 import BeautifulSoup

from src.models import JobDetailModel, JobUrlModel
from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text
from .selectors import DESC_SELECTORS_CSS



def extract_description(soup: BeautifulSoup) -> str:
    """Extract job description from detail page HTML - matches test_playwright_detail_pages.py"""
    # Primary: Full JD section (2025 Naukri structure)
    desc_elem = soup.select_one("div.styles_JDC__dang-inner-html__h0K4t")
    if not desc_elem:
        desc_elem = soup.select_one("div[class*='job-description']")
    
    if desc_elem:
        return desc_elem.get_text(strip=True)
    
    # Fallback selectors
    for sel in DESC_SELECTORS_CSS:
        node = soup.select_one(sel)
        if node:
            text = node.get_text(" ", strip=True)
            if text and len(text) > 100:
                return text
    
    return ""


def create_job_detail_model(
    job_url: str, 
    html: str,
    title: str = "",
    company: str = ""
) -> JobDetailModel | None:
    """Parse HTML and create JobDetailModel for two-table storage"""
    soup = BeautifulSoup(html, "html.parser")
    desc = extract_description(soup)
    
    if not desc:
        return None
    
    job_id = JobUrlModel.generate_job_id("Naukri", job_url)
    skills_list = extract_skills_from_text(desc)
    skills_str = ", ".join(skills_list) if skills_list else ""
    
    return JobDetailModel(
        job_id=job_id,
        platform="Naukri",
        actual_role=title,
        url=job_url,
        job_description=desc,
        skills=skills_str,
        company_name=company,
        company_detail=company,
        posted_date=datetime.now(),
        scraped_at=datetime.now()
    )
