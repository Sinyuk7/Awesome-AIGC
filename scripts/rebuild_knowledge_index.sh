#!/bin/bash
#
# rebuild_knowledge_index.sh - Rebuild the knowledge index
#
# Usage: ./scripts/rebuild_knowledge_index.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MCP_DIR="$REPO_ROOT/tools/mcp"
VENV_DIR="$MCP_DIR/.venv"

echo "Rebuilding knowledge index..."
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment not found at $VENV_DIR"
    echo "Please run ./scripts/setup_mcp.sh first"
    exit 1
fi

# Activate venv and rebuild
source "$VENV_DIR/bin/activate"

# Get before stats
if [ -f "$MCP_DIR/.knowledge_index/index.json" ]; then
    OLD_COUNT=$(python3 -c "import json; print(json.load(open('$MCP_DIR/.knowledge_index/index.json'))['file_count'])" 2>/dev/null || echo "0")
else
    OLD_COUNT="0"
fi

# Rebuild index
python3 "$MCP_DIR/server.py" --rebuild-index

# Get after stats
NEW_COUNT=$(python3 -c "import json; print(json.load(open('$MCP_DIR/.knowledge_index/index.json'))['file_count'])")

echo ""
echo "=========================================="
echo "  Index Rebuild Complete"
echo "=========================================="
echo ""
echo "Previous file count: $OLD_COUNT"
echo "Current file count:  $NEW_COUNT"
echo ""

# Show breakdown by source
python3 -c "
import json
with open('$MCP_DIR/.knowledge_index/index.json') as f:
    data = json.load(f)
    counts = {}
    for f in data['files']:
        src = f.get('source', 'unknown')
        counts[src] = counts.get(src, 0) + 1
    print('Files by source:')
    for src, count in sorted(counts.items()):
        print(f'  {src}: {count}')
"
