# BrightData API Setup Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Getting Your API Token](#getting-your-api-token)
3. [Dataset IDs (Pre-configured)](#dataset-ids-pre-configured)
4. [Environment Configuration](#environment-configuration)
5. [API Request Examples](#api-request-examples)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This job scraper uses **BrightData's Datasets API** to scrape jobs from:
- **LinkedIn** (via dataset `gd_lpfll7v5hcqtkxl6l`)
- **Indeed** (via dataset `gd_l4dx9j9sscpvs7no2`)
- **Naukri** (custom scraper - no BrightData required)

**You only need to configure ONE thing:** Your BrightData API Token

---

## 🔑 Getting Your API Token

### Step 1: Sign up / Log in to BrightData
1. Go to https://brightdata.com
2. Sign up for an account or log in
3. Navigate to the **Control Panel**: https://brightdata.com/cp

### Step 2: Find Your API Token
There are **two ways** to get your API token:

#### Method 1: From Datasets Section
1. Go to https://brightdata.com/cp/datasets
2. Click on **"API Access"** or **"Credentials"** tab
3. Look for **"API Token"** or **"Bearer Token"**
4. Copy the token (it will look like: `Bearer abc123...`)

#### Method 2: From Account Settings
1. Go to https://brightdata.com/cp/settings
2. Navigate to **"API Access"** section
3. Click **"Generate API Token"** if you don't have one
4. Copy the token

### Step 3: Keep Your Token Safe
⚠️ **IMPORTANT:** 
- Never commit your API token to Git
- Store it in `.env` file (which is in `.gitignore`)
- Treat it like a password

---

## 📊 Dataset IDs (Pre-configured)

Good news! **You don't need to find or configure dataset IDs manually.**

The dataset IDs are already hardcoded in the application:

| Platform | Dataset ID | Status |
|----------|-----------|--------|
| LinkedIn | `gd_lpfll7v5hcqtkxl6l` | ✅ Pre-configured |
| Indeed | `gd_l4dx9j9sscpvs7no2` | ✅ Pre-configured |
| Naukri | N/A (custom scraper) | ✅ No config needed |

### Where are they configured?
- **Code:** `src/scraper/brightdata/config/settings.py`
- **Environment:** `.env.template` (for reference)

### Can I override them?
Yes, if needed:
```bash
# In .env file
BRIGHTDATA_LINKEDIN_DATASET_ID=your_custom_dataset_id
BRIGHTDATA_INDEED_DATASET_ID=your_custom_dataset_id
```

But this is **not recommended** unless BrightData changes their dataset IDs.

---

## ⚙️ Environment Configuration

### Step 1: Copy the Template
```bash
cp .env.template .env
```

### Step 2: Edit `.env` and Add Your Token
```bash
# Open .env in your editor
nano .env  # or vim .env or code .env
```

### Step 3: Replace the Placeholder
```env
# BEFORE (placeholder)
BRIGHTDATA_API_TOKEN=your_brightdata_api_token_here

# AFTER (your actual token)
BRIGHTDATA_API_TOKEN=Bearer abc123def456ghi789jkl012mno345pqr678stu901
```

### Step 4: Verify Configuration
```python
# Test in Python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BRIGHTDATA_API_TOKEN")
print(f"Token configured: {token[:20]}..." if token else "Token NOT found!")
```

---

## 📡 API Request Examples

### LinkedIn Jobs API Request

```python
import requests

url = "https://api.brightdata.com/datasets/v3/trigger"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN_HERE",
    "Content-Type": "application/json",
}
params = {
    "dataset_id": "gd_lpfll7v5hcqtkxl6l",  # LinkedIn dataset
    "include_errors": "true",
    "type": "discover_new",
    "discover_by": "keyword",
}
data = [
    {
        "location": "New York",
        "keyword": "python developer",
        "country": "US",
        "time_range": "Past month",
        "job_type": "Full-time",
        "experience_level": "Mid-Senior level",
        "remote": "Remote",
        "company": "",
        "location_radius": ""
    }
]

response = requests.post(url, headers=headers, params=params, json=data)
print(response.json())
```

### Indeed Jobs API Request

```python
import requests

url = "https://api.brightdata.com/datasets/v3/trigger"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN_HERE",
    "Content-Type": "application/json",
}
params = {
    "dataset_id": "gd_l4dx9j9sscpvs7no2",  # Indeed dataset
    "include_errors": "true",
    "type": "discover_new",
    "discover_by": "keyword",
}
data = [
    {
        "country": "US",
        "domain": "indeed.com",
        "keyword_search": "data analyst",
        "location": "San Francisco, CA",
        "date_posted": "Last 7 days",
        "posted_by": "",
        "location_radius": ""
    }
]

response = requests.post(url, headers=headers, params=params, json=data)
print(response.json())
```

### Expected Response
```json
{
    "snapshot_id": "abc123...",
    "status": "running"
}
```

Then poll for results:
```python
# Poll endpoint
poll_url = f"https://api.brightdata.com/datasets/v3/snapshots/{snapshot_id}"
response = requests.get(poll_url, headers=headers)
print(response.json())
```

---

## 🔧 Troubleshooting

### Issue 1: "401 Unauthorized"
**Cause:** Invalid or missing API token

**Solutions:**
1. Verify your token in `.env` file
2. Make sure token starts with `Bearer ` (with space)
3. Check if token expired - regenerate from BrightData dashboard
4. Ensure `.env` file is in project root directory

### Issue 2: "Dataset not found"
**Cause:** Incorrect dataset ID

**Solutions:**
1. Verify dataset IDs haven't changed in BrightData
2. Check your BrightData subscription includes LinkedIn/Indeed datasets
3. Ensure you're using the correct API endpoint

### Issue 3: Rate Limiting
**Cause:** Too many requests in short time

**Solutions:**
1. Adjust `BRIGHTDATA_RATE_LIMIT_QPS` in `.env`
2. Add delays between requests
3. Upgrade BrightData plan for higher limits

### Issue 4: No Results Returned
**Cause:** Invalid search parameters or no jobs found

**Solutions:**
1. Verify `keyword`, `location`, and `country` parameters
2. Try broader search terms
3. Check BrightData dashboard for request logs
4. Ensure dataset supports the country you're searching

### Issue 5: Environment Variables Not Loading
**Cause:** `.env` file not found or not loaded

**Solutions:**
```python
# Add this at the top of your script
from dotenv import load_dotenv
load_dotenv()  # Load .env file

import os
print(os.getenv("BRIGHTDATA_API_TOKEN"))  # Should print your token
```

---

## 📞 Support Resources

- **BrightData Documentation:** https://docs.brightdata.com/
- **BrightData Support:** https://brightdata.com/support
- **LinkedIn Dataset Docs:** https://brightdata.com/products/datasets/linkedin
- **Indeed Dataset Docs:** https://brightdata.com/products/datasets/indeed

---

## ✅ Quick Setup Checklist

- [ ] Sign up for BrightData account
- [ ] Get API Token from dashboard
- [ ] Copy `.env.template` to `.env`
- [ ] Add API Token to `.env` file
- [ ] Verify token with test script
- [ ] Run your first scrape!

---

## 🚀 Next Steps

After configuration, you can:

1. **Test the scrapers:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Scrape jobs programmatically:**
   ```python
   from src.scraper.brightdata.clients.linkedin import LinkedInClient
   
   client = LinkedInClient()
   jobs = client.discover_jobs(keyword="Python Developer", location="New York", limit=50)
   print(f"Found {len(jobs)} jobs!")
   ```

3. **Scale to 50,000 jobs:**
   - Use the Streamlit slider to set job count
   - The system will handle pagination automatically

---

**Happy Scraping! 🎉**
