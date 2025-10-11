#!/bin/bash

echo "🐳 Starting HeadlessX Rendering Service with Docker..."
echo ""
echo "   HeadlessX: Chrome-based rendering for job scrapers"
echo "   API will be available at: http://localhost:3000"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    echo "   Run: sudo systemctl start docker"
    exit 1
fi

# Check if HeadlessX container already exists
if docker ps -a --format '{{.Names}}' | grep -q '^headlessx$'; then
    echo "♻️  HeadlessX container exists, restarting..."
    docker start headlessx
else
    echo "📦 Creating new HeadlessX container..."
    echo ""
    
    # Start HeadlessX with Docker
    docker run -d \
      --name headlessx \
      --restart unless-stopped \
      -p 3000:3000 \
      -e CHROME_ARGS="--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage" \
      browserless/chrome:latest
fi

echo ""
echo "✅ HeadlessX started successfully!"
echo ""
echo "📋 Quick Test:"
echo "   curl http://localhost:3000/json/version"
echo ""
echo "🔧 Update your .env file:"
echo "   HEADLESSX_BASE_URL=http://localhost:3000"
echo "   HEADLESSX_TOKEN=  # Leave empty for local development"
echo ""
