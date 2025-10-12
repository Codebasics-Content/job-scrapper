# BrightData LinkedIn Real-Time Fetcher - EMD Component
# Fetches live LinkedIn job data using BrightData browser

import logging
from bs4 import BeautifulSoup
from src.scraper.services.brightdata_client import BrightDataClient

logger = logging.getLogger(__name__)

async def fetch_linkedin_jobs(
    keyword: str,
    limit: int = 50,
    location: str = "Worldwide"
) -> list[dict[str, object]]:
    """Fetch LinkedIn jobs in real-time using BrightData
    
    Args:
        keyword: Job search keyword
        limit: Maximum jobs to fetch
        location: Job location filter
    
    Returns:
        List of job data dicts compatible with parser
    """
    logger.info(f"Fetching LinkedIn jobs: {keyword}, limit={limit}")
    
    # Build LinkedIn search URL
    search_url = _build_linkedin_search_url(keyword, location)
    
    # Fetch with BrightData
    async with BrightDataClient() as client:
        html = await client.render_with_captcha_solving(search_url)
    
    # Parse search results
    jobs = _parse_linkedin_search_results(html, limit)
    
    logger.info(f"Fetched {len(jobs)} LinkedIn jobs")
    return jobs


def _build_linkedin_search_url(keyword: str, location: str) -> str:
    """Build LinkedIn job search URL"""
    base_url = "https://www.linkedin.com/jobs/search/"
    keyword_param = keyword.replace(" ", "%20")
    location_param = location.replace(" ", "%20")
    
    return f"{base_url}?keywords={keyword_param}&location={location_param}"


def _parse_linkedin_search_results(
    html: str,
    limit: int
) -> list[dict[str, object]]:
    """Parse LinkedIn search results HTML to job dicts"""
    soup = BeautifulSoup(html, 'html.parser')
    jobs: list[dict[str, object]] = []
    
    # Find job cards (LinkedIn structure may vary)
    job_cards = soup.select('.job-search-card, .base-card')[:limit]
    
    for card in job_cards:
        job_data = _extract_job_from_card(card)
        if job_data:
            jobs.append(job_data)
    
    return jobs


def _extract_job_from_card(card: object) -> dict[str, object] | None:
    """Extract job data from LinkedIn job card"""
    try:
        title_elem = card.select_one('.base-search-card__title, h3')  # type: ignore
        company_elem = card.select_one('.base-search-card__subtitle, h4')  # type: ignore
        link_elem = card.select_one('a')  # type: ignore
        
        if not title_elem or not link_elem:
            return None
        
        return {
            "title": title_elem.get_text(strip=True),  # type: ignore
            "company": company_elem.get_text(strip=True) if company_elem else "",  # type: ignore
            "url": link_elem.get('href', ''),  # type: ignore
            "description": "",  # Will be enriched later if needed
        }
    except Exception as error:
        logger.debug(f"Failed to extract job card: {error}")
        return None
