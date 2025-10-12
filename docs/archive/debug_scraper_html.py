"""Debug HTML output to diagnose selector issues
EMD Compliance: ≤80 lines
"""
import asyncio
import logging
from src.scraper.services.playwright_browser import PlaywrightBrowser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def debug_html_output():
    """Capture and save actual HTML for debugging"""
    async with PlaywrightBrowser(headless=False) as browser:
        # Test Naukri
        naukri_url = "https://www.naukri.com/python-developer-jobs?k=Python+Developer&l=India"
        logger.info(f"Loading Naukri: {naukri_url}")
        naukri_html = await browser.render_url(naukri_url, wait_seconds=10.0)
        
        with open("debug_naukri_search.html", "w", encoding="utf-8") as f:
            f.write(naukri_html)
        logger.info(f"✅ Naukri HTML: {len(naukri_html)} chars saved to debug_naukri_search.html")
        
        # Test Indeed
        indeed_url = "https://www.indeed.com/jobs?q=Data+Engineer&l=United+States"
        logger.info(f"Loading Indeed: {indeed_url}")
        indeed_html = await browser.render_url(indeed_url, wait_seconds=10.0)
        
        with open("debug_indeed_search.html", "w", encoding="utf-8") as f:
            f.write(indeed_html)
        logger.info(f"✅ Indeed HTML: {len(indeed_html)} chars saved to debug_indeed_search.html")
        
        # Check for job card elements
        from bs4 import BeautifulSoup
        
        naukri_soup = BeautifulSoup(naukri_html, "html.parser")
        naukri_cards = len(naukri_soup.select("article.jobTuple"))
        logger.info(f"📊 Naukri: Found {naukri_cards} article.jobTuple cards")
        
        naukri_cards2 = len(naukri_soup.select(".cust-job-tuple"))
        logger.info(f"📊 Naukri: Found {naukri_cards2} .cust-job-tuple cards")
        
        indeed_soup = BeautifulSoup(indeed_html, "html.parser")
        indeed_cards = len(indeed_soup.select("div.job_seen_beacon"))
        logger.info(f"📊 Indeed: Found {indeed_cards} div.job_seen_beacon cards")
        
        indeed_cards2 = len(indeed_soup.select("div.jobsearch-SerpJobCard"))
        logger.info(f"📊 Indeed: Found {indeed_cards2} div.jobsearch-SerpJobCard cards")


if __name__ == "__main__":
    asyncio.run(debug_html_output())
