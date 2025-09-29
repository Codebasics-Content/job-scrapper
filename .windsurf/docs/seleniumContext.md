# Selenium Context - Job Scrapper (Production Implementation)

## Actual Browser Configuration

### Production: Undetected ChromeDriver with GUI Mode
**File**: `scrapers/base/anti_detection.py` (81 lines - EMD compliant)

```python
import undetected_chromedriver as uc
from fake_useragent import UserAgent

class AntiDetectionDriverFactory:
    def __init__(self):
        self.user_agent = UserAgent()
        
    def create_driver(self) -> uc.Chrome | None:
        """Create configured Chrome WebDriver with anti-bot measures"""
        options = self._configure_chrome_options()
        driver = uc.Chrome(options=options)
        self._apply_javascript_evasions(driver)
        return driver
```

### Production Chrome Options (GUI Mode - NOT Headless)
```python
def _configure_chrome_options(self) -> uc.ChromeOptions:
    options = uc.ChromeOptions()
    
    # Anti-detection basics
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={self.user_agent.random}")
    
    # GUI mode configuration (browser visible for debugging)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    
    # Popup handling preferences
    options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_settings.popups': 0
    })
    
    return options
```

### JavaScript Anti-Detection Evasions (Production)
```python
def _apply_javascript_evasions(self, driver: uc.Chrome) -> None:
    # Remove webdriver property
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    
    # Override navigator.languages
    driver.execute_script(
        "Object.defineProperty(navigator, 'languages', "
        "{get: () => ['en-US', 'en']})"
    )
    
    # Override permissions API
    driver.execute_script(
        "Object.defineProperty(navigator, 'permissions', "
        "{get: () => ({query: () => Promise.resolve({state: 'granted'})})})"
    )
    
    # Override plugins length
    driver.execute_script(
        "Object.defineProperty(navigator, 'plugins', "
        "{get: () => ({length: 3})})"
    )
```

## Production Platform-Specific Implementations

### LinkedIn ✅ PRODUCTION READY
**Status**: Fully implemented with 1000+ jobs tested
**Approach**: API-based extraction with infinite scroll
**Files**: `scrapers/linkedin/scraper.py`, `extractors/scroll_handler.py`, `extractors/api_job_fetcher.py`

**Challenges Solved**:
- ✅ **Guest Mode**: Uses `/jobs-guest/jobs/api/jobPosting/{job_id}` endpoint
- ✅ **Infinite Scroll**: JavaScript scroll injection with duplicate tracking
- ✅ **Rate Limiting**: 0.5s between API calls, 2s between scroll operations
- ✅ **Dynamic Loading**: Wait for `.job-search-card` elements before extraction

**Production Selectors**:
```python
job_cards = "li.jobs-search__results-list > li"
job_id_attr = "data-entity-urn" or "data-job-id"
see_more_btn = "button.infinite-scroller__show-more-button"
```

### Indeed ⚠️ STUB - INCOMPLETE
**Status**: Basic structure only (93 lines - EMD violation)
**File**: `scrapers/indeed/scraper.py`

**Outstanding Challenges**:
- ❌ **No pagination handler** - Cannot scrape beyond first page
- ❌ **Incomplete extractors** - Job data extraction not functional
- ❌ **No location filter** - Location parameter not implemented
- ❌ **Basic error handling** - Minimal recovery mechanisms

### Naukri ⚠️ STUB - INCOMPLETE
**Status**: Basic structure only (78 lines)
**File**: `scrapers/naukri/scraper.py`

**Outstanding Challenges**:
- ❌ **Incomplete extractor** - `extract_job_from_card()` not functional
- ❌ **No pagination** - Only scrapes first page
- ❌ **No location support** - Location parameter missing
- ❌ **Basic rate limiting** - Simple sleep(2) every 5 jobs

**Current Selectors** (may need update):
```python
job_cards = ".srp-jobtuple-wrapper, .jobTuple"
```

## Production Wait Strategies

### LinkedIn Production Timings
```python
# Between API calls
await asyncio.sleep(0.5)  # 0.5s between job detail fetches

# Between scroll operations
await asyncio.sleep(2)    # 2s after triggering infinite scroll

# Page load wait
driver.get(url)
await asyncio.sleep(3)    # Initial page load
```

### Naukri Production Timings
```python
# Initial page load
driver.get(search_url)
await asyncio.sleep(3)

# Rate limiting (every 5 jobs)
if i > 0 and i % 5 == 0:
    await asyncio.sleep(2)
```

### Element Wait Patterns (Not Used - Async Sleep Preferred)
Current implementation uses `asyncio.sleep()` instead of WebDriverWait for simplicity:
```python
# LinkedIn scroll handler
await asyncio.sleep(2)  # Wait for dynamic content to load

# Naukri job extraction
await asyncio.sleep(3)  # Wait for job listings to load
```

**Rationale**: Simple async delays work better with undetected-chromedriver than explicit waits

## Production Resource Management

### Single Browser with Multiple Tabs
**File**: `scrapers/base/driver_pool.py` (96 lines)

**Architecture**: Shared browser instance with platform-specific tabs
```python
class WebDriverPool:
    # Shared browser across all platforms
    _shared_browser: uc.Chrome | None = None
    _platform_tabs: dict[str, str] = {}  # platform_name -> window_handle
    _initialized: bool = False
    _creation_lock: threading.Lock = threading.Lock()
```

### Tab Management (Production)
```python
def initialize_pool(self, driver_factory):
    """Create tab for platform (thread-safe)"""
    with WebDriverPool._creation_lock:
        # Create shared browser if not exists
        if WebDriverPool._shared_browser is None:
            WebDriverPool._shared_browser = driver_factory.create_driver()
        
        # Create new tab for this platform
        browser = WebDriverPool._shared_browser
        browser.execute_script("window.open('about:blank', '_blank');")
        browser.switch_to.window(browser.window_handles[-1])
        
        self.tab_handle = browser.current_window_handle
        WebDriverPool._platform_tabs[self.platform_name] = self.tab_handle
```

### Driver Access Pattern
```python
def get_driver(self) -> uc.Chrome | None:
    """Get shared browser and switch to platform's tab"""
    if WebDriverPool._shared_browser is None:
        return None
    
    WebDriverPool._shared_browser.switch_to.window(self.tab_handle)
    return WebDriverPool._shared_browser
```

### Cleanup (Production)
```python
def cleanup_pool(self):
    """Close platform's tab"""
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

### Error Recovery (LinkedIn Production)
```python
try:
    driver = self.get_driver()
    # Scraping logic
finally:
    self.return_driver(driver)  # No-op for tab-based system
```

**Note**: No driver restart needed - single browser runs for entire session with GUI mode for debugging
