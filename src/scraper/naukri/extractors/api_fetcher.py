#!/usr/bin/env python3
# Naukri API job fetcher using requests
# EMD Compliance: ≤80 lines

import logging
import requests
from typing import Any
from ..config.api_config import (
    BASE_API_URL,
    get_headers,
    build_api_params,
)
from ..config.rate_limits import (
    RateLimitTier,
    DEFAULT_TIER,
    RATE_LIMIT_STATUS
)
from ..utils.rate_limiter import AdaptiveRateLimiter

logger = logging.getLogger(__name__)

class NaukriAPIFetcher:
    """Fetch jobs from Naukri API with rate limiting"""
    
    def __init__(self, tier: RateLimitTier = DEFAULT_TIER):
        self.session = requests.Session()
        # Use appid=109 for search API
        self.session.headers.update(get_headers(appid="109"))
        self.rate_limiter = AdaptiveRateLimiter(tier)
    
    def fetch_jobs_page(
        self,
        keyword: str,
        page_no: int = 1,
        timeout: int = 30
    ) -> dict[str, Any] | None:
        """Fetch single page with retry logic and rate limiting"""
        for attempt in range(self.rate_limiter.tier.retry_attempts):
            try:
                # Apply rate limiting
                self.rate_limiter.wait()
                
                params = build_api_params(keyword, page_no)
                response = self.session.get(
                    BASE_API_URL,
                    params=params,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.debug(
                        f"[API ✓] Page {page_no}: "
                        f"{len(data.get('jobDetails', []))} jobs"
                    )
                    return data
                    
                elif response.status_code == RATE_LIMIT_STATUS:
                    logger.warning(
                        f"[RATE LIMIT HIT] Page {page_no} - "
                        f"Attempt {attempt + 1}/{self.rate_limiter.tier.retry_attempts}"
                    )
                    self.rate_limiter.backoff(attempt)
                    continue
                    
                else:
                    logger.error(
                        f"[API ERROR] Page {page_no}: "
                        f"Status {response.status_code}"
                    )
                    return None
                    
            except requests.exceptions.Timeout:
                logger.warning(f"[TIMEOUT] Page {page_no} - Retry {attempt + 1}")
                self.rate_limiter.backoff(attempt)
                continue
                
            except requests.exceptions.RequestException as e:
                logger.error(f"[REQUEST FAILED] Page {page_no}: {e}")
                return None
                
        logger.error(f"[MAX RETRIES] Page {page_no} - All attempts failed")
        return None
    
    def get_total_jobs(self, keyword: str) -> int:
        """Get total number of jobs available"""
        data = self.fetch_jobs_page(keyword, page_no=1)
        if data:
            return data.get("noOfJobs", 0)
        return 0
    
    def close(self) -> None:
        """Close session"""
        self.session.close()
