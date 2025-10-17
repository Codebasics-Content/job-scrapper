# Scraper Module

## Purpose
Automates the collection of job postings from LinkedIn and Naukri using browser automation.

## What It Does
- **Phase 1: URL Collection** - Rapidly gathers job listing URLs through infinite scroll
- **Phase 2: Detail Extraction** - Opens each job page to extract title, company, description, skills
- **Anti-Detection** - Mimics human behavior (random delays, scrolling) to avoid platform blocks
- **Adaptive Concurrency** - Runs 8 parallel workers with intelligent rate limiting
- **Real-Time Deduplication** - Checks database before adding URLs to prevent duplicates

## Platform-Specific Adapters
- `linkedin/` - LinkedIn scraping with fallback selectors
- `naukri/` - Naukri.com scraping optimized for Indian job market
- `scalable/` - Adaptive rate limiter and user agent rotation

## Why It Matters
This is the data collection engine. Without reliable scraping, the entire system fails. The two-phase architecture ensures efficiency while the anti-detection measures maintain long-term reliability.

## Key Innovation
**Adaptive Rate Limiting** - Automatically adjusts scraping speed based on success rates, preventing platform blocks while maximizing throughput.
