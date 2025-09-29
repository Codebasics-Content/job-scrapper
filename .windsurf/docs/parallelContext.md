# Parallel Execution Context - Job Scrapper (Production Implementation)

## Actual Architecture: Single Browser Multi-Tab with AsyncIO

### Production Implementation: NOT Multi-Process
**Current Status**: Single browser instance with platform-specific tabs
**Approach**: Shared browser + asyncio (NOT multi-process or ThreadPoolExecutor)
**File**: `scrapers/base/driver_pool.py` (96 lines)

```python
class WebDriverPool:
    # Shared browser across all platforms (class-level)
    _shared_browser: uc.Chrome | None = None
    _platform_tabs: dict[str, str] = {}  # platform_name -> window_handle
    _initialized: bool = False
    _creation_lock: threading.Lock = threading.Lock()
```

### Actual Platform Execution Status
```python
# ✅ PRODUCTION READY
Platform 1: LinkedIn (asyncio) - API-based with infinite scroll

# ⚠️ STUB - INCOMPLETE
Platform 2: Indeed (asyncio stub) - Basic structure only
Platform 3: Naukri (asyncio stub) - Basic structure only

# ❌ NOT STARTED
Platform 4: YCombinator - No files exist
```

### AsyncIO Implementation (Production)
```python
class LinkedInScraper(BaseJobScraper):
    async def scrape_jobs(self, job_role: str, target_count: int) -> list[JobModel]:
        """Async scraping with single browser tab"""
        driver = self.get_driver()  # Get shared browser, switch to tab
        
        try:
            # Async loop with rate limiting
            while len(jobs) < target_count:
                # Extract job IDs from current page
                job_ids = extract_job_ids_from_page(driver)
                
                # Fetch details for each job ID
                for job_id in job_ids:
                    job = await asyncio.get_event_loop().run_in_executor(
                        None, fetch_job_via_api, job_id, job_role
                    )
                    await asyncio.sleep(0.5)  # Rate limiting
                
                # Scroll to load more
                has_more = await asyncio.get_event_loop().run_in_executor(
                    None, scroll_to_load_jobs, driver, target_count, len(jobs)
                )
                await asyncio.sleep(2)  # Scroll delay
        finally:
            self.return_driver(driver)  # No-op for tab system
```

**Note**: No ThreadPoolExecutor or multi-process - all platforms would share same browser with different tabs

## Platform-Specific Implementation Status

### LinkedIn ✅ PRODUCTION READY (AsyncIO Tab)
**Implementation**: `scrapers/linkedin/scraper.py` + extractors/
**Architecture**: Single tab in shared browser
**Challenge**: API-based extraction with infinite scroll
**Solution**: JavaScript scroll + API endpoint fetching
**Rate Limit**: 
- 0.5s between API calls (120 requests/minute)
- 2s between scroll operations
**Actual Runtime**: ~15-20 minutes for 100+ jobs (tested)
**Parallelization**: NOT parallel - sequential asyncio execution

### Indeed ⚠️ STUB - INCOMPLETE (AsyncIO Stub)
**Implementation**: `scrapers/indeed/scraper.py` (93 lines - EMD violation)
**Architecture**: Would use separate tab in shared browser (not implemented)
**Outstanding Issues**:
- No pagination handler
- Incomplete extractors
- No location filter
- Basic error handling only
**Rate Limit**: Not implemented
**Expected Runtime**: Unknown - not functional
**Parallelization**: Would NOT be parallel - would be sequential

### Naukri ⚠️ STUB - INCOMPLETE (AsyncIO Stub)
**Implementation**: `scrapers/naukri/scraper.py` (78 lines)
**Architecture**: Would use separate tab in shared browser (not implemented)
**Outstanding Issues**:
- Incomplete extractor
- No pagination
- No location support
- Basic rate limiting (sleep(2) every 5 jobs)
**Rate Limit**: Simple delay only (not adaptive)
**Expected Runtime**: Unknown - not functional
**Parallelization**: Would NOT be parallel - would be sequential

### YCombinator ❌ NOT STARTED
**Implementation**: No files exist
**Architecture**: Not defined
**Challenge**: Unknown - not researched
**Solution**: Not implemented
**Rate Limit**: Not defined
**Expected Runtime**: Unknown
**Parallelization**: Not applicable

## Production Resource Management

### Single Browser Architecture (Actual Implementation)
**File**: `scrapers/base/driver_pool.py`
```python
class WebDriverPool:
    # ONE browser shared across all platforms
    _shared_browser: uc.Chrome | None = None
    _platform_tabs: dict[str, str] = {}  # Only tab handles, not separate browsers
    _creation_lock: threading.Lock = threading.Lock()
    
    def initialize_pool(self, driver_factory):
        """Create single browser + tab for this platform"""
        with WebDriverPool._creation_lock:
            # Create shared browser once
            if WebDriverPool._shared_browser is None:
                WebDriverPool._shared_browser = driver_factory.create_driver()
            
            # Create new tab (NOT new browser)
            browser = WebDriverPool._shared_browser
            browser.execute_script("window.open('about:blank', '_blank');")
            browser.switch_to.window(browser.window_handles[-1])
            
            self.tab_handle = browser.current_window_handle
            WebDriverPool._platform_tabs[self.platform_name] = self.tab_handle
```

