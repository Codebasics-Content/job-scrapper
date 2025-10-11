#!/bin/bash

echo "🔍 Checking BrightData Proxy Manager Health..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

echo "✅ Docker is running"

# Check if proxy container is running
if docker ps | grep -q "brightdata-proxy"; then
    echo "✅ Proxy container is running"
else
    echo "❌ Proxy container is not running"
    echo "   Start it with: ./start_proxy_docker.sh"
    exit 1
fi

# Check Web UI
echo ""
echo "🌐 Checking Web UI (port 22999)..."
if curl -s -f -o /dev/null http://localhost:22999; then
    echo "✅ Web UI is accessible at http://localhost:22999"
else
    echo "⚠️  Web UI not accessible (may still be starting)"
fi

# Check US Proxy
echo ""
echo "🇺🇸 Checking US Proxy (port 24000)..."
US_IP=$(curl -s --proxy http://localhost:24000 --max-time 5 https://lumtest.com/myip.json 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ US Proxy is working"
    echo "   IP: $(echo $US_IP | grep -oP '(?<="ip":")[^"]*')"
    echo "   Country: $(echo $US_IP | grep -oP '(?<="country":")[^"]*')"
else
    echo "❌ US Proxy not responding"
fi

# Check India Proxy (if configured)
echo ""
echo "🇮🇳 Checking India Proxy (port 24001)..."
IN_IP=$(curl -s --proxy http://localhost:24001 --max-time 5 https://lumtest.com/myip.json 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ India Proxy is working"
    echo "   IP: $(echo $IN_IP | grep -oP '(?<="ip":")[^"]*')"
    echo "   Country: $(echo $IN_IP | grep -oP '(?<="country":")[^"]*')"
else
    echo "⚠️  India Proxy not configured or not responding"
fi

# Container stats
echo ""
echo "📊 Container Stats:"
docker stats brightdata-proxy-manager --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "✅ Health check complete!"
