"""LinkedIn n+5 Rolling Window - Continuous Processing
Job n completes → Job n+5 starts (1→6, 2→7, 3→8...)
"""
from __future__ import annotations

import asyncio
import logging
from typing import List
from playwright.async_api import async_playwright, BrowserContext
from src.models.models import JobDetailModel, JobUrlModel
from src.db.operations import JobStorageOperations
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
from .selector_config import DETAIL_SELECTORS, WAIT_TIMEOUTS

logger = logging.getLogger(__name__)


async def scrape_job_with_validation(
    idx: int,
    url_model: JobUrlModel,
    context: BrowserContext,
    extractor: AdvancedSkillExtractor,
    db_ops: JobStorageOperations,
    platform: str,
) -> JobDetailModel | None:
    """Scrape→Extract→Validate→Store (Edge case safe)"""
    page = None
    try:
        page = await context.new_page()
        logger.info(f"🔍 [{idx+1}] {url_model.url}")
        
        # Navigation with timeout handling
        try:
            await page.goto(url_model.url, timeout=WAIT_TIMEOUTS["navigation"], wait_until='domcontentloaded')
            await asyncio.sleep(2)
        except Exception as nav_err:
            logger.warning(f"⚠️ [{idx+1}] SKIPPED: Navigation failed - {nav_err}")
            return None
        
        # Extract with selector timeout
        desc_elem = await page.query_selector(DETAIL_SELECTORS["description"][0])
        description = await desc_elem.inner_text() if desc_elem else ""
        
        # Validate description
        if len(description.strip()) < 50:
            logger.warning(f"⚠️ [{idx+1}] SKIPPED: Description too short ({len(description)} chars)")
            return None
        
        # Extract skills with error handling
        try:
            skills = extractor.extract(description)
            cleaned_skills = [s for s in skills if isinstance(s, str) and len(s) > 1]
        except Exception as extract_err:
            logger.warning(f"⚠️ [{idx+1}] SKIPPED: Skill extraction failed - {extract_err}")
            return None
        
        # Validate skills
        if len(cleaned_skills) == 0:
            logger.warning(f"⚠️ [{idx+1}] SKIPPED: No valid skills")
            return None
        
        logger.info(f"🔧 [{idx+1}] Skills: {len(cleaned_skills)} → {cleaned_skills[:3]}...")
        
        # Store with database error handling
        job = JobDetailModel(
            job_id=url_model.job_id, platform=platform,
            actual_role=url_model.actual_role, url=url_model.url,
            job_description=description,
            skills=','.join(cleaned_skills),
            company_name="", posted_date=None
        )
        try:
            db_ops.store_details([job])
            logger.info(f"✅ [{idx+1}] VALIDATED & STORED")
            return job
        except Exception as db_err:
            logger.error(f"❌ [{idx+1}] Database storage failed: {db_err}")
            return None
    except Exception as e:
        logger.error(f"❌ [{idx+1}] Unexpected error: {e}")
        return None
    finally:
        if page:
            try:
                await page.close()
            except Exception:
                pass  # Ignore cleanup errors


async def rolling_window_n_plus_5(
    platform: str,
    input_role: str,
    total_jobs: int = 1000,
    window_size: int = 5,
    headless: bool = False,
) -> List[JobDetailModel]:
    """n+5 Rolling: Job n done → Job n+5 starts (1→6, 2→7, 3→8...)"""
    db_ops = JobStorageOperations()
    
    # Initialize extractor with error handling
    try:
        extractor = AdvancedSkillExtractor('src/config/skills_reference_2025.json')
    except Exception as e:
        logger.error(f"❌ Failed to load skills reference: {e}")
        return []
    
    url_models = db_ops.get_urls_to_scrape(platform, total_jobs)
    if not url_models:
        return []
    
    logger.info(f"🚀 n+5 Rolling: {len(url_models)} jobs, window={window_size}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        results: List[JobDetailModel | None] = []
        queue = asyncio.Queue()
        
        # Fill queue with ALL job indices
        for i in range(len(url_models)):
            await queue.put(i)
        
        async def worker():
            """Worker: Process jobs from queue (n+5 pattern)"""
            while not queue.empty():
                idx = await queue.get()
                job = await scrape_job_with_validation(
                    idx, url_models[idx], context, extractor, db_ops, platform
                )
                results.append(job)
        
        # Launch window_size workers (n+5 auto-managed)
        workers = [asyncio.create_task(worker()) for _ in range(window_size)]
        await asyncio.gather(*workers)
        
        await context.close()
        await browser.close()
    
    successful = [j for j in results if j is not None]
    logger.info(f"\n✅ Complete: {len(successful)}/{len(url_models)} jobs")
    return successful
