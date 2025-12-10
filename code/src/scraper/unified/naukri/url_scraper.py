# Phase 1: Naukri URL Collection - Fast 10-100x speedup
# EMD Compliance: ≤80 lines, Optimized for two-table architecture
from __future__ import annotations

import logging
import asyncio

from src.models.models import JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.db.operations import JobStorageOperations
from .url_builder import build_search_url
from .page_scraper import scrape_page_urls

logger = logging.getLogger(__name__)


async def scrape_naukri_urls(
    keyword: str,
    location: str = "India",
    limit: int = 10000,
    headless: bool = False,
    store_to_db: bool = True,
    city_gid: str | None = None,
) -> list[JobUrlModel]:
    """Phase 1: Scrape only job URLs from Naukri with real-time deduplication"""
    url_models: list[JobUrlModel] = []
    platform = "Naukri"
    input_role = JobUrlModel.normalize_role(keyword)
    
    # Real-time deduplication database
    db_ops = JobStorageOperations()
    job_urls: list[tuple[str, str]] = []
    seen_in_session: set[str] = set()
    total_duplicates_session = 0
    total_duplicates_database = 0

    async with PlaywrightBrowser(headless=headless) as browser:
        page = 1
        max_pages = 50
        concurrent_pages = 1  # Reduced to avoid bot detection

        while len(job_urls) < limit and page <= max_pages:
            page_batch = list(range(page, min(page + concurrent_pages, max_pages + 1)))
            
            batch_results = await asyncio.gather(*[
                scrape_page_urls(
                    browser,
                    build_search_url(keyword, location, page=pn, city_gid=city_gid),
                    pn,
                    save_debug=(pn == 1)
                ) for pn in page_batch
            ])

            urls_before = len(job_urls)
            
            for urls_list in batch_results:
                for title, url in urls_list:
                    # Skip if seen in this session
                    if url in seen_in_session:
                        total_duplicates_session += 1
                        print(f"⏭️  Session Duplicate #{total_duplicates_session}: {url[:60]}")
                        continue
                    
                    seen_in_session.add(url)
                    
                    # Real-time database check
                    existing = db_ops.get_existing_urls([url])
                    if url in existing:
                        total_duplicates_database += 1
                        print(f"💾 Database Duplicate #{total_duplicates_database}: {url[:60]}")
                        continue
                    
                    # NEW URL - count it
                    job_urls.append((title, url))
                    print(f"✅ NEW #{len(job_urls)}/{limit}: {url[:60]}")
                    
                    if len(job_urls) >= limit:
                        break
                if len(job_urls) >= limit:
                    break

            urls_added = len(job_urls) - urls_before
            print(f"\n📊 BATCH SUMMARY (Pages {page_batch[0]}-{page_batch[-1]}):")
            print(f"   ├─ NEW URLs this batch: {urls_added}")
            print(f"   ├─ Total NEW collected: {len(job_urls)}/{limit}")
            print(f"   ├─ Session duplicates: {total_duplicates_session}")
            print(f"   └─ Database duplicates: {total_duplicates_database}")
            page += concurrent_pages
            await asyncio.sleep(3.0)  # Longer delay to avoid detection

        for title, url in job_urls:
            job_id = JobUrlModel.generate_job_id(platform, url)
            url_model = JobUrlModel(
                job_id=job_id, platform=platform, input_role=input_role, actual_role=title, url=url
            )
            url_models.append(url_model)

        if url_models:
            stored = db_ops.store_urls(url_models)
            logger.info(f"💾 Stored {stored}/{len(url_models)} NEW URLs to database")

    print(f"\n{'='*70}")
    print(f"✅ SCRAPING COMPLETED")
    print(f"{'='*70}")
    print(f"📊 FINAL STATISTICS:")
    print(f"   ├─ NEW URLs collected: {len(url_models)}")
    print(f"   ├─ Session duplicates skipped: {total_duplicates_session}")
    print(f"   ├─ Database duplicates skipped: {total_duplicates_database}")
    print(f"   └─ Total URLs processed: {len(url_models) + total_duplicates_session + total_duplicates_database}")
    print(f"{'='*70}\n")
    return url_models
