"""Naukri URL construction utilities"""


def build_search_url(keyword: str, location: str) -> str:
    """Build Naukri job search URL with keyword and location"""
    k = keyword.replace(" ", "-")
    path = f"/{k}-jobs"
    
    if location and location.lower() != "india":
        loc = location.replace(" ", "-")
        path += f"-in-{loc}"
    
    return f"https://www.naukri.com{path}"


def normalize_job_url(href: str | list[str] | None) -> str | None:
    """Normalize Naukri job URL to absolute format"""
    if not href or not isinstance(href, str):
        return None
    
    if href.startswith("http"):
        return href
    
    return None
