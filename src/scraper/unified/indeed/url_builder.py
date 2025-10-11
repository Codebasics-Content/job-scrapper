"""Indeed URL construction utilities"""


def build_search_url(keyword: str, location: str = "") -> str:
    """Build Indeed global job search URL - searches worldwide by default"""
    k = keyword.replace(" ", "+")
    # Global search - no location filter for worldwide results
    return f"https://www.indeed.com/jobs?q={k}"


def normalize_job_url(href: str | list[str] | None) -> str | None:
    """Normalize Indeed job URL to absolute format"""
    if not href or not isinstance(href, str):
        return None
    
    if href.startswith("/"):
        return f"https://www.indeed.com{href}"
    
    if href.startswith("http"):
        return href
    
    return None
