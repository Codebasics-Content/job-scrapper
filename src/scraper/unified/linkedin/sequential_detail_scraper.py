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
from src.scraper.unified.linkedin.retry_helper import retry_with_backoff
from src.scraper.unified.linkedin.job_validator import JobValidator

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
    skills_validator = SkillValidator("skills_reference_2025.json")
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
        # Extract clean LinkedIn job ID (just the number from URL)
        linkedin_job_id = url.split('/')[-1]
        job_id = linkedin_job_id  # Store clean ID without prefix
        platform = "linkedin"  # Set platform name correctly
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
            logger.info(f"📝 Extracting job title...")
            scraped_job_title = ""
            for selector in DETAIL_SELECTORS["job_title"]:
                title_elem = await page.query_selector(selector)
                if title_elem:
                    scraped_job_title = (await title_elem.inner_text()).strip()
                    logger.info(f"✅ Found job title: {scraped_job_title}")
                    break
            
            if not scraped_job_title:
                logger.warning(f"⚠️ Job title not found on page, using URL-based: {actual_role}")
                scraped_job_title = actual_role
            
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
            
            if not company_name:
                logger.warning(f"⚠️ Company name not found on page for {job_id[:40]}")
                company_name = "Unknown Company"
            
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
            
            # Validate extracted skills against canonical 557 skills
            validated_skills = ""
            if extracted_skills.strip():
                # SkillValidator.validate_and_extract returns Set[str], not tuple
                canonical_skills = skills_validator.validate_and_extract(job_description)
                if canonical_skills:
                    validated_skills = ", ".join(sorted(canonical_skills))
                else:
                    logger.debug(f"💡 {job_id} - no canonical matches, using extracted")
                    validated_skills = extracted_skills
            
            # Parse posted date from relative time string
            posted_date = parse_linkedin_date(posted_date_str) if posted_date_str else None
            if posted_date:
                logger.debug(f"📅 Parsed date: {posted_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Create job model - use scraped title if available, fallback to URL-based
            final_job_title = scraped_job_title if scraped_job_title else actual_role
            job = JobDetailModel(
                job_id=job_id,
                platform=platform,
                actual_role=final_job_title,
                url=url,
                job_description=job_description[:5000],
                skills=validated_skills,
                company_name=company_name,
                posted_date=posted_date
            )
            
            # ✅ VALIDATION GATE 1: JobValidator - Required fields, URL, description length
            job_validator = JobValidator(min_description_length=100)
            is_valid, validation_reason = job_validator.validate_job(job)
            
            if not is_valid:
                logger.warning(f"⚠️ Validation failed: {job_id[:40]} - {validation_reason}")
                continue  # Skip to next job, do NOT mark scraped
            
            # ✅ VALIDATION GATE 2: SkillValidator - False positive/negative accuracy
            if validated_skills:
                accuracy_report = skills_validator.calculate_accuracy(
                    job.job_description, validated_skills
                )
                precision = accuracy_report.get('precision', 0)
                recall = accuracy_report.get('recall', 0)
                
                if precision < 0.5:  # Too many false positives
                    logger.warning(f"⚠️ Low precision ({precision:.2f}) for {job_id[:40]}")
                    # Use canonical skills only
                    canonical = accuracy_report.get('canonical_skills', [])
                    job.skills = ", ".join(canonical) if canonical else ""
                
                logger.debug(f"📊 Skills accuracy: precision={precision:.2f}, recall={recall:.2f}")
            
            # ✅ VALIDATION GATE 3: Database storage
            stored = db_ops.store_details([job])
            if stored > 0:
                # ✅ SUCCESS: Mark scraped=1 ONLY after successful storage
                db_ops.mark_urls_scraped([url])
                job_details.append(job)
                processed += 1
                logger.info(f"✅ Scraped & Stored #{processed} - {job_id[:40]}")
            else:
                logger.error(f"❌ Database storage failed for {job_id[:40]}")
                # Do NOT mark scraped - allow retry
                continue
            
        except Exception as e:
            logger.error(f"❌ Failed {job_id} - {e}")
            # Do NOT mark scraped - allow retry on next run
            continue
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
