#!/bin/bash

echo "🐳 Starting BrightData Proxy Manager with Docker..."
echo ""
echo "   This will create local proxy servers at:"
echo "   - http://localhost:24000 (US residential IPs)"
echo "   - http://localhost:24001 (India residential IPs)"
echo ""
echo "   Web UI: http://localhost:22999"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Pull latest image
echo "📦 Pulling latest BrightData Proxy Manager image..."
docker pull luminati/luminati-proxy:latest

echo ""
echo "🚀 Starting proxy manager..."
echo ""

# Start with Docker Compose
docker-compose up

# Alternative: Start with docker run (if docker-compose not available)
# docker run -it --rm \
#   --name brightdata-proxy-manager \
#   -p 22999:22999 \
#   -p 24000:24000 \
#   -p 24001:24001 \
#   luminati/luminati-proxy:latest \
#   proxy-manager \
#   --www_whitelist_ips "0.0.0.0/0" \
#   --ssl true \
#   --customer "hl_864cf5cf" \
#   --zone "residential" \
#   --password "bdx2gk7k5euj" \
#   --port 24000 \
#   --country "us" \
#   --session true
