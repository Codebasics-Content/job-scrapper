"""Naukri job data parsing logic"""

import re
from datetime import datetime
from bs4 import BeautifulSoup

from src.models import JobModel
from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text
from .selectors import DESC_SELECTORS, SKILLS_SELECTOR


def extract_job_id(url: str) -> str:
    """Extract job ID from Naukri URL"""
    m = re.search(r"job-listings-([A-Za-z0-9]+)", url)
    return f"naukri_{m.group(1)}" if m else url


def extract_description(soup: BeautifulSoup) -> str:
    """Extract job description from page HTML"""
    desc = ""
    for sel in DESC_SELECTORS:
        node = soup.select_one(sel)
        if node:
            desc = node.get_text(" ", strip=True)
            if desc:
                break
    
    # Append key skills section if present
    skills_section = soup.select_one(SKILLS_SELECTOR)
    if skills_section:
        ks = skills_section.get_text(" ", strip=True)
        if ks:
            desc = f"{desc} Key Skills: {ks}" if desc else ks
    
    return desc


def create_job_model(job_url: str, html: str) -> JobModel | None:
    """Parse HTML and create JobModel"""
    soup = BeautifulSoup(html, "html.parser")
    desc = extract_description(soup)
    
    if not desc:
        return None
    
    job_id = extract_job_id(job_url)
    skills_list = extract_skills_from_text(desc)
    skills_str = ", ".join(skills_list) if skills_list else ""
    
    return JobModel(
        job_id=job_id,
        Job_Role="",
        Company="",
        Experience="",
        Skills=skills_str,
        jd=desc,
        company_detail="",
        platform="naukri",
        url=job_url,
        location="",
        salary=None,
        posted_date=datetime.now(),
        skills_list=skills_list,
        normalized_skills=[s.lower() for s in skills_list],
    )
