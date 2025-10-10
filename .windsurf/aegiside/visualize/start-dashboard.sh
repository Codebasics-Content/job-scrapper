#!/bin/bash

# 🏏 Thala for a Reason - Port 7777 Dashboard
# Real-time Memory Bank Dashboard Server

cd "$(dirname "$0")/.."

echo "🏏 Starting Real-time Dashboard on Port 7777 - Thala for a Reason!"
echo "⚡ 500ms polling with smart change detection"
echo "🔥 Instant JSON updates without reload"
echo ""
echo "📊 Dashboard URL: http://localhost:7777/visualize/dashboard.html"
echo ""

npx http-server -p 7777 -c-1 --cors
