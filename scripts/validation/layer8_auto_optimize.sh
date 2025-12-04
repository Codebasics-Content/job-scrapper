#!/bin/bash
# ============================================================================
# LAYER 8: Autonomous Skill Optimizer
# Automatically discovers, validates, and adds new skills to the reference
#
# Usage:
#   ./layer8_auto_optimize.sh                    # Live run (modifies files)
#   ./layer8_auto_optimize.sh --dry-run          # Preview only (no changes)
#   ./layer8_auto_optimize.sh --min-coverage 2   # Min 2% coverage
#   ./layer8_auto_optimize.sh --max-add 10       # Add max 10 skills
#   ./layer8_auto_optimize.sh --confidence 0.8   # 80% confidence threshold
#
# Prerequisites:
#   - Layer 6 must be run first to generate emerging_skills_candidates.json
#   - better-sqlite3 npm package must be installed
#
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║           LAYER 8: AUTONOMOUS SKILL OPTIMIZER                        ║"
echo "║           Auto-discover and add skills to reference                  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if candidates file exists
CANDIDATES_FILE="$PROJECT_ROOT/data/emerging_skills_candidates.json"
if [ ! -f "$CANDIDATES_FILE" ]; then
    echo "⚠️  ERROR: Candidates file not found!"
    echo "   Run Layer 6 first to generate candidates:"
    echo ""
    echo "   bash scripts/validation/layer6_emerging_skills.sh"
    echo ""
    exit 1
fi

# Check if better-sqlite3 is available
if ! node -e "require('better-sqlite3')" 2>/dev/null; then
    echo "⚠️  ERROR: better-sqlite3 not installed!"
    echo "   Install with: npm install better-sqlite3"
    echo ""
    exit 1
fi

# Parse arguments
DRY_RUN=""
MIN_COVERAGE=""
MAX_ADD=""
CONFIDENCE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run|-n)
            DRY_RUN="--dry-run"
            shift
            ;;
        --min-coverage)
            MIN_COVERAGE="--min-coverage $2"
            shift 2
            ;;
        --max-add)
            MAX_ADD="--max-add $2"
            shift 2
            ;;
        --confidence)
            CONFIDENCE="--confidence $2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Change to project root and run optimizer
cd "$PROJECT_ROOT"
node scripts/validation/auto_skill_optimizer.js $DRY_RUN $MIN_COVERAGE $MAX_ADD $CONFIDENCE

echo ""
echo "✓ Layer 8 autonomous skill optimization complete"
