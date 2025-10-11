#!/bin/bash
# HeadlessX Service Manager
# Check status and provide configuration guidance

echo "🔍 Checking HeadlessX Service Status..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    echo "   Start Docker: sudo systemctl start docker"
    exit 1
fi

# Check HeadlessX container status
if docker ps --format '{{.Names}}' | grep -q '^headlessx$'; then
    echo "✅ HeadlessX is RUNNING"
    echo ""
    echo "📊 Container Info:"
    docker ps --filter "name=headlessx" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "🔗 API Endpoint: http://localhost:3000"
    echo ""
    echo "📋 Test Connection:"
    echo "   curl http://localhost:3000/json/version"
elif docker ps -a --format '{{.Names}}' | grep -q '^headlessx$'; then
    echo "⏸️  HeadlessX container exists but is STOPPED"
    echo ""
    echo "▶️  Start it with: ./start_proxy_docker.sh"
else
    echo "❌ HeadlessX container not found"
    echo ""
    echo "🚀 Create and start with: ./start_proxy_docker.sh"
fi

echo ""
echo "📝 Required .env Configuration:"
echo "   HEADLESSX_BASE_URL=http://localhost:3000"
echo "   HEADLESSX_TOKEN=  # Leave empty for local"
echo "   HEADLESSX_PROFILE=desktop-chrome"
echo "   HEADLESSX_STEALTH=maximum"
echo ""
