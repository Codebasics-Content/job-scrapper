"""Optimized LinkedIn scraper with concurrent processing and retry logic.

Features:
- Concurrent job description fetching
- Enhanced error handling and retry logic
- Batch skill extraction optimization
- Circuit breaker pattern for reliability
"""
from __future__ import annotations

import re
import asyncio
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup

from src.models import JobModel
from src.scraper.services.enhanced_headlessx_client import EnhancedHeadlessXClient, RetryConfig, CircuitBreakerConfig
from src.analysis.skill_extraction import extract_skills_from_text, load_skill_patterns


SEARCH_SELECTOR = "a.base-card__full-link"
DESC_SELECTORS = [
    ".description__text",
    ".show-more-less-html__markup", 
    ".jobs-description",
]


def _build_search_url(keyword: str, location: str) -> str:
    k = keyword.replace(" ", "%20")
    loc = location.replace(" ", "%20")
    return (
        f"https://www.linkedin.com/jobs/search/?keywords={k}&location={loc}"
    )


async def scrape_linkedin_jobs_unified(
    keyword: str,
    location: str = "United States",
    limit: int = 50,
) -> List[JobModel]:
    """Optimized LinkedIn scraping with concurrent processing"""
    
    # Configure enhanced client for LinkedIn's rate limits
    retry_config = RetryConfig(
        max_attempts=3,
        base_delay=2.0,
        max_delay=30.0,
        jitter=True
    )
    
    circuit_config = CircuitBreakerConfig(
        failure_threshold=3,
        recovery_timeout=60.0,
        success_threshold=2
    )
    
    async with EnhancedHeadlessXClient(
        retry_config=retry_config,
        circuit_config=circuit_config,
        max_concurrent=5,  # LinkedIn-friendly concurrency
        rate_limit_per_second=2.0  # Conservative rate limiting
    ) as client:
        
        # 1) Render search page to get job URLs
        search_url = _build_search_url(keyword, location)
        html = await client.render_url(search_url)
        soup = BeautifulSoup(html, "html.parser")

        # 2) Extract job URLs
        job_urls = []
        for a in soup.select(SEARCH_SELECTOR):
            href = a.get("href")
            if href and href.startswith("http"):
                job_urls.append(href)
            if len(job_urls) >= limit:
                break

        if not job_urls:
            return []

        # 3) Concurrent job description fetching
        results = await client.render_urls_concurrent(job_urls)
        
        # 4) Load skill patterns once for batch processing
        skill_patterns = load_skill_patterns()
        
        # 5) Process results and extract job data
        jobs: List[JobModel] = []
        
        for job_url, result in results:
            if isinstance(result, Exception):
                continue  # Skip failed requests - they're logged by circuit breaker
                
            page = BeautifulSoup(result, "html.parser")
            
            # Extract job description
            desc = ""
            for sel in DESC_SELECTORS:
                node = page.select_one(sel)
                if node:
                    desc = node.get_text(" ", strip=True)
                    if desc:
                        break
            
            if not desc:
                continue
            
            # Extract job ID from URL
            m = re.search(r"/view/(\d+)", job_url)
            job_id = f"linkedin_{m.group(1)}" if m else job_url
            
            # Extract skills using optimized regex patterns
            skills_list = extract_skills_from_text(desc, skill_patterns)
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            jobs.append(
                JobModel(
                    job_id=job_id,
                    Job_Role="",
                    Company="",
                    Experience="",
                    Skills=skills_str,
                    jd=desc,
                    company_detail="",
                    platform="linkedin",
                    url=job_url,
                    location="",
                    salary=None,
                    posted_date=datetime.now(),
                    skills_list=skills_list,
                    normalized_skills=[s.lower() for s in skills_list],
                )
            )

        return jobs


async def scrape_linkedin_jobs_batch(
    search_params: List[dict],
    max_concurrent_searches: int = 3
) -> List[JobModel]:
    """Batch process multiple LinkedIn searches concurrently"""
    
    async def process_search(params: dict) -> List[JobModel]:
        return await scrape_linkedin_jobs_unified(**params)
    
    # Limit concurrent searches to avoid overwhelming LinkedIn
    semaphore = asyncio.Semaphore(max_concurrent_searches)
    
    async def bounded_search(params: dict) -> List[JobModel]:
        async with semaphore:
            return await process_search(params)
    
    tasks = [bounded_search(params) for params in search_params]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Flatten results and filter out exceptions
    all_jobs = []
    for result in results:
        if isinstance(result, list):
            all_jobs.extend(result)
    
    return all_jobs