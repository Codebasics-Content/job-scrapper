# Parallel Job Detail Scraper with Dynamic 5-Concurrent Queue
# When 1 job completes, immediately adds next from queue
import asyncio
import logging
import random
from typing import List, Optional
import os
from playwright.async_api import async_playwright, ProxySettings, Browser, BrowserContext
from src.models.models import JobDetailModel
from .skills_validator import SkillsValidator
from .selector_config import DETAIL_SELECTORS
from .retry_helper import retry_with_backoff

logger = logging.getLogger(__name__)

async def scrape_job_details_parallel(
    urls: List[tuple[str, str, str, str]],
    headless: bool = False,
    min_skills_confidence: float = 0.5,
    browser: Optional[Browser] = None,
    context: Optional[BrowserContext] = None
) -> List[JobDetailModel]:
    """Scrape job details with 5-concurrent queue + skills validation
    
    Args:
        urls: List of (url, job_id, platform, actual_role)
        headless: Browser visibility
        min_skills_confidence: Minimum valid skills ratio (default 0.5 = 50%)
        browser: Optional reusable browser instance (prevents memory leak)
        context: Optional reusable context (prevents memory leak)
    """
    
    # Initialize skills validator
    skills_validator = SkillsValidator()
    
    # Proxy configuration
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
        logger.info(f"🔗 Using proxy for details")
    
    job_details: List[JobDetailModel] = []
    
    # Use provided browser/context or create new (for backward compatibility)
    should_close = browser is None
    
    if browser is None:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=headless, proxy=proxy_config)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
    
    # Create queue and semaphore for 5 concurrent workers
    queue: asyncio.Queue[tuple[str, str, str, str] | None] = asyncio.Queue()
    for url_data in urls:
        await queue.put(url_data)
    
    # Add sentinel values to signal workers to stop
    for _ in range(5):
        await queue.put(None)
    
    async def worker(worker_id: int) -> None:
        """Worker that processes jobs from queue"""
        # Stagger worker startup (prevent simultaneous requests)
        await asyncio.sleep(worker_id * random.uniform(0.5, 1.5))
        logger.info(f"👷 Worker {worker_id}: Started")
        processed = 0
        
        while True:
            url_tuple = await queue.get()
            
            if url_tuple is None:  # Sentinel value
                queue.task_done()
                break
            
            url = url_tuple[0]  # Extract URL from tuple
            job_id = f"linkedin_{url.split('/')[-1]}"
            platform = url_tuple[1]
            actual_role = url_tuple[2]
            page = None
            
            try:
                # Human-like delay before each request (2-5 seconds)
                await asyncio.sleep(random.uniform(2.0, 5.0))
                
                assert context is not None, "Browser context required"
                page = await context.new_page()
                
                # Fetch with retry (3 attempts, exponential backoff)
                async def fetch_job():
                    assert page is not None, "Page required for fetch"
                    await page.goto(url, timeout=30000)
                    
                    # Wait for description using fallback selectors
                    for selector in DETAIL_SELECTORS["description"]:
                        try:
                            await page.wait_for_selector(selector, timeout=5000)
                            return True
                        except Exception:
                            continue
                    raise Exception("No description selector found")
                
                _, success = await retry_with_backoff(
                    fetch_job,
                    max_retries=3,
                    operation_name=f"fetch_{job_id[:20]}"
                )
                
                if not success:
                    logger.warning(f"⏭️  Worker {worker_id}: Skipped {job_id} - failed after retries")
                    queue.task_done()
                    continue
                
                try:
                    # Extract description (try all selectors)
                    job_description = ""
                    for selector in DETAIL_SELECTORS["description"]:
                        desc_elem = await page.query_selector(selector)
                        if desc_elem:
                            job_description = await desc_elem.inner_text()
                            break
                    
                    # Extract skills from native LinkedIn skills section
                    extracted_skills = ""
                    for selector in DETAIL_SELECTORS["native_skills"]:
                        skills_elems = await page.query_selector_all(selector)
                        if skills_elems:
                            extracted_skills = ",".join([await s.inner_text() for s in skills_elems[:10]])
                            break
                    
                    # Extract company name (use job title area)
                    company_name = ""
                    company_elem = await page.query_selector(".job-details-jobs-unified-top-card__company-name")
                    if company_elem:
                        company_name = await company_elem.inner_text()
                    
                    # Validate: skip if empty fields
                    if not job_description.strip() or not extracted_skills.strip():
                        logger.warning(f"⏭️  Worker {worker_id}: Skipped {job_id} - empty fields")
                        continue
                    
                    # Validate skills against reference (filter false positives)
                    validated_skills, is_valid = skills_validator.validate_skills(
                        extracted_skills, 
                        min_confidence=min_skills_confidence
                    )
                    
                    if not is_valid:
                        logger.warning(
                            f"⏭️  Worker {worker_id}: Skipped {job_id} - "
                            f"skills validation failed (confidence < {min_skills_confidence})"
                        )
                        continue
                    
                    job_details.append(JobDetailModel(
                        job_id=job_id,
                        platform=platform,
                        actual_role=actual_role,
                        url=url,
                        job_description=job_description[:5000],
                        skills=validated_skills,  # Use validated skills (false positives removed)
                        company_name=company_name,
                        posted_date=None
                    ))
                    processed += 1
                    logger.info(f"✅ Worker {worker_id}: Scraped #{processed} - {job_id[:40]}")
                    
                except Exception as e:
                    logger.error(f"❌ Worker {worker_id}: Failed {job_id} - {e}")
                finally:
                    if page:
                        await page.close()
                    queue.task_done()
            
            except Exception as e:
                logger.error(f"❌ Worker {worker_id}: Outer error - {e}")
                if page:
                    await page.close()
                queue.task_done()
        
        logger.info(f"🏁 Worker {worker_id}: Completed {processed} jobs")
    
    # Launch 5 concurrent workers
    workers = [asyncio.create_task(worker(i+1)) for i in range(5)]
    await asyncio.gather(*workers)
    
    # Only close if we created the browser (not reused)
    if should_close and context is not None and browser is not None:
        await context.close()
        await browser.close()
    
    logger.info(f"✅ Scraped {len(job_details)} valid job details (5-concurrent queue)")
    return job_details
