"""Sequential Job Detail Scraper - Single Worker with Prefetch Queue
Anti-detection: Processes 1 job at a time with human-like delays
"""
import asyncio
import logging
import random
from typing import List, Optional, cast
import os
from playwright.async_api import async_playwright, ProxySettings, Browser, BrowserContext
from src.models.models import JobDetailModel
from src.scraper.unified.linkedin.date_parser import parse_linkedin_date
from src.scraper.unified.linkedin.selector_config import DETAIL_SELECTORS
from src.analysis.skill_extraction.extractor import AdvancedSkillExtractor
from src.analysis.skill_extraction.skill_validator import SkillValidator

logger = logging.getLogger(__name__)

async def scrape_job_details_sequential(
    urls: List[tuple[str, str, str, str]],
    headless: bool = False,
    min_skills_confidence: float = 0.5,
    browser: Optional[Browser] = None,
    context: Optional[BrowserContext] = None,
    prefetch_size: int = 5
) -> List[JobDetailModel]:
    """Sequential scraper: 1 job at a time, prefetch queue of 5
    
    Args:
        prefetch_size: Number of jobs to keep in queue (default 5)
    """
    skills_validator = SkillsValidator()
    skill_extractor = AdvancedSkillExtractor("skills_reference_2025.json")
    proxy_url = os.getenv("PROXY_URL")
    proxy_config = None
    if proxy_url:
        parts = proxy_url.replace("http://", "").split("@")
        if len(parts) == 2:
            auth, server = parts
            username, password = auth.split(":")
            proxy_config = ProxySettings(
                server=f"http://{server}",
                username=username,
                password=password
            )
        else:
            server = parts[0]
            proxy_config = ProxySettings(server=f"http://{server}")
    
    from src.db.operations import JobStorageOperations
    
    job_details: List[JobDetailModel] = []
    p = None
    should_close = browser is None
    db_ops = JobStorageOperations()
    
    if browser is None:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=headless, proxy=proxy_config)
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    assert context is not None, "Browser context required"
    processed = 0
    
    for idx, url_tuple in enumerate(urls, 1):
        url = url_tuple[0]
        job_id = f"linkedin_{url.split('/')[-1]}"
        platform = url_tuple[1]
        actual_role = url_tuple[2]
        
        logger.info(f"🔄 [{idx}/{len(urls)}] Processing: {job_id[:40]}")
        
        # FASTEST human-like delay (2-4 seconds)
        if idx > 1:
            delay = random.uniform(2.0, 4.0)
            logger.info(f"⏳ Waiting {delay:.1f}s before next job")
            await asyncio.sleep(delay)
        
        page = None
        try:
            page = await context.new_page()
            
            async def fetch_job():
                assert page is not None
                await page.goto(url, timeout=30000)
                for selector in DETAIL_SELECTORS["description"]:
                    try:
                        await page.wait_for_selector(selector, timeout=5000)
                        return True
                    except Exception:
                        continue
                raise Exception("No description selector found")
            
            logger.info(f"🌐 Navigating to: {url[:50]}...")
            _, success = await retry_with_backoff(
                fetch_job, max_retries=3, operation_name=f"fetch_{job_id[:20]}"
            )
            
            if not success:
                logger.warning(f"⏭️  Skipped {job_id} - failed after retries")
                continue
            
            logger.info(f"✅ Page loaded for {job_id[:30]}")
            
            # Extract data
            logger.info(f"📝 Extracting description...")
            job_description = ""
            for selector in DETAIL_SELECTORS["description"]:
                desc_elem = await page.query_selector(selector)
                if desc_elem:
                    job_description = await desc_elem.inner_text()
                    logger.info(f"✅ Found description: {len(job_description)} chars")
                    break
            
            # Extract company name with fallback selectors
            company_name = ""
            for selector in DETAIL_SELECTORS["company_name"]:
                company_elem = await page.query_selector(selector)
                if company_elem:
                    company_name = (await company_elem.inner_text()).strip()
                    logger.info(f"✅ Found company: {company_name}")
                    break
            
            # Extract posted date with fallback selectors
            posted_date_str = ""
            for selector in DETAIL_SELECTORS["posted_date"]:
                date_elem = await page.query_selector(selector)
                if date_elem:
                    posted_date_str = (await date_elem.inner_text()).strip()
                    logger.info(f"✅ Found posted date: {posted_date_str}")
                    break
            
            if not job_description.strip():
                logger.warning(f"⏭️  Skipped {job_id} - empty description")
                continue
            
            # Extract skills from job description using 3-layer advanced extractor
            extracted_skills_list = cast(list[str], skill_extractor.extract(job_description, return_confidence=False))
            extracted_skills = ", ".join(extracted_skills_list[:15]) if extracted_skills_list else ""
            
            # Validate extracted skills
            validated_skills = ""
            if extracted_skills.strip():
                validated_skills, is_valid = skills_validator.validate_skills(
                    extracted_skills, min_confidence=min_skills_confidence
                )
                if not is_valid:
                    logger.debug(f"💡 {job_id} - low confidence skills, using extracted")
                    validated_skills = extracted_skills  # Use extracted skills even if low confidence
            
            # Parse posted date from relative time string
            posted_date = parse_linkedin_date(posted_date_str) if posted_date_str else None
            if posted_date:
                logger.debug(f"📅 Parsed date: {posted_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Create job model
            job = JobDetailModel(
                job_id=job_id,
                platform=platform,
                actual_role=actual_role,
                url=url,
                job_description=job_description[:5000],
                skills=validated_skills,
                company_name=company_name,
                posted_date=posted_date
            )
            
            # Validate false positives/negatives
            is_valid = bool(job.job_description.strip())
            
            if is_valid:
                # Store immediately to database
                stored = db_ops.store_details([job])
                if stored > 0:
                    job_details.append(job)
                    processed += 1
                    logger.info(f"✅ Scraped & Stored #{processed} - {job_id[:40]}")
                else:
                    logger.warning(f"⚠️ Failed to store {job_id} - marking as scraped")
                    db_ops.mark_url_scraped(url)
            else:
                logger.warning(f"⏭️ Invalid job {job_id} - marking as scraped")
                db_ops.mark_url_scraped(url)
            
        except Exception as e:
            logger.error(f"❌ Failed {job_id} - {e}")
            # Mark failed URL as scraped to avoid retry
            db_ops.mark_url_scraped(url)
        finally:
            if page:
                await page.close()
    
    if should_close and context is not None and browser is not None:
        await context.close()
        await browser.close()
        if p is not None:
            await p.stop()
    
    logger.info(f"✅ Sequential scraper completed: {len(job_details)} valid jobs")
    return job_details
