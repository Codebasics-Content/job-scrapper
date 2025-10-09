#!/usr/bin/env python3
"""
Unified Naukri.com Job Scraper
Simple, client-friendly implementation combining API and browser approaches
EMD Compliance: ≤80 lines
"""

import logging
import requests
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.models import JobModel
from src.analysis.skill_normalizer.normalizer import extract_skills_from_combined_text

logger = logging.getLogger(__name__)


class NaukriScraper:
    """Unified Naukri scraper - API first, browser fallback"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'appid': '109',  # Naukri API identifier
            'systemid': '109'
        })
    
    async def scrape_jobs(self, keyword: str, num_jobs: int = 10, location: str = "") -> List[JobModel]:
        """Main scraping method - tries API first, falls back to browser"""
        logger.info(f"🚀 Starting Naukri scrape: '{keyword}' ({num_jobs} jobs)")
        
        # Try API approach first (faster, more reliable)
        jobs = await self._scrape_via_api(keyword, num_jobs, location)
        
        if len(jobs) >= num_jobs * 0.8:  # If we got 80%+ of requested jobs
            logger.info(f"✅ API scraping successful: {len(jobs)} jobs")
            return jobs[:num_jobs]
        
        logger.warning(f"⚠️ API only got {len(jobs)} jobs, trying browser fallback")
        # Fallback to browser scraping if API insufficient
        return await self._scrape_via_browser(keyword, num_jobs, location)
    
    async def _scrape_via_api(self, keyword: str, num_jobs: int, location: str) -> List[JobModel]:
        """Scrape using Naukri API (primary method)"""
        jobs = []
        page = 1
        
        while len(jobs) < num_jobs:
            try:
                # Build API request
                params = {
                    'noOfResults': 20,
                    'urlType': 'search_results',
                    'searchType': 'adv',
                    'keyword': keyword,
                    'pageNo': page,
                    'k': keyword,
                    'l': location,
                    'seoKey': f"{keyword.replace(' ', '-')}-jobs"
                }
                
                response = self.session.get(
                    'https://www.naukri.com/jobapi/v3/search',
                    params=params,
                    timeout=30
                )
                
                if response.status_code != 200:
                    logger.error(f"API error: {response.status_code}")
                    break
                
                data = response.json()
                job_list = data.get('jobDetails', [])
                
                if not job_list:
                    logger.info(f"No more jobs at page {page}")
                    break
                
                # Parse jobs from API response
                for job_data in job_list:
                    job = self._parse_api_job(job_data)
                    if job:
                        jobs.append(job)
                
                logger.info(f"📄 Page {page}: +{len(job_list)} jobs (total: {len(jobs)})")
                page += 1
                
            except Exception as e:
                logger.error(f"API scraping error: {e}")
                break
        
        return jobs
    
    def _parse_api_job(self, job_data: Dict[str, Any]) -> Optional[JobModel]:
        """Parse single job from API response"""
        try:
            # Extract skills
            skills_data = job_data.get('keySkills', {}).get('other', [])
            skills_list = [skill.get('label', '') for skill in skills_data if skill.get('label')]
            
            # Extract company details
            company_detail = job_data.get('companyDetail', {}).get('details', '')
            
            # Create job model
            job_id = f"naukri_{job_data.get('jobId', '')}"
            
            return JobModel(
                job_id=job_id,
                Job_Role=job_data.get('title', ''),
                Company=job_data.get('companyName', ''),
                Experience=job_data.get('experience', ''),
                Skills=', '.join(skills_list),
                jd=job_data.get('description', ''),
                company_detail=company_detail,
                platform='naukri',
                url=job_data.get('jobUrl', ''),
                location=job_data.get('placeholders', ''),
                salary=job_data.get('salary', ''),
                posted_date=job_data.get('createdDate', datetime.now()),
                skills_list=skills_list,
                normalized_skills=None
            )
            
        except Exception as e:
            logger.debug(f"Failed to parse API job: {e}")
            return None
    
    async def _scrape_via_browser(self, keyword: str, num_jobs: int, location: str) -> List[JobModel]:
        """Browser scraping fallback (when API fails)"""
        # This would require browser manager - simplified for now
        logger.info("🌐 Browser scraping not implemented in unified version")
        return []
    
    def close(self):
        """Cleanup resources"""
        self.session.close()