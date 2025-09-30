#!/usr/bin/env python3
# LinkedIn configuration module
from .countries import LINKEDIN_COUNTRIES
from .delays import (
    PAGE_LOAD_DELAY,
    SCROLL_DELAY,
    API_REQUEST_DELAY,
    TAB_SWITCH_DELAY,
    ERROR_RETRY_DELAY
)

__all__ = [
    "LINKEDIN_COUNTRIES",
    "PAGE_LOAD_DELAY",
    "SCROLL_DELAY",
    "API_REQUEST_DELAY",
    "TAB_SWITCH_DELAY",
    "ERROR_RETRY_DELAY"
]
