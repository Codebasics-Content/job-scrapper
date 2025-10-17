"""Test LinkedIn selectors and take screenshot for debugging"""
import asyncio
from playwright.async_api import async_playwright

async def test_linkedin_page():
    """Open LinkedIn jobs page and take screenshot"""
    keyword = "Python Developer"
    location = "United States"
    
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '+')}&location={location.replace(' ', '+')}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Visible browser
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        print(f"🌐 Opening: {search_url}")
        await page.goto(search_url, timeout=60000)
        
        # Wait a bit for page to load
        await asyncio.sleep(5)
        
        # Take screenshot
        await page.screenshot(path="linkedin_page.png", full_page=True)
        print("📸 Screenshot saved: linkedin_page.png")
        
        # Try to find job listings with various possible selectors
        possible_selectors = [
            "li.jobs-search-results__list-item",
            "div.jobs-search-results-list",
            "ul.jobs-search__results-list",
            "div.job-card-container",
            "div[class*='job']",
            "li[class*='job']",
        ]
        
        for selector in possible_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with: {selector}")
                else:
                    print(f"❌ No elements with: {selector}")
            except Exception as e:
                print(f"❌ Error with {selector}: {e}")
        
        # Get page HTML for analysis
        html = await page.content()
        with open("linkedin_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("💾 HTML saved: linkedin_page.html")
        
        # Keep browser open for manual inspection
        print("\n⏸️  Browser will stay open for 60 seconds - inspect the page!")
        await asyncio.sleep(60)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_linkedin_page())
