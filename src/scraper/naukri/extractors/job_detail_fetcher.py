#!/usr/bin/env python3
# Naukri job detail fetcher for individual job URLs
# EMD Compliance: ≤80 lines

import logging
import re
import aiohttp
from typing import Any
from ..config.api_config import get_headers

logger = logging.getLogger(__name__)

class NaukriJobDetailFetcher:
    """Fetch individual job details from Naukri API"""
    
    async def fetch_job_details(self, job_url: str) -> dict[str, Any] | None:
        """Fetch full job details including description from job URL"""
        try:
            # Extract job ID from URL (e.g., job-listings-...-170925500833)
            job_id_match = re.search(r'job-listings.*?(\d+)$', job_url)
            if not job_id_match:
                logger.debug(f"[JOB DETAIL] Could not extract job ID from: {job_url}")
                return None
            
            job_id = job_id_match.group(1)
            api_url = f"https://www.naukri.com/jobapi/v3/job/{job_id}"
            
            timeout = aiohttp.ClientTimeout(total=10)
            headers = get_headers(appid="121")  # Job details use appid 121
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.debug(f"[JOB DETAIL] Fetched details for job {job_id}")
                        return data
                    else:
                        logger.debug(f"[JOB DETAIL] Failed {response.status} for job {job_id}")
                        return None
                        
        except aiohttp.ClientError as e:
            logger.debug(f"[JOB DETAIL] Network error: {e}")
            return None
        except Exception as e:
            logger.debug(f"[JOB DETAIL] Fetch error: {e}")
            return None
