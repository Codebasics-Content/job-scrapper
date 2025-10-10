#!/usr/bin/env python3
# Naukri browser-based scraper
import asyncio
import logging
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from typing import TypedDict
from browser_manager.manager.selenium import BrowserManager
from src.scraper.base.base_scraper import BaseJobScraper
from .extractors.card_extractor import NaukriCardExtractor
from .extractors.job_detail_fetcher import NaukriJobDetailFetcher
from .extractors.api_parser import NaukriAPIParser
from src.scraper.base.skill_validator import SkillValidator
from src.models import JobModel
from .config.selectors import JOB_CARD_SELECTORS


class CompanyDetail(TypedDict, total=False):
    """Type definition for company detail in bulk API data."""
    name: str


class BulkJobData(TypedDict, total=False):
    """Type definition for bulk API job data structure."""
    jobDescription: str
    companyDetail: CompanyDetail
    tagsAndSkills: str


class JobCardHTML(TypedDict):
    """Structure for storing job card HTML temporarily."""
    job_id: str
    html_content: str
    card_index: int


logger = logging.getLogger(__name__)

class NaukriBrowserScraper(BaseJobScraper):
    """Naukri.com browser-based job scraper"""
    
    BASE_URL = "https://www.naukri.com"
    BATCH_SIZE: int = 20  # Process 20 job cards per batch
    
    def __init__(self, browser_manager: BrowserManager) -> None:
        self.browser_manager = browser_manager
        self.card_extractor = NaukriCardExtractor()
        self.skill_validator = SkillValidator()
        self.batch_html_storage: list[JobCardHTML] = []
        self.job_detail_fetcher = NaukriJobDetailFetcher()
        self.api_parser = NaukriAPIParser()
    
    async def scrape_jobs(
        self,
        job_role: str,
        target_count: int,
        location: str = ""
    ) -> list[JobModel]:
        """Scrape jobs using browser automation"""
        logger.info(f"[NAUKRI START] Browser scraping {target_count} jobs for '{job_role}'")
        
        self.setup_driver_pool()
        driver = self.get_driver()
        
        if not driver:
            logger.error("[NAUKRI] Failed to get driver from pool")
            return []
        
        try:
            all_jobs: list[JobModel] = []
            keyword_slug = job_role.replace(' ', '-').lower()
            keyword_param = job_role.replace(' ', '+')
            
            # Calculate pages needed (20 jobs per page)
            jobs_per_page = 20
            total_pages = (target_count // jobs_per_page) + 1
            
            logger.info(f"[NAUKRI] Scraping {total_pages} pages for {target_count} jobs")
            
            for page_num in range(1, total_pages + 1):
                if len(all_jobs) >= target_count:
                    break
                
                # Build pagination URL
                if page_num == 1:
                    page_url = f"{self.BASE_URL}/{keyword_slug}-jobs?k={keyword_param}"
                else:
                    page_url = f"{self.BASE_URL}/{keyword_slug}-jobs-{page_num}?k={keyword_param}"
                
                logger.info(f"[NAUKRI] Page {page_num}/{total_pages}: {page_url}")
                driver.get(page_url)
                
                # Special handling for first page - needs more time to load
                if page_num == 1:
                    time.sleep(5)  # Longer initial wait for first page
                else:
                    time.sleep(3)  # Standard wait
                page_title = driver.title
                current_url = driver.current_url
                logger.info(f"[NAUKRI DEBUG] Page title: {page_title}")
                logger.info(f"[NAUKRI DEBUG] Current URL: {current_url}")
                
                # Check page source for debugging
                page_source = driver.page_source
                if "jobTuple" in page_source:
                    logger.info("[NAUKRI DEBUG] Found 'jobTuple' in page source")
                if "srp-jobtuple" in page_source:
                    logger.info("[NAUKRI DEBUG] Found 'srp-jobtuple' in page source")
                if "cust-job-tuple" in page_source:
                    logger.info("[NAUKRI DEBUG] Found 'cust-job-tuple' in page source")
                if "No jobs found" in page_source or "0 Jobs" in page_source:
                    logger.warning("[NAUKRI DEBUG] Page indicates no jobs found")
                # More specific captcha detection to avoid false positives
                if "g-recaptcha" in page_source or "captcha-box" in page_source:
                    logger.error("[NAUKRI DEBUG] Captcha detected in page")
                    logger.warning("[NAUKRI] Stopping due to captcha detection")
                    break
                    
                # Save page source for debugging
                try:
                    source_path = f"/tmp/naukri_page_{page_num}.html"
                    with open(source_path, 'w', encoding='utf-8') as f:
                        f.write(page_source[:5000])  # First 5000 chars
                    logger.info(f"[NAUKRI DEBUG] Page source saved to {source_path}")
                except Exception as e:
                    logger.warning(f"[NAUKRI DEBUG] Could not save page source: {e}")
                
                # Save screenshot for debugging
                try:
                    screenshot_path = f"/tmp/naukri_page_{page_num}.png"
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"[NAUKRI DEBUG] Screenshot saved to {screenshot_path}")
                except Exception as e:
                    logger.warning(f"[NAUKRI DEBUG] Could not save screenshot: {e}")
                
                # Wait for any of the job card selectors to appear
                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ", ".join(JOB_CARD_SELECTORS)))
                    )
                    logger.info("[NAUKRI DEBUG] Job cards detected on page")
                except Exception as e:
                    logger.warning(f"[NAUKRI DEBUG] Timeout waiting for job cards: {e}")
                    # Check if we got redirected or blocked
                    if "captcha" in current_url.lower() or "verify" in current_url.lower():
                        logger.error("[NAUKRI] Captcha or verification detected!")
                    
                await asyncio.sleep(2)  # Additional wait for dynamic content
                
                # Extract all job cards on current page using multiple selectors
                job_cards = []
                        
                for selector in JOB_CARD_SELECTORS:
                    try:
                        if selector.startswith("."):
                            cards = driver.find_elements(By.CLASS_NAME, selector[1:])
                        else:
                            cards = driver.find_elements(By.CSS_SELECTOR, selector)
                        if cards:
                            job_cards = cards
                            logger.info(f"[NAUKRI] Found {len(cards)} jobs using selector: {selector}")
                            break
                        else:
                            logger.debug(f"[NAUKRI DEBUG] No elements found with selector: {selector}")
                    except Exception as e:
                        logger.debug(f"[NAUKRI DEBUG] Error with selector {selector}: {e}")
                        continue
                
                if not job_cards:
                    logger.info(f"[NAUKRI] Found 0 jobs on page {page_num}")
                    # Try to find ANY article elements as a last resort
                    articles = driver.find_elements(By.TAG_NAME, "article")
                    if articles:
                        logger.info(f"[NAUKRI DEBUG] Found {len(articles)} article elements on page")
                        # Log first article's attributes for debugging
                        if articles:
                            first = articles[0]
                            logger.info(f"[NAUKRI DEBUG] First article class: {first.get_attribute('class') or ''}")
                            outer_html = first.get_attribute('outerHTML') or ''
                            logger.info(f"[NAUKRI DEBUG] First article HTML: {outer_html[:200]}")
                    else:
                        logger.warning("[NAUKRI DEBUG] No article elements found at all")
                
                # Early exit if no jobs found (end of results)
                if len(job_cards) == 0:
                    logger.warning(f"[NAUKRI] No jobs on page {page_num} - reached end of available jobs")
                    break
                
                # Process jobs in batches for efficient HTML collection
                batch_cards: list[WebElement] = []
                for card in job_cards:
                    if len(all_jobs) >= target_count:
                        break
                    
                    batch_cards.append(card)
                    
                    # Process batch when it reaches BATCH_SIZE or is the last batch
                    if len(batch_cards) >= self.BATCH_SIZE or card == job_cards[-1]:
                        try:
                            # Collect HTML for all jobs in batch
                            batch_html_data = self._collect_batch_html(driver, batch_cards, len(batch_cards))
                            
                            # Process batch HTML to extract job details
                            batch_jobs = self._process_batch_html(batch_html_data)
                            
                            # Add processed jobs to results
                            for job in batch_jobs:
                                if len(all_jobs) < target_count and job:
                                    all_jobs.append(job)
                                    
                            logger.info(f"[NAUKRI] Batch progress: {len(all_jobs)}/{target_count} jobs processed")
                            
                            # Clear batch data for memory management
                            self._clear_batch_html(batch_html_data)
                            batch_cards.clear()
                            
                        except Exception as e:
                            logger.error(f"[NAUKRI] Error processing batch: {e}")
                            # Fall back to individual processing for this batch
                            for card in batch_cards:
                                try:
                                    job = self._extract_job_from_card(card, driver)
                                    if job and len(all_jobs) < target_count:
                                        all_jobs.append(job)
                                except Exception as card_error:
                                    logger.debug(f"[NAUKRI] Error extracting individual job: {card_error}")
                                    continue
                            batch_cards.clear()
            
            # Enrich all jobs with bulk API data
            logger.info(f"[NAUKRI] Enriching {len(all_jobs)} jobs with bulk API data")
            enriched_jobs = await self._enrich_with_bulk_data(all_jobs, {})
            
            # Log completion with clarity
            if len(enriched_jobs) < target_count:
                logger.warning(
                    f"[NAUKRI COMPLETE] Scraped {len(enriched_jobs)}/{target_count} jobs "
                    f"(only {len(enriched_jobs)} available on Naukri)"
                )
            else:
                logger.info(f"[NAUKRI COMPLETE] Scraped {len(enriched_jobs)} jobs")
            return enriched_jobs
            
        finally:
            # Immediate cleanup - browser closes instantly after scraping
            self.cleanup_pool()
            logger.info("[NAUKRI] Browser cleanup complete")
    
    def _extract_job_from_card(self, card: WebElement, driver: WebDriver) -> JobModel | None:
        """Extract job data from a job card element (card is Selenium WebElement)"""
        return self.card_extractor.extract_job_data(card, driver)
    
    async def _enrich_with_bulk_data(self, jobs: list[JobModel], bulk_job_map: dict[str, BulkJobData]) -> list[JobModel]:
        """Enrich jobs with bulk API data for skills, description, and company details"""
        try:
            # Simplified placeholder - bulk API data will be empty for now
            logger.info("[NAUKRI BULK] Bulk API data not implemented yet, returning original jobs")
            
            # Enrich scraped jobs with bulk API data
            enriched_jobs: list[JobModel] = []
            for job in jobs:
                # Try to find matching bulk API data
                bulk_match = bulk_job_map.get(job.job_role.strip().lower())
                if bulk_match:
                    # Extract full description from bulk API (NO LIMITS)
                    job_description: str = bulk_match.get('jobDescription', '')
                    if job_description:
                        job.jd = job_description  # No character limit
                        
                    # Extract company details
                    company_detail: CompanyDetail = bulk_match.get('companyDetail', {})
                    company_name: str = job.company  # Default company name
                    if company_detail and 'name' in company_detail:
                        company_name = company_detail.get('name', job.company)
                        job.company = company_name
                    
                    # Extract ALL skills from bulk API and validate relevance
                    skills_data: str = bulk_match.get('tagsAndSkills', '')
                    if skills_data and job_description:
                        all_skills: list[str] = [skill.strip() for skill in skills_data.split(',') if skill.strip()]
                        
                        # Validate skills against job description and company
                        validated_skills: list[str] = self._validate_skills_relevance(
                            all_skills, job_description, company_name, job.job_role
                        )
                        
                        if validated_skills:
                            job.skills = ", ".join(validated_skills)  # Convert list to comma-separated string
                            logger.info(f"[NAUKRI BULK] Enhanced {job.job_role} with {len(validated_skills)} validated skills")
                        else:
                            # Fallback: use all skills if validation fails
                            job.skills = ", ".join(all_skills)  # Convert list to comma-separated string
                            logger.info(f"[NAUKRI BULK] Enhanced {job.job_role} with {len(all_skills)} skills (no description)")
                        
                enriched_jobs.append(job)
                
            logger.info(f"[NAUKRI BULK] Enhanced {len(enriched_jobs)} jobs with bulk API data")
            return enriched_jobs
            
        except Exception as e:
            logger.error(f"[NAUKRI BULK] Bulk API enrichment failed: {e}")
            return jobs
    
    def _validate_skills_relevance(self, skills: list[str], job_description: str, company_name: str, job_title: str) -> list[str]:
        """Validate skill relevance against job description, company, and role"""
        try:
            validated_skills: list[str] = []
            
            if not job_description or not skills:
                return skills
            
            # Create combined text for matching
            description_lower: str = job_description.lower()
            company_lower: str = company_name.lower()
            title_lower: str = job_title.lower()
            combined_text: str = f"{description_lower} {company_lower} {title_lower}"
            
            for skill in skills:
                skill_clean: str = skill.strip()
                if not skill_clean or len(skill_clean) < 2:
                    continue
                    
                skill_lower: str = skill_clean.lower()
                
                # Check if skill is mentioned in job description, company, or title
                if (skill_lower in description_lower or 
                    skill_lower in company_lower or 
                    skill_lower in title_lower or
                    any(word in combined_text for word in skill_lower.split() if len(word) > 2)):
                    validated_skills.append(skill_clean)
                    continue
                
                # Check for partial matches and common variations
                skill_keywords: list[str] = skill_lower.split()
                if any(keyword in combined_text for keyword in skill_keywords if len(keyword) > 3):
                    validated_skills.append(skill_clean)
            
            logger.debug(f"[SKILL VALIDATION] {job_title}: {len(skills)} → {len(validated_skills)} relevant skills")
            return validated_skills
            
        except Exception as e:
            logger.warning(f"[SKILL VALIDATION] Validation failed for {job_title}: {e}")
            # Return all skills if validation fails
            return skills

    def _extract_job_url(self, card: WebElement) -> str | None:
        """Extract job URL from job card element."""
        try:
            # Try multiple selectors for job URL
            url_selectors = [
                "a[href*='/job-detail/']",  # Primary job detail link
                "a[href*='/jobs/']",        # Alternative job link
                ".title a",                 # Title link
                "a.title"                   # Title as link
            ]
            
            for selector in url_selectors:
                try:
                    link_element = card.find_element(By.CSS_SELECTOR, selector)
                    job_url = link_element.get_attribute('href')
                    if job_url and 'naukri.com' in job_url:
                        return job_url
                except Exception:
                    continue
                    
            logger.debug("[URL EXTRACT] No valid job URL found in card")
            return None
            
        except Exception as e:
            logger.debug(f"[URL EXTRACT] Failed to extract job URL: {e}")
            return None

    def _collect_batch_html(self, driver: WebDriver, batch_size: int = 20) -> list[JobCardHTML]:
        """Collect HTML from individual job detail pages."""
        batch_html: list[JobCardHTML] = []
        
        try:
            # Get job URLs from search result cards
            primary_selector = JOB_CARD_SELECTORS[0]
            job_cards = driver.find_elements(By.CSS_SELECTOR, primary_selector)
            logger.info(f"[BATCH COLLECT] Found {len(job_cards)} job cards on page")
            
            for i, card in enumerate(job_cards[:batch_size]):
                try:
                    # Extract job URL from card
                    job_url = self._extract_job_url(card)
                    if not job_url:
                        logger.debug(f"[BATCH COLLECT] No URL found for card {i}")
                        continue
                        
                    # Navigate to job detail page
                    logger.debug(f"[BATCH COLLECT] Navigating to job {i}: {job_url}")
                    driver.get(job_url)
                    
                    # Wait for page to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # Get complete HTML from job detail page
                    job_page_html = driver.page_source
                    job_id = f"batch-job-{i}-{datetime.now().timestamp()}"
                    
                    batch_html.append(JobCardHTML(
                        job_id=job_id,
                        html_content=job_page_html,
                        card_index=i
                    ))
                    
                    logger.debug(f"[BATCH COLLECT] Collected HTML for job {i} ({len(job_page_html)} chars)")
                    
                except Exception as e:
                    logger.debug(f"[BATCH COLLECT] Failed to collect HTML for job {i}: {e}")
                    
            logger.info(f"[BATCH COLLECT] Collected HTML from {len(batch_html)} job detail pages")
            return batch_html
            
        except Exception as e:
            logger.error(f"[BATCH COLLECT] Failed to collect batch HTML: {e}")
            return batch_html

    def _process_batch_html(self, driver: WebDriver, batch_html: list[JobCardHTML]) -> list[JobModel]:
        """Process batch HTML to extract job details from job detail pages."""
        processed_jobs: list[JobModel] = []
        
        try:
            logger.info(f"[BATCH PROCESS] Processing {len(batch_html)} job detail pages")
            
            for job_html in batch_html:
                try:
                    # Extract job data directly from job detail page HTML
                    job_data = self._extract_job_from_page_html(
                        job_html["html_content"],
                        job_html["job_id"]
                    )
                    
                    if job_data:
                        processed_jobs.append(job_data)
                    
                except Exception as e:
                    logger.debug(f"[BATCH PROCESS] Failed to process job {job_html['job_id']}: {e}")
                    
            logger.info(f"[BATCH PROCESS] Successfully processed {len(processed_jobs)} jobs")
            return processed_jobs
            
        except Exception as e:
            logger.error(f"[BATCH PROCESS] Failed to process batch HTML: {e}")
            return processed_jobs

    def _extract_job_from_page_html(self, html_content: str, job_id: str) -> JobModel | None:
        """Extract job data from job detail page HTML."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract job title
            job_title_elem = soup.select_one('[class*="jd-header-title"], h1, [data-testid="job-title"]')
            job_title = job_title_elem.get_text(strip=True) if job_title_elem else "Unknown"
            
            # Extract company name
            company_elem = soup.select_one('[class*="comp-name"], [class*="company"], [data-testid="company-name"]')
            company_name = company_elem.get_text(strip=True) if company_elem else "Unknown"
            
            # Extract job description
            jd_elem = soup.select_one('[class*="jd-desc"], [class*="job-desc"], [class*="description"]')
            job_description = jd_elem.get_text(strip=True) if jd_elem else ""
            
            # Extract experience
            exp_elem = soup.select_one('[class*="exp"], [class*="experience"]')
            experience = exp_elem.get_text(strip=True) if exp_elem else ""
            
            # Extract location  
            loc_elem = soup.select_one('[class*="loc"], [class*="location"]')
            location = loc_elem.get_text(strip=True) if loc_elem else ""
            
            # Extract salary
            salary_elem = soup.select_one('[class*="salary"], [class*="sal"]')
            salary = salary_elem.get_text(strip=True) if salary_elem else ""
            
            # Extract skills
            skills_text = ""
            skills_elems = soup.select('[class*="skill"], [class*="tag"]')
            if skills_elems:
                skills_text = ", ".join([elem.get_text(strip=True) for elem in skills_elems])
            
            return JobModel(
                job_id=job_id,
                Job_Role=job_title,
                Company=company_name,
                Experience=experience,
                Skills=skills_text,
                jd=job_description,
                company_detail="",
                platform="naukri",
                url="",
                location=location,
                salary=salary,
                posted_date=None,
                scraped_at=datetime.now(),
                skills_list=None,
                normalized_skills=None
            )
            
        except Exception as e:
            logger.debug(f"[HTML EXTRACT] Failed to extract job {job_id}: {e}")
            return None

    def _clear_batch_html(self, batch_html: list[JobCardHTML]) -> None:
        """Clear batch HTML data to free memory."""
        try:
            batch_html.clear()
            logger.debug("[BATCH CLEAR] Cleared batch HTML data")
        except Exception as e:
            logger.warning(f"[BATCH CLEAR] Failed to clear batch HTML: {e}")