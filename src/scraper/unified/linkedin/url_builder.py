"""LinkedIn URL construction utilities"""


def build_search_url(keyword: str, location: str) -> str:
    """Build LinkedIn job search URL with encoded parameters"""
    k = keyword.replace(" ", "%20")
    loc = location.replace(" ", "%20")
    return f"https://www.linkedin.com/jobs/search/?keywords={k}&location={loc}"
