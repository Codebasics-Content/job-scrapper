# BrightData Datasets API Integration - Complete Guide

## 🎯 Architecture Overview

### Current System:
```
Manual Browser Scraping (Slow)
    ↓
BrightData Scraping Browser → Playwright → Extract HTML → Parse → Skills Extraction
    ↓
Database Storage
```

### Recommended System (Using BrightData Datasets API):
```
BrightData Pre-Collected Data (Fast & Reliable)
    ↓
Datasets API → JSON Response → Skills Extraction → Database Storage
    ↓
Much Faster! (~1-2s total vs 2-3s per job)
```

---

## 📊 BrightData Datasets API Response Structures

### LinkedIn Jobs API Response Format

**Endpoint:**
```
POST https://api.brightdata.com/datasets/v3/trigger
```

**Request:**
```json
{
  "dataset_id": "gd_lpfll7v5hcqtkxl6l",
  "endpoint": "discover_new",
  "keyword": "Machine Learning Engineer",
  "location": "United States",
  "time_range": "Past week",
  "job_type": "Full-time",
  "limit": 50
}
```

**Response Structure (from your example):**
```json
[
  {
    "url": "https://www.linkedin.com/jobs/view/...",
    "job_posting_id": "4312792681",
    "job_title": "Machine Learning Engineer",
    "company_name": "Google",
    "company_id": "33247894",
    "job_location": "San Francisco, CA, United States",
    "job_summary": "Full detailed job description with requirements, responsibilities...",
    "job_seniority_level": "Mid-Senior level",
    "job_function": "Engineering",
    "job_employment_type": "Full-time",
    "job_industries": "Software Development",
    "job_base_pay_range": "$120,000 - $180,000",
    "company_url": "https://linkedin.com/company/google",
    "job_posted_time": "2 days ago",
    "job_num_applicants": 156,
    "apply_link": "https://www.linkedin.com/signup/...",
    "country_code": "US",
    "title_id": "6003",
    "company_logo": "https://media.licdn.com/...",
    "job_posted_date": "2025-10-08T14:23:11.482Z",
    "job_poster": {
      "name": "John Smith",
      "title": "Senior Recruiter",
      "url": "https://linkedin.com/in/johnsmith"
    },
    "application_availability": true,
    "job_description_formatted": "<div>HTML formatted description...</div>",
    "base_salary": {
      "currency": "USD",
      "max_amount": 180000,
      "min_amount": 120000,
      "payment_period": "YEAR"
    }
  }
]
```

**Key Fields for Mapping:**
| BrightData Field | JobModel Field | Notes |
|------------------|----------------|-------|
| `job_title` | `Job_Role` | Direct mapping |
| `company_name` | `Company` | Direct mapping |
| `job_location` | `location` | Direct mapping |
| `job_summary` | `jd` | ✅ **Full description for skills extraction** |
| `job_seniority_level` | `Experience` | Direct mapping |
| `url` | `url` | Direct mapping |
| `base_salary` | `salary` | Format as string |
| `job_posting_id` | `job_id` | Direct mapping |

---

### Indeed Jobs API Response Format

**Endpoint:**
```
POST https://api.brightdata.com/datasets/v3/trigger
```

**Request:**
```json
{
  "dataset_id": "gd_l4dx9j9sscpvs7no2",
  "endpoint": "discover_new",
  "keyword_search": "Data Scientist",
  "location": "Seattle, WA",
  "date_posted": "Last 7 days",
  "limit": 50
}
```

**Response Structure (from your example):**
```json
[
  {
    "jobid": "6240de59a4760f3b",
    "company_name": "Amazon",
    "date_posted_parsed": "2025-10-08T17:50:09.700Z",
    "job_title": "Data Scientist",
    "description_text": "Full plain text job description with requirements...",
    "benefits": ["Health insurance", "401k", "Flexible schedule"],
    "qualifications": ["PhD in CS", "3+ years Python"],
    "job_type": "Full-time",
    "location": "Seattle, WA 98109",
    "salary_formatted": "$150k - $180k a year",
    "company_rating": 4.2,
    "company_reviews_count": 12500,
    "country": "US",
    "date_posted": "2 days ago",
    "description": "Full HTML job description...",
    "region": "WA",
    "company_link": "https://www.indeed.com/cmp/Amazon",
    "company_website": "https://amazon.com",
    "domain": "https://www.indeed.com",
    "apply_link": "https://www.indeed.com/applystart?jk=...",
    "url": "https://www.indeed.com/viewjob?jk=6240de59a4760f3b",
    "is_expired": false,
    "job_description_formatted": "<div>HTML formatted description...</div>",
    "logo_url": "https://d2q79iu7y748jz.cloudfront.net/...",
    "shift_schedule": ["Day shift", "Monday to Friday"]
  }
]
```

