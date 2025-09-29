#!/usr/bin/env python3
# LinkedIn API job fetcher
# EMD Compliance: ≤80 lines

import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.job import JobModel
from utils.analysis.nlp.skill_extractor import extract_skills_from_text

logger = logging.getLogger(__name__)

def fetch_job_via_api(job_id: str, job_role: str) -> JobModel | None:
    """Fetch job details from LinkedIn API endpoint
    
    Args:
        job_id: LinkedIn job posting ID
        job_role: Job role being searched
        
    Returns:
        JobModel instance or None if fetch fails
    """
    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
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
        
        # Extract skills using NLP
        extracted_skills = extract_skills_from_text(job_description) if job_description else []
        skills_str = ", ".join(extracted_skills) if extracted_skills else "Not specified"
        
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
            posted_date=None,
            skills_list=extracted_skills,
            normalized_skills=[s.lower() for s in extracted_skills],
            scraped_at=datetime.now()
        )
        
    except Exception as error:
        logger.error(f"Failed to fetch job {job_id}: {error}")
        return None
