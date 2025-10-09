#!/usr/bin/env python3
# Naukri job detail fetcher - HTML file parsing with BeautifulSoup
# EMD Compliance: ≤80 lines

import logging
import re
from typing import Dict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class NaukriJobDetailFetcher:
    """Extract job details from saved HTML files using BeautifulSoup"""
    
    def __init__(self):
        logger.info("[JOB FETCHER] Initialized for HTML file parsing")
    
    def extract_from_html_file(self, html_filepath: str) -> Dict[str, str]:
        """
        Extract job description and company details from saved HTML file
        
        Args:
            html_filepath: Path to saved HTML file
            
        Returns:
            Dict with job_description, company_details, and skills
        """
        
        details = {
            "job_description": "",
            "company_details": "",
            "additional_skills": ""
        }
        
        try:
            # Read and parse HTML file
            with open(html_filepath, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.info(f"[PARSER] Loaded HTML file: {html_filepath}")
            
            # Extract job description using CSS selectors
            job_desc_selectors = [
                "section.job-desc div.text",
                ".job-desc .text",
                ".job-description",
                "[data-job-description]"
            ]
            
            for selector in job_desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    details["job_description"] = desc_elem.get_text().strip()
                    logger.info(f"[JD] Extracted {len(details['job_description'])} chars")
                    break
            
            # Extract company details using CSS selectors
            company_selectors = [
                "div.company-info p",
                "section.comp-sec div",
                ".company-details",
                "[data-company-info]"
            ]
            
            for selector in company_selectors:
                company_elem = soup.select_one(selector)
                if company_elem:
                    details["company_details"] = company_elem.get_text().strip()
                    logger.info(f"[CD] Extracted {len(details['company_details'])} chars")
                    break
            
            # Extract additional skills using regex
            combined_text = f"{details['job_description']} {details['company_details']}"
            skill_patterns = [
                r'\b(?:Python|JavaScript|Java|React|Node\.js|AWS|Docker|Kubernetes)\b',
                r'\b(?:SQL|NoSQL|MongoDB|PostgreSQL|MySQL)\b',
                r'\b(?:Machine Learning|AI|Data Science|Analytics)\b'
            ]
            
            found_skills = set()
            for pattern in skill_patterns:
                matches = re.findall(pattern, combined_text, re.IGNORECASE)
                found_skills.update(matches)
            
            details["additional_skills"] = ", ".join(found_skills) if found_skills else ""
            logger.info(f"[SKILLS] Found {len(found_skills)} additional skills")
            
        except FileNotFoundError:
            logger.error(f"[ERROR] HTML file not found: {html_filepath}")
                # Try fallback selectors
                fallback_selectors = [".company-details", "[data-qa='company_details']", ".comp-info"]
                for selector in fallback_selectors:
                    try:
                        company_elem = driver.find_element(By.CSS_SELECTOR, selector)
                        details["company_details"] = company_elem.text.strip()
                        if details["company_details"]:
                            logger.info(f"[COMPANY_DETAILS] FALLBACK SUCCESS with {selector}")
                            break
                    except NoSuchElementException:
                        continue
                
        except Exception as e:
            logger.error(f"[PHASE 2] Error fetching {job_url}: {e}")
        
        logger.info(f"[PHASE 2] Completed for {job_url} - JD: {len(details['job_description'])} chars, Company: {len(details['company_details'])} chars")
        return details
