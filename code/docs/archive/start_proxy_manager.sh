#!/bin/bash
# Job Scraper Infrastructure Status Checker

echo "🔍 Checking Job Scraper Infrastructure Status..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    echo "   Start Docker: sudo systemctl start docker"
    exit 1
fi

echo "📊 Service Status:"
echo ""

# Check docker compose services (V2)
if docker compose version &> /dev/null; then
    docker compose ps
else
    # Fallback to individual container checks
    echo "Luminati Proxy Manager:"
    if docker ps --format '{{.Names}}' | grep -q '^luminati-proxy$'; then
        docker ps --filter "name=luminati-proxy" --format "  ✅ {{.Names}} ({{.Status}})"
    else
        echo "  ❌ Not running"
    fi
    
    echo ""
    echo "HeadlessX:"
    if docker ps --format '{{.Names}}' | grep -q '^headlessx$'; then
        docker ps --filter "name=headlessx" --format "  ✅ {{.Names}} ({{.Status}})"
    else
        echo "  ❌ Not running"
    fi
fi

echo ""
echo "🔗 Service Endpoints:"
echo "   Luminati Web UI: http://localhost:22999"
echo "   Luminati US Proxy: http://localhost:24000"
echo "   Luminati India Proxy: http://localhost:24001"
echo "   HeadlessX API: http://localhost:3000"
echo ""
echo "📋 Quick Tests:"
echo "   curl http://localhost:22999  # Luminati UI"
echo "   curl http://localhost:3000/json/version  # HeadlessX"
echo ""

if ! docker ps | grep -q "luminati-proxy\|headlessx"; then
    echo "⚠️  Services not running. Start with:"
    echo "   ./start_proxy_docker.sh"
fi

echo ""
