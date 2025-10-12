# BrightData Web Datasets API Client - EMD Component
# Pre-collected LinkedIn job data via REST API
# Pricing: $250/100K records (one-time purchase)
# Budget: 4K records = $10 (one-time project)

import os
import logging
import aiohttp
from typing import Optional

logger = logging.getLogger(__name__)

class BrightDataDatasetsClient:
    """Client for BrightData Web Datasets API
    
    Pricing (One-Time Purchase):
    - $250 per 100,000 records (base rate)
    - $10 budget = Max 4,000 records (one-time)
    - Recommended: 2,000-4,000 jobs per collection
    """
    
    BASE_URL = "https://api.brightdata.com/datasets/v3"
    LINKEDIN_DATASET_ID = "gd_l7q7dkf244hwjntr0"
    
    # Budget-conscious defaults (one-time purchase)
    DEFAULT_SMALL_BATCH = 1000  # ~$2.50
    DEFAULT_MEDIUM_BATCH = 2000  # ~$5.00
    DEFAULT_LARGE_BATCH = 4000  # ~$10.00 (max budget)
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("BRIGHTDATA_API_TOKEN", "")
        if not self.api_token:
            raise ValueError("BRIGHTDATA_API_TOKEN not configured")
    
    async def fetch_linkedin_jobs(
        self,
        keyword: str,
        location: str = "Worldwide",
        limit: int = 2000  # Default to medium batch (~$5)
    ) -> list[dict[str, object]]:
        """Fetch LinkedIn jobs from pre-collected dataset
        
        Args:
            keyword: Job search keyword
            location: Job location filter
            limit: Maximum jobs to return
        
        Returns:
            List of job data dicts
        """
        url = f"{self.BASE_URL}/{self.LINKEDIN_DATASET_ID}"
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "keyword": keyword,
            "location": location,
            "limit": limit,
            "format": "json"
        }
        
        # Cost estimation (one-time purchase)
        estimated_cost = (limit / 100000) * 250  # One-time rate
        logger.info(
            f"Fetching LinkedIn dataset: {keyword} in {location} "
            f"(limit={limit}, est. cost=${estimated_cost:.2f} one-time)"
        )
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                
                # Extract jobs from response
                jobs = data if isinstance(data, list) else data.get("data", [])
                
                logger.info(f"Fetched {len(jobs)} jobs from dataset")
                return jobs  # type: ignore
