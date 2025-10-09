#!/usr/bin/env python3
# Naukri API response parser for detailed job data
# EMD Compliance: ≤80 lines

import logging
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
            # Handle different API response structures
            if "jobDetails" in api_data:
                job_details = api_data["jobDetails"]
            else:
                job_details = api_data
            
            # DEBUGGING: Log the raw API structure to identify all description-related fields
            logger.info(f"[API STRUCTURE] Available keys: {list(job_details.keys())}")
            
            # DEBUGGING: Log ALL description-related fields from API response
            for key in job_details.keys():
                if 'desc' in key.lower() or 'detail' in key.lower():
                    value = job_details[key]
                    logger.info(f"[RAW API] {key}: {str(value)[:200]}... (length: {len(str(value))})")
            
            # DEBUGGING: Log what we actually got from description field
            raw_description = job_details.get("description", "")
            logger.info(f"[DESCRIPTION FIELD] Raw value: {raw_description[:200]}... (length: {len(raw_description)})")
            
            # CRITICAL: Verify we have full description, not shortDescription
            if raw_description and len(raw_description) < 100:
                logger.warning(f"[SUSPICIOUS] Description too short ({len(raw_description)} chars), might be shortDescription: {raw_description[:50]}")
            
            # DEBUGGING: Log company detail from API response
            company_detail_obj = job_details.get("companyDetail", {})
            company_detail_raw = company_detail_obj.get("details", "") if company_detail_obj else ""
            logger.info(f"[COMPANY DETAIL] Raw API data: {company_detail_raw[:200] if company_detail_raw else 'EMPTY'}... (length: {len(company_detail_raw)})")
            
            # Extract skills from keySkills.other array
            key_skills = job_details.get("keySkills", {})
            skills_other = key_skills.get("other", [])
            skills_list = [skill.get("label", "") for skill in skills_other if skill.get("label")]
            
            # Extract basic info from API or use existing
            raw_job_id = job_details.get("jobId", existing_job.job_id if existing_job else "")
            # Add naukri prefix if not already present
            job_id = raw_job_id if raw_job_id.startswith("naukri_") else f"naukri_{raw_job_id}" if raw_job_id else ""
            # Convert skills list to comma-separated string for database storage
            skills_list_str = ', '.join(skills_list) if skills_list else ""
            
            # Create enhanced job model with API data using correct field names
            job_model = JobModel(
                job_id=job_id,
                Job_Role=job_details.get("title", existing_job.job_role if existing_job else ""),
                Company=job_details.get("companyName", existing_job.company if existing_job else ""),
                Experience=job_details.get("experience", existing_job.experience if existing_job else ""),
                Skills=skills_list_str or (existing_job.skills if existing_job else ""),
                jd=job_details.get("description", ""),  # Use raw HTML description without cleaning
                company_detail=company_detail_raw,  # Use raw company detail from API
                platform="naukri",
                url=job_details.get("jobUrl", existing_job.url if existing_job else ""),
                location=job_details.get("placeholders", existing_job.location if existing_job else ""),
                salary=job_details.get("salary", existing_job.salary if existing_job else ""),
                posted_date=job_details.get("createdDate", existing_job.posted_date if existing_job else datetime.now()),
                skills_list=skills_list,
                normalized_skills=None  # Will be auto-populated by model validator
            )
            logger.info(f"[ENRICH] Added {len(skills_list)} skills | Description: {len(job_details.get('description', ''))} chars")
            
            return job_model
            
        except Exception as e:
            logger.error(f"[API PARSE ERROR] {e}")
            if existing_job:
                return existing_job
            raise
    
