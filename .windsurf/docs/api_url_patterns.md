# Platform Scraper Implementation Status & URL Patterns

## 1. LinkedIn Jobs ✅ PRODUCTION READY

### Implementation Status
**Status**: PRODUCTION READY (Tested with 1000+ jobs)
**Approach**: API-based extraction with infinite scroll
**Files**:
- `scrapers/linkedin/scraper.py` (77 lines)
- `scrapers/linkedin/extractors/scroll_handler.py` (78 lines)
- `scrapers/linkedin/extractors/api_job_fetcher.py` (71 lines)
- `scrapers/linkedin/extractors/job_id_extractor.py` (74 lines)

### Actual Base URL Pattern
```python
base_url = "https://www.linkedin.com/jobs/search"
```

### Parameters Used in Production
```python
params = {
    'keywords': job_role,          # Job role from user input
    'f_TPR': 'r86400',            # Posted in last 24 hours
    'start': 0,                    # Pagination start (not used with scroll)
    'location': location           # Optional location filter
}
```

### Production URL Example
```
https://www.linkedin.com/jobs/search?keywords=AI%20Engineer&f_TPR=r86400&start=0
https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Mumbai&f_TPR=r86400&start=0
```

### API Endpoint for Job Details
```
https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}
```

### Implementation Details
- **Method**: Selenium with undetected-chromedriver (GUI mode)
- **Pagination**: Infinite scroll using JavaScript scroll injection
- **Job Extraction**: Extract job IDs from page → Fetch details via API
- **Duplicate Handling**: `processed_ids` set tracks all extracted IDs
- **Rate Limiting**: 0.5s between API calls, 2s between scroll operations
- **Selectors**: 
  - Job cards: `li.jobs-search__results-list > li`
  - Job ID attribute: `data-entity-urn` or `data-job-id`
  - See More button: `button.infinite-scroller__show-more-button`

## 2. Indeed Jobs ⚠️ STUB - INCOMPLETE

### Implementation Status
**Status**: INCOMPLETE (93 lines - EMD violation)
**Approach**: Selenium-based scraping (stub implementation)
**Files**:
- `scrapers/indeed/scraper.py` (93 lines - needs splitting)
- `scrapers/indeed/extractor.py` (incomplete)
- `scrapers/indeed/extractors/` (directory exists but incomplete)

### Current Base URL Pattern
```python
base_url = "https://www.indeed.com"
search_url = f"{base_url}/jobs"
```

### Parameters Planned
```python
search_query = f"{search_url}?q={job_role.replace(' ', '+')}"
# Location parameter not yet implemented
```

### Current URL Example (Stub)
```
https://www.indeed.com/jobs?q=AI+Engineer
```

### Implementation Gaps
1. **No pagination handler** - Cannot scrape beyond first page
2. **Incomplete extractors** - Job data extraction not functional
3. **No location filter** - Location parameter not implemented
4. **No rate limiting** - Basic structure only
5. **No error recovery** - Minimal error handling

### Required Implementation
- Complete `extractor.py` with proper job card parsing
- Implement pagination/scroll handler for multiple pages
- Add location parameter support
- Create extractors for description, company, salary
- Add proper CSS selectors for Indeed's current markup
- Implement rate limiting (1-2s between requests)
- Split scraper.py to comply with EMD (≤80 lines)

## 3. Naukri.com ⚠️ STUB - INCOMPLETE

### Implementation Status
**Status**: INCOMPLETE (78 lines)
**Approach**: Selenium-based scraping (stub implementation)
**Files**:
- `scrapers/naukri/scraper.py` (78 lines)
- `scrapers/naukri/extractor.py` (incomplete)

### Current Base URL Pattern
```python
base_url = "https://www.naukri.com"
```

### Current Search URL Construction
```python
search_url = f"{base_url}/{job_role.replace(' ', '-')}-jobs"
# Example: https://www.naukri.com/AI-Engineer-jobs
```

### Current URL Example (Stub)
```
https://www.naukri.com/AI-Engineer-jobs
https://www.naukri.com/Data-Scientist-jobs
```

### Current Selectors (May Need Update)
```python
job_cards = driver.find_elements(
    By.CSS_SELECTOR, 
    ".srp-jobtuple-wrapper, .jobTuple"
)
```

### Implementation Gaps
1. **Incomplete extractor** - `extract_job_from_card()` not functional
2. **No pagination** - Only scrapes first page
3. **No location support** - Location parameter not implemented
4. **Basic rate limiting** - Simple sleep(2) every 5 jobs
5. **Minimal error handling** - Only TimeoutException caught
6. **No scroll handler** - May miss dynamically loaded jobs

### Required Implementation
- Complete `extractor.py` with proper job card parsing
- Implement pagination handler (pageNo parameter or scroll)
- Add location filter support
- Add proper CSS selectors for current Naukri markup
- Implement comprehensive error handling
- Add retry mechanisms for failed requests
- Test with actual Naukri.com job searches

## 4. Y Combinator (Work at a Startup) ❌ NOT STARTED

### Implementation Status
**Status**: NOT IMPLEMENTED
**Approach**: Not defined
**Files**: No directory or files exist

### Planned Base URL Pattern
```
https://www.workatastartup.com/companies
```

### Alternative URL Option
```
https://www.ycombinator.com/jobs
```

### Required Implementation
1. **Create directory structure**:
   ```
   scrapers/ycombinator/
   ├── __init__.py
   ├── scraper.py (≤80 lines)
   ├── extractor.py (≤80 lines)
   └── extractors/
       ├── __init__.py
       ├── job_card_parser.py
       └── api_handler.py
   ```

2. **Determine scraping approach**:
   - Investigate if API endpoints exist
   - Test Selenium requirements for SPA
   - Identify job card selectors
   - Test pagination method (scroll vs URL params)

3. **Implement core functionality**:
   - Follow LinkedIn pattern for consistency
   - Implement proper error handling
   - Add rate limiting (3-5s between requests)
   - Create job extraction logic
   - Add pagination support

4. **Integration**:
   - Integrate with streamlit_app.py
   - Add to platform dropdown
   - Test end-to-end flow

### Technical Challenges
- **SPA Architecture**: Requires Selenium or Playwright
- **GraphQL API**: May need to intercept API calls
- **Dynamic Loading**: Infinite scroll likely required
- **Limited Documentation**: Need reverse engineering
- **YC-Specific**: Only YC-backed startups (niche market)

## Headers and Anti-Bot Measures

### Recommended Headers
```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
```

### Rate Limiting Strategy
- **LinkedIn**: 2-3 seconds between requests
- **Indeed**: 1-2 seconds between requests  
- **Naukri**: 2-4 seconds between requests
- **YC**: 3-5 seconds between requests (heavy JS)

### Selenium Requirements
- **Essential**: Naukri.com, Y Combinator
- **Optional**: LinkedIn (for dynamic content), Indeed (for complex searches)
- **Not Required**: Basic Indeed searches

## Implementation Priority
1. **Indeed**: Easiest to implement, good documentation
2. **Naukri**: Medium complexity, requires Selenium
3. **LinkedIn**: Medium-high complexity, anti-bot measures
4. **Y Combinator**: Most complex, SPA architecture
