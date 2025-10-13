"""Unified Indeed scraper with Playwright detail page navigation - Scale 10,000+

Navigates INSIDE each job for full descriptions with concurrent processing.
Includes playwright-stealth for Cloudflare bypass.
"""
from __future__ import annotations

import logging
import asyncio
from typing import List
from bs4 import BeautifulSoup

from src.models import JobDetailModel
from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.db.operations import JobStorageOperations
from .indeed.selectors import CARD_SELECTORS_CSS
from .indeed.url_builder import build_search_url, normalize_job_url
from .indeed.card_parser import parse_search_card
from .indeed.parser import create_job_detail_model

logger = logging.getLogger(__name__)


async def scrape_indeed_jobs_unified(
    keyword: str,
    location: str = "United States",
    limit: int = 10000,
    batch_size: int = 50,
    store_to_db: bool = True,
    headless: bool = False,
) -> List[JobDetailModel]:
    """Scrape Indeed at scale with Playwright detail page navigation"""
    all_jobs: List[JobDetailModel] = []
    db_ops = JobStorageOperations() if store_to_db else None

    async with PlaywrightBrowser(headless=headless, use_stealth=False) as browser:
        job_urls: list[str] = []
        start = 0
        max_pages = 100
        concurrent_pages = 5  # Phase 1: Scrape 5 pages concurrently
        
        # Phase 1: Parallel pagination with Cloudflare handling
        while len(job_urls) < limit and start < (max_pages * 10):
            # Create batch of start positions (Indeed: 0, 10, 20, 30, 40)
            start_batch = [start + (i * 10) for i in range(concurrent_pages)]
            
            # Scrape pages concurrently
            async def scrape_page(start_pos: int) -> list[str]:
                search_url = build_search_url(keyword, location, start=start_pos)
                list_html = await browser.render_url(search_url, wait_seconds=15.0)
                
                # Check Cloudflare
                if "just a moment" in list_html.lower() or "cloudflare" in list_html.lower():
                    logger.warning(f"⚠️ Cloudflare at start={start_pos}")
                    await asyncio.sleep(20)
                    return []
                
                soup = BeautifulSoup(list_html, "html.parser")
                logger.info(f"✅ Start={start_pos} scraped: {len(list_html)} chars")
                
                urls: list[str] = []
                for card_sel in CARD_SELECTORS_CSS:
                    for card in soup.select(card_sel):
                        card_data = parse_search_card(card)
                        if card_data["url"]:
                            url = normalize_job_url(card_data["url"]) or card_data["url"]
                            if url:
                                urls.append(url)
                return urls
            
            # Execute 5 pages concurrently
            batch_results = await asyncio.gather(*[scrape_page(s) for s in start_batch])
            
            # Flatten and deduplicate
            for urls_list in batch_results:
                for url in urls_list:
                    if url not in job_urls:
                        job_urls.append(url)
                    if len(job_urls) >= limit:
                        break
                if len(job_urls) >= limit:
                    break
            
            logger.info(f"📊 Batch start {start_batch[0]}-{start_batch[-1]}: Total {len(job_urls)} unique jobs")
            start += (concurrent_pages * 10)
            await asyncio.sleep(3.0)  # Longer delay for Cloudflare
        
        logger.info(f"Found {len(job_urls)} job URLs, processing in batches of {batch_size}")

        # Phase 2: Parallel detail page scraping (5 concurrent jobs)
        concurrent_jobs = 5
        for batch_start in range(0, len(job_urls), concurrent_jobs):
            batch_urls = job_urls[batch_start:batch_start + concurrent_jobs]
            
            # Scrape detail pages concurrently
            async def scrape_detail(job_url: str) -> JobDetailModel | None:
                try:
                    detail_html = await browser.render_url(job_url, wait_seconds=3.0)
                    job_id = job_url.split('/')[-1].split('?')[0]
                    job = create_job_detail_model(
                        job_id=f"indeed_{job_id}",
                        platform="indeed",
                        actual_role="AI Engineer",
                        url=job_url,
                        html=detail_html
                    )
                    return job
                except Exception as e:
                    logger.error(f"❌ Error {job_url}: {e}")
                    return None
            
            # Execute 5 jobs concurrently (includes skills extraction)
            batch_results = await asyncio.gather(*[scrape_detail(url) for url in batch_urls])
            batch_jobs = [job for job in batch_results if job]
            
            all_jobs.extend(batch_jobs)
            
            # Store to database immediately
            if db_ops and batch_jobs:
                stored = db_ops.store_jobs(batch_jobs)
                logger.info(f"💾 Batch {batch_start//concurrent_jobs + 1}: {stored}/{len(batch_jobs)} jobs stored to DB")
            
            await asyncio.sleep(2.0)  # Rate limiting between batches
            logger.info(f"📈 Progress: {len(all_jobs)}/{len(job_urls)} jobs scraped")

    return all_jobs
