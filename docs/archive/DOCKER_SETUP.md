# 🐳 Docker Setup Guide - HeadlessX + Luminati Proxy

## Architecture

This setup runs two services in Docker containers:

1. **HeadlessX (Browserless Chrome)** - Browser automation service on port 3000
2. **Luminati Proxy Manager** - BrightData proxy on ports 24000-24001

```
┌─────────────────┐
│  Streamlit App  │
│  (Host: 8501)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────────────┐     ┌─────────────────────┐
│   HeadlessX     │────▶│  Luminati Proxy     │
│ (Docker: 3000)  │     │ (Docker: 24000-01)  │
└─────────────────┘     └──────────┬──────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │  BrightData Network  │
                        │  (Residential IPs)   │
                        └──────────────────────┘
```

---

## Prerequisites

1. **Docker & Docker Compose** installed
2. **BrightData credentials** in `.env`:
   ```bash
   BRIGHTDATA_CUSTOMER_ID=hl_xxxxxxx
   BRIGHTDATA_PASSWORD=your_password
   ```

---

## Quick Start

### 1. Start All Services
```bash
docker-compose up -d
```

### 2. Check Service Status
```bash
docker-compose ps
```

Expected output:
```
NAME              STATUS    PORTS
headlessx         Up        0.0.0.0:3000->3000/tcp
luminati-proxy    Up        0.0.0.0:24000-24001->24000-24001/tcp
```

### 3. Verify Services

**HeadlessX:**
```bash
curl http://localhost:3000
```

**Luminati Proxy:**
```bash
curl http://localhost:22999  # Proxy Manager UI
```

### 4. Start Streamlit App
```bash
streamlit run streamlit_app.py
```

---

## Service Details

### HeadlessX (Browserless Chrome)
- **Port**: 3000
- **Image**: `browserless/chrome:latest`
- **Token**: `test-token` (configured in .env)
- **Features**:
  - Headless Chrome rendering
  - Automatic proxy integration with Luminati
  - 10 concurrent sessions
  - 60s connection timeout

### Luminati Proxy Manager
- **Ports**:
  - `24000`: US residential IPs
  - `24001`: India residential IPs  
  - `22999`: Proxy Manager UI
- **Image**: `luminati/luminati-proxy:latest`
- **Configuration**: `proxy_manager_config.json`

---

## Docker Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f headlessx
docker-compose logs -f luminati-proxy
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart headlessx
```

### Stop Services
```bash
docker-compose down
```

### Stop & Remove Volumes
```bash
docker-compose down -v
```

### Rebuild Services
```bash
docker-compose up -d --build
```

---

## Troubleshooting

### HeadlessX Not Responding
```bash
# Check logs
docker-compose logs headlessx

# Restart service
docker-compose restart headlessx

# Verify healthcheck
docker inspect headlessx | grep -A5 Health
```

### Luminati Proxy Connection Failed
```bash
# Check configuration
cat proxy_manager_config.json

# Verify credentials
echo $BRIGHTDATA_CUSTOMER_ID
echo $BRIGHTDATA_PASSWORD

# Check proxy status
curl http://localhost:22999
```

### Port Conflicts
If ports are already in use:
```bash
# Find process using port
lsof -i :3000
lsof -i :24000

# Kill existing proxy manager
pkill -f luminati
```

---

## Environment Variables

Required in `.env`:
```bash
# HeadlessX
HEADLESSX_BASE_URL=http://localhost:3000
HEADLESSX_TOKEN=test-token
HEADLESSX_PROFILE=desktop-chrome
HEADLESSX_STEALTH=maximum

# BrightData
BRIGHTDATA_CUSTOMER_ID=hl_xxxxxxx
BRIGHTDATA_PASSWORD=your_password

# Proxy URLs
PROXY_URL=http://localhost:24000
PROXY_URL_US=http://localhost:24000
PROXY_URL_INDIA=http://localhost:24001
```

---

## Performance Tips

### 1. Resource Limits
Add to `docker-compose.yml`:
```yaml
services:
  headlessx:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

### 2. Increase Chrome Instances
```yaml
environment:
  - MAX_CONCURRENT_SESSIONS=20
```

### 3. Monitor Resource Usage
```bash
docker stats
```

---

## Production Deployment

### 1. Use Docker Swarm or Kubernetes
```bash
# Docker Swarm
docker stack deploy -c docker-compose.yml scraper

# Kubernetes
kubectl apply -f k8s/
```

### 2. Add Monitoring
```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
```

### 3. Enable HTTPS
Use Nginx reverse proxy with SSL certificates.

---

## Cost Optimization

### BrightData Usage
- Monitor proxy usage at: https://brightdata.com/cp/zones
- Use India proxy (24001) for Naukri - cheaper than US
- Set monthly bandwidth limits

### Docker Resources
- Stop services when not scraping: `docker-compose stop`
- Use resource limits to prevent memory leaks
- Clean up unused images: `docker system prune -a`

---

## Integration with Streamlit

The Streamlit app automatically connects to Docker services via localhost:

1. HeadlessX renders pages at `http://localhost:3000`
2. Luminati proxies requests through `http://localhost:24000`
3. Jobs are scraped and stored in SQLite database
4. Analytics dashboard shows real-time results

**No code changes needed!** The existing `naukri_unified.py` will work seamlessly.

---

## Next Steps

1. ✅ Services running: `docker-compose ps`
2. ✅ Test scraping: Try 10 jobs from Streamlit UI
3. ✅ Monitor logs: `docker-compose logs -f`
4. ✅ Check analytics: View results in dashboard

**Happy Scraping! 🎉**
