"""Naukri URL construction utilities"""


def build_search_url(keyword: str, location: str = "", page: int = 1) -> str:
    """Build Naukri job search URL with keyword, location, and page parameters
    
    Naukri pagination: Page 1 has no suffix, Page 2+ use -<page> suffix
    Example: python-developer-jobs-2, python-developer-jobs-3
    """
    from urllib.parse import quote_plus
    
    keyword_encoded = quote_plus(keyword)
    base_slug = keyword.replace(' ', '-').lower()
    
    # Page 1: no suffix, Page 2+: add -<page>
    page_suffix = f"-{page}" if page > 1 else ""
    base_url = f"https://www.naukri.com/{base_slug}-jobs{page_suffix}"
    
    if location:
        location_encoded = quote_plus(location)
        return f"{base_url}?k={keyword_encoded}&l={location_encoded}"
    
    return f"{base_url}?k={keyword_encoded}"


def normalize_job_url(href: str | list[str] | None) -> str | None:
    """Normalize Naukri job URL to absolute format"""
    if not href or not isinstance(href, str):
        return None
    
    if href.startswith("http"):
        return href
    
    return None
