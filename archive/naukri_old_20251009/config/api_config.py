#!/usr/bin/env python3
# Naukri API Configuration
# EMD Compliance: ≤80 lines

from typing import Final

# API Endpoints
BASE_URL: Final[str] = "https://www.naukri.com"
BASE_API_URL: Final[str] = f"{BASE_URL}/jobapi/v3/search"
BASE_WEB_URL: Final[str] = BASE_URL

# Request headers to mimic browser with anti-bot evasion
API_HEADERS: Final[dict[str, str]] = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Referer": BASE_URL,
    "Origin": BASE_URL,
    "Connection": "keep-alive",
    # Naukri-specific anti-bot headers (CRITICAL)
    "appid": "109",  # 109 for search, 121 for job details
    "clientid": "d3skt0p",
    "systemid": "Naukri",
    "gid": "LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
    # Browser fingerprint headers
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "Priority": "u=4"
}

# API Parameters
DEFAULT_RESULTS_PER_PAGE: Final[int] = 20
MAX_RESULTS_PER_PAGE: Final[int] = 20
MAX_JOBS_LIMIT: Final[int] = 50000  # Maximum jobs for bulk scraping
RATE_LIMIT_DELAY: Final[float] = 1.0  # Seconds between requests
SEARCH_TYPE: Final[str] = "adv"
URL_TYPE: Final[str] = "search_by_keyword"
SRC_PARAM: Final[str] = "jobsearchDesk"

# Default coordinates (Mumbai)
DEFAULT_LAT_LONG: Final[str] = "19.0760_72.8777"

def build_api_params(
    keyword: str,
    page_no: int = 1,
    results: int = DEFAULT_RESULTS_PER_PAGE
) -> dict[str, str | int]:
    """Build API query parameters"""
    seo_key = keyword.replace(" ", "-").lower() + "-jobs"
    
    return {
        "noOfResults": results,
        "urlType": URL_TYPE,
        "searchType": SEARCH_TYPE,
        "keyword": keyword,
        "pageNo": page_no,
        "k": keyword,
        "seoKey": seo_key,
        "src": SRC_PARAM,
        "latLong": DEFAULT_LAT_LONG,
    }

def get_headers(appid: str = "109") -> dict[str, str]:
    """Generate headers with dynamic appid (109=search, 121=job details)"""
    headers = API_HEADERS.copy()
    headers["appid"] = appid
    return headers

def build_job_url(job_id: str, title: str, company: str) -> str:
    """Build job detail URL from job ID"""
    # Naukri uses jdURL from API response
    return f"{BASE_WEB_URL}/job-listings-{title.lower().replace(' ', '-')}-{company.lower().replace(' ', '-')}-{job_id}"