**Key Fields for Mapping:**
| BrightData Field | JobModel Field | Notes |
|------------------|----------------|-------|
| `job_title` | `Job_Role` | Direct mapping |
| `company_name` | `Company` | Direct mapping |
| `location` | `location` | Direct mapping |
| `description_text` OR `description` | `jd` | ✅ **Full description for skills extraction** |
| `job_type` | `Experience` | Map "Full-time" → Experience |
| `url` | `url` | Direct mapping |
| `salary_formatted` | `salary` | Direct mapping |
| `jobid` | `job_id` | Direct mapping |
| `qualifications` | - | Extract skills from this array too |

---

## 🔧 Implementation Plan

### Step 1: Create BrightData Dataset Scrapers (Using Existing Clients)

Your codebase already has the structure! Let's enhance it:

**File: `src/scraper/brightdata/linkedin_dataset_scraper.py`** (NEW)
```python
"""LinkedIn scraper using BrightData Datasets API (pre-collected data)."""
from typing import List
from datetime import datetime

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from src.scraper.brightdata.clients.linkedin import LinkedInClient


async def scrape_linkedin_jobs_dataset(
    keyword: str,
    location: str = "United States",
    limit: int = 50
) -> List[JobModel]:
    """Scrape LinkedIn jobs using BrightData Datasets API.
    
    Args:
        keyword: Job search keyword (e.g., "Machine Learning Engineer")
        location: Location filter (e.g., "United States", "San Francisco, CA")
        limit: Maximum number of jobs to scrape
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"🚀 Starting LinkedIn Datasets API scraping...")
    print(f"   Keyword: {keyword}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize clients
    client = LinkedInClient()
    skills_parser = SkillsParser()
    
    # Discover jobs via BrightData Datasets API
    print(f"📡 Calling BrightData Datasets API...")
    raw_jobs = client.discover_jobs(
        keyword=keyword,
        location=location,
        time_range="past_week",
        limit=limit
    )
    
    print(f"📥 Received {len(raw_jobs)} jobs from BrightData")
    
    # Convert to JobModel with skills extraction
    job_models = []
    for idx, raw_job in enumerate(raw_jobs, 1):
        try:
            # Extract fields from BrightData response
            job_title = raw_job.get("job_title", "Unknown")
            company_name = raw_job.get("company_name", "Unknown")
            job_location = raw_job.get("job_location", "Unknown")
            job_url = raw_job.get("url", "")
            job_id = raw_job.get("job_posting_id") or job_url
            
            # Get full job description
            job_description = raw_job.get("job_summary", "")
            
            # Extract skills from description
            skills_list = skills_parser.extract_from_text(job_description)
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            # Log first 2 jobs for debugging
            if idx <= 2:
                print(f"\n📝 Job #{idx}:")
                print(f"   Title: {job_title}")
                print(f"   Company: {company_name}")
                print(f"   Description Length: {len(job_description)} chars")
                print(f"   Extracted Skills ({len(skills_list)}): {skills_list[:10]}")
            
            # Extract salary info
            salary = None
            base_salary = raw_job.get("base_salary", {})
            if base_salary and base_salary.get("min_amount"):
                min_amt = base_salary.get("min_amount", 0)
                max_amt = base_salary.get("max_amount", 0)
                currency = base_salary.get("currency", "USD")
                period = base_salary.get("payment_period", "YEAR")
                salary = f"${min_amt:,} - ${max_amt:,} {currency}/{period}"
            
            # Create JobModel
            job = JobModel(
                job_id=str(job_id),
                Job_Role=job_title,
                Company=company_name,
                Experience=raw_job.get("job_seniority_level", ""),
                Skills=skills_str,
                jd=job_description,
                company_detail=raw_job.get("job_industries", ""),
                platform="linkedin",
                url=job_url,
                location=job_location,
                salary=salary,
                posted_date=datetime.now(),
                skills_list=skills_list,
                normalized_skills=[s.lower() for s in skills_list]
            )
            
            job_models.append(job)
            
        except Exception as e:
            print(f"⚠️  Failed to process job #{idx}: {e}")
            continue
    
    print(f"\n✅ Successfully created {len(job_models)} JobModel objects with skills")
    return job_models
```

