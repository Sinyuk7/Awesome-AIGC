#!/bin/bash
#
# run_mcp.sh - Run the MCP server (for debugging or manual testing)
#
# Usage: ./scripts/run_mcp.sh
#
# Note: This script is primarily for debugging. Claude Code uses .mcp.json
# to start the server automatically.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MCP_DIR="$REPO_ROOT/tools/mcp"
VENV_DIR="$MCP_DIR/.venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment not found at $VENV_DIR" >&2
    echo "Please run ./scripts/setup_mcp.sh first" >&2
    exit 1
fi

# Activate venv and run server
source "$VENV_DIR/bin/activate"
exec python3 "$MCP_DIR/server.py"
