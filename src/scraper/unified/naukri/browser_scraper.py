"""Naukri Browser Scraper - Direct HTML extraction via Playwright
EMD Compliance: <=80 lines, browser automation
"""
from __future__ import annotations

import asyncio
import logging

from bs4 import BeautifulSoup, Tag

from src.models.models import JobDetailModel, JobUrlModel
from src.scraper.services.playwright_browser import PlaywrightBrowser

logger = logging.getLogger(__name__)


async def scrape_naukri_jobs_browser(
    keyword: str,
    location: str = "",
    limit: int = 20,
    headless: bool = False
) -> list[JobDetailModel]:
    """Scrape Naukri jobs with pagination - no caps, dynamic limit"""

    jobs: list[JobDetailModel] = []
    base_url = f"https://www.naukri.com/{keyword.lower().replace(' ', '-')}-jobs"
    page = 1
    
    async with PlaywrightBrowser(headless=headless) as browser:
        while len(jobs) < limit:
            try:
                # Build paginated URL (page 1 has no suffix, page 2+ has -2, -3, etc.)
                search_url = f"{base_url}-{page}" if page > 1 else base_url
                logger.info(f"📄 Page {page}: {search_url} (collected {len(jobs)}/{limit})")
                
                # Render search page
                html = await browser.render_url(search_url, wait_seconds=3.0)
                
                if not html:
                    logger.error(f"Failed to render page {page}")
                    break
                
                # Parse HTML
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find job cards
                selectors = ['.cust-job-tuple', 'article.jobTuple', 'article[data-job-id]']
                job_cards: list[Tag] = []
                for selector in selectors:
                    job_cards = soup.select(selector)
                    if job_cards:
                        break
                
                if not job_cards:
                    logger.info(f"No more jobs found on page {page}")
                    break
                
                # Extract job data from current page
                for card in job_cards:
                    try:
                        # Extract title
                        title_elem = card.select_one('.title, .jobTuple-title a, [class*="title"]')
                        title: str = title_elem.text.strip() if title_elem else "Unknown Title"

                        # Extract URL
                        link_elem = card.select_one('a[href*="job-listings"]')
                        href_val: str | list[str] | None = link_elem.get('href') if link_elem else None
                        href: str = href_val if isinstance(href_val, str) else ''
                        url: str = href if href.startswith('http') else f"https://www.naukri.com{href}"

                        # Extract company (2025 Naukri: .comp-name inside .comp-dtls-wrap)
                        company_elem = card.select_one('.comp-name, .companyInfo, [class*="company"]')
                        company: str = company_elem.text.strip() if company_elem else "Unknown Company"

                        # Generate job_id from URL
                        job_id: str = JobUrlModel.generate_job_id("naukri", url) if url else JobUrlModel.generate_job_id("naukri", f"{title}-{company}")

                        jobs.append(JobDetailModel(
                            job_id=job_id,
                            platform="naukri",
                            actual_role=title,
                            url=url,
                            job_description="",
                            company_name=company,
                            posted_date=None  # JobDetailModel expects datetime | None
                        ))

                        # Stop if we've reached the limit
                        if len(jobs) >= limit:
                            break

                    except Exception as e:
                        logger.warning(f"Failed to parse job card: {e}")
                        continue
                
                # Move to next page
                page += 1
                
            except Exception as e:
                logger.error(f"Page {page} scraping failed: {e}")
                break
        
        logger.info(f"✅ Scraped {len(jobs)} jobs from {page-1} pages")
        
        # Enrich with parallel page scraping (5 concurrent tabs)
        if jobs:
            jobs = await _enrich_parallel_pages(jobs, browser)
    
    return jobs


async def _enrich_parallel_pages(
    jobs: list[JobDetailModel], browser: PlaywrightBrowser
) -> list[JobDetailModel]:
    """Enrich jobs by scraping individual pages in parallel (5 tabs)"""
    try:
        # Create 5 concurrent tasks (semaphore limits to 5 at once)
        semaphore = asyncio.Semaphore(5)
        tasks = [_scrape_job_page(job, browser, semaphore) for job in jobs]
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Enriched {len(jobs)} jobs via parallel page scraping")
    except Exception as e:
        logger.warning(f"Parallel page scraping failed: {e}")
    return jobs


async def _scrape_job_page(
    job: JobDetailModel, browser: PlaywrightBrowser, semaphore: asyncio.Semaphore
) -> None:
    """Scrape individual job page for description and skills"""
    from playwright.async_api import Page

    async with semaphore:
        page: Page | None = None
        try:
            page = await browser.new_page()
            await page.goto(job.url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            html: str = await page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Extract description (more specific selectors)
            desc_elem: Tag | None = soup.select_one('.styles_JDC__dang-inner-html__h0K4t, [class*="job-description"], .dang-inner-html')
            if not desc_elem:
                desc_elem = soup.select_one('.job-description, section[class*="job"] p, div[class*="description"] p')
            if desc_elem:
                job.job_description = desc_elem.get_text(separator=" ", strip=True)[:2000]

            # Extract skills (target skill chips/tags specifically)
            skills_container: Tag | None = soup.select_one('.styles_jhc__key-skill__DKjCg, [class*="key-skill"], .key-skill')
            if skills_container:
                skills_elems: list[Tag] = skills_container.select('a, span.chip, .chip-text')
                skills: list[str] = [s.get_text(strip=True) for s in skills_elems if s.get_text(strip=True)][:10]
                job.skills = ",".join(skills)

        except Exception as e:
            logger.warning(f"Failed to scrape {job.url}: {e}")
        finally:
            if page:
                await page.close()
