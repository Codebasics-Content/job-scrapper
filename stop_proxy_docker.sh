#!/bin/bash

echo "🛑 Stopping Job Scraper Infrastructure..."
echo ""

# Stop all services (Docker Compose V2)
docker compose down

echo ""
echo "✅ All services stopped"
echo ""
echo "💡 To remove containers and volumes:"
echo "   docker compose down -v"
echo ""
echo "💡 To remove everything including images:"
echo "   docker compose down -v --rmi all"
echo ""
