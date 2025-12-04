"""Phase 2: API-based detail scraping with deduplication
Fetches only unscraped URLs from job_urls table
"""

from __future__ import annotations

import asyncio
import logging
from typing import TypedDict

from src.db.operations import JobStorageOperations
from src.models.models import JobDetailModel, JobUrlModel
from src.scraper.services.naukri_api_client import NaukriAPIClient
from src.scraper.services.session_manager import (
    close_session,
    create_authenticated_session,
)


class KeySkillsData(TypedDict, total=False):
    """Type for keySkills field in Naukri API response"""
    other: list[str]


class CompanyDetailData(TypedDict, total=False):
    """Type for companyDetail field in Naukri API response"""
    name: str


class JobDetailsData(TypedDict, total=False):
    """Type for jobDetails field in Naukri API response"""
    title: str
    description: str
    keySkills: KeySkillsData
    companyDetail: CompanyDetailData
    createdDate: str


class NaukriAPIResponse(TypedDict, total=False):
    """Type for Naukri API response"""
    jobDetails: JobDetailsData

logger = logging.getLogger(__name__)


async def scrape_naukri_details_api(
    platform: str = "naukri",
    input_role: str | None = None,
    limit: int = 100,
    headless: bool = False,  # Always visible browser to avoid rate limits
    store_to_db: bool = True,
) -> list[JobDetailModel]:
    """Phase 2: Fetch job details via API (5 concurrent)"""

    # Step 1: Get unscraped URLs (deduplication)
    db_ops = JobStorageOperations()
    url_tuples = db_ops.get_unscraped_urls(
        platform, input_role or "python_developer", limit
    )

    # Convert tuples to JobUrlModel
    url_models = [
        JobUrlModel(
            url=url,
            job_id=job_id,
            platform=plat,
            input_role=input_role or "python_developer",
            actual_role=actual,
        )
        for url, job_id, plat, actual in url_tuples
    ]

    if not url_models:
        logger.info("No unscraped URLs found")
        return []

    # Step 2: Establish session
    browser, context, cookies = await create_authenticated_session(headless)

    # Step 3: Create API client
    client = NaukriAPIClient(cookies)

    try:
        # Step 4: Fetch details concurrently (5 concurrent)
        semaphore = asyncio.Semaphore(5)

        async def fetch_detail(url_model: JobUrlModel) -> JobDetailModel | None:
            async with semaphore:
                try:
                    raw_data = await client.get_job_detail(url_model.job_id)
                    # Extract and narrow jobDetails type
                    job_details_raw = raw_data.get("jobDetails", {})
                    job_details: JobDetailsData = job_details_raw if isinstance(job_details_raw, dict) else {}  # type: ignore[assignment]
                    data: NaukriAPIResponse = {"jobDetails": job_details}
                    return _parse_job_detail(data, url_model)
                except Exception as e:
                    logger.error(f"Failed {url_model.job_id}: {e}")
                    return None

        tasks = [fetch_detail(u) for u in url_models]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Step 5: Filter successes
        job_models = [r for r in results if isinstance(r, JobDetailModel)]

        # Step 6: Store to DB
        if store_to_db and job_models:
            await asyncio.to_thread(db_ops.store_details, job_models)

        logger.info(f"Scraped {len(job_models)} job details via API")
        return job_models

    finally:
        await client.close()
        await close_session(browser, context)


def _parse_job_detail(
    data: NaukriAPIResponse, url_model: JobUrlModel
) -> JobDetailModel:
    """Parse API response to JobDetailModel"""
    job: JobDetailsData = data.get("jobDetails", {})

    # Extract nested values with safe defaults
    key_skills: KeySkillsData = job.get("keySkills", {})
    skills_list: list[str] = key_skills.get("other", [])

    company_detail: CompanyDetailData = job.get("companyDetail", {})
    company_name: str = company_detail.get("name", "")

    return JobDetailModel(
        job_id=url_model.job_id,
        platform="naukri",
        actual_role=job.get("title", url_model.actual_role),
        url=url_model.url,
        job_description=job.get("description", ""),
        skills=",".join(skills_list),
        company_name=company_name,
        posted_date=None,  # createdDate is str, but field expects datetime | None
    )
