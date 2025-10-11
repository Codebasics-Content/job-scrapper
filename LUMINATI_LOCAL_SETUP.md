# 🚀 Luminati Proxy Manager - Free Local Setup

## Overview

The **Luminati Proxy Manager** is a **FREE** local application that connects to BrightData's residential proxy network. You only pay for the bandwidth you use, not for the proxy manager software itself.

---

## ✅ Installation (Native - Recommended)

### Step 1: Install Node.js (Required)

```bash
# Check if Node.js is installed
node --version

# If not installed:
# Ubuntu/Debian
sudo apt update && sudo apt install -y nodejs npm

# Or download from: https://nodejs.org/
```

### Step 2: Install Luminati Proxy Manager

```bash
# Install globally via npm (FREE)
sudo npm install -g @luminati-io/luminati-proxy

# Verify installation
luminati-proxy --version
```

---

## 🔧 Configuration

### Your BrightData Credentials

From your `.env` file:
```bash
BRIGHTDATA_CUSTOMER_ID=hl_864cf5cf
BRIGHTDATA_ZONE=residential
BRIGHTDATA_PASSWORD=bdx2gk7k5euj
```

---

## 🚀 Start Luminati Proxy Manager

### Option 1: Quick Start (Single Port)

```bash
# Start US residential proxy on port 24000
luminati-proxy \
  --customer hl_864cf5cf \
  --zone residential \
  --password bdx2gk7k5euj \
  --port 24000 \
  --country us \
  --www 22999

# Web UI: http://localhost:22999
```

### Option 2: Multi-Port Setup (US + India)

Use the provided config file:

```bash
# Start with config file
luminati-proxy --config proxy_manager_config.json --www 22999
```

---

## 📋 Verify Setup

### Test Proxy Endpoints

```bash
# Test US proxy (port 24000)
curl -x http://hl_864cf5cf-zone-residential-country-us:bdx2gk7k5euj@localhost:24000 \
  https://lumtest.com/myip.json

# Test India proxy (port 24001)  
curl -x http://hl_864cf5cf-zone-residential-country-in:bdx2gk7k5euj@localhost:24001 \
  https://lumtest.com/myip.json

# Check Web UI
curl http://localhost:22999
```

---

## 🐳 Docker Services

### Start HeadlessX (Chrome Rendering)

```bash
# Start HeadlessX only
docker compose up -d

# HeadlessX will use host proxy at http://host.docker.internal:24000
```

### Architecture

```
┌─────────────────────────────────────┐
│   Docker: HeadlessX (Port 3000)     │
│   Chrome rendering with proxy       │
└────────────┬────────────────────────┘
             │ Uses host proxy
             ↓
┌─────────────────────────────────────┐
│   Host: Luminati Proxy Manager      │
│   Ports: 24000 (US), 24001 (India)  │
│   Web UI: 22999                      │
└────────────┬────────────────────────┘
             │ Connects to
             ↓
┌─────────────────────────────────────┐
│   BrightData Cloud Network          │
│   Residential IPs (150+ countries)  │
└─────────────────────────────────────┘
```

---

## 💰 Cost Breakdown

### Free Components
✅ **Luminati Proxy Manager** - FREE software  
✅ **HeadlessX (Docker)** - FREE browser automation  
✅ **Job Scraper Code** - FREE (yours)

### Paid Components
💵 **BrightData Bandwidth** - Pay only for what you use  
   - Typical: $0.001 - $0.01 per request  
   - 100 jobs ≈ $0.10 - $1.00  
   - Much cheaper than cloud browsers

---

## 🔄 Integration with Job Scraper

### Update Scraper Configuration

Your scrapers will automatically use the local proxy:

```python
# In src/scraper/services/headlessx_client.py
# HeadlessX forwards requests through local Luminati proxy
async with HeadlessXClient() as client:
    html = await client.render_url(
        url,
        proxy_url="http://host.docker.internal:24000"  # Auto-configured
    )
```

---

## 🛠️ Troubleshooting

### Luminati Not Starting

```bash
# Check if port is in use
lsof -i :24000

# Kill existing process
kill -9 $(lsof -t -i:24000)

# Restart
luminati-proxy --config proxy_manager_config.json --www 22999
```

### Connection Errors

```bash
# Test credentials
curl -x http://hl_864cf5cf-zone-residential:bdx2gk7k5euj@brd.superproxy.io:22225 \
  https://lumtest.com/myip.json

# Check BrightData dashboard
open https://brightdata.com/cp/zones
```

### Docker Can't Connect to Host Proxy

```bash
# Verify host.docker.internal works
docker run --rm curlimages/curl:latest \
  curl http://host.docker.internal:22999

# If fails, use your actual local IP
docker run --rm curlimages/curl:latest \
  curl http://192.168.x.x:24000
```

---

## 📚 Next Steps

1. **Install Luminati**: `sudo npm install -g @luminati-io/luminati-proxy`
2. **Start Proxy Manager**: `luminati-proxy --config proxy_manager_config.json --www 22999`
3. **Start HeadlessX**: `docker compose up -d`
4. **Run Integration Tests**: `python tests/run_integration_tests.py`

---

## 🔗 Resources

- **Luminati Docs**: https://docs.brightdata.com/proxy-networks/proxy-manager/introduction
- **BrightData Dashboard**: https://brightdata.com/cp/zones
- **Cost Calculator**: https://brightdata.com/pricing/residential-proxies

---

**Status**: HeadlessX running ✅ | Luminati needs native installation 📦
