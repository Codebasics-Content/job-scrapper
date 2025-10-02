#!/usr/bin/env python3
# LinkedIn API job fetcher - async version
# EMD Compliance: ≤80 lines

import logging
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from src.models import JobModel
from src.analysis.date_parser import parse_relative_date
from src.scraper.config.delays import get_api_delay, API_TIMEOUT
from src.scraper.linkedin.extractors.api_retry_handler import retry_with_backoff
from src.scraper.base.dynamic_skill_extractor import extract_dynamic_skills

logger = logging.getLogger(__name__)

async def fetch_job_via_api(
    job_id: str, 
    job_role: str,
    job_number: int = 0,
    total_target: int = 0
) -> JobModel | None:
    """Fetch job details from LinkedIn API endpoint
    
    Args:
        job_id: LinkedIn job posting ID
        job_role: Job role being searched
        
    Returns:
        JobModel instance or None if fetch fails
    """
    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    
    try:
        logger.info(f"[API FETCH] Fetching job {job_id}...")
        
        # Wrapper function for retry logic
        async def fetch_with_session() -> str | None:
            timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
            await asyncio.sleep(get_api_delay())  # Randomized delay (1-2.5s)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url) as response:  # type: ignore[attr-defined]
                    if response.status == 429:  # type: ignore[attr-defined]
                        # Create custom error for rate limiting
                        error = Exception("Rate limited")
                        setattr(error, 'status', 429)
                        raise error
                    
                    if response.status != 200:  # type: ignore[attr-defined]
                        logger.error(f"Failed to fetch job {job_id}: {response.status}")
                        return None
                    
                    return await response.text()  # type: ignore[attr-defined]
        
        # Retry with backoff
        html_content = await retry_with_backoff(fetch_with_session, max_retries=3)
        if not html_content:
            return None
        
        logger.debug(f"[API FETCH] Job {job_id} - HTTP 200")
        await asyncio.sleep(get_api_delay())  # Randomized delay (1-2.5s)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract job title
        title_elem = soup.select_one('h2.top-card-layout__title')
        title = title_elem.get_text(strip=True) if title_elem else job_role
        
        # Extract company
        company_elem = soup.select_one('a.topcard__org-name-link')
        company = company_elem.get_text(strip=True) if company_elem else "Unknown"
        
        # Extract location
        location_elem = soup.select_one('span.topcard__flavor--bullet')
        location = location_elem.get_text(strip=True) if location_elem else "Remote"
        
        # Extract job description
        jd_elem = soup.select_one('div.show-more-less-html__markup')
        job_description = jd_elem.get_text(strip=True) if jd_elem else ""
        
        # Extract posted date
        posted_date_elem = soup.select_one('span.posted-time-ago__text')
        posted_date_text = posted_date_elem.get_text(strip=True) if posted_date_elem else ""
        posted_date = parse_relative_date(posted_date_text) if posted_date_text else datetime.now()
        
        # Extract criteria items (seniority, employment type)
        criteria_items = soup.select('li.description__job-criteria-item')
        seniority_level = "Not specified"
        employment_type = "Not specified"
        
        for item in criteria_items:
            header = item.select_one('h3.description__job-criteria-subheader')
            value = item.select_one('span.description__job-criteria-text')
            
            if header and value:
                header_text = header.get_text(strip=True).lower()
                if 'seniority' in header_text:
                    seniority_level = value.get_text(strip=True)
                elif 'employment' in header_text:
                    employment_type = value.get_text(strip=True)
        
        # Fast skill extraction integrated into scraping pipeline (no batch processing needed)
        extracted_skills = extract_dynamic_skills(job_description) if job_description else []
        skills_str = ", ".join(extracted_skills) if extracted_skills else "No skills extracted"
        
        progress_info = f" [Job {job_number}/{total_target}]" if total_target > 0 else ""
        logger.info(f"[API SUCCESS]{progress_info} {title} at {company} - Skills deferred")
        
        return JobModel(
            job_id=f"linkedin_{job_id}",
            Job_Role=title,
            Company=company,
            Experience=seniority_level,
            Skills=skills_str,
            jd=job_description,
            platform="linkedin",
            location=location,
            salary=employment_type,
            url=f"https://www.linkedin.com/jobs/view/{job_id}",
            posted_date=posted_date,
            skills_list=extracted_skills,
            normalized_skills=[s.lower() for s in extracted_skills],
            scraped_at=datetime.now()
        )
        
    except Exception as error:
        logger.error(f"Failed to fetch job {job_id}: {error}")
        return None
