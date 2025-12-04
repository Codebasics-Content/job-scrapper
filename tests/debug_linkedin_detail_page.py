"""Debug LinkedIn Job Detail Page Selectors (2025)
Find current working selectors for job description and other fields
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.async_api import async_playwright

async def debug_job_detail_page():
    """Open a LinkedIn job detail page and find working selectors"""
    
    # Use the first URL from your scraping queue
    test_url = "https://www.linkedin.com/jobs/view/4314587136"
    
    print(f"🔍 Testing selectors for: {test_url}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Visible browser
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        print("🌐 Navigating to job page...")
        await page.goto(test_url, timeout=30000, wait_until="domcontentloaded")
        
        # Wait for page to fully load
        await asyncio.sleep(3)
        
        # Take screenshot
        await page.screenshot(path="tests/linkedin_detail_debug.png", full_page=True)
        print("📸 Screenshot saved: tests/linkedin_detail_debug.png\n")
        
        # Check if login wall appears
        print("🔐 Checking for login wall...")
        login_selectors = [
            "form[class*='login']",
            "div[class*='authwall']",
            "button[class*='sign-in']",
            "a[href*='/login']"
        ]
        for selector in login_selectors:
            if await page.query_selector(selector):
                print(f"⚠️  LOGIN WALL DETECTED: {selector}")
                print("❌ LinkedIn requires authentication. Job details not accessible without login.\n")
                break
        
        print("=" * 70)
        print("TESTING JOB DESCRIPTION SELECTORS:")
        print("=" * 70)
        
        # Old selectors from config
        old_selectors = [
            ".show-more-less-html__markup",
            ".description__text",
            ".jobs-description__content",
        ]
        
        # Additional possible selectors (2025 LinkedIn structure)
        new_selectors = [
            "div[class*='description']",
            "article[class*='description']",
            "section[class*='description']",
            "div.jobs-box__html-content",
            "div.jobs-description",
            "div#job-details",
            "div[data-test-id*='description']",
            ".jobs-unified-top-card__job-insight",
            "div.mt4",  # Common class for description container
        ]
        
        all_selectors = old_selectors + new_selectors
        found_description = False
        
        for selector in all_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    text = await element.inner_text()
                    if text and len(text.strip()) > 50:  # Valid description
                        print(f"✅ WORKING: {selector}")
                        print(f"   Text length: {len(text)} chars")
                        print(f"   Preview: {text[:100]}...\n")
                        found_description = True
                    else:
                        print(f"⚠️  FOUND BUT EMPTY: {selector}\n")
                else:
                    print(f"❌ NOT FOUND: {selector}")
            except Exception as e:
                print(f"❌ ERROR: {selector} - {e}")
        
        if not found_description:
            print("\n⚠️  NO VALID DESCRIPTION SELECTOR FOUND!")
            print("Saving full page HTML for manual inspection...")
            html = await page.content()
            with open("tests/linkedin_detail_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("💾 HTML saved: tests/linkedin_detail_page.html")
        
        print("\n" + "=" * 70)
        print("TESTING OTHER SELECTORS:")
        print("=" * 70)
        
        # Test other important selectors
        test_cases = {
            "Job Title": ["h1", ".top-card-layout__title", "h1.t-24", "h2.t-24"],
            "Company Name": [
                "a.topcard__org-name-link",
                ".top-card-layout__second-subline a",
                ".job-details-jobs-unified-top-card__company-name",
                "div[class*='company'] a"
            ],
            "Posted Date": [
                ".job-details-jobs-unified-top-card__posted-date",
                ".jobs-unified-top-card__posted-date",
                "span[class*='posted']"
            ],
        }
        
        for field, selectors in test_cases.items():
            print(f"\n{field}:")
            for selector in selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        print(f"  ✅ {selector}: '{text.strip()[:50]}'")
                        break
                    else:
                        print(f"  ❌ {selector}")
                except Exception as e:
                    print(f"  ❌ {selector} - {e}")
        
        print("\n" + "=" * 70)
        print("⏸️  Browser will stay open for 30 seconds - manually inspect!")
        print("=" * 70)
        await asyncio.sleep(30)
        
        await browser.close()
        
        print("\n✅ Debug complete. Check saved files:")
        print("   - tests/linkedin_detail_debug.png")
        print("   - tests/linkedin_detail_page.html (if description not found)")

if __name__ == "__main__":
    asyncio.run(debug_job_detail_page())
