# Parallel Execution Context - Job Scrapper

## Parallel Architecture Design

### Multi-Process Strategy
```python
# 4 isolated processes to prevent conflicts
Process 1: LinkedIn Scraper (Most complex - longest runtime)
Process 2: Indeed Scraper (Dynamic content + CAPTCHAs)
Process 3: Naukri Scraper (Popup handling + registration walls)
Process 4: YCombinator Scraper (Fastest - requests only)
```

### ThreadPoolExecutor Implementation
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading

class ParallelJobScraper:
    def __init__(self):
        self.results_queue = Queue()
        self.rate_limiters = {
            'linkedin': RateLimiter(20),   # 20 requests/minute
            'indeed': RateLimiter(30),     # 30 requests/minute
            'naukri': RateLimiter(25),     # 25 requests/minute
            'ycombinator': RateLimiter(60) # 60 requests/minute
        }
    
    def scrape_all_platforms(self, job_role: str):
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.scrape_linkedin, job_role): 'linkedin',
                executor.submit(self.scrape_indeed, job_role): 'indeed',
                executor.submit(self.scrape_naukri, job_role): 'naukri',
                executor.submit(self.scrape_ycombinator, job_role): 'ycombinator'
            }
```

## Platform-Specific Parallelization

### LinkedIn (Process 1)
- **Challenge**: Most complex, requires guest mode navigation
- **Solution**: Dedicated ChromeDriver instance with longest timeout
- **Rate Limit**: 20 requests/minute (most restrictive)
- **Expected Runtime**: 15-20 minutes for 100+ jobs

### Indeed (Process 2)  
- **Challenge**: CAPTCHA detection, dynamic loading
- **Solution**: CAPTCHA handling + retry mechanism
- **Rate Limit**: 30 requests/minute
- **Expected Runtime**: 10-15 minutes for 100+ jobs

### Naukri (Process 3)
- **Challenge**: Location popups, registration prompts
- **Solution**: Popup dismissal automation
- **Rate Limit**: 25 requests/minute  
- **Expected Runtime**: 8-12 minutes for 100+ jobs

### YCombinator (Process 4)
- **Challenge**: None (static content)
- **Solution**: Simple requests + BeautifulSoup
- **Rate Limit**: 60 requests/minute (fastest)
- **Expected Runtime**: 2-3 minutes for 50+ jobs

## Resource Management

### Memory Optimization
```python
# Per-process resource limits
MEMORY_LIMIT_PER_PROCESS = 512 * 1024 * 1024  # 512MB
CPU_CORES_PER_PROCESS = 1
MAX_BROWSER_INSTANCES = 4
```

### Thread-Safe Database Operations
```python
import sqlite3
import threading

class ThreadSafeDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.local = threading.local()
        
    def get_connection(self):
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(
                self.db_path, 
                check_same_thread=False,
                isolation_level=None  # WAL mode
            )
        return self.local.connection
```

## Coordination & Monitoring

### Progress Tracking
- Real-time status updates from each process
- Completion percentage per platform
- Error count and retry attempts
- Total jobs collected across all platforms

### Graceful Shutdown
- Signal handling for clean termination
- Browser cleanup for all ChromeDriver instances  
- Database connection cleanup
- Partial results preservation
