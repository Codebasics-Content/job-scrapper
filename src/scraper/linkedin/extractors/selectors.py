#!/usr/bin/env python3
# LinkedIn CSS selector fallback configuration
# EMD Compliance: ≤80 lines

from typing import Final

# Job listing container selectors (try in order)
JOB_LISTING_SELECTORS: Final[list[str]] = [
    '.jobs-search__results-list > li',
    'div[data-job-id]',
    'li[data-occludable-job-id]',
    '.scaffold-layout__list-container > li',
    '.jobs-search-results__list-item'
]

# Job card title selectors (try in order)
JOB_TITLE_SELECTORS: Final[list[str]] = [
    '.job-card-list__title',
    '.base-search-card__title',
    'h3.base-search-card__title',
    '.job-card-container__link',
    'a.job-card-list__title'
]

# Company name selectors (try in order)
COMPANY_SELECTORS: Final[list[str]] = [
    '.job-card-container__primary-description',
    '.base-search-card__subtitle',
    'h4.base-search-card__subtitle',
    '.job-card-container__company-name',
    'a.job-card-container__company-name'
]

# Location selectors (try in order)
LOCATION_SELECTORS: Final[list[str]] = [
    '.job-card-container__metadata-item',
    '.job-search-card__location',
    '.base-search-card__metadata',
    'span.job-card-container__metadata-item'
]

# Wait for results container
RESULTS_CONTAINER_SELECTORS: Final[list[str]] = [
    '.jobs-search__results-list',
    '.scaffold-layout__list',
    '.jobs-search-results__list'
]
