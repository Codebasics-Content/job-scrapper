"""Two-Phase Naukri Scraper - 80-90% Speedup via URL Caching

Phase 1: Scrape URLs only (10-100x faster)
Phase 2: Scrape details only for unscraped URLs (LEFT JOIN deduplication)
"""
from __future__ import annotations

from .naukri.url_scraper import scrape_naukri_urls
from .naukri.detail_scraper import scrape_naukri_details

__all__ = ["scrape_naukri_urls", "scrape_naukri_details"]
