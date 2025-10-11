#!/bin/bash

echo "🛑 Stopping HeadlessX Rendering Service..."
echo ""

# Stop HeadlessX container
if docker ps --format '{{.Names}}' | grep -q '^headlessx$'; then
    docker stop headlessx
    echo "✅ HeadlessX container stopped"
else
    echo "ℹ️  HeadlessX container is not running"
fi

echo ""
echo "💡 To remove the container completely:"
echo "   docker rm headlessx"
echo ""
