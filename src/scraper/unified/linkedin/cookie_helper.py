# LinkedIn Cookie Helper - Login via Playwright's Chromium and save cookies
# Opens browser for manual login, then saves cookies for scraping

import asyncio
import json
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = str(Path(__file__).resolve().parents[4])
sys.path.insert(0, PROJECT_ROOT)


async def login_and_save_cookies(cookie_file: str = "linkedin_cookies.json") -> bool:
    """
    Open Playwright Chromium for manual LinkedIn login.
    After user logs in, saves cookies to file.

    Returns True if cookies were saved successfully.
    """
    from playwright.async_api import async_playwright

    print("=" * 60)
    print("🔐 LinkedIn Cookie Helper")
    print("=" * 60)
    print()
    print("1. A Chromium browser will open")
    print("2. Login to LinkedIn manually")
    print("3. Once logged in, the cookies will be saved automatically")
    print("4. Close this window when done")
    print()
    print("=" * 60)

    async with async_playwright() as p:
        # Launch visible browser
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            no_viewport=True  # Use full window size
        )

        page = await context.new_page()

        # Navigate to LinkedIn login
        await page.goto("https://www.linkedin.com/login")

        print()
        print("👆 Please login to LinkedIn in the browser window...")
        print("   Waiting for successful login...")
        print()

        # Wait for successful login (redirect to feed or home)
        try:
            # Wait up to 5 minutes for user to login
            await page.wait_for_url(
                lambda url: "/feed" in url or "/home" in url or "/mynetwork" in url,
                timeout=300000  # 5 minutes
            )

            print("✅ Login detected! Saving cookies...")

            # Get all cookies
            cookies = await context.cookies()

            # Filter for LinkedIn cookies
            linkedin_cookies = [
                c for c in cookies
                if "linkedin.com" in c.get("domain", "")
            ]

            # Save to file
            cookie_path = os.path.join(PROJECT_ROOT, cookie_file)
            with open(cookie_path, "w") as f:
                json.dump(linkedin_cookies, f, indent=2)

            print(f"✅ Saved {len(linkedin_cookies)} cookies to {cookie_file}")

            # Check for important cookies
            cookie_names = [c.get("name", "") for c in linkedin_cookies]
            if "li_at" in cookie_names:
                print("✅ li_at cookie found (session token)")
            else:
                print("⚠️ Warning: li_at cookie not found!")

            if "JSESSIONID" in cookie_names:
                print("✅ JSESSIONID cookie found")

            print()
            print("=" * 60)
            print("🎉 Cookies saved successfully!")
            print("   You can now close this browser and run the scraper.")
            print("=" * 60)

            # Keep browser open for a moment so user sees the message
            await asyncio.sleep(3)

            await browser.close()
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            await browser.close()
            return False


def run_login_helper():
    """Synchronous wrapper to run the login helper"""
    return asyncio.run(login_and_save_cookies())


if __name__ == "__main__":
    run_login_helper()