**File: `src/scraper/brightdata/indeed_dataset_scraper.py`** (NEW)
```python
"""Indeed scraper using BrightData Datasets API (pre-collected data)."""
from typing import List
from datetime import datetime

from src.models import JobModel
from src.scraper.brightdata.parsers.skills_parser import SkillsParser
from src.scraper.brightdata.clients.indeed import IndeedClient


async def scrape_indeed_jobs_dataset(
    query: str,
    location: str = "United States",
    limit: int = 50
) -> List[JobModel]:
    """Scrape Indeed jobs using BrightData Datasets API.
    
    Args:
        query: Job search query (e.g., "Data Scientist")
        location: Location filter (e.g., "Seattle, WA")
        limit: Maximum number of jobs to scrape
    
    Returns:
        List of JobModel objects with extracted skills
    """
    print(f"🚀 Starting Indeed Datasets API scraping...")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    # Initialize clients
    client = IndeedClient()
    skills_parser = SkillsParser()
    
    # Discover jobs via BrightData Datasets API
    print(f"📡 Calling BrightData Datasets API...")
    raw_jobs = client.discover_jobs(
        query=query,
        location=location,
        days_back=7,
        limit=limit
    )
    
    print(f"📥 Received {len(raw_jobs)} jobs from BrightData")
    
    # Convert to JobModel with skills extraction
    job_models = []
    for idx, raw_job in enumerate(raw_jobs, 1):
        try:
            # Extract fields from BrightData response
            job_title = raw_job.get("job_title", "Unknown")
            company_name = raw_job.get("company_name", "Unknown")
            job_location = raw_job.get("location", "Unknown")
            job_url = raw_job.get("url", "")
            job_id = raw_job.get("jobid") or job_url
            
            # Get full job description (try both fields)
            job_description = raw_job.get("description_text") or raw_job.get("description", "")
            
            # Extract skills from description
            skills_list = skills_parser.extract_from_text(job_description)
            
            # Also extract from qualifications array if available
            qualifications = raw_job.get("qualifications", [])
            if qualifications:
                quals_text = " ".join(qualifications)
                quals_skills = skills_parser.extract_from_text(quals_text)
                skills_list = list(set(skills_list + quals_skills))
            
            skills_str = ", ".join(skills_list) if skills_list else ""
            
            # Log first 2 jobs for debugging
            if idx <= 2:
                print(f"\n📝 Job #{idx}:")
                print(f"   Title: {job_title}")
                print(f"   Company: {company_name}")
                print(f"   Description Length: {len(job_description)} chars")
                print(f"   Extracted Skills ({len(skills_list)}): {skills_list[:10]}")
            
            # Create JobModel
            job = JobModel(
                job_id=str(job_id),
                Job_Role=job_title,
                Company=company_name,
                Experience=raw_job.get("job_type", ""),
                Skills=skills_str,
                jd=job_description,
                company_detail="",
                platform="indeed",
                url=job_url,
                location=job_location,
                salary=raw_job.get("salary_formatted"),
                posted_date=datetime.now(),
                skills_list=skills_list,
                normalized_skills=[s.lower() for s in skills_list]
            )
            
            job_models.append(job)
            
        except Exception as e:
            print(f"⚠️  Failed to process job #{idx}: {e}")
            continue
    
    print(f"\n✅ Successfully created {len(job_models)} JobModel objects with skills")
    return job_models
```

---

### Step 2: Update Streamlit App to Use Datasets API

**File: `streamlit_app.py`** - Add import and switch logic:

```python
# At the top, add new imports
from src.scraper.brightdata.linkedin_dataset_scraper import scrape_linkedin_jobs_dataset
from src.scraper.brightdata.indeed_dataset_scraper import scrape_indeed_jobs_dataset

# In the scraping section, replace browser scraping with datasets API:

# BRIGHTDATA DATASETS API (LinkedIn/Indeed) - Pre-collected data
if platform in ["LinkedIn", "Indeed"]:
    status_text.write(f"📡 Calling BrightData Datasets API for {platform}...")
    progress_bar.progress(0.1)
    
    # Use first selected location or default
    location = selected_countries[0] if selected_countries else "United States"
    
    status_text.write(f"🔍 Fetching {num_jobs} jobs from {platform} Datasets API...")
    progress_bar.progress(0.3)
    
    try:
        if platform == "LinkedIn":
            jobs = await scrape_linkedin_jobs_dataset(
                keyword=job_role,
                location=location,
                limit=num_jobs
            )
        else:  # Indeed
            jobs = await scrape_indeed_jobs_dataset(
                query=job_role,
                location=location,
                limit=num_jobs
            )
        
        scraped_metric.metric("Jobs Scraped", len(jobs))
        progress_bar.progress(0.7)
        
    except Exception as e:
        st.error(f"❌ Datasets API failed: {str(e)}")
        logging.exception("Datasets API error")
        raise
```

