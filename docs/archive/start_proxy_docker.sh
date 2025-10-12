#!/bin/bash

echo "🐳 Starting Job Scraper Infrastructure with Docker..."
echo ""
echo "   Services:"
echo "   1. Luminati Proxy Manager (Local BrightData Proxy)"
echo "      - Web UI: http://localhost:22999"
echo "      - US Proxy: http://localhost:24000"
echo "      - India Proxy: http://localhost:24001"
echo ""
echo "   2. HeadlessX (Chrome Rendering Service)"
echo "      - API: http://localhost:3000"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    echo "   Run: sudo systemctl start docker"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "   Copy .env.example to .env and configure:"
    echo "   - BRIGHTDATA_CUSTOMER_ID"
    echo "   - BRIGHTDATA_ZONE"
    echo "   - BRIGHTDATA_PASSWORD"
    exit 1
fi

# Load environment variables
source .env

# Validate BrightData credentials
if [ -z "$BRIGHTDATA_CUSTOMER_ID" ] || [ -z "$BRIGHTDATA_PASSWORD" ]; then
    echo "❌ Missing BrightData credentials in .env!"
    echo "   Required: BRIGHTDATA_CUSTOMER_ID, BRIGHTDATA_PASSWORD"
    exit 1
fi

echo "📦 Starting services with docker compose..."
echo ""

# Start all services (Docker Compose V2)
docker compose up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🔍 Check status:"
echo "   docker compose ps"
echo ""
echo "📋 Quick Tests:"
echo "   # Luminati Proxy"
echo "   curl http://localhost:22999"
echo ""
echo "   # HeadlessX"
echo "   curl http://localhost:3000/json/version"
echo ""
echo "📊 View logs:"
echo "   docker compose logs -f"
echo ""
