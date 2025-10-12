# 🚀 Quick Start: BrightData Proxy Scraping

## ✅ What You Need

1. **BrightData Account** with proxy zone configured
2. **3 Environment Variables** in `.env`:
   ```bash
   BRIGHTDATA_CUSTOMER_ID=hl_xxxxxxx
   BRIGHTDATA_ZONE=residential
   BRIGHTDATA_PASSWORD=your_zone_password
   ```
3. **Install Dependencies**:
   ```bash
   pip install httpx beautifulsoup4 lxml
   ```

---

## 🎯 Usage (3 Simple Steps)

### Step 1: Configure .env

Copy `.env.example` to `.env` and add your BrightData proxy credentials:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

### Step 2: Test Connection

```bash
python3 src/scraper/proxy/config.py
```

Expected output:
```
✅ Proxy config loaded successfully
   Customer ID: hl_xxxxxxx
   ...
```

### Step 3: Run Scrapers

**LinkedIn:**
```bash
python3 src/scraper/proxy/linkedin_scraper.py
```

**Indeed:**
```bash
python3 src/scraper/proxy/indeed_scraper.py
```

**Naukri:**
```bash
python3 src/scraper/proxy/naukri_scraper.py
```

---

## 💡 In Your Code

```python
import asyncio
from src.scraper.proxy.linkedin_scraper import scrape_linkedin_jobs

async def main():
    # That's it! Auto-loads from .env
    jobs = await scrape_linkedin_jobs(
        keyword="Python Developer",
        location="United States",
        limit=50
    )
    
    print(f"✅ Scraped {len(jobs)} jobs with skills")
    for job in jobs[:3]:
        print(f"- {job.Job_Role} at {job.Company}")
        print(f"  Skills: {', '.join(job.skills_list[:5])}")

asyncio.run(main())
```

---

## 📊 What Gets Extracted

Each job includes:
- ✅ **URL** - Direct link to job posting
- ✅ **Job Description** - Full text (for skills extraction)
- ✅ **Skills List** - Extracted from description (20,000+ skill database)
- ✅ **Company, Role, Location, Experience**

**Focus:** Only what's needed for skill trend analysis!

---

## ⚡ Why Proxy > Scraping Browser?

| Feature | Proxy Method | Scraping Browser |
|---------|-------------|------------------|
| **Speed** | 20-30s for 20 jobs | 60-90s for 20 jobs |
| **Setup** | 3 env vars | Browser URL + CDP |
| **Code** | Simple HTTP | Complex browser automation |
| **Cost** | Proxy credits ($) | Browser credits ($$) |
| **Maintenance** | Low | Medium |

**Result: 3x faster, simpler, cheaper!** 🚀

---

## 🌍 Geo-Targeting (Optional)

Target specific countries for better results:

```python
from src.scraper.proxy.config import BrightDataProxy
from src.scraper.proxy.linkedin_scraper import scrape_linkedin_jobs

proxy = BrightDataProxy.from_env()
proxy = proxy.with_country("us")  # US IPs

jobs = await scrape_linkedin_jobs(keyword="Python Dev", proxy=proxy)
```

**Available:** `us`, `in`, `gb`, `ca`, `au`, and 150+ countries

---

## 🔄 Sticky Sessions (Optional)

Use same IP for all requests (recommended for multi-page scraping):

```python
proxy = BrightDataProxy.from_env()
proxy = proxy.with_session()  # Auto-generates session ID

# Now all requests use the same IP
```

---

## 🚨 Troubleshooting

### ❌ "Missing required BrightData credentials"
**Fix:** Add to `.env`:
```bash
BRIGHTDATA_CUSTOMER_ID=hl_xxxxxxx
BRIGHTDATA_ZONE=residential  
BRIGHTDATA_PASSWORD=your_password
```

### ❌ "Proxy authentication failed"
**Fix:** 
1. Verify credentials in BrightData dashboard
2. Check zone is active and has bandwidth
3. Ensure customer ID matches your account

### ❌ "No job cards found"
**Fix:**
1. Site HTML may have changed - check selectors
2. Add delay: `await asyncio.sleep(2)`
3. Try residential proxies
4. Add geo-targeting: `proxy.with_country("us")`

---

## 📚 Full Documentation

See [`PROXY_SCRAPING_GUIDE.md`](PROXY_SCRAPING_GUIDE.md) for:
- Complete setup instructions
- Advanced configuration
- Scaling strategies
- Cost optimization tips
- All troubleshooting scenarios

---

## 🎯 Next Steps

1. ✅ Configure `.env` with BrightData proxy credentials
2. ✅ Test connection: `python3 src/scraper/proxy/config.py`
3. ✅ Test scrapers individually
4. ✅ Integrate into Streamlit app
5. ✅ Monitor bandwidth in BrightData dashboard

---

**Ready to scrape! 🚀**

Need help? Check the [full guide](PROXY_SCRAPING_GUIDE.md) or BrightData [docs](https://docs.brightdata.com/proxy-networks/proxy-manager/introduction).
