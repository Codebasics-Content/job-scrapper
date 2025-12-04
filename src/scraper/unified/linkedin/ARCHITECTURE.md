# LinkedIn Playwright Scraper Architecture

## Overview
Playwright-based LinkedIn scraper using BrightData scraping_browser2 proxy for reliable job extraction with skills parsing.

## Architecture Pattern (Following Naukri)

### Phase 1: URL Collection
**File**: `playwright_url_scraper.py`
**Purpose**: Extract job URLs from search results

**Flow**:
1. Connect to browser via wss:// proxy (BrightData scraping_browser2)
2. Navigate to LinkedIn jobs search
3. Scroll incrementally (10 jobs per scroll)
4. Extract job card URLs
5. Store to `job_urls` table
6. Return JobUrlModel list

**Selectors**:
- Job cards: `.base-card.relative.w-full`
- Job link: `.base-card__full-link`
- Title: `.base-search-card__title`

### Phase 2: Detail Scraping
**File**: `playwright_detail_scraper.py`
**Purpose**: Extract full job descriptions and skills

**Flow**:
1. Read URLs from `job_urls` table
2. Navigate to each job detail page
3. Extract description from `.show-more-less-html__markup`
4. Parse skills using AdvancedSkillExtractor
5. Deduplicate against existing database
6. Store to `jobs` table
7. Return JobDetailModel list

**Skills Extraction**:
- Primary: LinkedIn native skills (`.job-details-skill-match-status-list__skill`)
- Fallback: AdvancedSkillExtractor from description text
- Normalize and deduplicate

### Unified Entry Point
**File**: `linkedin_unified.py`
**Purpose**: Orchestrate complete scraping workflow

**Async Pattern**:
```python
async def scrape_linkedin_jobs_unified(
    keyword: str,
    location: str,
    limit: int = 100,
    headless: bool = False,  # Always visible browser to avoid rate limits
) -> List[JobDetailModel]:
    # Phase 1: URL collection
    urls = await scrape_linkedin_urls_playwright(...)
    
    # Phase 2: Detail scraping
    jobs = await scrape_linkedin_details_playwright(...)
    
    return jobs
```

## BrightData Integration

### Proxy Connection
**Type**: scraping_browser2 zone (WebSocket)
**Format**: `wss://brd-customer-hl_xxx-zone-scraping_browser2:PASSWORD@brd.superproxy.io:9222`

**Playwright Connection**:
```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp(
        "wss://brd-customer-hl_xxx-zone-scraping_browser2:PASSWORD@brd.superproxy.io:9222"
    )
    page = await browser.new_page()
```

### Anti-Detection Features
- Residential IPs via BrightData
- Real browser fingerprints
- Human-like scrolling patterns
- Random delays between actions

## LinkedIn Selectors (2025)

### Job Search Page
```css
/* Container */
.jobs-search__results-list

/* Job cards */
.base-card.relative.w-full.hover\:no-underline

/* Card elements */
.base-search-card__title          # Job title
.base-search-card__subtitle       # Company name  
.job-search-card__location        # Location
.base-card__full-link             # Job URL (href)
```

### Job Detail Page
```css
/* Description */
.show-more-less-html__markup      # Full HTML description

/* Skills (if available) */
.job-details-skill-match-status-list__skill

/* Metadata */
.topcard__flavor-row              # Posted date, applicants
```

## Data Flow

```
User Input (keyword, location, limit)
    ↓
Phase 1: URL Collection
    ├─ Connect via wss:// proxy
    ├─ Search LinkedIn jobs
    ├─ Scroll & extract URLs
    └─ Store to job_urls table (100 URLs)
    ↓
Phase 2: Detail Scraping
    ├─ Read URLs from database
    ├─ Navigate to each job
    ├─ Extract description
    ├─ Parse skills (AdvancedSkillExtractor)
    ├─ Deduplicate (check existing URLs)
    └─ Store to jobs table (47 NEW jobs)
    ↓
Return JobDetailModel[] to caller
```

## Deduplication Strategy

### Layer 1: Database URL Check
- Query existing URLs in `jobs` table
- Skip already scraped jobs
- Only process NEW URLs

### Layer 2: Skills Validation
- Reject jobs with empty skills
- Ensure quality data only

### Layer 3: Fuzzy Matching
- Title/company/location similarity
- Prevents near-duplicates

## Error Handling

### Connection Errors
- Retry with exponential backoff (3 attempts)
- Fallback to direct connection if proxy fails
- Log errors to `mistakes.json`

### Selector Changes
- Multiple fallback selectors
- Graceful degradation
- Alert on repeated failures

### Rate Limiting
- Respect LinkedIn's rate limits
- Random delays (2-5s between requests)
- Human-like scrolling speed

## EMD Compliance

All files ≤80 lines:
- `playwright_url_scraper.py` (≤80 lines)
- `playwright_detail_scraper.py` (≤80 lines)
- `linkedin_unified.py` (≤80 lines)
- `selector_config.py` (≤80 lines)
- `__init__.py` (≤80 lines)

## Performance Targets

- **URL Collection**: ~100 URLs in 30-45 seconds
- **Detail Scraping**: ~50 jobs in 60-90 seconds
- **Total Time**: ~2 minutes for 100 jobs
- **Success Rate**: ≥80% with proxy
- **Skills Extraction**: ≥90% accuracy
