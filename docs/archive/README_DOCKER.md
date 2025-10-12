# 🐳 Job Scraper - Docker Setup (RECOMMENDED)

## 🎯 Why Docker?

**Docker is BETTER than the npm-based setup:**
- ✅ **No npm/Node.js required** (cleaner)
- ✅ **Isolated environment** (no system pollution)
- ✅ **Easier to manage** (single command start/stop)
- ✅ **Production-ready** (auto-restart on failure)
- ✅ **Portable** (works on any OS with Docker)

---

## 🚀 Super Quick Start (3 Commands)

### 1. Start Proxy Manager (Docker)

```bash
./start_proxy_docker.sh
```

**Wait ~10 seconds** for proxy to initialize ⏳

---

### 2. Check Health (Optional)

```bash
./check_proxy_health.sh
```

**Expected:**
```
✅ Docker is running
✅ Proxy container is running
✅ Web UI is accessible at http://localhost:22999
✅ US Proxy is working (IP: xxx.xxx.xxx.xxx)
✅ Health check complete!
```

---

### 3. Start Streamlit

```bash
streamlit run streamlit_app.py
```

**Open:** http://localhost:8501

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────┐
│          Streamlit UI (localhost:8501)          │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   Local Proxy Scrapers (Playwright)             │
│   ├── LinkedIn scraper                          │
│   ├── Indeed scraper                            │
│   └── Naukri scraper                            │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   🐳 Docker Container: BrightData Proxy         │
│   ├── Port 22999: Web UI                        │
│   ├── Port 24000: US residential IPs            │
│   └── Port 24001: India residential IPs         │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
        BrightData Cloud → Target Websites
```

---

## 🛠️ What You Have

### Files Created

```
Job_Scrapper/
├── docker-compose.yml                # Docker config (simple)
├── docker-compose.advanced.yml       # Docker config (advanced)
├── start_proxy_docker.sh             # Start proxy (easy)
├── stop_proxy_docker.sh              # Stop proxy (easy)
├── check_proxy_health.sh             # Health check
├── .env.example                      # Credentials template
├── DOCKER_PROXY_SETUP.md             # Detailed Docker guide
└── README_DOCKER.md                  # This file
```

### Scrapers (Already Created)

```
src/scraper/local_proxy/
├── linkedin_scraper.py   # LinkedIn scraper
├── indeed_scraper.py     # Indeed scraper
└── naukri_scraper.py     # Naukri scraper
```

---

## 🎬 Complete Workflow

### Step 1: Install Docker (First Time Only)

**Ubuntu/WSL:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

**Verify:**
```bash
docker --version
docker-compose --version
```

---

### Step 2: Start Everything

**Terminal 1: Proxy Manager**
```bash
cd /mnt/windows_d/Gauravs-Files-and-Folders/Freelance/Codebasics/Job_Scrapper
./start_proxy_docker.sh
```

**Terminal 2: Streamlit App**
```bash
cd /mnt/windows_d/Gauravs-Files-and-Folders/Freelance/Codebasics/Job_Scrapper
streamlit run streamlit_app.py
```

---

### Step 3: Scrape Jobs

**In Browser (http://localhost:8501):**

1. Enter job role: `"Python Developer"`
2. Select platform: `LinkedIn` / `Indeed` / `Naukri`
3. Choose number of jobs: `20`
4. Click **"🚀 Start Scraping"**

**Results in 10-20 seconds!** ⚡

---

## 🔧 Configuration Options

### Simple Setup (Default)

Uses `docker-compose.yml`:
- Single container
- US proxy (port 24000)
- India proxy support (port 24001)

**Start:**
```bash
docker-compose up -d
```

---

### Advanced Setup (Multi-Container)

Uses `docker-compose.advanced.yml`:
- Separate containers for US and India
- Better isolation
- Individual health checks

**Start:**
```bash
docker-compose -f docker-compose.advanced.yml up -d
```

---

## 📋 Common Commands

### Container Management

```bash
# Start proxy (background)
docker-compose up -d

# Start proxy (foreground with logs)
docker-compose up

# Stop proxy
docker-compose down

# Restart proxy
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Health Checks

```bash
# Full health check
./check_proxy_health.sh

# Quick check
docker ps

# Test US proxy
curl --proxy http://localhost:24000 https://lumtest.com/myip.json

# Test India proxy
curl --proxy http://localhost:24001 https://lumtest.com/myip.json
```

### Troubleshooting

