#!/usr/bin/env python3
# Anti-bot detection delay configuration
# EMD Compliance: ≤80 lines

# Anti-bot detection delays (in seconds) - increased to avoid rate limiting
PAGE_LOAD_DELAY: float = 2.0
SCROLL_DELAY: float = 1.5
API_REQUEST_DELAY: float = 1.5  # Increased from 0.8 to avoid 429 errors
TAB_SWITCH_DELAY: float = 0.5
ERROR_RETRY_DELAY: float = 5.0  # Increased from 3.0 for better recovery
