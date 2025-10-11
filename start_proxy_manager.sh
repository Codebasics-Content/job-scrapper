#!/bin/bash
# Start BrightData Proxy Manager locally
# This creates a local proxy server that connects to BrightData's network

# Load credentials from .env
source .env

# Start Proxy Manager with config
echo "🚀 Starting BrightData Proxy Manager..."
echo "   This will create local proxy servers at:"
echo "   - http://localhost:24000 (US residential IPs)"
echo "   - http://localhost:24001 (India residential IPs)"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Extract customer ID and password from Browser URL
CUSTOMER_ID=$(echo $BRIGHTDATA_BROWSER_URL | grep -oP 'brd-customer-\K[^-]+')
PASSWORD=$(echo $BRIGHTDATA_BROWSER_URL | grep -oP 'zone-[^:]+:\K[^@]+')

echo "Using credentials:"
echo "  Customer: $CUSTOMER_ID"
echo "  Password: ${PASSWORD:0:4}***"
echo ""

# Start Proxy Manager
luminati-proxy \
  --customer "$CUSTOMER_ID" \
  --zone residential \
  --password "$PASSWORD" \
  --port 24000 \
  --country us \
  --session_random true \
  --keep_alive true \
  --pool_size 10 \
  --www 22999 \
  --config proxy_manager_config.json

# Note: Web UI will be available at http://localhost:22999
