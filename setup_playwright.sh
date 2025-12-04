#!/bin/bash
# Playwright Browser Setup Script
# This installs browsers in the project directory to prevent WSL cache cleanup

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment variables
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Activate virtual environment
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "❌ Virtual environment not found. Please create it first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Install Playwright browsers
echo "🌐 Installing Playwright browsers to: $PLAYWRIGHT_BROWSERS_PATH"
playwright install chromium

echo "✅ Playwright setup complete!"
echo "📁 Browsers installed at: $PLAYWRIGHT_BROWSERS_PATH"
echo ""
echo "Note: Browsers are now stored in your project directory"
echo "and will not be cleared by system cache cleanup."
