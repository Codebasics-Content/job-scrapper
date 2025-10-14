"""Phase 1: API-based URL extraction with 5 concurrent batches
Uses session transfer for captcha bypass
"""
from __future__ import annotations
import asyncio
from typing import List, Dict
from src.models import JobURLModel
from src.scraper.services.session_manager import (
    create_authenticated_session,
    close_session,
)
from src.scraper.services.naukri_api_client import NaukriAPIClient
from src.db.operations import batch_upsert_job_urls
import logging

logger = logging.getLogger(__name__)


async def scrape_naukri_urls_api(
    keyword: str,
    location: str,
    limit: int = 100,
    headless: bool = True,
    store_to_db: bool = True,
) -> List[JobURLModel]:
    """Phase 1: Extract job URLs via API (5 concurrent pages)"""
    
    # Step 1: Establish session
    browser, context, cookies = await create_authenticated_session(headless)
    
    # Step 2: Create API client with session
    client = NaukriAPIClient(cookies)
    
    try:
        
        # Step 3: Calculate pages (20 jobs per page)
        total_pages = (limit + 19) // 20
        pages = list(range(1, min(total_pages + 1, 6)))  # Max 5 pages
        
        # Step 4: Fetch concurrently (5 concurrent)
        semaphore = asyncio.Semaphore(5)
        
        async def fetch_page(page_no: int) -> List[JobURLModel]:
            async with semaphore:
                data = await client.search_jobs(keyword, page_no, 20)
                return _parse_job_urls(data, keyword)
        
        tasks = [fetch_page(p) for p in pages]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Step 5: Flatten results
        url_models: List[JobURLModel] = []
        for result in results:
            if isinstance(result, list):
                url_models.extend(result)
        
        # Step 6: Store to DB
        if store_to_db and url_models:
            batch_upsert_job_urls(url_models)
        
        logger.info(f"Scraped {len(url_models)} URLs via API")
        return url_models[:limit]
        
    finally:
        await client.close()
        await close_session(browser, context)


def _parse_job_urls(data: Dict[str, object], keyword: str) -> List[JobURLModel]:
    """Parse API response to JobURLModel"""
    models = []
    job_list = data.get("jobDetails", [])
    assert isinstance(job_list, list)
    for job in job_list:
        models.append(
            JobURLModel(
                job_id=job["jobId"],
                platform="naukri",
                input_role=keyword,
                actual_role=job.get("title", keyword),
                url=f"https://www.naukri.com{job['jdURL']}",
            )
        )
    return models
