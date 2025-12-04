# LinkedIn Concurrent URL Scraper - 5 Tabs Worldwide
# Scrapes multiple countries in parallel, stops when threshold reached
from __future__ import annotations

import asyncio
import logging
from typing import List

from playwright.async_api import BrowserContext, async_playwright

from src.config.countries import LINKEDIN_COUNTRIES
from src.db.operations import JobStorageOperations
from src.models.models import JobUrlModel

from .selector_config import SEARCH_SELECTORS

logger = logging.getLogger(__name__)


# Shared state for threshold tracking
class SharedState:
    def __init__(self, threshold: int):
        self.threshold = threshold
        self.total_collected = 0
        self.lock = asyncio.Lock()
        self.should_stop = False
        self.all_urls: List[JobUrlModel] = []
        self.seen_urls: set[str] = set()

    async def add_urls(self, urls: List[JobUrlModel]) -> int:
        """Add URLs and return count of new ones added"""
        async with self.lock:
            new_count = 0
            for url in urls:
                if url.url not in self.seen_urls:
                    self.seen_urls.add(url.url)
                    self.all_urls.append(url)
                    new_count += 1
                    self.total_collected += 1

            # Check if threshold reached
            if self.total_collected >= self.threshold:
                self.should_stop = True
                logger.info(
                    f"🎯 Threshold {self.threshold} reached! Stopping all tabs..."
                )

            return new_count


async def scrape_single_country(
    context: BrowserContext,
    keyword: str,
    location: str,
    state: SharedState,
    db_ops: JobStorageOperations,
) -> int:
    """Scrape URLs from a single country in one tab"""

    if state.should_stop:
        return 0

    page = await context.new_page()
    collected = 0

    try:
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '+')}&location={location.replace(' ', '+')}"
        logger.info(f"🌍 [{location}] Starting scrape...")

        await page.goto(search_url, timeout=60000)
        await asyncio.sleep(2)

        # Close popup if present
        try:
            close_button = await page.query_selector(
                "xpath=/html/body/div[4]/div/div/section/button"
            )
            if close_button:
                await close_button.click()
                await asyncio.sleep(0.5)
        except Exception:
            pass

        # Wait for job cards
        job_cards_loaded = False
        for selector in SEARCH_SELECTORS["job_card"]:
            try:
                await page.wait_for_selector(selector, timeout=10000)
                job_cards_loaded = True
                break
            except Exception:
                continue

        if not job_cards_loaded:
            logger.warning(f"⚠️ [{location}] No job cards found")
            return 0

        # Scroll and collect URLs
        scroll_rounds = 0
        max_scroll_rounds = 10
        previous_count = 0
        no_new_attempts = 0

        while scroll_rounds < max_scroll_rounds and not state.should_stop:
            # Get all job cards
            job_cards = []
            for selector in SEARCH_SELECTORS["job_card"]:
                job_cards = await page.query_selector_all(selector)
                if job_cards:
                    break

            current_count = len(job_cards)

            # Extract URLs from cards
            batch_urls: List[JobUrlModel] = []
            for card in job_cards:
                link = None
                for link_selector in SEARCH_SELECTORS["job_link"]:
                    link = await card.query_selector(link_selector)
                    if link:
                        break

                if link:
                    try:
                        url = await link.get_attribute("href")
                        if url and "linkedin.com/jobs/view/" in url:
                            url = url.split("?")[0]
                            job_id = f"linkedin_{url.split('/')[-1]}"
                            batch_urls.append(
                                JobUrlModel(
                                    job_id=job_id,
                                    platform="linkedin",
                                    input_role=keyword,
                                    actual_role=keyword,
                                    url=url,
                                )
                            )
                    except Exception:
                        pass

            # Add to shared state (deduplicates automatically)
            new_added = await state.add_urls(batch_urls)
            collected += new_added

            if new_added > 0:
                logger.info(
                    f"📊 [{location}] +{new_added} URLs (Total: {state.total_collected}/{state.threshold})"
                )

            # Check threshold
            if state.should_stop:
                break

            # Check if no new cards loaded
            if current_count == previous_count:
                no_new_attempts += 1
                if no_new_attempts >= 3:
                    logger.info(f"✅ [{location}] No more jobs to load")
                    break
            else:
                no_new_attempts = 0
                previous_count = current_count

            # Scroll down
            for _ in range(3):
                await page.evaluate("window.scrollBy(0, 800)")
                await asyncio.sleep(1)

            scroll_rounds += 1
            await asyncio.sleep(1.5)

        logger.info(f"✅ [{location}] Completed: {collected} URLs collected")

    except Exception as e:
        logger.error(f"❌ [{location}] Error: {e}")
    finally:
        await page.close()

    return collected


async def scrape_worldwide_concurrent(
    keyword: str, threshold: int = 100, max_concurrent: int = 5, headless: bool = False
) -> List[JobUrlModel]:
    """
    Scrape LinkedIn jobs from multiple countries concurrently.

    Args:
        keyword: Job role to search for
        threshold: Stop when this many URLs collected
        max_concurrent: Number of concurrent browser tabs (default 5)
        headless: Run browser in headless mode (default False - visible)

    Returns:
        List of JobUrlModel objects
    """

    db_ops = JobStorageOperations()
    state = SharedState(threshold)

    # Will be populated during scraping with deduplication
    state.seen_urls = set()

    logger.info(f"🚀 Starting worldwide scrape for '{keyword}'")
    logger.info(f"🎯 Target: {threshold} URLs | Concurrent tabs: {max_concurrent}")
    logger.info(f"🌍 Countries: {len(LINKEDIN_COUNTRIES)}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )

        try:
            # Process countries in batches of max_concurrent
            country_index = 0

            while country_index < len(LINKEDIN_COUNTRIES) and not state.should_stop:
                # Get next batch of countries
                batch_countries = LINKEDIN_COUNTRIES[
                    country_index : country_index + max_concurrent
                ]

                logger.info(f"\n{'=' * 60}")
                logger.info(f"📦 Batch: {batch_countries}")
                logger.info(f"{'=' * 60}\n")

                # Create tasks for concurrent scraping
                tasks = [
                    scrape_single_country(context, keyword, country, state, db_ops)
                    for country in batch_countries
                ]

                # Run concurrently
                await asyncio.gather(*tasks)

                country_index += max_concurrent

                # Check if we should stop
                if state.should_stop:
                    logger.info(f"🛑 Threshold reached - stopping early")
                    break

                # Small delay between batches
                await asyncio.sleep(2)

        finally:
            await context.close()
            await browser.close()

    # Store collected URLs to database
    if state.all_urls:
        stored = db_ops.store_urls(state.all_urls)
        logger.info(f"💾 Stored {stored} NEW URLs to database")

    logger.info(f"\n{'=' * 60}")
    logger.info(f"✅ WORLDWIDE SCRAPE COMPLETE")
    logger.info(f"   Total collected: {state.total_collected}")
    logger.info(f"   Threshold was: {threshold}")
    logger.info(f"{'=' * 60}\n")

    return state.all_urls


# For direct testing
if __name__ == "__main__":
    import sys

    keyword = sys.argv[1] if len(sys.argv) > 1 else "Data Analyst"
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    urls = asyncio.run(scrape_worldwide_concurrent(keyword, threshold))
    print(f"Collected {len(urls)} URLs")
