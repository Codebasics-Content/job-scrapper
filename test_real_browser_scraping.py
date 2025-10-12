"""Real Browser E2E Test - Visual Verification Mode
Actual Chromium browser will popup for visual scraping validation
"""
import asyncio
import logging
from bs4 import BeautifulSoup

from src.scraper.services.playwright_browser import PlaywrightBrowser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_naukri_visual_scraping():
    """Test Naukri scraping with real browser"""
    logger.info("\n" + "="*60)
    logger.info("NAUKRI VISUAL SCRAPING TEST")
    logger.info("="*60)
    
    async with PlaywrightBrowser(headless=False) as browser:
        url = "https://www.naukri.com/ai-engineer-jobs?k=AI+Engineer&l=India"
        html = await browser.render_url(url, wait_seconds=5.0)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        selectors = ["article.jobTuple", ".cust-job-tuple", "article[data-job-id]"]
        job_cards = []
        
        for selector in selectors:
            job_cards = soup.select(selector)
            if job_cards:
                logger.info(f"✅ Found {len(job_cards)} cards with selector: {selector}")
                break
        
        if not job_cards:
            logger.warning("❌ No job cards found with any selector")
            logger.info(f"HTML preview (first 500 chars):\n{html[:500]}")
        else:
            logger.info(f"\nFirst card HTML preview:\n{job_cards[0].prettify()[:500]}")


async def test_indeed_visual_scraping():
    """Test Indeed scraping with real browser (skip on timeout)"""
    logger.info("\n" + "="*60)
    logger.info("INDEED VISUAL SCRAPING TEST")
    logger.info("="*60)
    
    async with PlaywrightBrowser(headless=False) as browser:
        url = "https://www.indeed.com/jobs?q=AI+Engineer&l=India"
        html = await browser.render_url(url, wait_seconds=5.0, timeout_ms=60000)
        
        if not html:
            logger.warning("⚠️ Indeed timeout/blocked - skipping (common for bot detection)")
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select("div.job_seen_beacon")
        
        logger.info(f"Found {len(job_cards)} job cards")
        if job_cards:
            logger.info(f"\nFirst card HTML preview:\n{job_cards[0].prettify()[:500]}")


async def test_linkedin_visual_scraping():
    """Test LinkedIn scraping with real browser"""
    logger.info("\n" + "="*60)
    logger.info("LINKEDIN VISUAL SCRAPING TEST")
    logger.info("="*60)
    
    async with PlaywrightBrowser(headless=False) as browser:
        url = "https://www.linkedin.com/jobs/search/?keywords=AI+Engineer&location=India"
        html = await browser.render_url(url, wait_seconds=5.0)
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select("li.jobs-search-results__list-item")
        
        logger.info(f"Found {len(job_cards)} job cards")
        if job_cards:
            logger.info(f"\nFirst card HTML preview:\n{job_cards[0].prettify()[:500]}")


async def run_all_tests():
    """Run all platform tests with real browser"""
    await test_naukri_visual_scraping()
    await asyncio.sleep(2)
    await test_indeed_visual_scraping()
    await asyncio.sleep(2)
    await test_linkedin_visual_scraping()


if __name__ == "__main__":
    asyncio.run(run_all_tests())
