"""Capture Naukri API headers from browser network requests"""
import asyncio
from playwright.async_api import async_playwright


async def capture_api_headers():
    """Intercept network requests to capture API headers"""
    
    captured_headers = {}
    
    async def handle_request(route, request):
        # Capture headers from API requests
        if "jobapi" in request.url:
            print(f"\n🔍 API Request: {request.url}")
            print(f"Headers: {request.headers}")
            captured_headers.update(request.headers)
        await route.continue_()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Intercept requests
        await page.route("**/*", handle_request)
        
        # Navigate directly to job search results page (triggers API calls)
        print("Navigating to job search results...")
        search_url = "https://www.naukri.com/python-developer-jobs?k=python%20developer"
        await page.goto(search_url, wait_until="networkidle")
        
        # Wait for API calls to complete
        print("Waiting for API calls...")
        await asyncio.sleep(5)
        
        print(f"\n✅ Captured Headers:")
        for key, value in captured_headers.items():
            if key.lower() in ['appid', 'systemid', 'app-id', 'system-id']:
                print(f"  {key}: {value}")
        
        await browser.close()
        return captured_headers


if __name__ == "__main__":
    headers = asyncio.run(capture_api_headers())
    print(f"\nAll captured: {len(headers)} headers")
