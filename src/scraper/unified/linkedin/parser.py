"""LinkedIn job data parsing logic"""

import re
from datetime import datetime
from bs4 import BeautifulSoup

from src.models import JobModel
from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text
from .selectors import DESC_SELECTORS


def extract_job_id(url: str) -> str:
    """Extract job ID from LinkedIn URL"""
    m = re.search(r"/view/(\d+)", url)
    return f"linkedin_{m.group(1)}" if m else url


def extract_description(soup: BeautifulSoup) -> str:
    """Extract job description from page HTML"""
    for sel in DESC_SELECTORS:
        node = soup.select_one(sel)
        if node:
            desc = node.get_text(" ", strip=True)
            if desc:
                return desc
    return ""


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
        platform="linkedin",
        url=job_url,
        location="",
        salary=None,
        posted_date=datetime.now(),
        skills_list=skills_list,
        normalized_skills=[s.lower() for s in skills_list],
    )
