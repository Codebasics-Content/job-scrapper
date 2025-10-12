"""Indeed URL construction utilities"""


def build_search_url(keyword: str, location: str = "", start: int = 0) -> str:
    """Build Indeed job search URL with keyword, location, and pagination
    
    Indeed pagination: Uses &start=0, &start=10, &start=20 (10 jobs per page)
    """
    from urllib.parse import quote_plus
    
    keyword_encoded = quote_plus(keyword)
    base_params = f"q={keyword_encoded}"
    
    if location:
        location_encoded = quote_plus(location)
        base_params += f"&l={location_encoded}"
    
    if start > 0:
        base_params += f"&start={start}"
    
    return f"https://www.indeed.com/jobs?{base_params}"


def normalize_job_url(href: str | list[str] | None) -> str | None:
    """Normalize Indeed job URL to absolute format"""
    if not href or not isinstance(href, str):
        return None
    
    if href.startswith("/"):
        return f"https://www.indeed.com{href}"
    
    if href.startswith("http"):
        return href
    
    return None
