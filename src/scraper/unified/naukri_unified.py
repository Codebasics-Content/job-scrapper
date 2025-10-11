"""Unified Naukri scraper via HeadlessX - EMD compliant

Returns only Job URL, Job Description, and Skills.
"""
from __future__ import annotations

from typing import List
from bs4 import BeautifulSoup

from src.models import JobModel
from src.scraper.services.headlessx_client import HeadlessXClient
from .naukri.selectors import CARD_SELECTORS, TITLE_SELECTOR
from .naukri.url_builder import build_search_url, normalize_job_url
from .naukri.parser import create_job_model


async def scrape_naukri_jobs_unified(
    keyword: str,
    location: str = "India",
    limit: int = 50,
) -> List[JobModel]:
    """Scrape Naukri jobs with HeadlessX client"""
    jobs: List[JobModel] = []

    async with HeadlessXClient() as client:
        # 1) Render search page
        search_url = build_search_url(keyword, location)
        html = await client.render_url(search_url)
        soup = BeautifulSoup(html, "html.parser")

        # 2) Collect job URLs with multiple selector fallbacks
        links: list[str] = []
        for card_sel in CARD_SELECTORS:
            for card in soup.select(card_sel):
                a = card.select_one(TITLE_SELECTOR)
                href = a.get("href") if a else None
                normalized = normalize_job_url(href)
                if normalized:
                    links.append(normalized)
                    if len(links) >= limit:
                        break
            if len(links) >= limit:
                break

        # 3) Render job URLs concurrently with error isolation
        job_results = await client.render_urls_concurrent(links)
        
        # 4) Process results and extract job data
        for job_url, result in job_results:
            if not result.get("success"):
                continue  # Skip failed URLs
            
            html_content = result.get("html", "")
            if isinstance(html_content, str):
                job = create_job_model(job_url, html_content)
                if job:
                    jobs.append(job)

    return jobs
