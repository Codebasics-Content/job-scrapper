"""Debug: Save rendered HTML to check actual structure"""
import asyncio
from src.scraper.services.headlessx_client import HeadlessXClient


async def debug_html():
    async with HeadlessXClient() as client:
        # Test Indeed
        indeed_url = "https://www.indeed.com/jobs?q=data+analyst&l=United+States"
        html = await client.render_url(indeed_url)
        
        with open("/tmp/indeed_debug.html", "w") as f:
            f.write(html)
        
        print(f"✅ Saved {len(html)} chars to /tmp/indeed_debug.html")
        print(f"Contains 'job': {'job' in html.lower()}")
        print(f"Contains 'data analyst': {'data analyst' in html.lower()}")
        
        # Show first job card class if exists
        if '<div class="job' in html or '<article' in html:
            print("✅ Found job-related elements")
        else:
            print("❌ No job elements found - likely bot detection")


asyncio.run(debug_html())
