# 🐳 Docker-Based Proxy Setup - Complete Guide

## 🎯 What This Does

**Run BrightData Proxy Manager in Docker container:**
- ✅ **Isolated environment** (no npm dependencies)
- ✅ **Easy to start/stop** (one command)
- ✅ **Portable** (works on any system with Docker)
- ✅ **Production-ready** (automatic restarts)
- ✅ **Clean setup** (no system pollution)

**Speed:** Same as before (10-20s for 20 jobs) ⚡  
**Setup:** Easier! Just Docker 🐳

---

## 📦 Prerequisites

### Install Docker

**Ubuntu/WSL:**
```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (no sudo needed)
sudo usermod -aG docker $USER

# Apply group changes (logout/login or run)
newgrp docker

# Install Docker Compose (if not included)
sudo apt-get install docker-compose-plugin

# Verify installation
docker --version
docker-compose --version
```

**For Windows (native Docker Desktop):**
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify: Open terminal and run `docker --version`

---

## 🚀 Quick Start (3 Methods)

### Method 1: Docker Compose (Recommended)

**Start proxy manager:**
```bash
cd /mnt/windows_d/Gauravs-Files-and-Folders/Freelance/Codebasics/Job_Scrapper

# Start in foreground (see logs)
docker-compose up

# OR start in background (detached mode)
docker-compose up -d
```

**Stop proxy manager:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

---

### Method 2: Using Scripts (Easiest)

**Start:**
```bash
./start_proxy_docker.sh
```

**Stop** (Ctrl+C or in another terminal):
```bash
./stop_proxy_docker.sh
```

---

### Method 3: Docker Run (Manual)

**Start:**
```bash
docker run -d \
  --name brightdata-proxy-manager \
  -p 22999:22999 \
  -p 24000:24000 \
  -p 24001:24001 \
  luminati/luminati-proxy:latest \
  proxy-manager \
  --www_whitelist_ips "0.0.0.0/0" \
  --ssl true \
  --customer "hl_864cf5cf" \
  --zone "residential" \
  --password "bdx2gk7k5euj" \
  --port 24000 \
  --country "us" \
  --session true
```

**Stop:**
```bash
docker stop brightdata-proxy-manager
docker rm brightdata-proxy-manager
```

---

## 🔧 Configuration

### Simple Setup (docker-compose.yml)

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  brightdata-proxy:
    image: luminati/luminati-proxy:latest
    container_name: brightdata-proxy-manager
    command: >
      proxy-manager
      --www_whitelist_ips "0.0.0.0/0"
      --ssl true
      --customer "hl_864cf5cf"
      --zone "residential"
      --password "bdx2gk7k5euj"
      --port 24000
      --country "us"
      --session true
    ports:
      - "22999:22999"  # Web UI & API
      - "24000:24000"  # US residential proxy
      - "24001:24001"  # India residential proxy
    restart: unless-stopped
```

**Ports:**
- **22999** → Web UI & API
- **24000** → US residential IPs (LinkedIn, Indeed)
- **24001** → India residential IPs (Naukri)

---

### Advanced Setup (Multiple Proxies)

**File:** `docker-compose.advanced.yml`

Run separate containers for US and India:

```bash
docker-compose -f docker-compose.advanced.yml up -d
```

This creates:
- `brightdata-proxy-us` → Port 24000 (US IPs)
- `brightdata-proxy-in` → Port 24001 (India IPs)

---

## ✅ Verify Setup

### 1. Check Container Status

```bash
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE                          STATUS         PORTS
abc123def456   luminati/luminati-proxy:latest Up 2 minutes   0.0.0.0:22999->22999/tcp, 0.0.0.0:24000->24000/tcp
```

### 2. Test Web UI

Open browser: http://localhost:22999

You should see BrightData Proxy Manager dashboard.

### 3. Test Proxy Connection

**US Proxy (port 24000):**
```bash
curl --proxy http://localhost:24000 https://lumtest.com/myip.json
```

**Expected:** US IP address

**India Proxy (port 24001):**
```bash
curl --proxy http://localhost:24001 https://lumtest.com/myip.json
```

**Expected:** India IP address

---

## 🎬 Using with Streamlit

Once Docker proxy is running, use Streamlit **exactly as before**:

### Terminal 1: Start Proxy (Docker)
```bash
./start_proxy_docker.sh
```

### Terminal 2: Start Streamlit
```bash
streamlit run streamlit_app.py
```

### Browser
Open http://localhost:8501

**That's it!** Your scrapers will automatically use the Docker proxy. ✅

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Docker daemon"

**Cause:** Docker not running

**Solution:**
```bash
# Start Docker daemon
sudo systemctl start docker

