"""Playwright Session Manager - Cookie Extraction
Establishes authenticated browser session for API use
"""
from __future__ import annotations
from playwright.async_api import async_playwright, Browser, BrowserContext
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


async def create_authenticated_session(
    headless: bool = True
) -> tuple[Browser, BrowserContext, List[Dict[str, Any]]]:
    """Create Playwright session and extract cookies
    
    Returns:
        (browser, context, cookies) for API client transfer
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    )
    
    # Navigate to establish session
    page = await context.new_page()
    await page.goto("https://www.naukri.com", wait_until="networkidle")
    
    # Extract cookies for API transfer
    cookies = await context.cookies()
    logger.info(f"Extracted {len(cookies)} cookies from session")
    
    return browser, context, cookies


async def close_session(
    browser: Browser, context: BrowserContext
) -> None:
    """Cleanup browser session"""
    await context.close()
    await browser.close()
