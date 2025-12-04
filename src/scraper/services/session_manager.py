"""Playwright Session Manager - Cookie Extraction
Establishes authenticated browser session for API use
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict

from playwright.async_api import Browser, BrowserContext, async_playwright

logger = logging.getLogger(__name__)


async def create_authenticated_session(
    headless: bool = False,  # Always visible browser to avoid rate limits
) -> tuple[Browser, BrowserContext, Dict[str, str]]:
    """Create Playwright session and extract cookies

    Returns:
        (browser, context, cookies) for API client transfer
    """
    playwright = await async_playwright().start()

    try:
        browser = await asyncio.wait_for(
            playwright.chromium.launch(headless=headless),
            timeout=30.0  # 30s timeout for browser launch
        )
    except asyncio.TimeoutError:
        logger.error("❌ Browser launch timed out after 30s")
        await playwright.stop()
        raise

    try:
        context = await asyncio.wait_for(
            browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            ),
            timeout=10.0  # 10s timeout for context
        )
    except asyncio.TimeoutError:
        logger.error("❌ Context creation timed out after 10s")
        await browser.close()
        await playwright.stop()
        raise

    # Navigate to establish session WITH TIMEOUT
    try:
        page = await asyncio.wait_for(context.new_page(), timeout=10.0)
        await asyncio.wait_for(
            page.goto("https://www.naukri.com", wait_until="networkidle", timeout=30000),
            timeout=35.0  # Slightly longer than Playwright timeout
        )
    except asyncio.TimeoutError:
        logger.error("❌ Navigation to Naukri timed out")
        await context.close()
        await browser.close()
        await playwright.stop()
        raise

    # Extract cookies as dict for httpx
    raw_cookies = await context.cookies()
    cookies: Dict[str, str] = {
        str(c.get("name", "")): str(c.get("value", "")) for c in raw_cookies
    }
    logger.info(f"Extracted {len(cookies)} cookies from session")

    return browser, context, cookies


async def close_session(browser: Browser, context: BrowserContext) -> None:
    """Cleanup browser session with timeouts"""
    try:
        await asyncio.wait_for(context.close(), timeout=10.0)
    except Exception:
        pass  # Ignore cleanup errors
    try:
        await asyncio.wait_for(browser.close(), timeout=10.0)
    except Exception:
        pass  # Ignore cleanup errors