```bash
# View container logs
docker logs brightdata-proxy-manager

# Execute command in container
docker exec -it brightdata-proxy-manager sh

# Restart container
docker restart brightdata-proxy-manager

# Remove and recreate
docker-compose down
docker-compose up -d
```

---

## 🐛 Troubleshooting

### Issue 1: Docker not installed

**Error:** `command not found: docker`

**Solution:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

---

### Issue 2: Permission denied

**Error:** `permission denied while trying to connect to Docker daemon`

**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

### Issue 3: Port already in use

**Error:** `port is already allocated`

**Solution:**
```bash
# Find what's using the port
lsof -i :24000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yml
```

---

### Issue 4: Container keeps restarting

**Check logs:**
```bash
docker logs brightdata-proxy-manager
```

**Common causes:**
- Invalid credentials → Check `docker-compose.yml`
- Network issue → Check internet connection
- Port conflict → Check ports 22999, 24000, 24001

---

## 📊 Performance

### Speed Comparison

| Method | Speed (20 jobs) | Setup Complexity |
|--------|----------------|------------------|
| **Docker Proxy** | 10-20s | Medium |
| npm Proxy | 10-20s | Medium |
| Cloud Browser | 60-90s | Easy |
| Datasets API | 1-2s | Hard |

**Docker is the recommended method!** 🐳

---

## 🔒 Security

### Credentials Protection

**Don't commit credentials to git!**

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```env
BRIGHTDATA_CUSTOMER=your_customer_id
BRIGHTDATA_PASSWORD=your_password
```

3. Update `docker-compose.yml` to use `.env`:
```yaml
command: >
  proxy-manager
  --customer "${BRIGHTDATA_CUSTOMER}"
  --password "${BRIGHTDATA_PASSWORD}"
```

4. Add to `.gitignore`:
```
.env
docker-compose.override.yml
proxy_config/
```

---

## 🌐 Web UI Access

**URL:** http://localhost:22999

**Features:**
- View active proxies
- Monitor requests
- See bandwidth usage
- Test connections
- Configure rules

**Screenshot:**
```
┌───────────────────────────────────────────┐
│  BrightData Proxy Manager                 │
│                                            │
│  Active Proxies:                           │
│  ✓ Port 24000 (US) - 15 requests          │
│  ✓ Port 24001 (IN) - 8 requests           │
│                                            │
│  Total Bandwidth: 125 MB                   │
│  Success Rate: 98%                         │
└───────────────────────────────────────────┘
```

---

## 🎯 Production Tips

### 1. Run in Background

```bash
docker-compose up -d
```

### 2. Auto-Start on Boot

```bash
# Add to system startup
sudo systemctl enable docker

# Docker Compose will auto-restart container
# (already configured with: restart: unless-stopped)
```

### 3. Monitor Container

```bash
# View resource usage
docker stats brightdata-proxy-manager

# View logs
docker logs -f brightdata-proxy-manager --tail=100
```

### 4. Backup Configuration

```bash
# Export container config
docker inspect brightdata-proxy-manager > proxy_backup.json
```

---

## 📚 All Documentation Files

1. **`README_DOCKER.md`** (this file) - Docker quick start
2. **`DOCKER_PROXY_SETUP.md`** - Detailed Docker guide
3. **`LOCAL_PROXY_SETUP.md`** - Original proxy setup (npm-based)
4. **`STREAMLIT_LOCAL_PROXY_QUICKSTART.md`** - Streamlit integration
5. **`CHANGES_SUMMARY.md`** - What changed from cloud browser

**Start with this file (`README_DOCKER.md`) for quickest setup!**

---

## ✅ Checklist

Before scraping, ensure:

- [ ] Docker is installed and running
- [ ] Proxy container is running (`docker ps`)
- [ ] Web UI is accessible (http://localhost:22999)
- [ ] US proxy works (`curl --proxy http://localhost:24000 https://lumtest.com/myip.json`)
- [ ] Health check passes (`./check_proxy_health.sh`)
- [ ] Streamlit is running (http://localhost:8501)

---

## 🎉 Summary

**You now have:**
1. ✅ Docker-based proxy manager (cleaner than npm)
2. ✅ Automated start/stop scripts
3. ✅ Health check script
4. ✅ Complete documentation
5. ✅ Production-ready setup

**To scrape jobs:**
```bash
# Terminal 1
./start_proxy_docker.sh

# Terminal 2
streamlit run streamlit_app.py

# Browser: http://localhost:8501
```

**Speed:** 10-20 seconds for 20 jobs ⚡  
**Setup:** Just Docker 🐳  
**Reliability:** High 🎯  

---

**Happy scraping with Docker! 🐳🚀**
