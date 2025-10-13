# Phase 1: Naukri URL Collection - Fast 10-100x speedup
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


async def scrape_naukri_urls(
    keyword: str,
    location: str = "India",
    limit: int = 10000,
    headless: bool = True,
    store_to_db: bool = True,
) -> list[JobUrlModel]:
    """Phase 1: Scrape only job URLs from Naukri (10-100x faster than full scraping)"""
    url_models: list[JobUrlModel] = []
    platform = "Naukri"
    input_role = JobUrlModel.normalize_role(keyword)
    db_ops = JobStorageOperations() if store_to_db else None

    async with PlaywrightBrowser(headless=headless) as browser:
        job_urls: list[tuple[str, str]] = []  # (title, url)
        page = 1
        max_pages = 50
        concurrent_pages = 1  # Reduced to avoid bot detection

        while len(job_urls) < limit and page <= max_pages:
            page_batch = list(range(page, min(page + concurrent_pages, max_pages + 1)))

            async def _scrape_page_urls(browser: PlaywrightBrowser, page_num: int, headless: bool = False, save_debug: bool = False) -> list[tuple[str, str]]:
                search_url = build_search_url(keyword, location, page=page_num)
                html = await browser.render_url(search_url, wait_seconds=5.0)
                if not html:
                    logger.error(f"❌ No HTML returned for page {page_num}")
                    return []
                
                logger.debug(f"📄 Page {page_num} HTML length: {len(html)} bytes")
                
                # Save HTML for debugging (first page only)
                if save_debug:
                    from pathlib import Path
                    debug_file = Path("debug_naukri_listing.html")
                    debug_file.write_text(html, encoding="utf-8")
                    logger.info(f"✅ Saved HTML to {debug_file.absolute()}")
                
                soup = BeautifulSoup(html, "html.parser")
                
                urls: list[tuple[str, str]] = []
                for card_sel in CARD_SELECTORS_CSS:
                    cards = soup.select(card_sel)
                    logger.info(f"🔍 Page {page_num} selector '{card_sel}': {len(cards)} cards")
                    for card in cards:
                        card_data = parse_search_card(card)
                        if card_data["url"] and card_data["title"]:
                            url = normalize_job_url(card_data["url"]) or card_data["url"]
                            urls.append((card_data["title"], url))
                    if urls:  # Stop after first successful selector
                        break
                
                logger.info(f"✅ Page {page_num}: extracted {len(urls)} URLs")
                return urls

            batch_results = await asyncio.gather(*[_scrape_page_urls(browser, page_num, headless, save_debug=(page_num == 1)) for page_num in page_batch])

            for urls_list in batch_results:
                for title, url in urls_list:
                    if url not in [existing_url for _, existing_url in job_urls]:
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
