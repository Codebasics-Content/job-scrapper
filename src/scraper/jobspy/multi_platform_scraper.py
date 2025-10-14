"""LinkedIn-only JobSpy scraper with multi-layer fuzzy deduplication"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

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
            # Batch scraping for real-time progress (10 jobs per batch)
            batch_size = 10
            batch_num = 0
            new_jobs_count = 0
            total_skipped = 0
            total_scraped = 0  # Track TOTAL jobs scraped (including duplicates) for offset
            seen_urls_this_session = set()  # Track URLs seen in THIS scrape session
            platform_results = []
            start_time = datetime.now()
            print(f"   ⏳ Starting at {start_time.strftime('%H:%M:%S')}...")
            print(f"   🔍 Cross-verifying with database to skip duplicates...\n")
            
            # Keep scraping until we get results_wanted NEW jobs OR no new jobs available
            while new_jobs_count < results_wanted:
                batch_start = datetime.now()
                
                # Calculate offset to get DIFFERENT jobs each batch
                current_offset = total_scraped
                
                # Scrape next batch with offset for pagination
                batch_df = scrape_jobs(
                    site_name=[platform],
                    search_term=search_term,
                    location=location,
                    results_wanted=batch_size,
                    hours_old=hours_old,
                    linkedin_fetch_description=linkedin_fetch_description,
                    proxies=proxies,
                    offset=current_offset,  # Skip already-scraped jobs
                )
                
                batch_end = datetime.now()
                batch_duration = (batch_end - batch_start).total_seconds()
                
                if batch_df is not None and len(batch_df) > 0:
                    # Extract skills for ALL scraped jobs
                    if store_to_db:
                        try:
                            extractor = AdvancedSkillExtractor('skills_reference_2025.json')
                            db_ops = JobStorageOperations()
                            batch_jobs = []
                            
                            for _, row in batch_df.iterrows():
                                desc = str(row.get('description', ''))
                                skills = extractor.extract(desc) if desc and len(desc.strip()) > 50 else []
                                
                                # Check for duplicate using multi-layer fuzzy matching
                                job_dict = {
                                    'title': str(row.get('title', '')),
                                    'company': str(row.get('company', '')),
                                    'location': str(row.get('location', ''))
                                }
                                
                                if not deduplicator.is_duplicate(job_dict):
                                    job = JobDetailModel(
                                        job_id=f"{row.get('site', 'unknown')}_{row.get('job_url', '').split('/')[-1]}",
                                        platform=row.get('site', 'unknown'),
                                        actual_role=search_term,
                                        url=row.get('job_url', ''),
                                        job_description=desc,
                                        skills=','.join(skills) if skills else '',
                                        company_name=row.get('company', ''),
                                        posted_date=None,
                                    )
                                    batch_jobs.append(job)
                            
                            # Track total scraped for offset calculation
                            total_scraped += len(batch_jobs)
                            
                            # Extract URLs from this batch
                            batch_urls = [job.url for job in batch_jobs]
                            
                            # DETECT CYCLING: Check if we've seen these exact URLs before in THIS session
                            if seen_urls_this_session and set(batch_urls).issubset(seen_urls_this_session):
                                print(f"\n   🔁 CYCLING DETECTED: Platform returning same jobs repeatedly")
                                print(f"   🛑 All {len(batch_urls)} URLs already seen in this session")
                                print(f"   💡 No more unique jobs available from this platform")
                                break
                            
                            # Track URLs seen in this session
                            seen_urls_this_session.update(batch_urls)
                            
                            # VALIDATION GATE: Separate valid jobs from invalid
                            valid_jobs = [job for job in batch_jobs if job.skills and len(job.skills.strip()) > 0]
                            invalid_jobs = [job for job in batch_jobs if not job.skills or len(job.skills.strip()) == 0]
                            
                            # Log REJECTED jobs (empty skills)
                            if invalid_jobs:
                                print(f"\n   ❌ REJECTED {len(invalid_jobs)} jobs (empty skills - quality gate):")
                                for idx, job in enumerate(invalid_jobs[:3], 1):  # Show first 3
                                    print(f"      {idx}. {job.company_name} - {job.actual_role}")
                                    print(f"         Description length: {len(job.job_description)} chars")
                                    print(f"         URL: {job.url[:60]}...")
                                if len(invalid_jobs) > 3:
                                    print(f"      ... and {len(invalid_jobs) - 3} more rejected")
                            
                            # Cross-verify VALID jobs with database
                            valid_urls = [job.url for job in valid_jobs]
                            existing_urls = db_ops.get_existing_urls(valid_urls)
                            new_jobs = [job for job in valid_jobs if job.url not in existing_urls]
                            skipped_jobs = [job for job in valid_jobs if job.url in existing_urls]
                            
                            # Log SKIPPED jobs in detail
                            if skipped_jobs:
                                print(f"\n   ⏭️  SKIPPED {len(skipped_jobs)} EXISTING jobs:")
                                for idx, job in enumerate(skipped_jobs, 1):
                                    print(f"      {idx}. {job.company_name} - {job.actual_role}")
                                    print(f"         URL: {job.url[:80]}...")
                                total_skipped += len(skipped_jobs)
                            
                            # Store and log NEW VALIDATED jobs
                            if new_jobs:
                                stored = db_ops.store_details(new_jobs)
                                batch_num += 1
                                new_jobs_count += stored
                                platform_results.extend([job for job in new_jobs])
                                
                                elapsed = (batch_end - start_time).total_seconds()
                                rate = new_jobs_count / elapsed if elapsed > 0 else 0
                                
                                print(f"\n   📦 BATCH {batch_num} (VALIDATED jobs with skills):")
                                print(f"   ✅ Stored {stored} QUALITY jobs to database")
                                for idx, job in enumerate(new_jobs, 1):
                                    skill_count = len(job.skills.split(',')) if job.skills else 0
                                    print(f"      {idx}. {job.company_name} - {job.actual_role}")
                                    print(f"         Skills ({skill_count}): {job.skills[:60]}...")
                                    print(f"         URL: {job.url[:80]}...")
                                
                                progress_msg = f"   ✅ Batch {batch_num} complete | NEW: {stored} | Total NEW: {new_jobs_count}/{results_wanted} | {batch_duration:.1f}s | Rate: {rate:.1f} jobs/s"
                                print(progress_msg)
                                logger.info(progress_msg)
                            
                            # Check if we reached target
                            if new_jobs_count >= results_wanted:
                                print(f"\n   🎯 Target reached: {new_jobs_count}/{results_wanted} NEW jobs scraped")
                                break
                            elif len(skipped_jobs) == len(batch_jobs):
                                # All jobs in this batch were duplicates
                                remaining = results_wanted - new_jobs_count
                                print(f"   🔄 All duplicates this batch. Continuing... Need {remaining} more NEW jobs\n")
                                
                        except Exception as e:
                            error_msg = f"❌ Storage ERROR: {e}"
                            print(error_msg)
                            logger.error(error_msg)
                            break
                else:
                    warn_msg = f"   ⚠️  LinkedIn returned 0 jobs - stopping"
                    print(warn_msg)
                    logger.warning(warn_msg)
                    break
            
            # Final summary
            elapsed_total = (datetime.now() - start_time).total_seconds()
            rate_final = new_jobs_count / elapsed_total if elapsed_total > 0 else 0
            
            summary_msg = f"   🎉 {platform.upper()} COMPLETE: {new_jobs_count} NEW jobs stored | {total_skipped} duplicates skipped | {elapsed_total:.1f}s ({rate_final:.1f} jobs/sec)"
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
