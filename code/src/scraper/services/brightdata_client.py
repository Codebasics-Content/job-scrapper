"""BrightData Scraping Browser client with captcha solving"""
from __future__ import annotations
import os
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page


class BrightDataClient:
    """Client for BrightData Scraping Browser with automatic captcha solving"""
    
    def __init__(self):
        self.browser_url = os.getenv("BRIGHTDATA_BROWSER_URL", "")
        if not self.browser_url:
            raise ValueError("BRIGHTDATA_BROWSER_URL not configured")
        
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object) -> None:
        await self.disconnect()
    
    async def connect(self):
        """Connect to BrightData Scraping Browser"""
        if self.browser:
            return
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.connect_over_cdp(
            self.browser_url
        )
    
    async def disconnect(self):
        """Disconnect from browser"""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
    
    async def render_with_captcha_solving(
        self, 
        url: str, 
        timeout: int = 120000
    ) -> str:
        """Render URL with automatic captcha detection and solving"""
        if not self.browser:
            await self.connect()
        
        assert self.browser is not None, "Browser connection failed"
        page: Page = await self.browser.new_page()
        
        try:
            # Create CDP session for captcha solving
            client = await page.context.new_cdp_session(page)
            
            # Navigate to URL
            await page.goto(url, timeout=timeout)
            
            # Wait for captcha detection and automatic solving
            try:
                result = await client.send('Captcha.waitForSolve', {
                    'detectTimeout': 10000,
                })
                print(f"Captcha solved: {result.get('status', 'ok')}")
            except Exception:
                pass  # No captcha detected, continue
            
            # Return rendered HTML
            return await page.content()
        
        finally:
            await page.close()
