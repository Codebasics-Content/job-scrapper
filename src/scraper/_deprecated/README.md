# Deprecated Scraper Components

**⚠️ DO NOT USE - LEGACY CODE**

This directory contains deprecated scraping implementations that have been superseded by the unified HeadlessX + Local Luminati Proxy architecture.

## Deprecated Components

### Browser Scrapers (BrightData Cloud)
- `brightdata/indeed_browser_scraper.py`
- `brightdata/linkedin_browser_scraper.py`
- `brightdata/naukri_browser_scraper.py`
- `brightdata/indeed_dataset_scraper.py`
- `brightdata/linkedin_dataset_scraper.py`

### Local/Proxy Scrapers (Old Architecture)
- `local_proxy/` - Old local proxy implementation
- `proxy/` - Old proxy configuration

## Current Architecture (Use Instead)

**Location**: `src/scraper/unified/`

**Components**:
- `service.py` - Main orchestrator
- `linkedin_unified.py` - LinkedIn scraper
- `indeed_unified.py` - Indeed scraper
- `naukri_unified.py` - Naukri scraper

**Stack**:
- HeadlessX (https://github.com/saifyxpro/HeadlessX)
- Local Luminati Proxy Manager (https://github.com/luminati-io/luminati-proxy)
- Port: 24000 (local)
- No cloud dependencies

## Why Deprecated?

1. **Complexity**: Multiple implementations per platform
2. **Cloud Lock-in**: BrightData cloud API dependencies
3. **Maintenance**: Duplicated code across scrapers
4. **Reliability**: Selenium-based approaches prone to detection

## Migration Date

2025-10-11
