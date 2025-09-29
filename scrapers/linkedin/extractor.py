#!/usr/bin/env python3
# LinkedIn job data extraction with NLP skill extraction
# EMD Compliance: ≤80 lines

import logging
import time
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from models.job import JobModel
from utils.analysis.nlp.skill_extractor import extract_skills_from_text
from .extractors.job_detail_extractor import extract_job_description, extract_criteria_items
from .extractors.selectors import (
    JOB_LISTING_SELECTORS,
    JOB_TITLE_SELECTORS,
    COMPANY_SELECTORS,
    LOCATION_SELECTORS,
    RESULTS_CONTAINER_SELECTORS
)

logger = logging.getLogger(__name__)

def _try_selectors(element: WebElement, selectors: list[str]) -> str:
    """Try multiple selectors and return first match"""
    for selector in selectors:
        try:
            return element.find_element(By.CSS_SELECTOR, selector).text.strip()
        except NoSuchElementException:
            continue
    return "Not specified"

def extract_job_from_url(url: str, job_role: str = "") -> list[JobModel]:
    """Extract jobs with fallback selector strategy
    
    Note: job_role parameter kept for API compatibility but filtering
    moved to scraper level for better separation of concerns
    """
    jobs: list[JobModel] = []
    driver: uc.Chrome | None = None
    
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options)
        driver.get(url)
        
        # Wait with fallback selectors
        for selector in RESULTS_CONTAINER_SELECTORS:
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                break
            except TimeoutException:
                continue
        
        # Find job listings with fallback
        job_elements = []
        for selector in JOB_LISTING_SELECTORS:
            job_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if job_elements:
                break
        
        for idx, job_element in enumerate(job_elements[:25]):
            try:
                # Click on job card to load details
                job_element.click()
                time.sleep(2)  # Wait for job details to load
                
                # Extract basic info from card
                job_title = _try_selectors(job_element, JOB_TITLE_SELECTORS)
                company = _try_selectors(job_element, COMPANY_SELECTORS)
                location = _try_selectors(job_element, LOCATION_SELECTORS)
                
                if job_title == "Not specified":
                    continue
                
                # Extract full job description from detail panel
                jd_text = extract_job_description(driver)
                criteria = extract_criteria_items(driver)
                
                # Extract skills using NLP
                skills_list = extract_skills_from_text(jd_text) if jd_text else []
                skills_str = ", ".join(skills_list) if skills_list else "Not specified"
                
                # Get experience from criteria or default
                experience = criteria.get("experience_level", "Not specified")
                
                jobs.append(JobModel(
                    job_id=f'linkedin_{hash(f"{job_title}_{company}_{idx}")}',
                    Job_Role=job_title, Company=company, location=location,
                    Experience=experience, Skills=skills_str,
                    jd=jd_text if jd_text else f'Job at {company}',
                    platform='LinkedIn', url=url,
                    salary=criteria.get("salary", "Not specified"),
                    posted_date=datetime.now(),
                    skills_list=skills_list,
                    normalized_skills=[s.lower() for s in skills_list],
                    scraped_at=datetime.now()
                ))
                
                logger.debug(f"Extracted job {idx+1}: {job_title} with {len(skills_list)} skills")
            except Exception as job_error:
                logger.warning(f"Failed to extract job {idx}: {job_error}")
                continue
        
        logger.info(f"Extracted {len(jobs)} jobs from LinkedIn")
    except Exception as error:
        logger.error(f"LinkedIn extraction error: {error}")
    finally:
        if driver:
            driver.quit()
    
    return jobs