# Or for Docker Desktop (Windows)
# Start Docker Desktop app
```

### Error: "Port 24000 already in use"

**Cause:** Another service using port 24000

**Solution:**
```bash
# Find process using port
lsof -i :24000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "24002:24000"  # Use 24002 instead
```

### Error: "Pull access denied"

**Cause:** Need to pull image first

**Solution:**
```bash
docker pull luminati/luminati-proxy:latest
```

### Container Keeps Restarting

**Check logs:**
```bash
docker logs brightdata-proxy-manager
```

**Common issues:**
- Invalid BrightData credentials → Check `--customer` and `--password`
- Port conflicts → Check if ports are available
- Network issues → Check internet connection

### Proxy Returns Errors

**Check container logs:**
```bash
docker logs -f brightdata-proxy-manager
```

**Test from inside container:**
```bash
docker exec -it brightdata-proxy-manager sh
curl http://localhost:24000
```

---

## 📊 Docker Commands Cheat Sheet

### Basic Operations

```bash
# Start (foreground)
docker-compose up

# Start (background)
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop brightdata-proxy-manager

# Remove container
docker rm brightdata-proxy-manager

# View logs
docker logs brightdata-proxy-manager

# Execute command in container
docker exec -it brightdata-proxy-manager sh
```

### Image Management

```bash
# Pull latest image
docker pull luminati/luminati-proxy:latest

# List images
docker images

# Remove image
docker rmi luminati/luminati-proxy:latest

# Update to latest
docker-compose pull
docker-compose up -d
```

---

## 🔐 Security Best Practices

### 1. Don't Commit Credentials

Add to `.gitignore`:
```
docker-compose.yml
*.env
proxy_config/
```

### 2. Use Environment Variables

Create `.env` file:
```env
BRIGHTDATA_CUSTOMER=hl_864cf5cf
BRIGHTDATA_PASSWORD=bdx2gk7k5euj
BRIGHTDATA_ZONE=residential
```

Update `docker-compose.yml`:
```yaml
command: >
  proxy-manager
  --customer "${BRIGHTDATA_CUSTOMER}"
  --password "${BRIGHTDATA_PASSWORD}"
  --zone "${BRIGHTDATA_ZONE}"
```

### 3. Restrict Web UI Access

Only allow localhost:
```yaml
command: >
  proxy-manager
  --www_whitelist_ips "127.0.0.1"
```

---

## 📈 Performance Tuning

### Increase Memory Limit

```yaml
services:
  brightdata-proxy:
    # ... existing config ...
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Enable Persistent Configuration

```yaml
services:
  brightdata-proxy:
    # ... existing config ...
    volumes:
      - ./proxy_config:/root/.luminati-proxy
```

### Add Health Checks

```yaml
services:
  brightdata-proxy:
    # ... existing config ...
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:22999"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 🎯 Production Deployment

### Run in Background (Detached)

```bash
docker-compose up -d
```

### Auto-Restart on Failure

Already configured in `docker-compose.yml`:
```yaml
restart: unless-stopped
```

### Monitor Container

```bash
# Check status
docker-compose ps

# View resource usage
docker stats brightdata-proxy-manager

# View logs
docker-compose logs -f --tail=100
```

### Backup Configuration

```bash
# Export container config
docker inspect brightdata-proxy-manager > proxy_backup.json

# Backup volumes (if using)
docker run --rm -v proxy_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/proxy_backup.tar.gz /data
```

---

## 🆚 Docker vs NPM Comparison

| Feature | Docker 🐳 | NPM 📦 |
|---------|----------|--------|
| **Setup** | Install Docker only | Install Node.js + npm |
| **Isolation** | Full container | Global npm package |
| **Cleanup** | `docker-compose down` | `npm uninstall -g` |
| **Portability** | Works everywhere | Requires Node.js |
| **Updates** | `docker pull` | `npm update -g` |
| **Dependencies** | None (in container) | Node.js runtime |
| **Recommended** | ✅ Yes (cleaner) | ⚠️ OK (more dependencies) |

**Verdict: Docker is better!** 🐳

---

## 🚀 Next Steps

### 1. Test Docker Setup

```bash
# Start proxy
./start_proxy_docker.sh

# Test in another terminal
curl --proxy http://localhost:24000 https://lumtest.com/myip.json
```

### 2. Run Streamlit

```bash
streamlit run streamlit_app.py
```

### 3. Scrape Jobs

Use Streamlit UI to scrape from LinkedIn, Indeed, or Naukri!

---

## 📚 Additional Resources

- **Docker Hub:** https://hub.docker.com/r/luminati/luminati-proxy/
- **BrightData Docs:** https://docs.brightdata.com/proxy-networks/proxy-manager
- **Docker Compose Docs:** https://docs.docker.com/compose/

---

## ✅ Summary

**What you have now:**
1. ✅ Docker-based proxy manager (cleaner than npm)
2. ✅ Docker Compose configuration
3. ✅ Start/stop scripts
4. ✅ Advanced multi-container setup
5. ✅ Complete documentation

**To use:**
```bash
# Terminal 1: Start proxy (Docker)
./start_proxy_docker.sh

# Terminal 2: Start Streamlit
streamlit run streamlit_app.py

# Browser: Open http://localhost:8501
```

**Advantages:**
- 🐳 Cleaner (no npm dependencies)
- ⚡ Same speed (10-20s for 20 jobs)
- 🔧 Easier to manage (docker-compose)
- 🚀 Production-ready (auto-restart)

**Ready to scrape with Docker! 🐳🚀**
