"""LinkedIn URL Collection via Playwright (Phase 1)
EMD Compliance: ≤80 lines, 5 concurrent contexts (Naukri pattern)
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import List
from playwright.async_api import async_playwright
from src.models import JobUrlModel
from src.db.operations import JobStorageOperations
from .selector_config import SEARCH_SELECTORS, SCROLL_CONFIG, WAIT_TIMEOUTS

logger = logging.getLogger(__name__)


async def scrape_linkedin_urls_playwright(
    keyword: str,
    location: str,
    limit: int = 100,
    store_to_db: bool = True,
    headless: bool = False,
) -> List[JobUrlModel]:
    """Phase 1: Extract LinkedIn job URLs via Playwright + BrightData HTTP proxy"""
    
    proxy_url = os.getenv("PROXY_URL")
    proxy_config = None
    
    if proxy_url and proxy_url.startswith("http"):
        # Parse proxy URL: http://user:pass@host:port
        proxy_parts = proxy_url.replace("http://", "").replace("https://", "")
        auth_host = proxy_parts.split("@")
        username, password = auth_host[0].split(":")
        server = f"http://{auth_host[1]}"
        proxy_config = {"server": server, "username": username, "password": password}
        logger.info(f"🔗 Using proxy: {server}")
    else:
        logger.info("🔗 No proxy - direct connection")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, proxy=proxy_config)
        page = await browser.new_page()
        
        # Navigate to LinkedIn jobs search
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '+')}&location={location.replace(' ', '+')}"
        await page.goto(search_url, timeout=WAIT_TIMEOUTS["navigation"])
        logger.info(f"📄 Loaded: {search_url}")
        
        # Wait for job cards to load
        await page.wait_for_selector(SEARCH_SELECTORS["job_card"][0], timeout=WAIT_TIMEOUTS["element"])
        
        # Concurrent scrolling (5 contexts like Naukri)
        semaphore = asyncio.Semaphore(5)
        url_models: List[JobUrlModel] = []
        
        async def scroll_batch(start_scroll: int, count: int) -> List[JobUrlModel]:
            async with semaphore:
                batch_urls: List[JobUrlModel] = []
                for scroll_num in range(count):
                    job_cards = await page.query_selector_all(SEARCH_SELECTORS["job_card"][0])
                    for card in job_cards:
                        link = await card.query_selector(SEARCH_SELECTORS["job_link"][0])
                        if link:
                            url = await link.get_attribute("href")
                            if url:
                                job_id = f"linkedin_{url.split('/')[-1].split('?')[0]}"
                                batch_urls.append(JobUrlModel(
                                    job_id=job_id, platform="linkedin",
                                    input_role=keyword, actual_role=keyword,
                                    url=url.split("?")[0]
                                ))
                    logger.debug(f"Scroll {scroll_num + 1}/{count}: {len(batch_urls)} URLs")
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(SCROLL_CONFIG["scroll_pause"])
                return batch_urls
        
        scrolls = min(limit // SCROLL_CONFIG["jobs_per_scroll"], SCROLL_CONFIG["max_scrolls"])
        url_models = await scroll_batch(0, scrolls)
        
        await browser.close()
    
    logger.info(f"✅ Collected {len(url_models)} LinkedIn URLs")
    
    if store_to_db:
        db_ops = JobStorageOperations()
        db_ops.store_urls(url_models)
    
    return url_models[:limit]
