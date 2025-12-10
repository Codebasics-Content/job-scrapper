# JobSpy LinkedIn Scraping Setup

## ✅ Quick Start (Already Installed!)

JobSpy is now integrated and ready to use for **FREE, unlimited LinkedIn job scraping**.

### Installation Status
- ✅ `python-jobspy` library installed
- ✅ Scraper module created: `src/importer/jobspy/linkedin_scraper.py`
- ✅ Test script available: `test_jobspy_linkedin.py`
- ✅ Successfully tested: 10 jobs scraped without proxy

---

## 🚀 Usage

### Basic Usage (No Proxy)
```python
from src.importer.jobspy import scrape_linkedin_jobs

jobs = scrape_linkedin_jobs(
    keyword="Python Developer",
    location="United States",
    limit=50
)

print(f"Found {len(jobs)} jobs")
```

### With BrightData Proxy (Recommended)
```bash
# 1. Configure proxy in .env
PROXY_URL=http://localhost:24000

# 2. Start BrightData Proxy Manager
./start_proxy_manager.sh

# 3. Run scraper (automatically uses proxy from .env)
python test_jobspy_linkedin.py
```

---

## 🎯 Function Parameters

```python
scrape_linkedin_jobs(
    keyword: str,              # Required: Job search term
    location: str = "Worldwide",
    limit: int = 100,          # Max jobs to scrape
    hours_old: int = None,     # Filter by job age (e.g., 72 for 3 days)
    job_type: str = None,      # "fulltime", "parttime", "internship", "contract"
    is_remote: bool = False,   # Filter remote jobs only
    fetch_description: bool = True  # Get full descriptions (slower but complete)
)
```

---

## 📋 Output Schema

Each job returns a dictionary with:
```python
{
    "title": "Software Engineer",
    "company": "Google",
    "company_url": "https://google.com",
    "job_url": "https://linkedin.com/jobs/view/...",
    "location": "San Francisco, CA",
    "description": "Full job description...",
    "job_type": "fulltime",
    "date_posted": "2025-10-12",
    "is_remote": False,
    "job_level": "Mid-Senior level",
    "company_industry": "Technology"
}
```

---

## 💡 Comparison: JobSpy vs BrightData Datasets

| Feature | JobSpy (FREE) | BrightData Datasets |
|---------|---------------|---------------------|
| **Cost** | $0 | $250/100K (one-time) |
| **LinkedIn** | ✅ Unlimited | Limited to purchased records |
| **Real-time** | ✅ Fresh data | Pre-collected data |
| **Platforms** | 6+ (LinkedIn, Indeed, etc.) | LinkedIn only |
| **Proxy Support** | ✅ Built-in | N/A |
| **Setup** | Already done! | Requires API token |

**Recommendation:** Use JobSpy for all LinkedIn scraping needs.

---

## 🔧 Advanced: Integrate with Streamlit

```python
# In streamlit_app.py
from src.importer.jobspy import scrape_linkedin_jobs

if platform == "LinkedIn":
    jobs = scrape_linkedin_jobs(
        keyword=job_role,
        location=location,
        limit=num_jobs,
        fetch_description=True
    )
    # Store in database...
```

---

## ⚠️ Rate Limiting Tips

1. **Use BrightData Proxy** (recommended)
   - Configure `PROXY_URL` in `.env`
   - Start proxy manager: `./start_proxy_manager.sh`

2. **Without Proxy**
   - LinkedIn may rate limit after ~100-200 jobs
   - Wait 10-15 minutes between large scrapes
   - Use smaller batch sizes (20-50 jobs)

3. **Best Practice**
   - Always use proxy for production
   - Test with small batches first
   - Monitor logs for rate limit warnings

---

## 🎉 Success!

JobSpy is ready to use. Run the test:
```bash
python test_jobspy_linkedin.py
```

Expected output: 10 LinkedIn jobs with full details!
