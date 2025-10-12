# 🚀 BrightData Proxy Scraping - Complete Guide

## 📋 Overview

This guide explains how to use **BrightData Proxies** for job scraping instead of the heavier Scraping Browser approach. This method is:

✅ **Much Faster** - Direct HTTP requests vs CDP (Chrome DevTools Protocol)  
✅ **Simpler** - No browser automation complexity  
✅ **Cost-Effective** - Proxy credits vs Scraping Browser credits  
✅ **Scalable** - Easy to parallelize and scale  
✅ **Focused** - Extract only: URL, Job Description, Skills  

---

## 🏗️ Architecture

```
User Query → Proxy-Based Scrapers → BrightData Proxy Network
                 ↓
    LinkedIn / Indeed / Naukri (HTML fetch)
                 ↓
        BeautifulSoup Parser
                 ↓
         Skills Extraction
                 ↓
       SQLite Database
                 ↓
    Streamlit Analytics Dashboard
```

**Key Components:**
1. **BrightDataProxy** - Configuration class with session & geo-targeting
2. **ProxySession** - HTTP client with automatic retry logic
3. **Platform Scrapers** - LinkedIn, Indeed, Naukri specific parsers
4. **SkillsParser** - Existing 20,000+ skills extraction

---

## 🔧 Setup Instructions

### Step 1: Get BrightData Proxy Credentials

