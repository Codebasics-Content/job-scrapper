"""Unified scraping orchestrator using HeadlessX for rendering.

Supported platforms: linkedin, indeed, naukri.
Returns list[JobModel] with only url, jd, skills-related fields populated.

PERFORMANCE (Based on Playwright vs Selenium Testing):
- HeadlessX uses Playwright WITHOUT proxy for all platforms
- Indeed: ✅ 10 jobs, ~5s (Playwright wins)
- Naukri: ✅ 10 jobs, ~6s (Bulk API primary, browser fallback)
- LinkedIn: ✅ 10 jobs, ~7s (Playwright works, official API recommended)
- NO proxy configuration needed - direct connections optimal

SCALABLE COMPONENTS (10K+ jobs):
- BatchProcessor: Streaming batches with validation (1000 jobs/batch)
- CheckpointManager: Crash recovery with JSON persistence
- ProgressTracker: Real-time ETA with moving average throughput
- Rate Limiters: Platform-specific (Indeed=5, LinkedIn=2, Naukri=15)

For 10K+ job scraping, use scalable.* components directly in platform scrapers.
"""
from __future__ import annotations

from typing import List

from src.models import JobModel
from src.analysis.skill_extraction import extract_skills_from_text, load_skill_patterns
from .linkedin_unified import scrape_linkedin_jobs_unified
from .indeed_unified import scrape_indeed_jobs_unified
from .naukri_unified import scrape_naukri_jobs_unified

# Scalable components available for 10K+ job operations
from .scalable import (
    BatchProcessor,
    CheckpointManager, 
    ProgressTracker,
    get_rate_limiter,
)


async def scrape_jobs(
    platform: str,
    *,
    keyword: str,
    location: str,
    limit: int = 50,
) -> List[JobModel]:
    """Scrape jobs and extract skills using lightweight regex patterns"""
    p = platform.lower()
    
    # Get raw jobs without skills extraction
    if p == "linkedin":
        jobs = await scrape_linkedin_jobs_unified(keyword=keyword, location=location, limit=limit)
    elif p == "indeed":
        jobs = await scrape_indeed_jobs_unified(keyword=keyword, location=location, limit=limit)
    elif p == "naukri":
        jobs = await scrape_naukri_jobs_unified(keyword=keyword, location=location, limit=limit)
    else:
        raise ValueError(f"Unsupported platform: {platform}")
    
    # Load skill patterns once for batch processing (performance optimization)
    skill_patterns = load_skill_patterns()
    
    # Extract skills for each job using fast regex matching
    for job in jobs:
        if hasattr(job, 'jd') and job.jd:
            skills = extract_skills_from_text(job.jd, skill_patterns)
            job.skills = ','.join(skills) if skills else ''
    
    return jobs
