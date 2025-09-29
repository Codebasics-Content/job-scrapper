# API URL Patterns - Job Platforms

## 1. LinkedIn Jobs

### Base URL Pattern
```
https://www.linkedin.com/jobs/search/
```

### Key Parameters
- `keywords`: Job title or skills (e.g., "software engineer", "AI engineer")
- `location`: Geographic location (e.g., "San Francisco, California", "Mumbai, India")
- `f_E`: Experience level
  - `1`: Internship
  - `2`: Entry level (1-3 years)
  - `3`: Associate (3-5 years)
  - `4`: Mid-Senior level (5-10 years)
  - `5`: Director (10+ years)
- `f_TP`: Job type
  - `F`: Full-time
  - `P`: Part-time
  - `C`: Contract
  - `T`: Temporary
  - `I`: Internship
- `start`: Pagination offset (0, 25, 50, etc.)

### Example URLs
```
# AI Engineer jobs in Mumbai
https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer&location=Mumbai%2C%20India&f_E=2

# AI Engineer jobs with pagination
https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=San%20Francisco%2C%20California&start=25
```

### Important Notes
- Results are paginated with 25 listings per page
- LinkedIn limits accessible results to ~1,000 jobs
- Requires proper User-Agent headers to avoid blocking
- May need Selenium for JavaScript-heavy content

## 2. Indeed Jobs

### Base URL Pattern
```
https://www.indeed.com/jobs
```

### Key Parameters
- `q`: Query/job title (e.g., "python developer", "data scientist")
- `l`: Location (e.g., "Texas", "New York, NY", "Mumbai")
- `start`: Pagination offset (0, 10, 20, etc.)
- `sort`: Sort order
  - `date`: Most recent
  - `relevance`: Most relevant (default)
- `radius`: Search radius in miles/km
- `fromage`: Days since posted
  - `1`: Last 24 hours
  - `3`: Last 3 days
  - `7`: Last week
  - `14`: Last 2 weeks

### Example URLs
```
# Python jobs in Texas
https://www.indeed.com/jobs?q=python&l=Texas

# AI Engineer jobs with pagination
https://www.indeed.com/jobs?q=AI%20Engineer&l=Mumbai&start=10

# Recent data scientist jobs
https://www.indeed.com/jobs?q=data%20scientist&l=New%20York%2C%20NY&fromage=7&sort=date
```

### Important Notes
- Results show 15 job listings per page
- Hidden JSON data available in page source (window.mosaic.providerData)
- Requires proper headers to avoid 403 blocking
- Use `start` parameter for pagination (0, 10, 20, 30...)

## 3. Naukri.com

### Base URL Pattern
```
https://www.naukri.com/[job-title]-jobs-in-[location]
```

### Alternative Search Pattern
```
https://www.naukri.com/jobapi/v3/search
```

### Key Parameters
- `k`: Keywords/job title (e.g., "financial analyst", "software engineer")
- `l`: Location (e.g., "mumbai", "bangalore", "delhi")
- `noOfResults`: Number of results per page (default: 20)
- `pageNo`: Page number for pagination (1, 2, 3...)
- `searchType`: Search type (`adv` for advanced)
- `urlType`: URL type (`search_by_keyword`)

### Example URLs
```
# Financial Analyst jobs in Mumbai (SEO URL)
https://www.naukri.com/financial-analyst-jobs-in-mumbai?k=financial%20analyst&l=mumbai

# API-style search
https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword=data%20science&pageNo=1&k=data%20science&l=mumbai
```

### Important Notes
- Uses SEO-friendly URLs for job searches
- Requires Selenium due to heavy JavaScript content
- API endpoint available for JSON responses
- Location parameter uses lowercase city names
- Pagination through `pageNo` parameter

## 4. Y Combinator (Work at a Startup)

### Base URL Pattern
```
https://www.workatastartup.com/companies
```

### Alternative Job Board
```
https://www.ycombinator.com/jobs
```

### Key Parameters (workatastartup.com)
- Search appears to be handled via frontend JavaScript
- No direct URL parameters for job filtering
- Uses GraphQL/API calls for data loading

### Example URLs
```
# Main job board
https://www.workatastartup.com/

# YC job board
https://www.ycombinator.com/jobs

# Specific role filtering (frontend-handled)
https://www.workatastartup.com/companies?role=Software%20Engineer
```

### Important Notes
- Heavily JavaScript-dependent (requires Selenium)
- Uses modern SPA architecture
- API calls likely needed for data extraction
- Limited direct URL parameter support
- Focus on YC-backed startup jobs only

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
