#!/usr/bin/env python3
# Naukri job card data extractor
# EMD Compliance: ≤80 lines

import hashlib
import logging
from datetime import datetime, timedelta
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.models import JobModel
from ..config.selectors import ELEMENT_SELECTORS
from src.analysis.skill_normalizer.normalizer import extract_skills_from_combined_text

logger = logging.getLogger(__name__)

class NaukriCardExtractor:
    """Extract job data from Naukri job card elements"""
    
    @staticmethod
    def extract_job_data(card: WebElement, driver: WebDriver) -> JobModel:
        """Extract all job data from a job card (card is Selenium WebElement)"""
        try:
            # Title - try multiple selectors
            title = ""
            for selector in ELEMENT_SELECTORS["title"]:
                try:
                    logger.info(f"[TITLE] Trying selector: {selector}")
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        logger.info(f"[TITLE] SUCCESS with selector '{selector}': {title[:50]}")
                        break
                    else:
                        logger.info(f"[TITLE] Empty text with selector: {selector}")
                except NoSuchElementException:
                    logger.info(f"[TITLE] FAILED - Element not found for selector: {selector}")
                    continue
            
            # Company - try multiple selectors
            company = ""
            for selector in ELEMENT_SELECTORS["company"]:
                try:
                    logger.info(f"[COMPANY] Trying selector: {selector}")
                    company_elem = card.find_element(By.CSS_SELECTOR, selector)
                    company = company_elem.text.strip()
                    if company:
                        logger.info(f"[COMPANY] SUCCESS with selector '{selector}': {company[:30]}")
                        break
                    else:
                        logger.info(f"[COMPANY] Empty text with selector: {selector}")
                except NoSuchElementException:
                    logger.info(f"[COMPANY] FAILED - Element not found for selector: {selector}")
                    continue
            
            # Experience (optional) - try multiple selectors
            experience = ""
            for selector in ELEMENT_SELECTORS["experience"]:
                try:
                    logger.info(f"[EXPERIENCE] Trying selector: {selector}")
                    if selector.startswith("."):
                        exp_elem = card.find_element(By.CLASS_NAME, selector[1:])
                    else:
                        exp_elem = card.find_element(By.CSS_SELECTOR, selector)
                    experience = exp_elem.text.strip()
                    if experience:
                        logger.info(f"[EXPERIENCE] SUCCESS with selector '{selector}': {experience[:40]}")
                        break
                    else:
                        logger.info(f"[EXPERIENCE] Empty text with selector: {selector}")
                except NoSuchElementException:
                    logger.info(f"[EXPERIENCE] FAILED - Element not found for selector: {selector}")
                    continue
            
            # Skills (optional) - try multiple selectors
            skills_list: list[str] = []
            for selector in ELEMENT_SELECTORS["skills"]:
                try:
                    logger.info(f"[SKILLS] Trying selector: {selector}")
                    skill_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    skills_list = [s.text.strip() for s in skill_elems if s.text.strip()]
                    if skills_list:
                        logger.info(f"[SKILLS] SUCCESS with selector '{selector}': Found {len(skills_list)} skills")
                        break
                    else:
                        logger.info(f"[SKILLS] Empty skills list with selector: {selector}")
                except NoSuchElementException:
                    logger.info(f"[SKILLS] FAILED - Element not found for selector: {selector}")
                    continue
            
            # Location (optional) - try multiple selectors
            location = ""
            for selector in ELEMENT_SELECTORS["location"]:
                try:
                    logger.info(f"[LOCATION] Trying selector: {selector}")
                    if selector.startswith("."):
                        loc_elem = card.find_element(By.CLASS_NAME, selector[1:])
                    else:
                        loc_elem = card.find_element(By.CSS_SELECTOR, selector)
                    location = loc_elem.text.strip()
                    if location:
                        logger.info(f"[LOCATION] SUCCESS with selector '{selector}': {location[:30]}")
                        break
                    else:
                        logger.info(f"[LOCATION] Empty text with selector: {selector}")
                except NoSuchElementException:
                    logger.info(f"[LOCATION] FAILED - Element not found for selector: {selector}")
                    continue
            
            # Job link - try multiple selectors
            job_url = ""
            for selector in ELEMENT_SELECTORS["title"]:
                try:
                    logger.info(f"[JOB_URL] Trying selector: {selector}")
                    link_elem = card.find_element(By.CSS_SELECTOR, selector)
                    if link_elem.tag_name.lower() == "a":
                        job_url = link_elem.get_attribute("href") or ""
                        if job_url:
                            logger.info(f"[JOB_URL] SUCCESS with direct link '{selector}': {job_url[:50]}")
                            break
                    else:
                        # Check if there's a link inside this element
                        try:
                            inner_link = link_elem.find_element(By.TAG_NAME, "a")
                            job_url = inner_link.get_attribute("href") or ""
                            if job_url:
                                logger.info(f"[JOB_URL] SUCCESS with inner link '{selector}': {job_url[:50]}")
                                break
                        except NoSuchElementException:
                            logger.info(f"[JOB_URL] No inner link found in selector: {selector}")
                            continue
                except NoSuchElementException:
                    logger.info(f"[JOB_URL] FAILED - Element not found for selector: {selector}")
                    continue
            
            # Extract job description and company details from search results page using XPath
            job_description = ""
            company_details = ""
            
            # Try job description XPath from config
            for xpath_selector in ELEMENT_SELECTORS["job_description"]:
                try:
                    logger.info(f"[JOB_DESC] Trying XPath: {xpath_selector}")
                    desc_elem = driver.find_element(By.XPATH, xpath_selector)
                    job_description = desc_elem.text.strip()
                    if job_description:
                        logger.info(f"[JOB_DESC] SUCCESS with XPath: {len(job_description)} chars")
                        break
                    else:
                        logger.info(f"[JOB_DESC] Empty content at XPath: {xpath_selector}")
                except NoSuchElementException:
                    logger.info(f"[JOB_DESC] XPath not found: {xpath_selector}")
                    continue
            
            # Try company details XPath from config
            for xpath_selector in ELEMENT_SELECTORS["company_details"]:
                try:
                    logger.info(f"[COMPANY_DETAILS] Trying XPath: {xpath_selector}")
                    company_elem = driver.find_element(By.XPATH, xpath_selector)
                    company_details = company_elem.text.strip()
                    if company_details:
                        logger.info(f"[COMPANY_DETAILS] SUCCESS with XPath: {len(company_details)} chars")
                        break
                    else:
                        logger.info(f"[COMPANY_DETAILS] Empty content at XPath: {xpath_selector}")
                except NoSuchElementException:
                    logger.info(f"[COMPANY_DETAILS] XPath not found: {xpath_selector}")
                    continue
            
            # Extract salary range - try multiple selectors
            salary_range = ""
            for selector in ELEMENT_SELECTORS["salary_range"]:
                try:
                    salary_elem = card.find_element(By.CSS_SELECTOR, selector)
                    salary_range = salary_elem.text.strip()
                    if salary_range and len(salary_range) > 3:  # Valid salary info
                        break
                except NoSuchElementException:
                    continue
            
            # Extract posted date - try multiple selectors
            posted_date_text = ""
            for selector in ELEMENT_SELECTORS["posted_date_element"]:
                try:
                    posted_elem = card.find_element(By.CSS_SELECTOR, selector)
                    posted_date_text = posted_elem.text.strip()
                    if posted_date_text:
                        break
                except NoSuchElementException:
                    continue
            
            # Parse posted date to datetime if available
            posted_date = None
            if posted_date_text:
                try:
                    # Try common date formats from Naukri
                    if "day" in posted_date_text.lower():
                        days_ago = int(''.join(filter(str.isdigit, posted_date_text)))
                        posted_date = datetime.now() - timedelta(days=days_ago)
                    elif "hour" in posted_date_text.lower():
                        hours_ago = int(''.join(filter(str.isdigit, posted_date_text)))
                        posted_date = datetime.now() - timedelta(hours=hours_ago)
                except (ValueError, AttributeError):
                    logger.debug(f"[CARD EXTRACT] Could not parse date: {posted_date_text}")
            
            # Enhance skills using centralized skill extraction and normalization
            enhanced_skills = extract_skills_from_combined_text(
                jd=job_description or "",
                company_detail=company_details or "",
                existing_skills=", ".join(skills_list) if skills_list else ""
            )
            # Use enhanced skills or fallback to original skills
            skills_list = enhanced_skills if enhanced_skills else skills_list
            
            # Use extracted description or fallback to constructed one
            description = job_description if job_description else f"{title} at {company}. {experience}. Location: {location}"
            
            # Generate unique job_id with naukri prefix
            job_id_str = f"{title}_{company}_{datetime.now().isoformat()}"
            hash_id = hashlib.md5(job_id_str.encode()).hexdigest()
            job_id = f"naukri_{hash_id}"
            logger.info(f"[CARD EXTRACT] Job: {title[:30]} | Salary: {salary_range[:20] if salary_range else 'N/A'} | Posted: {posted_date_text[:15] if posted_date_text else 'N/A'}")
            
            return JobModel(
                job_id=job_id,
                Job_Role=title,
                Company=company,
                Experience=experience,
                Skills=", ".join(skills_list) if skills_list else "",
                jd=description,
                company_detail=company_details,
                platform="naukri",
                url=job_url,
                location=location,
                salary=salary_range,
                posted_date=posted_date,
                scraped_at=datetime.now(),
                skills_list=skills_list if skills_list else None,
                normalized_skills=None
            )
            
        except Exception as e:
            logger.debug(f"[CARD EXTRACT ERROR] {e}")
            # Return minimal valid job model on error
            return JobModel(
                job_id="error-job",
                Job_Role="Error: Unable to extract",
                Company="Unknown",
                Experience="Unknown",
                Skills="",
                jd="Error during extraction",
                company_detail="",
                platform="naukri",
                url="",
                location="",
                salary="",
                posted_date=None,
                scraped_at=datetime.now(),
                skills_list=None,
                normalized_skills=None
            )
