# Phase 1: Indeed URL Collection - Fast 10-100x speedup
# EMD Compliance: ≤80 lines, Optimized for two-table architecture
from __future__ import annotations

import logging
import asyncio
from bs4 import BeautifulSoup

from src.models import JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.db.operations import JobStorageOperations
from .selectors import CARD_SELECTORS_CSS
from .url_builder import build_search_url, normalize_job_url
from .card_parser import parse_search_card

logger = logging.getLogger(__name__)


async def scrape_indeed_urls(
    keyword: str,
    location: str = "United States",
    limit: int = 10000,
    headless: bool = True,
    store_to_db: bool = True,
) -> list[JobUrlModel]:
    """Phase 1: Scrape only job URLs from Indeed (10-100x faster than full scraping)"""
    url_models: list[JobUrlModel] = []
    platform = "Indeed"
    input_role = JobUrlModel.normalize_role(keyword)
    db_ops = JobStorageOperations() if store_to_db else None

    async with PlaywrightBrowser(headless=headless) as browser:
        job_urls: list[tuple[str, str]] = []  # (title, url)
        page = 0  # Indeed uses 0-based pagination
        max_pages = 50
        concurrent_pages = 1  # Single page to avoid bot detection

        while len(job_urls) < limit and page < max_pages:
            page_batch = list(range(page, min(page + concurrent_pages, max_pages)))

            async def scrape_page(page_num: int) -> list[tuple[str, str]]:
                search_url = build_search_url(keyword, location, start=page_num * 10)
                list_html = await browser.render_url(search_url, wait_seconds=5.0, wait_until='domcontentloaded')
                soup = BeautifulSoup(list_html, "html.parser")
                logger.info(f"✅ Page {page_num} scraped")

                urls: list[tuple[str, str]] = []
                seen_urls = set()
                for card_sel in CARD_SELECTORS_CSS:
                    for card in soup.select(card_sel):
                        card_data = parse_search_card(card)
                        if card_data:
                            title = card_data["title"]
                            url_href = card_data["url"]
                            if not url_href or url_href in seen_urls:
                                continue
                            seen_urls.add(url_href)
                            normalized_url = normalize_job_url(url_href)
                            if normalized_url:
                                urls.append((title, normalized_url))
                return urls

            results = await asyncio.gather(*[scrape_page(p) for p in page_batch])
            for urls_list in results:
                for title, url in urls_list:
                    if url not in [u for _, u in job_urls]:
                        job_urls.append((title, url))
                    if len(job_urls) >= limit:
                        break
                if len(job_urls) >= limit:
                    break

            logger.info(f"📊 Pages {page_batch[0]}-{page_batch[-1]}: {len(job_urls)} URLs")
            page += concurrent_pages
            await asyncio.sleep(3.0)  # Longer delay to avoid detection

        for title, url in job_urls:
            job_id = JobUrlModel.generate_job_id(platform, url)
            url_model = JobUrlModel(
                job_id=job_id, platform=platform, input_role=input_role, actual_role=title, url=url
            )
            url_models.append(url_model)

        if db_ops and url_models:
            stored = db_ops.store_urls(url_models)
            logger.info(f"💾 Stored {stored}/{len(url_models)} URLs to database")

    return url_models
