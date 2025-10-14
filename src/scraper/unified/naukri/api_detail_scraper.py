"""Phase 2: API-based detail scraping with deduplication
Fetches only unscraped URLs from job_urls table
"""
from __future__ import annotations
import asyncio
from typing import List, Dict
from src.models import JobDetailModel, JobURLModel
from src.scraper.services.session_manager import (
    create_authenticated_session,
    close_session,
)
from src.scraper.services.naukri_api_client import NaukriAPIClient
from src.db.operations import (
    get_unscraped_job_urls,
    batch_upsert_jobs,
)
import logging

logger = logging.getLogger(__name__)


async def scrape_naukri_details_api(
    platform: str = "naukri",
    input_role: str | None = None,
    limit: int = 100,
    headless: bool = True,
    store_to_db: bool = True,
) -> List[JobDetailModel]:
    """Phase 2: Fetch job details via API (5 concurrent)"""
    
    # Step 1: Get unscraped URLs (deduplication)
    url_models = get_unscraped_job_urls(platform, input_role, limit)
    
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
        
        async def fetch_detail(url_model) -> JobDetailModel | None:
            async with semaphore:
                try:
                    data = await client.get_job_detail(url_model.job_id)
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
            batch_upsert_jobs(job_models)
        
        logger.info(f"Scraped {len(job_models)} job details via API")
        return job_models
        
    finally:
        await client.close()
        await close_session(browser, context)


def _parse_job_detail(data: Dict[str, object], url_model: JobURLModel) -> JobDetailModel:
    """Parse API response to JobDetailModel"""
    job = data.get("jobDetails", {})
    
    return JobDetailModel(
        job_id=url_model.job_id,
        platform="naukri",
        actual_role=job.get("title", url_model.actual_role),
        url=url_model.url,
        job_description=job.get("description", ""),
        skills=",".join(job.get("keySkills", {}).get("other", [])),
        company_name=job.get("companyDetail", {}).get("name", ""),
        company_detail=str(job.get("companyDetail", {})),
        posted_date=job.get("createdDate", ""),
    )
