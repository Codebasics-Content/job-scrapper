"""LinkedIn URL construction utilities"""


def build_search_url(keyword: str, location: str = "") -> str:
    """Build LinkedIn global job search URL - searches worldwide by default"""
    k = keyword.replace(" ", "%20")
    # Global search - no location filter for worldwide results
    return f"https://www.linkedin.com/jobs/search/?keywords={k}"
