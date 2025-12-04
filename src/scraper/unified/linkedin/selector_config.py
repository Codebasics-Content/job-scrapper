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
    "see_more_button": [
        "button.infinite-scroller__show-more-button",
        "button[aria-label='See more jobs']",
        ".infinite-scroller__show-more-button--visible",
    ],
}

# Job Detail Page Selectors (Updated for 2025)
DETAIL_SELECTORS = {
    "job_title": [
        "[data-job-title]",  # 2025: Data attribute (most stable)
        ".jobs-details__main-content h1",  # 2025: New structure
        "h1.t-24",
        ".top-card-layout__title",
        "h1",  # Fallback: Generic
    ],
    "description": [
        "[data-jobs-details-main-content]",  # 2025: Primary data attribute
        ".jobs-details__content",  # 2025: New class
        ".jobs-box__html-content",  # 2025: Alternate
        ".show-more-less-html",  # Parent container
        ".show-more-less-html__markup",  # Legacy (keep)
        ".description__text",
        ".jobs-description__content",
    ],
    "company_name": [
        "[data-company-name]",  # 2025: Data attribute
        ".jobs-details-top-card__company-name",  # 2025: New class
        ".job-details-jobs-unified-top-card__company-name",
        "a.topcard__org-name-link",
        ".top-card-layout__second-subline a",
    ],
    "posted_date": [
        "time",  # 2025: Semantic HTML (most reliable)
        "[data-posted-date]",  # Data attribute
        ".job-details-jobs-unified-top-card__posted-date",
        ".jobs-unified-top-card__posted-date",
        "span.job-details-jobs-unified-top-card__posted-date",
    ],
    "native_skills": [
        ".job-details-skill-match-status-list__skill",
        ".skill-match-status-item__skill-name",
    ],
    "show_more_button": [
        "button[aria-label='Show more']",
        ".show-more-less-html__button--more",
    ],
}

# Wait Strategies
WAIT_TIMEOUTS = {
    "navigation": 30000,  # 30s for page load
    "element": 10000,  # 10s for element appearance
    "scroll_delay": 2000,  # 2s between scrolls (human-like)
}

# Scroll Configuration
SCROLL_CONFIG = {
    "jobs_per_scroll": 10,
    "max_scrolls": 10,  # 100 jobs max per search
    "scroll_pause": 2,  # seconds between scrolls
}

# Expired Job Detection - English Only (Simplified)
EXPIRED_JOB_INDICATORS = {
    "error_messages": [
        "no longer available",
        "no longer accepting applications",
        "job posting has expired",
        "this job is closed",
        "not available",
        "page not found",
        "404",
        "expired",
        "unavailable",
        "removed",
        "this job posting no longer exists",
    ],
    "error_selectors": [
        ".artdeco-empty-state__headline",  # LinkedIn empty state
        ".job-view-layout__error-state",  # Error state component
        "[data-test-empty-state-headline]",  # Empty state data attribute
        ".artdeco-inline-feedback__message",  # Feedback message
        ".error-container",  # Generic error container
    ],
    "generic_titles": [
        # REMOVED: "LinkedIn" - causes false positives on valid job pages
        "Page Not Found",
        "404",
        "Error",
        "Job Not Found",
        "This page could not be found",
    ],
}

# Login/Auth Wall Detection
LOGIN_WALL_INDICATORS = {
    "login_selectors": [
        "button:has-text('Sign in')",
        "button:has-text('Continue with Google')",
        "button:has-text('Continue with Microsoft')",
        "input[name='session_key']",  # Email input on login
        "input[name='session_password']",  # Password input
        ".login-form",
        ".auth-button-google",
        ".auth-button-microsoft",
    ],
    "login_messages": [
        "sign in",
        "log in",
        "join now",
        "to continue",
        "user agreement",
        "privacy policy",
        "cookie policy",
    ],
    "login_urls": ["/authwall", "/login", "/signup", "/checkpoint"],
}


def get_first_matching_selector(selectors: list[str]) -> str:
    """Get first selector from fallback list"""
    return selectors[0]
