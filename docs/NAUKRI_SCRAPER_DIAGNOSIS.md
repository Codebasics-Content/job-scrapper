# Naukri Scraper Diagnosis - Phase 1 URL Extraction Failure

**Date**: 2025-10-13T21:35:13+05:30
**Status**: CRITICAL - 0 URLs extracted from Naukri

## Root Cause Analysis

### Issue
Test shows **0 jobs scraped** despite:
- ✅ Selectors fixed (`.srp-jobtuple-wrapper` with `data-job-id`)
- ✅ Phase 1 storage enabled (`store_to_db=True`)
- ✅ Debug logging added
- ❌ **NO debug logs appearing** - suggests Playwright not rendering page

### Two-Phase Architecture (CORRECT DESIGN)
```
Phase 1: URL Collection (url_scraper.py)
├── Scrape search results pages → Extract job URLs + titles
├── Store JobUrlModel(platform="naukri", url, input_role, actual_role)
└── DB: INSERT INTO job_urls (deduplicated by platform + url)

Phase 2: Detail Scraping (detail_scraper.py)  
├── Query: LEFT JOIN job_urls with jobs WHERE platform="naukri"
├── Get unscraped URLs only (no duplicates)
└── Scrape detail pages → Store to jobs table
```

### Likely Causes (Priority Order)

1. **Bot Detection** ⚠️ HIGH
   - Naukri detecting headless browser
   - Blocking automated requests
   - Need: `headless=False` with stealth mode

2. **Page Load Timing** ⚠️ MEDIUM
   - Current wait: 5 seconds (`wait_seconds=5.0`)
   - May need network idle detection
   - Dynamic content not loading

3. **Selector Changes** ⚠️ LOW
   - HTML verified with `debug_naukri_listing.html` (works locally)
   - Selectors correct: `.srp-jobtuple-wrapper` has `data-job-id`

## Test Evidence
```bash
🧪 Naukri 20-Job Validation Test
✅ Scraped 0 jobs in 13.8s
❌ RL PENALTY: -20 (0 jobs scraped - scraper broken)
```

**Missing**: No selector logs (`🔍 Page 1 selector...`) = Playwright not rendering

## Action Plan

### Immediate Fixes
1. **Force Non-Headless Mode** - See actual browser behavior
2. **Add Stealth Plugin** - Bypass bot detection
3. **Network Idle Wait** - Ensure page fully loads
4. **Verify HTML Content** - Log actual HTML length received

### Validation
```python
# Should see in logs:
📄 Page 1 HTML length: 500000+ bytes
🔍 Page 1 selector '.srp-jobtuple-wrapper': 20 cards
✅ Page 1: extracted 20 URLs
💾 Stored 20/20 URLs to database
```

## Code Status
- ✅ `naukri_unified.py` - Phase 1 calls with `store_to_db=True`
- ✅ `url_scraper.py` - Creates JobUrlModel + stores to DB
- ✅ `card_parser.py` - Extracts URL from `data-job-id`
- ❌ **Playwright rendering** - NOT working (0 HTML content)
