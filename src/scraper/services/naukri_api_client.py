"""Naukri API Client - Session Transfer from Playwright
Bypasses 406/captcha by using authenticated browser session
"""
from __future__ import annotations
import httpx
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class NaukriAPIClient:
    """API client using transferred browser session"""
    
    BASE_URL = "https://www.naukri.com"
    SEARCH_API = f"{BASE_URL}/jobapi/v3/search"
    DETAIL_API = f"{BASE_URL}/jobapi/v4/job"
    
    def __init__(self, cookies: Dict[str, str]):
        """Initialize with Playwright cookies"""
        self.client = httpx.AsyncClient(
            cookies=cookies,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": self.BASE_URL,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "appid": "109",
                "systemid": "Naukri",
                "clientid": "d3skt0p",
                "gid": "LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
            },
            timeout=30.0,
        )
    
    async def search_jobs(
        self, keyword: str, page_no: int = 1, limit: int = 20
    ) -> Dict[str, object]:
        """Search API - returns job list with IDs"""
        # Match exact captured API parameters
        seo_key = keyword.lower().replace(" ", "-") + "-jobs"
        params = {
            "noOfResults": limit,
            "urlType": "search_by_keyword",
            "searchType": "adv",
            "keyword": keyword,
            "pageNo": page_no,
            "k": keyword,
            "seoKey": seo_key,
            "src": "directSearch",
            "latLong": "",
        }
        
        try:
            response = await self.client.get(self.SEARCH_API, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Search API error: {e}")
            raise
    
    async def get_job_detail(self, job_id: str) -> Dict[str, object]:
        """Detail API - returns full job data"""
        url = f"{self.DETAIL_API}/{job_id}"
        params = {
            "microsite": "y",
            "brandedConsultantJd": "true",
            "src": "jobsearchDesk",
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Detail API error for {job_id}: {e}")
            raise
    
    async def fetch_jobs_bulk(self, keyword: str, limit: int = 20) -> Dict[str, object]:
        """Bulk fetch jobs with all details via search API"""
        return await self.search_jobs(keyword=keyword, limit=limit)
    
    async def close(self):
        """Cleanup client"""
        await self.client.aclose()
