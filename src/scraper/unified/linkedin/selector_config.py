"""LinkedIn Playwright Selectors Configuration (2025)
EMD Compliance: ≤80 lines
"""
from __future__ import annotations

# Job Search Page Selectors
SEARCH_SELECTORS = {
    "job_cards_container": ".jobs-search__results-list",
    "job_card": [
        ".base-card.relative.w-full",
        ".job-search-card",
        "li.jobs-search-results__list-item",
    ],
    "job_link": [
        ".base-card__full-link",
        "a.base-card__full-link",
        ".job-card-container__link",
    ],
    "job_title": [
        ".base-search-card__title",
        "h3.base-search-card__title",
    ],
    "company_name": [
        ".base-search-card__subtitle",
        "h4.base-search-card__subtitle",
    ],
    "location": [
        ".job-search-card__location",
        "span.job-search-card__location",
    ],
    "posted_date": [
        ".job-search-card__listdate",
        "time.job-search-card__listdate",
    ],
}

# Job Detail Page Selectors
DETAIL_SELECTORS = {
    "description": [
        ".show-more-less-html__markup",
        ".description__text",
        ".jobs-description__content",
    ],
    "native_skills": [
        ".job-details-skill-match-status-list__skill",
        ".skill-match-status-item__skill-name",
    ],
    "show_more_button": [
        ".show-more-less-html__button--more",
        "button[aria-label='Show more']",
    ],
}

# Wait Strategies
WAIT_TIMEOUTS = {
    "navigation": 30000,  # 30s for page load
    "element": 10000,     # 10s for element appearance
    "scroll_delay": 2000,  # 2s between scrolls (human-like)
}

# Scroll Configuration
SCROLL_CONFIG = {
    "jobs_per_scroll": 10,
    "max_scrolls": 10,  # 100 jobs max per search
    "scroll_pause": 2,  # seconds between scrolls
}

def get_first_matching_selector(selectors: list[str]) -> str:
    """Get first selector from fallback list"""
    return selectors[0]
