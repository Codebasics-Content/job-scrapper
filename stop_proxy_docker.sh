#!/bin/bash

echo "🛑 Stopping BrightData Proxy Manager Docker container..."

# Stop docker-compose
docker-compose down

# Alternative: Stop docker run container
# docker stop brightdata-proxy-manager

echo "✅ Proxy manager stopped"
