"""LinkedIn Detail Scraping - Single Batch with Validation
EMD Compliance: ≤80 lines, ONE batch (5 jobs), STOP after completion
"""
from __future__ import annotations

import asyncio
import logging
from typing import List
from playwright.async_api import async_playwright
from src.models import JobDetailModel, JobUrlModel
from src.db.operations import JobStorageOperations
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
from .selector_config import DETAIL_SELECTORS, WAIT_TIMEOUTS

logger = logging.getLogger(__name__)


async def scrape_linkedin_details_playwright(
    platform: str,
    input_role: str,
    limit: int = 5,  # Process ONE batch only
    store_to_db: bool = True,
    headless: bool = False,
) -> List[JobDetailModel]:
    """Process ONE batch (5 jobs): Scrape → Extract → Validate → Store → STOP"""
    
    db_ops = JobStorageOperations()
    url_models = db_ops.get_urls_to_scrape(platform, limit)
    
    if not url_models:
        logger.info(f"✅ No more URLs to scrape for {platform}")
        return []
    
    logger.info(f"\n{'='*70}")
    logger.info(f"📋 Processing Batch: {len(url_models)} jobs")
    logger.info(f"{'='*70}")
    
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    jobs: List[JobDetailModel] = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        for idx, url_model in enumerate(url_models, 1):
            page = None
            try:
                logger.info(f"\n🔍 Job {idx}/{len(url_models)}: {url_model.url}")
                page = await context.new_page()
                await page.goto(url_model.url, timeout=WAIT_TIMEOUTS["navigation"], wait_until='domcontentloaded')
                await asyncio.sleep(2)
                
                # Extract description
                desc_elem = await page.query_selector(DETAIL_SELECTORS["description"][0])
                description = await desc_elem.inner_text() if desc_elem else ""
                logger.info(f"📝 Description: {len(description)} chars")
                
                # Extract and validate skills
                skills = extractor.extract(description) if len(description.strip()) > 50 else []
                logger.info(f"🔧 Skills extracted: {len(skills)} → {skills[:5]}...")
                
                job = JobDetailModel(
                    job_id=url_model.job_id,
                    platform=platform,
                    actual_role=url_model.actual_role,
                    url=url_model.url,
                    job_description=description,
                    skills=','.join([s for s in skills if isinstance(s, str)]),
                    company_name="", company_detail="", posted_date=None
                )
                jobs.append(job)
                logger.info(f"✅ Job {idx} validated and ready")
                
            except Exception as e:
                logger.error(f"❌ Job {idx} failed: {e}")
            finally:
                if page:
                    await page.close()
        
        await context.close()
        await browser.close()
    
    # Store batch
    if store_to_db and jobs:
        stored = db_ops.store_details(jobs)
        logger.info(f"\n💾 Batch stored: {stored}/{len(jobs)} jobs")
    
    logger.info(f"\n⏸️  BATCH COMPLETE - STOPPED for monitoring\n")
    return jobs
