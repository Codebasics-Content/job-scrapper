"""Debug Naukri HTML structure"""
import asyncio
from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.scraper.unified.naukri.url_builder import build_search_url

async def main():
    search_url = build_search_url("AI Engineer", "India", page=1)
    print(f"URL: {search_url}\n")
    
    async with PlaywrightBrowser(headless=False) as browser:
        html = await browser.render_url(search_url, wait_seconds=8.0)
        
        # Save HTML for inspection
        with open("naukri_debug_page1.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"HTML length: {len(html)} chars")
        print(f"Saved to: naukri_debug_page1.html")
        print(f"\nFirst 500 chars:\n{html[:500]}")

if __name__ == "__main__":
    asyncio.run(main())
