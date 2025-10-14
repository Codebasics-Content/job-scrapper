# Multi-Platform Job Scraper Service - Centralized Skill Extraction
# 2-Platform Architecture: LinkedIn (JobSpy) + Naukri (Playwright)
from __future__ import annotations

import logging
from typing import List

from src.models import JobDetailModel
from src.analysis.skill_extraction import AdvancedSkillExtractor
from .jobspy.multi_platform_scraper import scrape_multi_platform
from .unified.naukri_unified import scrape_naukri_jobs_unified

logger = logging.getLogger(__name__)


async def scrape_jobs_with_skills(
    platforms: list[str],
    keyword: str,
    location: str = "United States",
    limit: int = 100,
    headless: bool = False,
    store_to_db: bool = True,
) -> List[JobDetailModel]:
    """2-Platform scraper with advanced deduplication
    
    Platforms:
        - linkedin: JobSpy (multi-layer fuzzy deduplication)
        - naukri: Playwright (headless=False for anti-detection)
    
    Returns:
        List of JobDetailModel with skills extracted and deduplicated
    """
    all_jobs: List[JobDetailModel] = []
    extractor = AdvancedSkillExtractor('skills_reference_2025.json')
    
    # Separate platforms: JobSpy (LinkedIn only) vs Playwright (Naukri)
    jobspy_platforms = [p for p in platforms if p == "linkedin"]
    naukri_requested = "naukri" in platforms
    
    # Scrape via JobSpy (LinkedIn only with fuzzy deduplication)
    if jobspy_platforms:
        logger.info(f"Scraping LinkedIn via JobSpy with multi-layer deduplication...")
        df = scrape_multi_platform(
            platforms=jobspy_platforms,
            search_term=keyword,
            location=location,
            results_wanted=limit,
            store_to_db=store_to_db,
        )
        
        if df is not None and len(df) > 0:
            # Jobs already stored by multi_platform_scraper per batch
            # Just collect for return
            for _, row in df.iterrows():
                job = JobDetailModel(
                    job_id=f"{row.get('site', 'unknown')}_{row.get('job_url', '').split('/')[-1]}",
                    platform=row.get('site', 'unknown'),
                    actual_role=keyword,
                    url=row.get('job_url', ''),
                    job_description=str(row.get('description', '')),
                    skills=str(row.get('skills', '')),  # Already extracted and stored
                    company_name=row.get('company', ''),
                    posted_date=None,
                )
                all_jobs.append(job)
    
    # Scrape via Naukri Playwright (headless=False to bypass bot detection)
    if naukri_requested:
        logger.info("Scraping Naukri via Playwright (headless=False, visible browser)...")
        naukri_jobs = await scrape_naukri_jobs_unified(
            keyword=keyword,
            location=location,
            limit=limit,
            headless=False,  # Opens visible browser to bypass bot detection
        )
        
        # Extract skills from Naukri jobs
        for job in naukri_jobs:
            if hasattr(job, 'jd') and job.jd and len(job.jd.strip()) > 50:
                skills = extractor.extract(job.jd)
                job.skills = ','.join(skills) if skills else ''
        
        all_jobs.extend(naukri_jobs)
    
    logger.info(f"Total jobs scraped: {len(all_jobs)} with skills extracted")
    if store_to_db:
        logger.info(f"✅ All {len(all_jobs)} jobs stored to database in batches")
    
    return all_jobs