**Actual Resource Limits**:
- `MAX_BROWSER_INSTANCES = 1` (NOT 4)
- `MAX_TABS_PER_BROWSER = unlimited` (limited by platform count)
- Memory: Single browser process (~200-500MB)
- CPU: Single browser process utilization

### Thread-Safe Database Operations (Production)
**Files**: `database/core/connection_manager.py`, `database/core/batch_operations.py`

```python
class ConnectionManager:
    """Thread-safe SQLite connection with context manager"""
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.connection: sqlite3.Connection | None = None
    
    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=30.0
        )
        # Enable WAL mode for concurrent reads
        self.connection.execute("PRAGMA journal_mode=WAL")
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection:
            self.connection.close()
```

**Batch Operations** (Production):
```python
class BatchOperations:
    """Efficient bulk job storage"""
    def store_jobs_batch(self, jobs: list[JobModel], db_path: str) -> int:
        with ConnectionManager(db_path) as conn:
            cursor = conn.cursor()
            job_data = [
                (
                    job.job_id, job.job_role, job.company,
                    job.experience, json.dumps(job.skills), job.jd
                )
                for job in jobs
            ]
            cursor.executemany(
                "INSERT OR REPLACE INTO jobs VALUES (?, ?, ?, ?, ?, ?)",
                job_data
            )
            conn.commit()
            return len(jobs)
```

## Production Coordination & Monitoring

### Actual Progress Tracking
**Current Status**: Basic logging only (no real-time dashboard)

**LinkedIn Production Logging**:
```python
logger.info(f"Starting API-based LinkedIn scrape for {target_count} {job_role} jobs")
logger.info(f"Fetched job {len(jobs)}/{target_count}: {job.job_role}")
logger.info(f"Completed: {len(jobs)} jobs with NLP-extracted skills")
```

**Implementation Gaps**:
- ❌ No real-time status updates
- ❌ No completion percentage tracking
- ❌ No error count aggregation
- ❌ No cross-platform job count
- ✅ Basic per-platform logging only

### Production Graceful Shutdown
**File**: `scrapers/base/driver_pool.py`

```python
def cleanup_pool(self):
    """Close platform's tab (NOT entire browser)"""
    if WebDriverPool._shared_browser and self.tab_handle:
        WebDriverPool._shared_browser.switch_to.window(self.tab_handle)
        WebDriverPool._shared_browser.close()
        WebDriverPool._platform_tabs.pop(self.platform_name)

@classmethod
def cleanup_shared_browser(cls):
    """Cleanup shared browser completely"""
    if cls._shared_browser:
        cls._shared_browser.quit()
        cls._shared_browser = None
        cls._platform_tabs.clear()
        cls._initialized = False
```

**Database Cleanup** (Production):
```python
with ConnectionManager(db_path) as conn:
    # Context manager handles cleanup automatically
    cursor.execute("SELECT * FROM jobs")
# Connection closed automatically on __exit__
```

**Actual Shutdown Behavior**:
- ✅ Browser cleanup via context manager
- ✅ Database connection cleanup via context manager
- ✅ Tab cleanup per platform
- ❌ No signal handling implemented
- ⚠️ Partial results preserved if exception during scraping

## Future Parallelization Plans

### NOT CURRENTLY IMPLEMENTED
The following parallelization strategies are NOT implemented and would require significant refactoring:

1. **Multi-Process Architecture**: Current single-browser design doesn't support true parallel execution
2. **ThreadPoolExecutor**: No concurrent platform scraping (sequential only)
3. **Rate Limiter Classes**: No sophisticated rate limiting (simple asyncio.sleep)
4. **Process Isolation**: All platforms share same browser (potential conflicts)
5. **Resource Limits Per Process**: Not applicable (single process only)

### To Enable True Parallelization
Would require:
- Separate browser instances per platform (NOT shared tabs)
- Process-based or thread-based executor for concurrent execution
- Sophisticated rate limiting per platform
- Process-safe database operations with proper locking
- Resource monitoring and limits per platform process

## Summary: Production vs Planned Architecture

| Feature | Planned (Documentation) | Actual (Production) |
|---------|------------------------|---------------------|
| **Execution Model** | Multi-process (4 processes) | Single asyncio process |
| **Browser Instances** | 4 separate browsers | 1 shared browser |
| **Platform Isolation** | Process-level isolation | Tab-level isolation |
| **Concurrency** | Parallel execution | Sequential execution |
| **Rate Limiting** | Sophisticated RateLimiter classes | Simple asyncio.sleep() |
| **Resource Management** | Per-process limits | Single process limits |
| **ThreadPoolExecutor** | 4 workers | Not used |
| **Progress Tracking** | Real-time dashboard | Basic logging only |
| **Signal Handling** | Implemented | Not implemented |
| **LinkedIn** | ✅ Production ready | ✅ Production ready |
| **Indeed** | ✅ Parallel process | ⚠️ Stub (incomplete) |
| **Naukri** | ✅ Parallel process | ⚠️ Stub (incomplete) |
| **YCombinator** | ✅ Parallel process | ❌ Not started |
