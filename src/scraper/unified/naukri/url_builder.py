"""Naukri URL construction utilities"""


def build_search_url(keyword: str, location: str = "") -> str:
    """Build Naukri global job search URL - searches all India by default"""
    k = keyword.replace(" ", "-")
    # Global search across all of India - no location restriction
    return f"https://www.naukri.com/{k}-jobs"


def normalize_job_url(href: str | list[str] | None) -> str | None:
    """Normalize Naukri job URL to absolute format"""
    if not href or not isinstance(href, str):
        return None
    
    if href.startswith("http"):
        return href
    
    return None