---

## 🔑 Configuration Required

### .env File Setup

```bash
# BrightData Configuration
BRIGHTDATA_API_TOKEN=Bearer your_actual_token_here

# Optional: Override dataset IDs (usually not needed)
# BRIGHTDATA_LINKEDIN_DATASET_ID=gd_lpfll7v5hcqtkxl6l
# BRIGHTDATA_INDEED_DATASET_ID=gd_l4dx9j9sscpvs7no2
```

**Steps:**
1. Login to https://brightdata.com
2. Go to **Control Panel** → **Datasets** → **API Access**
3. Copy your **API Token** (format: `Bearer abc123...`)
4. Update `.env` file with your token

---

## 📊 Comparison: Browser Scraping vs Datasets API

| Feature | Browser Scraping | Datasets API |
|---------|------------------|--------------|
| **Speed** | 2-3s per job | ~1-2s total for 50 jobs |
| **Reliability** | Can break if site changes | BrightData maintains scrapers |
| **Setup** | Requires BROWSER_URL | Only requires API_TOKEN |
| **Cost** | Scraping Browser credits | Datasets API credits |
| **Data Quality** | Full HTML, need to parse | Pre-parsed JSON |
| **Skills Extraction** | Need to fetch full page | Description already in response |
| **Maintenance** | You maintain selectors | BrightData maintains |
| **Rate Limiting** | Need to handle | BrightData handles |

**Recommendation:** ✅ **Use Datasets API** - Faster, more reliable, less maintenance!

---

## 🧪 Testing

### Test 1: Verify .env Configuration
```bash
cd /mnt/windows_d/Gauravs-Files-and-Folders/Freelance/Codebasics/Job_Scrapper
python3 -c "
import sys
sys.path.insert(0, 'src')
from scraper.brightdata.config.settings import get_settings

settings = get_settings()
print(f'✅ API Token: {settings.api_token[:20]}...')
print(f'✅ LinkedIn Dataset ID: {settings.linkedin_dataset_id}')
print(f'✅ Indeed Dataset ID: {settings.indeed_dataset_id}')
"
```

### Test 2: Test LinkedIn Datasets API
```bash
python3 -c "
import sys
import asyncio
sys.path.insert(0, 'src')

async def test():
    from scraper.brightdata.linkedin_dataset_scraper import scrape_linkedin_jobs_dataset
    jobs = await scrape_linkedin_jobs_dataset(
        keyword='Machine Learning Engineer',
        location='United States',
        limit=5
    )
    print(f'\nResults: {len(jobs)} jobs')
    for job in jobs[:2]:
        print(f'\n- {job.Job_Role} at {job.Company}')
        print(f'  Skills: {job.Skills[:100]}...')

asyncio.run(test())
"
```

### Test 3: Test Indeed Datasets API
```bash
python3 -c "
import sys
import asyncio
sys.path.insert(0, 'src')

async def test():
    from scraper.brightdata.indeed_dataset_scraper import scrape_indeed_jobs_dataset
    jobs = await scrape_indeed_jobs_dataset(
        query='Data Scientist',
        location='Seattle, WA',
        limit=5
    )
    print(f'\nResults: {len(jobs)} jobs')
    for job in jobs[:2]:
        print(f'\n- {job.Job_Role} at {job.Company}')
        print(f'  Skills: {job.Skills[:100]}...')

asyncio.run(test())
"
```

---

## 🎯 Next Steps

### ✅ Immediate Actions:
1. **Update `.env`** with your BrightData API token
2. **Create new scrapers**: `linkedin_dataset_scraper.py` and `indeed_dataset_scraper.py`
3. **Update `streamlit_app.py`** to use Datasets API instead of browser scraping
4. **Test** with 5-10 jobs to verify everything works

### 🔄 Optional Improvements:
- [ ] Add caching for API responses
- [ ] Implement batch processing for large job counts
- [ ] Add parallel processing for multiple locations
- [ ] Create background job queue for large scraping tasks
- [ ] Add retry logic with exponential backoff

---

## 📖 Summary

✅ **BrightData Datasets API** provides pre-collected, structured JSON data  
✅ **Much faster** than browser scraping (bulk data vs per-job fetching)  
✅ **Full job descriptions** included in response for skills extraction  
✅ **Your existing SkillsParser** works perfectly with the data  
✅ **Less maintenance** - BrightData handles scraper updates  
🔑 **Only need API Token** - No Browser URL required  

**Result: Faster, more reliable job scraping with comprehensive skills extraction!** 🚀
