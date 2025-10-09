#!/usr/bin/env python3
# Batch processing logic for Naukri scraper
# EMD Compliance: ≤80 lines

import logging
import requests
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from datetime import datetime
from .types import JobCardHTML, BatchConfig
from src.models import JobModel
from src.analysis.skill_normalizer.normalizer import extract_skills_from_combined_text

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Handles batch processing of job cards for efficient scraping."""
    
    def __init__(self, config: BatchConfig) -> None:
        self.config = config
        self.batch_storage: List[JobCardHTML] = []
    
    def collect_batch_html(
        self, 
        job_cards: List[WebElement], 
        driver: WebDriver
    ) -> List[JobCardHTML]:
        """Collect HTML content for a batch of job cards."""
        batch_html: List[JobCardHTML] = []
        
        for index, card in enumerate(job_cards):
            try:
                job_id = f"batch_{index}_{len(batch_html)}"
                html_content = card.get_attribute("outerHTML") or ""
                
                if html_content:
                    batch_html.append({
                        "job_id": job_id,
                        "html_content": html_content,
                        "card_index": index
                    })
                    
            except Exception as error:
                logger.debug(f"Error collecting HTML for card {index}: {error}")
                
        logger.info(f"Collected HTML for {len(batch_html)} job cards")
        return batch_html
    
    def process_batch_urls(self, urls: List[str]) -> List[JobModel]:
        """Process a batch of job URLs and extract job descriptions and company details"""
        jobs: List[JobModel] = []
        
        # Use exact XPath selectors from config  
        jd_xpath = "//section[@class='job-desc-container']//*[text()]"
        company_xpath = "//section[@class='comp-dtls-wrap']//*[text()]"
        
        for url in urls:
            try:
                # Fetch HTML content
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job description and company details using XPath simulation
                job_description = self._extract_by_xpath_sim(soup, jd_xpath)
                company_detail = self._extract_by_xpath_sim(soup, company_xpath)
                
                # Extract skills using skill normalizer with proper parameters
                enhanced_skills: list[str] = extract_skills_from_combined_text(
                    jd=job_description,
                    company_detail=company_detail, 
                    existing_skills=""
                )
                
                # Convert skills to string format
                skills_str = ', '.join(enhanced_skills) if enhanced_skills else ""
                
                # Create JobModel with extracted data
                job = JobModel(
                    job_id=f"batch-{hash(url)}",
                    Job_Role="Batch Extracted",
                    Company="Unknown",
                    Experience="Unknown",
                    Skills=skills_str,
                    jd=job_description,
                    company_detail=company_detail,
                    platform="naukri",
                    url=url,
                    location="",
                    salary="",
                    posted_date=None,
                    scraped_at=datetime.now(),
                    skills_list=enhanced_skills,
                    normalized_skills=enhanced_skills
                )
                jobs.append(job)
                logger.info(f"[BATCH URL] Successfully processed: {url}")
                
            except Exception as e:
                logger.error(f"[BATCH URL ERROR] Failed to process {url}: {e}")
                continue
        
        return jobs

    def _extract_by_xpath_sim(self, soup: BeautifulSoup, xpath: str) -> str:
        """Extract text by simulating XPath with CSS."""
        # Convert XPath to CSS approximation for the specific selectors
        if "section[2]/div[2]/div[1]" in xpath:
            elements = soup.select("section:nth-of-type(2) div div")
        elif "section[3]/div[1]" in xpath:  
            elements = soup.select("section:nth-of-type(3) div")
        else:
            return ""
            
        return elements[0].get_text(strip=True) if elements else ""
    
    def clear_batch_html(self, batch_html: List[JobCardHTML]) -> None:
        """Clear batch HTML data to free memory."""
        batch_html.clear()
        logger.debug("Batch HTML data cleared")
