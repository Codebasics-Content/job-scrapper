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
from .id_collector import collect_job_ids
from .detail_fetcher import fetch_job_details_batch

__all__ = [
    'JOB_LISTING_SELECTORS',
    'JOB_TITLE_SELECTORS', 
    'COMPANY_SELECTORS',
    'LOCATION_SELECTORS',
    'RESULTS_CONTAINER_SELECTORS',
    'collect_job_ids',
    'fetch_job_details_batch'
]
