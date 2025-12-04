"""Playwright Browser Client - Real Browser Mode with Visual Verification
EMD Compliance: ≤80 lines, visual browser automation
"""
import asyncio
from typing import Optional, Literal
from types import TracebackType
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

import logging

logger = logging.getLogger(__name__)


class PlaywrightBrowser:
    """Direct Playwright browser with headless=False for visual verification"""
    
    browser: Optional[Browser]
    context: Optional[BrowserContext]
    
    def __init__(self, headless: bool = False, use_stealth: bool = False):
        self.headless = headless
        self.use_stealth = use_stealth
        self.browser = None
        self.context = None
        self.playwright = None
    
    async def __aenter__(self):
        """Launch browser with visual mode and optional stealth - WITH TIMEOUTS"""
        self.playwright = await async_playwright().start()

        try:
            self.browser = await asyncio.wait_for(
                self.playwright.chromium.launch(
                    headless=self.headless,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                ),
                timeout=30.0  # 30s timeout for browser launch
            )
        except asyncio.TimeoutError:
            logger.error("❌ Browser launch timed out after 30s")
            await self.playwright.stop()
            raise

        try:
            self.context = await asyncio.wait_for(
                self.browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ),
                timeout=10.0  # 10s timeout for context
            )
        except asyncio.TimeoutError:
            logger.error("❌ Context creation timed out after 10s")
            await self.browser.close()
            await self.playwright.stop()
            raise

        # Apply stealth if requested (Cloudflare bypass)
        if self.use_stealth:
            from playwright_stealth import stealth_async
            try:
                page = await asyncio.wait_for(self.context.new_page(), timeout=10.0)
                await stealth_async(page)
                await asyncio.wait_for(page.close(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("⚠️ Stealth setup timed out, continuing without stealth")

        logger.info(f"Browser launched (headless={self.headless}, stealth={self.use_stealth})")
        return self
    
    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        """Cleanup browser resources WITH TIMEOUTS"""
        if self.context:
            try:
                await asyncio.wait_for(self.context.close(), timeout=10.0)
            except Exception:
                pass  # Ignore cleanup errors
        if self.browser:
            try:
                await asyncio.wait_for(self.browser.close(), timeout=10.0)
            except Exception:
                pass
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser closed")

    async def new_page(self) -> Page:
        """Create new page in current context WITH TIMEOUT"""
        if not self.context:
            raise RuntimeError("Browser context not initialized")
        page = await asyncio.wait_for(self.context.new_page(), timeout=10.0)
        return page
    
    async def get_cookies(self) -> list[dict[str, str]]:
        """Get cookies from browser context"""
        if not self.context:
            raise RuntimeError("Browser context not initialized")
        cookies = await self.context.cookies()
        return [{k: str(v) for k, v in cookie.items()} for cookie in cookies]
    
    async def render_url(self, url: str, wait_seconds: float = 3.0, timeout_ms: int = 60000, wait_until: Literal['commit', 'domcontentloaded', 'load', 'networkidle'] = 'networkidle') -> str:
        """Render URL with error handling and configurable timeout"""
        page = await self.new_page()
        try:
            # Add hard timeout wrapper for entire render operation
            await asyncio.wait_for(
                page.goto(url, wait_until=wait_until, timeout=timeout_ms),
                timeout=(timeout_ms / 1000) + 5.0  # Slightly longer than Playwright timeout
            )
            await asyncio.sleep(wait_seconds)
            html = await page.content()
            logger.info(f"✅ Rendered {url}: {len(html)} chars")
            return html
        except asyncio.TimeoutError:
            logger.error(f"❌ Hard timeout rendering {url}")
            return ""
        except Exception as e:
            logger.error(f"❌ Failed to render {url}: {e}")
            return ""
        finally:
            try:
                await asyncio.wait_for(page.close(), timeout=5.0)
            except Exception:
                pass  # Ignore cleanup errors
