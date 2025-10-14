"""Minimal Naukri API test to diagnose 400 error"""
import asyncio
import httpx
from playwright.async_api import async_playwright


async def test_minimal_naukri_api():
    """Test Naukri API with minimal parameters and proper headers"""
    
    # Test 1: Direct API call without authentication
    print("Test 1: Direct API call (likely to fail)")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.naukri.com/jobapi/v3/search",
            params={"keyword": "Python Developer"},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://www.naukri.com/",
            },
            timeout=10.0
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Jobs found: {len(response.json().get('jobDetails', []))}")
        else:
            print(f"Error: {response.text[:200]}")
    
    # Test 2: With browser session transfer
    print("\nTest 2: With Playwright browser session")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to Naukri homepage
        await page.goto("https://www.naukri.com/", wait_until="networkidle")
        await asyncio.sleep(2)
        
        # Get cookies
        cookies = await context.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        
        # Test API with session cookies
        async with httpx.AsyncClient(cookies=cookie_dict) as client:
            response = await client.get(
                "https://www.naukri.com/jobapi/v3/search",
                params={"keyword": "Python Developer"},
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json",
                    "Referer": "https://www.naukri.com/",
                },
                timeout=10.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Jobs found: {len(data.get('jobDetails', []))}")
                if data.get('jobDetails'):
                    print(f"Sample job: {data['jobDetails'][0].get('title', 'N/A')}")
            else:
                print(f"Error: {response.text[:200]}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_minimal_naukri_api())
