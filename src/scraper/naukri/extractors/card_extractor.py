#!/usr/bin/env python3
# Naukri job card data extractor
# EMD Compliance: ≤80 lines

import logging
import hashlib
from datetime import datetime
from typing import Any
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.models import JobModel
from ..config.selectors import ELEMENT_SELECTORS

logger = logging.getLogger(__name__)

class NaukriCardExtractor:
    """Extract job data from Naukri job card elements"""
    
    @staticmethod
    def extract_job_data(card: Any, job_role: str) -> JobModel | None:
        """Extract all job data from a job card (card is Selenium WebElement)"""
        try:
            # Title - try multiple selectors
            title = ""
            for selector in ELEMENT_SELECTORS["title"]:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except NoSuchElementException:
                    continue
            
            # Company - try multiple selectors
            company = ""
            for selector in ELEMENT_SELECTORS["company"]:
                try:
                    company_elem = card.find_element(By.CSS_SELECTOR, selector)
                    company = company_elem.text.strip()
                    if company:
                        break
                except NoSuchElementException:
                    continue
            
            # Experience (optional) - try multiple selectors
            experience = ""
            for selector in ELEMENT_SELECTORS["experience"]:
                try:
                    if selector.startswith("."):
                        exp_elem = card.find_element(By.CLASS_NAME, selector[1:])
                    else:
                        exp_elem = card.find_element(By.CSS_SELECTOR, selector)
                    experience = exp_elem.text.strip()
                    if experience:
                        break
                except NoSuchElementException:
                    continue
            
            # Skills (optional) - try multiple selectors
            skills_list: list[str] = []
            for selector in ELEMENT_SELECTORS["skills"]:
                try:
                    skill_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    skills_list = [s.text.strip() for s in skill_elems if s.text.strip()]
                    if skills_list:
                        break
                except NoSuchElementException:
                    continue
            
            # Location (optional) - try multiple selectors
            location = ""
            for selector in ELEMENT_SELECTORS["location"]:
                try:
                    if selector.startswith("."):
                        loc_elem = card.find_element(By.CLASS_NAME, selector[1:])
                    else:
                        loc_elem = card.find_element(By.CSS_SELECTOR, selector)
                    location = loc_elem.text.strip()
                    if location:
                        break
                except NoSuchElementException:
                    continue
            
            # Job link - try multiple selectors
            job_url = ""
            for selector in ELEMENT_SELECTORS["title"]:
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, selector)
                    if link_elem.tag_name.lower() == "a":
                        job_url = link_elem.get_attribute("href") or ""
                        if job_url:
                            break
                except NoSuchElementException:
                    continue
            
            # Generate unique job_id with naukri prefix
            job_id_str = f"{title}_{company}_{datetime.now().isoformat()}"
            hash_id = hashlib.md5(job_id_str.encode()).hexdigest()
            job_id = f"naukri_{hash_id}"
            logger.info(f"[CARD EXTRACT] Job: {title[:50]} | ID: {job_id} | Skills: {len(skills_list)}")
            
            # Description placeholder (will be enriched from API if available)
            description = f"{title} at {company}. {experience}. Location: {location}"
            
            return JobModel(
                job_id=job_id,
                Job_Role=title,
                Company=company,
                Experience=experience,
                Skills=", ".join(skills_list) if skills_list else "",
                jd=description,
                platform="naukri",
                url=job_url,
                location=location,
                salary=None,
                posted_date=None,
                scraped_at=datetime.now(),
                skills_list=skills_list if skills_list else None,
                normalized_skills=None
            )
            
        except Exception as e:
            logger.debug(f"[CARD EXTRACT ERROR] {e}")
            return None
