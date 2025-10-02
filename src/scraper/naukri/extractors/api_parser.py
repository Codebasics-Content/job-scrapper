#!/usr/bin/env python3
# Naukri API response parser for detailed job data
# EMD Compliance: ≤80 lines

import logging
import re
from datetime import datetime
from typing import Any
from src.models import JobModel

logger = logging.getLogger(__name__)

class NaukriAPIParser:
    """Parse Naukri API response to extract detailed job information"""
    
    @staticmethod
    def parse_jobs(api_data: dict[str, Any]) -> list[JobModel]:
        """Parse multiple jobs from API response"""
        jobs: list[JobModel] = []
        job_list = api_data.get("jobDetails", [])
        
        for job_data in job_list:
            try:
                job = NaukriAPIParser.parse_api_response(job_data, None)
                jobs.append(job)
            except Exception as e:
                logger.debug(f"[PARSE ERROR] Skipping job: {e}")
                continue
        
        return jobs
    
    @staticmethod
    def parse_api_response(api_data: dict[str, Any], existing_job: JobModel | None = None) -> JobModel:
        """Parse API response to create new job or enrich existing one"""
        try:
            job_details = api_data.get("jobDetails", {}) if "jobDetails" in api_data else api_data
            
            # Extract full HTML description and clean it
            raw_description = job_details.get("description", "")
            clean_description = NaukriAPIParser._clean_html_description(raw_description)
            
            # Extract skills from keySkills.other array
            key_skills = job_details.get("keySkills", {})
            skills_other = key_skills.get("other", [])
            skills_list = [skill.get("label", "") for skill in skills_other if skill.get("label")]
            
            # Extract basic info from API or use existing
            raw_job_id = job_details.get("jobId", existing_job.job_id if existing_job else "")
            # Add naukri prefix if not already present
            job_id = raw_job_id if raw_job_id.startswith("naukri_") else f"naukri_{raw_job_id}" if raw_job_id else ""
            logger.info(f"[API ENRICH] Job ID: {job_id} | Existing: {existing_job is not None}")
            title = job_details.get("title", existing_job.job_role if existing_job else "")
            company = job_details.get("companyName", existing_job.company if existing_job else "")
            location = job_details.get("location", existing_job.location if existing_job else "")
            url = job_details.get("jdURL", existing_job.url if existing_job else "")
            
            # Extract salary and experience
            salary_detail = job_details.get("salaryDetail", {})
            salary_label = salary_detail.get("label")
            experience_text = job_details.get("experienceText", existing_job.experience if existing_job else "")
            
            # Create/update job model
            logger.info(f"[ENRICH] Added {len(skills_list)} skills | Description: {len(clean_description)} chars")
            
            # Convert skills list to comma-separated string
            skills_list_str = ', '.join(skills_list) if skills_list else ""
            
            return JobModel(
                job_id=str(job_id),
                Job_Role=title,
                Company=company,
                Experience=experience_text,
                Skills=skills_list_str or (existing_job.skills if existing_job else ""),
                jd=clean_description or (existing_job.jd if existing_job else ""),
                platform="naukri",
                url=url,
                location=location,
                salary=salary_label,
                posted_date=existing_job.posted_date if existing_job else None,
                scraped_at=existing_job.scraped_at if existing_job else datetime.now(),
                skills_list=skills_list if skills_list else (existing_job.skills_list if existing_job else []),
                normalized_skills=None
            )
            
        except Exception as e:
            logger.error(f"[API PARSE ERROR] {e}")
            if existing_job:
                return existing_job
            raise
    
    @staticmethod
    def _clean_html_description(html_text: str) -> str:
        """Remove HTML tags and clean description text"""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', ' ', html_text)
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean)
        # Remove escape sequences
        clean = clean.replace('\\r', '').replace('\\n', ' ')
        return clean.strip()
