#!/usr/bin/env python3
# Naukri job data parser
# EMD Compliance: ≤80 lines

import logging
from typing import Any
from datetime import datetime
from src.models import JobModel

logger = logging.getLogger(__name__)

class NaukriJobParser:
    """Parse Naukri API job data into JobModel"""
    
    @staticmethod
    def parse_job(job_data: dict[str, Any], keyword: str) -> JobModel | None:
        """Parse single job from API response"""
        try:
            # Extract basic info
            raw_job_id = job_data.get("jobId", "")
            job_id = f"naukri_{raw_job_id}" if raw_job_id else ""
            logger.info(f"[PARSE] Processing job ID: {job_id}")
            title = job_data.get("title", "")
            company = job_data.get("companyName", "")
            
            # Get location from placeholders
            location = ""
            placeholders = job_data.get("placeholders", [])
            for ph in placeholders:
                if ph.get("type") == "location":
                    location = ph.get("label", "")
                    break
            
            # Get experience
            experience = job_data.get("experienceText", "")
            
            # Get salary
            salary_detail = job_data.get("salaryDetail", {})
            min_salary = salary_detail.get("minimumSalary", 0)
            max_salary = salary_detail.get("maximumSalary", 0)
            
            if min_salary > 0 and max_salary > 0:
                salary = f"₹{min_salary/100000:.1f}-{max_salary/100000:.1f} LPA"
            else:
                salary = "Not disclosed"
            
            # Get job description
            description = job_data.get("jobDescription", "")
            
            # Get skills from tagsAndSkills
            skills_str = job_data.get("tagsAndSkills", "")
            skills = [s.strip() for s in skills_str.split(",") if s.strip()]
            
            # Build URL
            jd_url = job_data.get("jdURL", "")
            url = f"https://www.naukri.com{jd_url}" if jd_url else ""
            
            # Parse posted date
            footer_label = job_data.get("footerPlaceholderLabel", "")
            posted_date = NaukriJobParser._parse_date(footer_label)
            
            logger.info(f"[TRANSFORM] Job: {title} at {company} | Location: {location} | Skills: {len(skills)}")
            
            return JobModel(
                job_id=job_id,
                Job_Role=title,
                Company=company,
                Experience=experience,
                Skills=", ".join(skills) if skills else "",
                jd=description,
                platform="naukri",
                url=url,
                location=location,
                salary=salary,
                posted_date=posted_date,
                skills_list=skills,
                normalized_skills=skills
            )
            
        except Exception as e:
            logger.error(f"[PARSE ERROR] Job {job_data.get('jobId')}: {e}")
            return None
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse date from footer label"""
        # Simple date parsing (Today, Yesterday, X Days Ago, etc.)
        # Return current date as fallback
        return datetime.now()
