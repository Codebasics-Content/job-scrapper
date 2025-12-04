#!/usr/bin/env python3
"""Save LinkedIn cookies for authenticated scraping

Run this script ONCE to login and save your LinkedIn session cookies.
The scraper will then use these cookies to bypass login walls.

Usage:
    python save_linkedin_cookies.py
"""
import asyncio
import json
from playwright.async_api import async_playwright

async def save_linkedin_cookies():
    """Login to LinkedIn and save cookies"""
    print("🌐 Opening LinkedIn login page...")
    print("⚠️  You will need to manually login in the browser window")
    print()
    
    async with async_playwright() as p:
        # Launch visible browser (headless=False required for manual login)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        # Navigate to LinkedIn login
        await page.goto("https://www.linkedin.com/login")
        
        print("=" * 60)
        print("⏸️  PAUSED: Please login to LinkedIn in the browser window")
        print("=" * 60)
        print()
        print("Steps:")
        print("1. Enter your email and password")
        print("2. Complete any verification (if asked)")
        print("3. Wait until you see your LinkedIn feed/homepage")
        print("4. Then come back here and press Enter")
        print()
        
        # Wait for user to login manually
        input("Press Enter AFTER you've successfully logged in to LinkedIn...")
        
        # Verify login by checking current URL
        current_url = page.url
        if "feed" in current_url or "mynetwork" in current_url or "jobs" in current_url:
            print("✅ Login detected! Saving cookies...")
        else:
            print(f"⚠️  Warning: Current URL doesn't look like LinkedIn homepage: {current_url}")
            print("Saving cookies anyway...")
        
        # Save cookies to file
        cookies = await context.cookies()
        cookie_file = '.linkedin_cookies.json'
        
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print()
        print("=" * 60)
        print(f"✅ SUCCESS! Cookies saved to {cookie_file}")
        print("=" * 60)
        print()
        print(f"📊 Saved {len(cookies)} cookies")
        print()
        print("Next steps:")
        print("1. Run your scraper: streamlit run streamlit_app.py")
        print("2. The scraper will automatically load these cookies")
        print("3. You should no longer see login walls!")
        print()
        print("⚠️  Important:")
        print("- Cookies expire after ~30 days - re-run this script if needed")
        print("- Never commit .linkedin_cookies.json to git (already in .gitignore)")
        print("- Keep this file secure - it contains your login session")
        print()
        
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(save_linkedin_cookies())
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure Playwright browsers are installed: playwright install chromium")
        print("- Check your internet connection")
        print("- Try again and make sure to complete the login")
