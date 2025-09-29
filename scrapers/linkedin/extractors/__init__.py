#!/usr/bin/env python3
# LinkedIn extractors module
# EMD Compliance: ≤80 lines

from .selectors import (
    JOB_LISTING_SELECTORS,
    JOB_TITLE_SELECTORS,
    COMPANY_SELECTORS,
    LOCATION_SELECTORS,
    RESULTS_CONTAINER_SELECTORS
)

__all__ = [
    'JOB_LISTING_SELECTORS',
    'JOB_TITLE_SELECTORS', 
    'COMPANY_SELECTORS',
    'LOCATION_SELECTORS',
    'RESULTS_CONTAINER_SELECTORS'
]
