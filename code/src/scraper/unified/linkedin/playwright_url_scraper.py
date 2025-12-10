"""LinkedIn URL Collection via Playwright (Phase 1)
EMD Compliance: ≤80 lines, 5 concurrent contexts (Naukri pattern)
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import List
from playwright.async_api import async_playwright, ProxySettings
from src.models.models import JobUrlModel
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
    """Phase 1: Collect NEW LinkedIn URLs (skips existing in database)"""
    
    # Get existing URLs from database to skip duplicates
    db_ops = JobStorageOperations()
    
    # Proxy configuration (optional)
    proxy_url = os.getenv("PROXY_URL")
    proxy_config = None
    server = ""
    if proxy_url:
        parts = proxy_url.replace("http://", "").split("@")
        if len(parts) == 2:
            auth, server = parts
            username, password = auth.split(":")
            proxy_config = ProxySettings(
                server=f"http://{server}",
                username=username,
                password=password
            )
        else:
            server = parts[0]
            proxy_config = ProxySettings(server=f"http://{server}")
        logger.info(f"🔗 Using proxy: {server}")
    else:
        logger.info("🔗 No proxy - direct connection")
    
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '+')}&location={location.replace(' ', '+')}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, proxy=proxy_config)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        # 5 CONCURRENT TABS scraping
        semaphore = asyncio.Semaphore(5)
        scrolls_per_tab = max(1, (limit // SCROLL_CONFIG["jobs_per_scroll"]) // 5)
        
        async def scrape_tab(tab_id: int, start_offset: int) -> List[JobUrlModel]:
            async with semaphore:
                page = await context.new_page()
                tab_urls: List[JobUrlModel] = []
                try:
                    # Each tab starts at different offset for pagination
                    paginated_url = f"{search_url}&start={start_offset}"
                    await page.goto(paginated_url, timeout=WAIT_TIMEOUTS["navigation"])
                    await page.wait_for_selector(SEARCH_SELECTORS["job_card"][0], timeout=WAIT_TIMEOUTS["element"])
                    logger.info(f"📄 Tab {tab_id}: Loaded (offset={start_offset})")
                    
                    for scroll_idx in range(scrolls_per_tab):
                        job_cards = await page.query_selector_all(SEARCH_SELECTORS["job_card"][0])
                        for card in job_cards:
                            link = await card.query_selector(SEARCH_SELECTORS["job_link"][0])
                            if link:
                                url_raw = await link.get_attribute("href")
                                if url_raw:
                                    url = url_raw.split("?")[0]  # Clean URL
                                    # Extract clean LinkedIn job ID (just the number)
                                    job_id = url.split('/')[-1]
                                    
                                    # Skip if already in this tab's results OR database
                                    if url not in [u.url for u in tab_urls]:
                                        tab_urls.append(JobUrlModel(
                                            job_id=job_id, platform="linkedin",
                                            input_role=keyword, actual_role=keyword,
                                            url=url
                                        ))
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await asyncio.sleep(SCROLL_CONFIG["scroll_pause"])
                        logger.debug(f"Tab {tab_id} scroll {scroll_idx+1}: {len(tab_urls)} URLs")
                except Exception as e:
                    logger.error(f"Tab {tab_id} error: {e}")
                finally:
                    await page.close()
                return tab_urls
        
        # Launch 5 concurrent tabs with different start offsets (pagination)
        logger.info("🚀 Launching 5 concurrent tabs for URL scraping...")
        # Each tab starts at different offset: 0, 25, 50, 75, 100
        tasks = [scrape_tab(i+1, i*25) for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        # Combine and deduplicate in-memory
        url_models = []
        seen_urls = set()
        for tab_result in results:
            for url_model in tab_result:
                if url_model.url not in seen_urls:
                    url_models.append(url_model)
                    seen_urls.add(url_model.url)
        
        # Filter out URLs already in database BEFORE storing
        all_urls = [u.url for u in url_models]
        existing_urls = db_ops.get_existing_urls(all_urls)
        new_url_models = [u for u in url_models if u.url not in existing_urls]
        
        logger.info(f"✅ Collected {len(url_models)} URLs, {len(new_url_models)} NEW (skipped {len(existing_urls)} duplicates)")
        
        await context.close()
        await browser.close()
    
    if store_to_db and new_url_models:
        db_ops.store_urls(new_url_models)
    
    return new_url_models[:limit]
