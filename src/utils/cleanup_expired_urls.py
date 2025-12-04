"""Utility to mark expired/removed LinkedIn job URLs as processed
Prevents wasting time on 404 URLs in future scraping runs
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import asyncio
import logging
import sqlite3

from playwright.async_api import Browser, async_playwright

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def check_if_url_expired(url: str, browser: Browser) -> bool:
    """Check if a single URL returns 404"""
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    )
    page = await context.new_page()

    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await asyncio.sleep(1)  # Brief wait for page to render

        # Check page title
        page_title = await page.title()
        if "404" in page_title or page_title == "LinkedIn":
            h1_elem = await page.query_selector("h1")
            if h1_elem:
                h1_text = await h1_elem.inner_text()
                error_indicators = [
                    "not found",
                    "404",
                    "لم يتم العثور",
                    "expired",
                    "unavailable",
                ]
                if any(indicator in h1_text.lower() for indicator in error_indicators):
                    return True  # It's expired

        return False  # Valid URL

    except Exception as e:
        logger.warning(f"Error checking URL {url[:50]}: {e}")
        return False  # Assume valid on error to be safe
    finally:
        await page.close()
        await context.close()


async def cleanup_expired_urls(
    db_path: str = "data/jobs.db", batch_size: int = 50, max_check: int = 100
):
    """
    Check unscraped URLs and mark expired ones as processed

    Args:
        db_path: Path to SQLite database
        batch_size: Number of URLs to check in parallel
        max_check: Maximum URLs to check (prevent long runtime)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get unscraped LinkedIn URLs
    cursor.execute(
        """
        SELECT url FROM job_urls
        WHERE platform = 'linkedin' AND scraped = 0
        LIMIT ?
    """,
        (max_check,),
    )

    unscraped_urls = [row[0] for row in cursor.fetchall()]
    logger.info(
        f"🔍 Checking {len(unscraped_urls)} unscraped LinkedIn URLs for expiration..."
    )

    if not unscraped_urls:
        logger.info("✅ No unscraped URLs to check")
        conn.close()
        return

    expired_count = 0
    valid_count = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )  # Always visible browser to avoid rate limits

        # Process in batches
        for i in range(0, len(unscraped_urls), batch_size):
            batch = unscraped_urls[i : i + batch_size]
            logger.info(
                f"📦 Processing batch {i // batch_size + 1}/{(len(unscraped_urls) - 1) // batch_size + 1}..."
            )

            # Check each URL in batch sequentially (avoid overwhelming LinkedIn)
            for url in batch:
                is_expired = await check_if_url_expired(url, browser)

                if is_expired:
                    # Mark as scraped to skip in future
                    cursor.execute(
                        """
                        UPDATE job_urls
                        SET scraped = 1
                        WHERE url = ?
                    """,
                        (url,),
                    )
                    conn.commit()
                    expired_count += 1
                    logger.info(f"🗑️  Marked expired: {url[:70]}")
                else:
                    valid_count += 1
                    logger.info(f"✅ Valid: {url[:70]}")

                # Brief delay between checks
                await asyncio.sleep(2)

        await browser.close()

    conn.close()

    logger.info(f"\n✅ Cleanup complete:")
    logger.info(f"   🗑️  Expired (marked as processed): {expired_count}")
    logger.info(f"   ✅ Valid URLs remaining: {valid_count}")
    logger.info(f"   Total checked: {expired_count + valid_count}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean up expired LinkedIn job URLs")
    parser.add_argument("--db", default="data/jobs.db", help="Database path")
    parser.add_argument("--batch", type=int, default=50, help="Batch size")
    parser.add_argument("--max", type=int, default=100, help="Maximum URLs to check")

    args = parser.parse_args()

    asyncio.run(cleanup_expired_urls(args.db, args.batch, args.max))
