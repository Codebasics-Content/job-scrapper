"""Demo: Detail Page Navigation with Playwright
Shows how scrapers go INSIDE each job to get full descriptions
"""
import asyncio
import logging
from bs4 import BeautifulSoup

from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.analysis.skill_extraction import extract_skills_from_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("\n" + "="*80)
    logger.info("DEMO: Detail Page Navigation - Going INSIDE Each Job")
    logger.info("="*80 + "\n")
    
    # Example job URLs to visit (you can add real URLs here)
    job_urls = [
        "https://www.naukri.com/job-listings-ai-engineer-accenture-bengaluru-3-to-8-years-130125500879",
        "https://www.naukri.com/job-listings-senior-ai-engineer-ibm-pune-5-to-10-years-130125501234"
    ]
    
    async with PlaywrightBrowser(headless=False) as browser:
        for idx, url in enumerate(job_urls, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Job {idx}: Navigating INSIDE job page...")
            logger.info(f"URL: {url}")
            logger.info(f"{'='*60}")
            
            try:
                # Navigate INSIDE the job detail page
                html = await browser.render_url(url, wait_seconds=3.0)
                
                if not html:
                    logger.warning(f"⚠️ No HTML returned for job {idx}")
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract FULL job description from detail page
                desc_selectors = [
                    "div.styles_JDC__dang-inner-html__h0K4t",
                    "div.job-description",
                    "div[class*='description']"
                ]
                
                full_description = ""
                for selector in desc_selectors:
                    desc_elem = soup.select_one(selector)
                    if desc_elem:
                        full_description = desc_elem.get_text(strip=True)
                        break
                
                if full_description:
                    logger.info(f"\n✅ FULL Description Extracted:")
                    logger.info(f"   Length: {len(full_description)} characters")
                    logger.info(f"   Preview: {full_description[:200]}...")
                    
                    # Extract skills from FULL description
                    skills = extract_skills_from_text(full_description)
                    logger.info(f"\n🎯 Skills Extracted: {len(skills)} skills")
                    logger.info(f"   Skills: {', '.join(skills[:10])}")
                else:
                    logger.warning(f"⚠️ Could not extract description")
                
            except Exception as e:
                logger.error(f"❌ Error processing job {idx}: {e}")
    
    logger.info("\n" + "="*80)
    logger.info("DEMO COMPLETE: This is how unified scrapers work!")
    logger.info("They navigate INSIDE each job page to get full descriptions")
    logger.info("="*80)


if __name__ == "__main__":
    asyncio.run(main())