1. Log in to [BrightData Dashboard](https://bright data.com)
2. Navigate to **"Proxies & Scraping Infrastructure"** → **"Proxy Products"**
3. Create a new **Proxy Zone** (Residential, Datacenter, ISP, or Mobile)
4. Note down these values:
   - **Customer ID**: `hl_xxxxxxx`
   - **Zone Name**: Your zone name (e.g., `residential`, `datacenter1`)
   - **Password**: Zone password

### Step 2: Configure Environment Variables

Update your `.env` file with BrightData proxy credentials:

```bash
# BrightData Proxy Configuration (Required for new proxy-based scraping)
BRIGHTDATA_CUSTOMER_ID=hl_xxxxxxx
BRIGHTDATA_ZONE=residential
BRIGHTDATA_PASSWORD=your_zone_password_here

# Optional: Custom proxy host/port (defaults shown)
BRIGHTDATA_PROXY_HOST=brd.superproxy.io
BRIGHTDATA_PROXY_PORT=22225
```

### Step 3: Install Dependencies

Add these to `requirements.txt` if not already present:

```bash
httpx>=0.25.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

Install:

```bash
pip install httpx beautifulsoup4 lxml
```

---

## 💡 Usage Examples

### Example 1: Scrape LinkedIn Jobs

```python
import asyncio
from src.scraper.proxy.linkedin_scraper import scrape_linkedin_jobs

async def main():
    jobs = await scrape_linkedin_jobs(
        keyword="Machine Learning Engineer",
        location="United States",
        limit=50
    )
    
    print(f"Scraped {len(jobs)} jobs")
    for job in jobs[:5]:
        print(f"- {job.Job_Role} at {job.Company}")
        print(f"  Skills: {', '.join(job.skills_list[:5])}")

asyncio.run(main())
```

### Example 2: Scrape Indeed Jobs

```python
from src.scraper.proxy.indeed_scraper import scrape_indeed_jobs

async def main():
    jobs = await scrape_indeed_jobs(
        query="Data Scientist",
        location="Seattle, WA",
        limit=30
    )
    
    print(f"Scraped {len(jobs)} jobs")

asyncio.run(main())
```

### Example 3: Scrape Naukri Jobs (India)

```python
from src.scraper.proxy.naukri_scraper import scrape_naukri_jobs

async def main():
    jobs = await scrape_naukri_jobs(
        keyword="Python Developer",
        location="Bangalore",
        limit=25
    )
    
    print(f"Scraped {len(jobs)} jobs")

asyncio.run(main())
```

### Example 4: Custom Proxy Configuration

```python
from src.scraper.proxy.config import BrightDataProxy
from src.scraper.proxy.linkedin_scraper import scrape_linkedin_jobs

async def main():
    # Create custom proxy with specific settings
    proxy = BrightDataProxy(
        customer_id="hl_xxxxxxx",
        zone_name="residential",
        password="your_password"
    )
    
    # Add session for sticky IP (same IP for all requests)
    proxy = proxy.with_session()
    
    # Add geo-targeting
    proxy = proxy.with_country("us")  # US residential IPs
    
    # Use in scraper
    jobs = await scrape_linkedin_jobs(
        keyword="DevOps Engineer",
        location="San Francisco",
        limit=20,
        proxy=proxy
    )

asyncio.run(main())
```

---

## 🌍 Geo-Targeting

BrightData proxies support geo-targeting for better results:

```python
# Target US IPs for US job sites
proxy = proxy.with_country("us")

# Target India IPs for Naukri
proxy = proxy.with_country("in")

# Target UK IPs
proxy = proxy.with_country("gb")
```

**Available Countries:** 
- `us` - United States
- `in` - India
- `gb` - United Kingdom
- `ca` - Canada
- `au` - Australia
- And 150+ more countries...

---

## 🔄 Session Management (Sticky IPs)

Use sessions to maintain the same IP across multiple requests:

```python
# Without session - IP rotates on each request
proxy = BrightDataProxy.from_env()

# With session - Same IP for all requests in this session
proxy = proxy.with_session()  # Auto-generates UUID
proxy = proxy.with_session("my-custom-session-id")  # Custom ID
```

**When to use sessions:**
- When scraping requires multiple requests to the same site
- To avoid being flagged for IP hopping
- For maintaining cookie-based sessions

---

## ⚡ Performance Comparison

| Method | Speed (20 jobs) | Setup Complexity | Maintenance |
|--------|----------------|------------------|-------------|
| **Scraping Browser** | 60-90s | High (CDP, Browser mgmt) | Medium |
| **Proxy + HTTP** | 20-30s | Low (HTTP only) | Low |

**Proxy scraping is 3x faster!** ⚡

---

## 📊 BrightData Proxy Types

| Proxy Type | Use Case | Cost | Speed |
|------------|----------|------|-------|
| **Residential** | Highest success rate, looks like real users | $$$ | Medium |
| **Datacenter** | Fast, cost-effective for easy targets | $ | Fast |
| **ISP** | Balance of residential trust + datacenter speed | $$ | Fast |
| **Mobile** | Mobile-specific sites, highest trust | $$$$ | Slow |

**Recommendation for job scraping:** Start with **Datacenter** (cheapest), upgrade to **Residential** if blocked.

---

##  🧪 Testing Your Setup

### Test 1: Verify Environment Variables

```bash
python3 -c "
from src.scraper.proxy.config import BrightDataProxy

try:
    proxy = BrightDataProxy.from_env()
    print('✅ Proxy config loaded successfully')
    print(f'   Customer ID: {proxy.customer_id}')
    print(f'   Zone: {proxy.zone_name}')
    print(f'   Host: {proxy.host}:{proxy.port}')
    print(f'   Proxy URL: {proxy.url[:50]}...')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Test 2: Test Proxy Connection

```bash
python3 src/scraper/proxy/config.py
```

Expected output:
```
Testing Proxy Configuration...
Proxy URL: http://brd-customer-xxx-zone-residential...
...
Testing Proxy Session...
Response: 200
IP: {'origin': 'xxx.xxx.xxx.xxx'}
```

### Test 3: Test LinkedIn Scraper

```bash
python3 src/scraper/proxy/linkedin_scraper.py
```

### Test 4: Test Indeed Scraper

```bash
python3 src/scraper/proxy/indeed_scraper.py
```

### Test 5: Test Naukri Scraper

```bash
python3 src/scraper/proxy/naukri_scraper.py
```

---

## 🚨 Troubleshooting

### Error: "Missing required BrightData credentials"

**Solution:** Ensure `.env` file has:
```bash
BRIGHTDATA_CUSTOMER_ID=hl_xxxxxxx
BRIGHTDATA_ZONE=residential
BRIGHTDATA_PASSWORD=your_password
```

### Error: "Proxy authentication failed"

**Solutions:**
1. Verify password is correct in BrightData dashboard
2. Check if zone is active and has available bandwidth
3. Ensure customer ID matches your account

### Error: "No job cards found"

**Solutions:**
1. Site may have changed HTML structure - update selectors
2. Try adding delay between requests: `await asyncio.sleep(2)`
3. Switch to residential proxies for better trust
4. Add geo-targeting: `proxy.with_country("us")`

### Error: "Connection timeout"

**Solutions:**
1. Increase timeout: `ProxySession(timeout=60.0)`
2. Check BrightData dashboard for service status
3. Verify you have bandwidth available

---

## 📈 Scaling Tips

### 1. Parallel Scraping

```python
import asyncio
from src.scraper.proxy.linkedin_scraper import scrape_linkedin_jobs

async def scrape_multiple_keywords():
    keywords = ["Python Developer", "Data Scientist", "ML Engineer"]
    
    tasks = [
        scrape_linkedin_jobs(keyword, limit=50)
        for keyword in keywords
    ]
    
    results = await asyncio.gather(*tasks)
    
    total_jobs = sum(len(jobs) for jobs in results)
    print(f"Total jobs scraped: {total_jobs}")

asyncio.run(scrape_multiple_keywords())
```

### 2. Multiple Sessions

```python
# Create unique session per scraping task
proxy1 = proxy.with_session(f"task-1-{uuid.uuid4()}")
proxy2 = proxy.with_session(f"task-2-{uuid.uuid4()}")
```

### 3. Batch Processing

```python
# Process jobs in batches to avoid memory issues
for i in range(0, 1000, 50):
    jobs = await scrape_linkedin_jobs(keyword="Python", limit=50)
    save_to_database(jobs)
    await asyncio.sleep(5)  # Cool down between batches
```

---

## 💰 Cost Optimization

1. **Use Datacenter proxies** for initial testing (cheapest)
2. **Enable sessions** to reduce IP rotations
3. **Cache results** to avoid re-scraping same jobs
4. **Rate limit** to avoid burning credits unnecessarily
5. **Monitor bandwidth** in BrightData dashboard

---

## 🔐 Best Practices

1. ✅ Always use sessions for multi-page scraping
2. ✅ Add delays between requests (1-2 seconds)
3. ✅ Use geo-targeting for better success rates
4. ✅ Implement retry logic (already built-in)
5. ✅ Monitor proxy bandwidth usage
6. ✅ Rotate session IDs for different scraping tasks
7. ✅ Handle errors gracefully and log failures

---

## 📚 Additional Resources

- [BrightData Proxy Documentation](https://docs.brightdata.com/proxy-networks/proxy-manager/introduction)
- [BrightData Dashboard](https://brightdata.com/cp/zones)
- [Proxy Configuration Guide](https://docs.brightdata.com/proxy-networks/proxy-manager/configuration)

---

## 🎯 Next Steps

1. Configure `.env` with your BrightData credentials
2. Test connection with `python3 src/scraper/proxy/config.py`
3. Run individual scrapers to verify they work
4. Integrate into your Streamlit app (replace Scraping Browser calls)
5. Monitor bandwidth usage and optimize

---

## 📞 Support

For BrightData-specific issues:
- Check [BrightData Status Page](https://status.brightdata.com/)
- Contact BrightData Support via dashboard
- Review [Proxy Manager FAQs](https://docs.brightdata.com/proxy-networks/proxy-manager/faqs)

For scraper code issues:
- Check HTML selectors may have changed
- Verify proxy credentials in `.env`
- Review error logs for specific failures

---

**Ready to scrape! 🚀**
