"""Unified LinkedIn scraper via HeadlessX - EMD compliant

Goal: Return only Job URL, Job Description, and Skills at scale.
"""
from __future__ import annotations

from typing import List
from bs4 import BeautifulSoup

from src.models import JobModel
from src.scraper.services.headlessx_client import HeadlessXClient
from .linkedin.selectors import SEARCH_SELECTOR
from .linkedin.url_builder import build_search_url
from .linkedin.parser import create_job_model


async def scrape_linkedin_jobs_unified(
    keyword: str,
    location: str = "United States",
    limit: int = 50,
) -> List[JobModel]:
    """Scrape LinkedIn jobs with HeadlessX client"""
    jobs: List[JobModel] = []

    async with HeadlessXClient() as client:
        # 1) Render search page
        search_url = build_search_url(keyword, location)
        html = await client.render_url(search_url)
        soup = BeautifulSoup(html, "html.parser")

        # 2) Collect job URLs
        links = []
        for a in soup.select(SEARCH_SELECTOR):
            href = a.get("href")
            if href and href.startswith("http"):
                links.append(href)
            if len(links) >= limit:
                break

        # 3) Render job URLs concurrently with error isolation
        job_results = await client.render_urls_concurrent(links)
        
        # 4) Process results and extract job data
        for job_url, result in job_results:
            if not result.get("success"):
                continue  # Skip failed URLs
            
            html = result.get("html", "")
            if isinstance(html, str):
                job = create_job_model(job_url, html)
                if job:
                    jobs.append(job)

    return jobs
