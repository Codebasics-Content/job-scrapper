"""E2E Test: Naukri + Indeed Skills Extraction with Analysis
Tests complete pipeline: Scraping → Job Models → Skills Extraction → Statistical Analysis
"""
import asyncio
import logging
from bs4 import BeautifulSoup

from src.scraper.services.playwright_browser import PlaywrightBrowser
from src.models import JobModel
from src.analysis.skill_extraction import extract_skills_from_text
from src.analysis.skill_statistics import calculate_skill_percentages, get_top_skills
from src.analysis.statistics import generate_skill_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def scrape_naukri_jobs(limit: int = 10) -> list[JobModel]:
    """Scrape Naukri jobs and create JobModel instances"""
    jobs: list[JobModel] = []
    
    async with PlaywrightBrowser(headless=False) as browser:
        url = "https://www.naukri.com/ai-engineer-jobs?k=AI+Engineer&l=India"
        html = await browser.render_url(url, wait_seconds=5.0)
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select(".cust-job-tuple")[:limit]
        
        logger.info(f"✅ Naukri: Found {len(job_cards)} job cards")
        
        for idx, card in enumerate(job_cards, 1):
            try:
                # Extract metadata
                title_elem = card.select_one(".title")
                company_elem = card.select_one(".comp-name")
                exp_elem = card.select_one(".expwdth")
                location_elem = card.select_one(".locWdth")
                desc_elem = card.select_one(".job-desc")
                
                title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                experience = exp_elem.get_text(strip=True) if exp_elem else "Not specified"
                location = location_elem.get_text(strip=True) if location_elem else "India"
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract skills from description
                skills_list = extract_skills_from_text(description)
                skills_str = ", ".join(skills_list) if skills_list else "None"
                
                # Create JobModel
                job = JobModel(
                    job_id=f"naukri_{idx}",
                    Job_Role=title,
                    Company=company,
                    Experience=experience,
                    Skills=skills_str,
                    jd=description,
                    platform="Naukri",
                    location=location
                )
                jobs.append(job)
                logger.info(f"  [{idx}] {title} @ {company} - {len(skills_list)} skills extracted")
                
            except Exception as e:
                logger.error(f"Failed to parse Naukri job {idx}: {e}")
    
    return jobs


async def scrape_indeed_jobs(limit: int = 10) -> list[JobModel]:
    """Scrape Indeed jobs and create JobModel instances"""
    jobs: list[JobModel] = []
    
    async with PlaywrightBrowser(headless=False) as browser:
        url = "https://www.indeed.com/jobs?q=AI+Engineer&l=India"
        html = await browser.render_url(url, wait_seconds=5.0, timeout_ms=60000)
        
        if not html:
            logger.warning("⚠️ Indeed timeout/blocked")
            return jobs
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select("div.job_seen_beacon")[:limit]
        
        logger.info(f"✅ Indeed: Found {len(job_cards)} job cards")
        
        for idx, card in enumerate(job_cards, 1):
            try:
                # Extract metadata
                title_elem = card.select_one("h2.jobTitle span")
                company_elem = card.select_one("[data-testid='company-name']")
                location_elem = card.select_one("[data-testid='text-location']")
                desc_elem = card.select_one("div.job-snippet")
                
                title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                location = location_elem.get_text(strip=True) if location_elem else "India"
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract skills from description
                skills_list = extract_skills_from_text(description)
                skills_str = ", ".join(skills_list) if skills_list else "None"
                
                # Create JobModel
                job = JobModel(
                    job_id=f"indeed_{idx}",
                    Job_Role=title,
                    Company=company,
                    Experience="Not specified",
                    Skills=skills_str,
                    jd=description,
                    platform="Indeed",
                    location=location
                )
                jobs.append(job)
                logger.info(f"  [{idx}] {title} @ {company} - {len(skills_list)} skills extracted")
                
            except Exception as e:
                logger.error(f"Failed to parse Indeed job {idx}: {e}")
    
    return jobs


async def main():
    logger.info("\n" + "="*80)
    logger.info("E2E TEST: Naukri + Indeed Skills Extraction & Analysis")
    logger.info("="*80 + "\n")
    
    # Step 1: Scrape jobs from both platforms
    logger.info("📥 STEP 1: Scraping Jobs...")
    naukri_jobs = await scrape_naukri_jobs(limit=10)
    indeed_jobs = await scrape_indeed_jobs(limit=10)
    all_jobs = naukri_jobs + indeed_jobs
    
    logger.info(f"\n✅ Total Jobs Scraped: {len(all_jobs)} (Naukri: {len(naukri_jobs)}, Indeed: {len(indeed_jobs)})")
    
    if not all_jobs:
        logger.error("❌ No jobs scraped. Exiting.")
        return
    
    # Step 2: Calculate skill percentages using formula
    logger.info("\n📊 STEP 2: Calculating Skill Percentages...")
    skill_percentages = calculate_skill_percentages(all_jobs)
    logger.info(f"✅ Calculated percentages for {len(skill_percentages)} unique skills")
    
    # Step 3: Get top skills
    logger.info("\n🏆 STEP 3: Top 10 Skills by Occurrence...")
    top_skills = get_top_skills(all_jobs, top_n=10)
    for rank, (skill, percentage) in enumerate(top_skills, 1):
        logger.info(f"  {rank}. {skill}: {percentage}%")
    
    # Step 4: Generate comprehensive report
    logger.info("\n📈 STEP 4: Generating Skill Report...")
    report = generate_skill_report(all_jobs, min_percentage=5.0)
    logger.info(f"  Total Jobs: {report['total_jobs']}")
    logger.info(f"  Total Skills: {report['total_skills']}")
    logger.info(f"  Skills >5%: {report['analyzed_skills']}")
    logger.info(f"  Platform Distribution: {report['platform_distribution']}")
    
    # Step 5: Platform-specific analysis
    logger.info("\n🔍 STEP 5: Platform-Specific Top Skills...")
    if naukri_jobs:
        naukri_top = get_top_skills(naukri_jobs, top_n=5)
        logger.info(f"\n  Naukri Top 5:")
        for rank, (skill, percentage) in enumerate(naukri_top, 1):
            logger.info(f"    {rank}. {skill}: {percentage}%")
    
    if indeed_jobs:
        indeed_top = get_top_skills(indeed_jobs, top_n=5)
        logger.info(f"\n  Indeed Top 5:")
        for rank, (skill, percentage) in enumerate(indeed_top, 1):
            logger.info(f"    {rank}. {skill}: {percentage}%")
    
    logger.info("\n" + "="*80)
    logger.info("✅ E2E TEST COMPLETE")
    logger.info("="*80)


if __name__ == "__main__":
    asyncio.run(main())
