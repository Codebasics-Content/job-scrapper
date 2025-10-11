"""Unified Indeed scraper via HeadlessX.

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


SEARCH_SELECTOR = "a.tapItem"
DESC_SELECTORS = [
    "#jobDescriptionText",
    ".jobsearch-JobComponent-description",
    "#jobDescriptionText .icl-u-xs-mt--md",
]


def _build_search_url(keyword: str, location: str) -> str:
    k = keyword.replace(" ", "+")
    loc = location.replace(" ", "+")
    return f"https://www.indeed.com/jobs?q={k}&l={loc}"


async def scrape_indeed_jobs_unified(
    keyword: str,
    location: str = "United States",
    limit: int = 50,
) -> List[JobModel]:
    # Use direct skill extraction function
    jobs: List[JobModel] = []

    # Use enhanced HeadlessX client with retry and concurrency
    async with HeadlessXClient() as client:
        search_url = _build_search_url(keyword, location)
        html = await client.render_url(search_url)
        soup = BeautifulSoup(html, "html.parser")

        links: list[str] = []
        for a in soup.select(SEARCH_SELECTOR):
            href = a.get("href")
            if href and isinstance(href, str):
                if href.startswith("/"):
                    href = f"https://www.indeed.com{href}"
                if href.startswith("http"):
                    links.append(href)
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
            if not desc:
                continue

            m = re.search(r"jk=([A-Za-z0-9]+)", job_url)
            job_id = f"indeed_{m.group(1)}" if m else job_url

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
                    platform="indeed",
                    url=job_url,
                    location="",
                    salary=None,
                    posted_date=datetime.now(),
                    skills_list=skills_list,
                    normalized_skills=[s.lower() for s in skills_list],
                )
            )

    return jobs
