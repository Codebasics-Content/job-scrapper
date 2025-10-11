"""Indeed URL construction utilities"""


def build_search_url(keyword: str, location: str) -> str:
    """Build Indeed job search URL with encoded parameters"""
    k = keyword.replace(" ", "+")
    loc = location.replace(" ", "+")
    return f"https://www.indeed.com/jobs?q={k}&l={loc}"


def normalize_job_url(href: str) -> str | None:
    """Normalize Indeed job URL to absolute format"""
    if not isinstance(href, str):
        return None
    
    if href.startswith("/"):
        return f"https://www.indeed.com{href}"
    
    if href.startswith("http"):
        return href
    
    return None
