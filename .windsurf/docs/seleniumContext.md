# Selenium Context - Job Scrapper

## Browser Configuration

### Chrome Options (Anti-Detection)
```python
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage') 
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-extensions')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
```

### WebDriver Manager Setup
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

## Platform-Specific Challenges

### LinkedIn
- **Login Required**: Most content requires authentication
- **Rate Limiting**: Aggressive bot detection
- **Dynamic Loading**: Infinite scroll for job listings
- **Solution**: Use guest mode, implement scroll delays, rotate user agents

### Indeed
- **CAPTCHA**: Frequent CAPTCHA challenges
- **JavaScript Heavy**: Most content loaded dynamically
- **Popup Overlays**: Cookie consent, location popups
- **Solution**: Handle popups first, implement CAPTCHA detection

### Naukri
- **Location Popups**: Always asks for location
- **Registration Wall**: Some content behind registration
- **Solution**: Handle location dialog, use guest browsing

## Wait Strategies

### Element Wait Patterns
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for job listings to load
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card")))

# Wait for specific job details
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View Details")))
```

### Smart Delays
- **Between pages**: 2-5 seconds random delay
- **After clicks**: 1-3 seconds
- **Scroll actions**: 0.5-2 seconds
- **Page loads**: Wait for specific elements, not fixed time

## Resource Management

### Memory Optimization
- Close tabs after scraping each job
- Clear browser cache periodically  
- Restart driver every 50-100 jobs
- Use headless mode for production

### Error Recovery
- Implement retry mechanism (3 attempts)
- Save progress frequently to database
- Resume from last successful job ID
- Log all failures for manual review
