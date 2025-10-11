"""Unified Naukri scraper via HeadlessX.

Returns only Job URL, Job Description, and Skills.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup

from src.models import JobModel
from src.analysis.skill_extraction.regex_extractor import extract_skills_from_text
from src.scraper.services.headlessx_client import HeadlessXClient


CARD_SELECTORS = [
    "article.jobTuple",
    ".cust-job-tuple",
    "article[data-job-id]",
]
TITLE_SELECTOR = "a.title, a.title-text, a[title]"
DESC_SELECTORS = [
    "div.jd-content",
    "div.job-description",
    "div.JDC",
    "section.job-desc",
]
SKILLS_SELECTOR = "div.key-skill"


def _build_search_url(keyword: str, location: str) -> str:
    k = keyword.replace(" ", "-")
    path = f"/{k}-jobs"
    if location and location.lower() != "india":
        loc = location.replace(" ", "-")
        path += f"-in-{loc}"
    return f"https://www.naukri.com{path}"


async def scrape_naukri_jobs_unified(
    keyword: str,
    location: str = "India",
    limit: int = 50,
) -> List[JobModel]:
    # Use direct skill extraction function
    jobs: List[JobModel] = []

    # Use enhanced HeadlessX client with retry and concurrency
    async with HeadlessXClient() as client:
        search_url = _build_search_url(keyword, location)
        html = await client.render_url(search_url)
        soup = BeautifulSoup(html, "html.parser")

        # Collect job URLs
        links: list[str] = []
        for card_sel in CARD_SELECTORS:
            for card in soup.select(card_sel):
                a = card.select_one(TITLE_SELECTOR)
                href = a.get("href") if a else None
                if href and isinstance(href, str) and href.startswith("http"):
                    links.append(href)
                    if len(links) >= limit:
                        break
            if len(links) >= limit:
                break

        # Render job URLs concurrently with error isolation
        job_results = await client.render_urls_concurrent(links)
        
        # Process results and extract job data
        for job_url, result in job_results:
            if isinstance(result, Exception):
                continue  # Skip failed URLs
            
            page = BeautifulSoup(result, "html.parser")

            desc = ""
            for sel in DESC_SELECTORS:
                node = page.select_one(sel)
                if node:
                    desc = node.get_text(" ", strip=True)
                    if desc:
                        break
            # Append key skills text if present
            skills_section = page.select_one(SKILLS_SELECTOR)
            if skills_section:
                ks = skills_section.get_text(" ", strip=True)
                if ks:
                    desc = f"{desc} Key Skills: {ks}" if desc else ks

            if not desc:
                continue

            m = re.search(r"job-listings-([A-Za-z0-9]+)", job_url)
            job_id = f"naukri_{m.group(1)}" if m else job_url

            skills_list = extract_skills_from_text(desc)
            skills_str = ", ".join(skills_list) if skills_list else ""

            jobs.append(
                JobModel(
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
            )

    return jobs
