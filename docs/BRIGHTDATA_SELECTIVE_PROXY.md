# BrightData Selective Proxy Usage Guide

## Strategy: 3 Platforms - Proxy Only for LinkedIn

**Supported Platforms**: LinkedIn (proxy), Indeed (direct), Naukri (direct)

**Cost Optimization**: Use BrightData proxy **only for LinkedIn** (rate-limited platform), keep Indeed + Naukri proxy-free (unlimited).

---

## Configuration

### 1. Environment Variables

Add to `.env`:

```bash
# BrightData WebSocket proxy for LinkedIn
BRIGHTDATA_BROWSER_URL=wss://brd-customer-{YOUR_ID}-zone-{ZONE}:{PASSWORD}@brd.superproxy.io:9222
```

**Get your credentials from**: BrightData dashboard → Proxy & Scraping Infrastructure → Browser

---

## Usage

### Option 1: Multi-Platform Scraper (Recommended)

```python
from src.scraper.jobspy import scrape_multi_platform

# Automatically uses proxy for LinkedIn, none for Indeed/Naukri
jobs = scrape_multi_platform(
    platforms=["linkedin", "indeed", "naukri"],
    search_term="AI Engineer",
    location="United States",
    results_wanted=500,
    linkedin_fetch_description=True
)

# Output:
# 🔍 Scraping LINKEDIN...
#    🌐 Using BrightData proxy
#    ✅ Found 500 jobs
#
# 🔍 Scraping INDEED...
#    🆓 Free scraping (no proxy)
#    ✅ Found 500 jobs
#
# 🔍 Scraping NAUKRI...
#    🆓 Free scraping (no proxy)
#    ✅ Found 500 jobs
```

### Option 2: Manual Control

```python
from python_jobspy import scrape_jobs
from src.scraper.jobspy import get_proxy_for_platform

# LinkedIn with proxy
linkedin_proxy = get_proxy_for_platform("linkedin")
linkedin_jobs = scrape_jobs(
    site_name=["linkedin"],
    search_term="AI Engineer",
    results_wanted=1000,
    proxies=linkedin_proxy  # BrightData proxy
)

# Indeed without proxy
indeed_jobs = scrape_jobs(
    site_name=["indeed"],
    search_term="AI Engineer",
    results_wanted=1000,
    proxies=None  # Free, unlimited
)

# Naukri without proxy
naukri_jobs = scrape_jobs(
    site_name=["naukri"],
    search_term="AI Engineer",
    results_wanted=1000,
    proxies=None  # Free, unlimited + native skills!
)
```

---

## Check Proxy Status

```python
from src.scraper.jobspy import proxy_status

status = proxy_status()
print(status)

# Output:
# {
#     "linkedin": True,         # Proxy configured
#     "indeed": False,          # Direct scraping (unlimited)
#     "naukri": False,          # Direct scraping (unlimited + native skills)
#     "brightdata_configured": True
# }
```

---

## Platform Proxy Requirements

| Platform | Proxy Required? | Reason | Cost |
|----------|----------------|--------|------|
| **LinkedIn** | ✅ Yes (for >100 jobs) | Aggressive rate limiting (~10 pages per IP) | BrightData |
| **Indeed** | ❌ No | No rate limiting, unlimited scraping | $0 |
| **Naukri** | ❌ No | Direct scraping, native skills field | $0 |

---

## Cost Analysis

### Without Selective Proxy (All platforms proxied)
- **LinkedIn**: $15/GB BrightData
- **Indeed**: $15/GB BrightData (WASTED - no rate limits)
- **Naukri**: $15/GB BrightData (WASTED - free-tier works)
- **Total**: ~$45/month for 10,000 jobs

### With Selective Proxy (LinkedIn only)
- **LinkedIn**: $15/GB BrightData
- **Indeed**: $0 (no proxy)
- **Naukri**: $0 (no proxy)
- **Total**: ~$15/month for 10,000 jobs
- **Savings**: $30/month (66% reduction)

---

## Scale Estimates

### Free Tier (No Proxy)
- **Indeed**: 10,000+ jobs/day
- **Naukri**: 10,000+ jobs/day
- **LinkedIn**: 100 jobs/day (without proxy)
- **Total**: 20,100 jobs/day

### With LinkedIn Proxy
- **Indeed**: 10,000+ jobs/day (free)
- **Naukri**: 10,000+ jobs/day (free)
- **LinkedIn**: 50,000+ jobs/day (with BrightData)
- **Total**: 70,000+ jobs/day
- **Cost**: ~$15/month

---

## Implementation Files

- **`proxy_config.py`** - Manages BrightData proxy configuration
- **`multi_platform_scraper.py`** - Multi-platform scraper with selective proxy logic
- **`__init__.py`** - Exports scraper functions

---

## Example: Streamlit Integration

```python
import streamlit as st
from src.scraper.jobspy import scrape_multi_platform, proxy_status

# Check proxy status
st.sidebar.header("Proxy Status")
status = proxy_status()
if status["linkedin"]:
    st.sidebar.success("✅ LinkedIn proxy configured")
else:
    st.sidebar.warning("⚠️ LinkedIn proxy not configured (100 jobs limit)")

# Scrape with selective proxy
platforms = st.multiselect(
    "Platforms",
    ["linkedin", "indeed", "naukri"],
    default=["indeed", "naukri"]  # Default to free platforms
)

if st.button("Scrape Jobs"):
    with st.spinner("Scraping..."):
        jobs = scrape_multi_platform(
            platforms=platforms,
            search_term=st.text_input("Search Term"),
            results_wanted=st.number_input("Jobs per platform", value=500)
        )
        st.success(f"Scraped {len(jobs)} jobs!")
        st.dataframe(jobs)
```

---

## Troubleshooting

### Proxy Not Working
```python
import os
proxy = os.getenv("BRIGHTDATA_BROWSER_URL")
if not proxy:
    print("❌ BRIGHTDATA_BROWSER_URL not set in .env")
elif not proxy.startswith("wss://brd-customer-"):
    print("❌ Invalid proxy format")
else:
    print(f"✅ Proxy configured: {proxy[:30]}...")
```

### Testing Proxy
```python
from src.scraper.jobspy import scrape_multi_platform

# Test LinkedIn with proxy
jobs = scrape_multi_platform(
    platforms=["linkedin"],
    search_term="test",
    results_wanted=10
)

if len(jobs) > 0:
    print("✅ Proxy working!")
else:
    print("❌ Proxy failed or no results")
```

---

## Best Practices

1. **Use Indeed + Naukri for bulk scraping** (free, unlimited)
2. **Use LinkedIn only when needed** (premium roles, full descriptions)
3. **Monitor BrightData usage** to avoid surprise bills
4. **Keep BRIGHTDATA_BROWSER_URL in .env** (never commit to git)
5. **Test without proxy first** to ensure setup is correct

---

## Summary

**Selective proxy usage = 66% cost savings while maintaining 70,000+ jobs/day capacity.**

- LinkedIn: Proxy (needed for scale)
- Indeed: No proxy (unlimited free)
- Naukri: No proxy (unlimited free + native skills!)
