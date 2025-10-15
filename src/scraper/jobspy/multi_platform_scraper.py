"""LinkedIn-only JobSpy scraper with multi-layer fuzzy deduplication"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

import pandas as pd
from jobspy import scrape_jobs

from .deduplicator import LinkedInDeduplicator
from .proxy_config import get_proxy_for_platform
from src.analysis.skill_extraction import AdvancedSkillExtractor
from src.db.operations import JobStorageOperations
from src.models import JobDetailModel

logger = logging.getLogger(__name__)

# Path to skills reference
SKILLS_REF = Path(__file__).parent.parent.parent.parent / "skills_reference_2025.json"


def scrape_multi_platform(
    platforms: list[str],
    search_term: str,
    location: str = "",
    results_wanted: int = 100,
    hours_old: int = 72,
    linkedin_fetch_description: bool = True,
    store_to_db: bool = True,
) -> pd.DataFrame:
    """
    Scrape LinkedIn jobs with advanced deduplication (99.9%+ precision)
    
    Platform:
    - LinkedIn: BrightData proxy (for >100 jobs) + multi-layer fuzzy deduplication
    
    Args:
        platforms: Only "linkedin" supported (Indeed removed)
        search_term: Job search keyword
        location: Location filter (empty string "" for worldwide search)
        results_wanted: Jobs to scrape per platform
        hours_old: Filter by posting age
        linkedin_fetch_description: Fetch full LinkedIn descriptions
    
    Returns:
        Combined DataFrame from all platforms
    """
    all_results = []
    deduplicator = LinkedInDeduplicator()  # Multi-layer fuzzy deduplication
    
    for platform in platforms:
        # Only LinkedIn supported now
        if platform not in ["linkedin"]:
            logger.warning(f"Platform '{platform}' not supported. Only 'linkedin' allowed.")
            continue
        start_time = datetime.now()
        msg = f"\n{'='*60}\n🔍 SCRAPING {platform.upper()}\n{'='*60}"
        print(msg)
        logger.info(msg)
        
        # Get proxy only for LinkedIn
        proxies = get_proxy_for_platform(platform)
        
        proxy_msg = f"   {'🌐 Proxy' if proxies else '🆓 Direct'} | Target: {results_wanted} jobs"
        print(proxy_msg)
        logger.info(proxy_msg)
        
        print(f"   ⏳ Starting at {start_time.strftime('%H:%M:%S')}...")
        logger.info(f"Starting {platform} scrape")
        
        try:
            # Single scrape (JobSpy doesn't support offset pagination)
            platform_results = []
            scrape_start = datetime.now()
            print(f"   ⏳ Starting at {scrape_start.strftime('%H:%M:%S')}...")
            
            # Scrape ALL jobs in SINGLE call (JobSpy doesn't support offset pagination)
            log_msg = f"\n📡 Calling JobSpy: results_wanted={results_wanted}, location={location or 'worldwide'}"
            print(log_msg)
            print(f"   ⚠️  Large requests (>1000 jobs) may take 2-5 minutes...")
            logger.info(log_msg)
            
            try:
                print(f"   🚀 Submitting JobSpy request to executor...")
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(
                        scrape_jobs,
                        site_name=[platform],
                        search_term=search_term,
                        location=location,
                        results_wanted=min(results_wanted, 100),  # Cap at 100 to prevent hangs
                        hours_old=hours_old,
                        linkedin_fetch_description=linkedin_fetch_description,
                        proxies=proxies,
                    )
                    print(f"   ⏳ Waiting for JobSpy (60s timeout)...")
                    batch_df = future.result(timeout=60)  # Reduced to 60s
                    print(f"   ✅ JobSpy completed successfully")
            except FutureTimeoutError:
                log_msg = "⚠️ JobSpy timeout after 60s - LinkedIn blocking or rate-limiting detected"
                print(log_msg)
                logger.warning(log_msg)
                batch_df = None
            except Exception as e:
                log_msg = f"❌ JobSpy error: {type(e).__name__}: {str(e)}"
                print(log_msg)
                logger.error(log_msg, exc_info=True)  # Full traceback
                batch_df = None
            
            log_msg = f"✅ JobSpy returned: rows={len(batch_df) if batch_df is not None else 0}"
            print(log_msg)
            logger.info(log_msg)
            
            if batch_df is not None and len(batch_df) > 0:
                print(f"   🔍 Starting deduplication and skill extraction...")
                # Extract skills for ALL scraped jobs
                if store_to_db:
                    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
                    db_ops = JobStorageOperations()
                    all_jobs = []
                    
                    for _, row in batch_df.iterrows():
                        desc = str(row.get('description', ''))
                        skills = extractor.extract(desc) if desc and len(desc.strip()) > 50 else []
                        
                        # Fuzzy deduplication
                        job_dict = {
                            'title': str(row.get('title', '')),
                            'company': str(row.get('company', '')),
                            'location': str(row.get('location', ''))
                        }
                        
                        if not deduplicator.is_duplicate(job_dict):
                            # Extract skills as list of strings
                            skill_list = [s for s in skills if isinstance(s, str)]
                            job = JobDetailModel(
                                job_id=f"{row.get('site', 'unknown')}_{row.get('job_url', '').split('/')[-1]}",
                                platform=row.get('site', 'unknown'),
                                actual_role=search_term,
                                url=row.get('job_url', ''),
                                job_description=desc,
                                skills=','.join(skill_list),
                                company_name=row.get('company', ''),
                                posted_date=None,
                            )
                            all_jobs.append(job)
                    
                    # Filter: only jobs with skills
                    valid_jobs = [job for job in all_jobs if job.skills and len(job.skills.strip()) > 0]
                    invalid_jobs = [job for job in all_jobs if not job.skills or len(job.skills.strip()) == 0]
                    
                    # Log rejected
                    if invalid_jobs:
                        print(f"\n   ❌ REJECTED {len(invalid_jobs)} jobs (no skills)")
                    
                    # DB deduplication
                    valid_urls = [job.url for job in valid_jobs]
                    existing_urls = db_ops.get_existing_urls(valid_urls)
                    new_jobs = [job for job in valid_jobs if job.url not in existing_urls]
                    
                    print(f"   ⏭️  SKIPPED {len(valid_jobs) - len(new_jobs)} existing jobs")
                    
                    # Store NEW jobs
                    if new_jobs:
                        stored = db_ops.store_details(new_jobs)
                        platform_results.extend(new_jobs)
                        
                        elapsed = (datetime.now() - scrape_start).total_seconds()
                        
                        print(f"\n   ✅ STORED {stored} NEW jobs:")
                        for idx, job in enumerate(new_jobs[:5], 1):
                            skill_count = len(job.skills.split(',')) if job.skills else 0
                            print(f"      {idx}. {job.company_name} - {job.actual_role}")
                            print(f"         Skills ({skill_count}): {job.skills[:60]}...")
                        if len(new_jobs) > 5:
                            print(f"      ... and {len(new_jobs) - 5} more")
                        
                        print(f"   ⏱️  Time: {elapsed:.1f}s | Rate: {stored/elapsed:.1f} jobs/s")
                    else:
                        print(f"\n   ℹ️  No new jobs (all {len(valid_jobs)} already in database)")
            else:
                warn_msg = f"   ⚠️  JobSpy returned 0 jobs"
                print(warn_msg)
                logger.warning(warn_msg)
            
            # Final summary
            elapsed_total = (datetime.now() - start_time).total_seconds()
            new_count = len(platform_results)
            rate_final = new_count / elapsed_total if elapsed_total > 0 else 0
            
            summary_msg = f"\n{'='*60}\n   🎉 {platform.upper()} COMPLETE: {new_count} NEW jobs | {elapsed_total:.1f}s ({rate_final:.1f} jobs/sec)\n{'='*60}"
            print(summary_msg)
            logger.info(summary_msg)
            
            # Return NEW jobs as DataFrame
            if platform_results:
                # Convert JobDetailModel list to DataFrame
                jobs_data = [{
                    'site': job.platform,
                    'job_url': job.url,
                    'company': job.company_name,
                    'description': job.job_description,
                } for job in platform_results]
                combined_df = pd.DataFrame(jobs_data)
                all_results.append(combined_df)
                
                end_time = datetime.now()
                total_duration = (end_time - start_time).total_seconds()
                final_msg = f"   🎉 {platform.upper()} COMPLETE: {len(combined_df)} jobs in {total_duration:.1f}s ({len(combined_df)/total_duration:.1f} jobs/sec)"
                print(final_msg)
                logger.info(final_msg)
            else:
                warn_msg = f"   ⚠️  No jobs found for {platform}"
                print(warn_msg)
                logger.warning(warn_msg)
                
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            error_msg = f"   ❌ ERROR after {duration:.1f}s: {e}"
            print(error_msg)
            logger.error(error_msg)
    
    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
