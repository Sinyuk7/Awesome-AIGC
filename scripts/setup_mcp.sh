#!/bin/bash
#
# setup_mcp.sh - Initialize MCP knowledge server environment
#
# Usage: ./scripts/setup_mcp.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MCP_DIR="$REPO_ROOT/tools/mcp"
VENV_DIR="$MCP_DIR/.venv"

echo "=========================================="
echo "  AIGC Knowledge MCP Server Setup"
echo "=========================================="
echo ""
echo "Repository root: $REPO_ROOT"
echo "MCP directory:   $MCP_DIR"
echo ""

# Check Python version
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "ERROR: Python not found. Please install Python 3.10 or later."
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    MAJOR_VERSION=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
    MINOR_VERSION=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

    if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 10 ]); then
        echo "ERROR: Python 3.10 or later is required. Found: $PYTHON_VERSION"
        exit 1
    fi

    echo "✓ Python $PYTHON_VERSION found ($PYTHON_CMD)"
}

# Create virtual environment
create_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "✓ Virtual environment already exists at $VENV_DIR"
    else
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        echo "✓ Virtual environment created at $VENV_DIR"
    fi
}

# Install dependencies
install_deps() {
    echo "Installing dependencies..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip -q
    pip install "mcp>=1.0.0" -q
    echo "✓ Dependencies installed"
}

# Create index directory
create_index_dir() {
    INDEX_DIR="$MCP_DIR/.knowledge_index"
    if [ ! -d "$INDEX_DIR" ]; then
        mkdir -p "$INDEX_DIR"
        echo "✓ Index directory created at $INDEX_DIR"
    else
        echo "✓ Index directory already exists"
    fi
}

# Build initial index
build_index() {
    echo "Building knowledge index..."
    source "$VENV_DIR/bin/activate"
    $PYTHON_CMD "$MCP_DIR/server.py" --rebuild-index
    echo "✓ Knowledge index built"
}

# Main setup
main() {
    check_python
    create_venv
    install_deps
    create_index_dir
    build_index

    echo ""
    echo "=========================================="
    echo "  Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Restart Claude Code to load the MCP server"
    echo "  2. Test with: 'Search the knowledge base for Midjourney prompts'"
    echo ""
    echo "Useful commands:"
    echo "  Rebuild index:   ./scripts/rebuild_knowledge_index.sh"
    echo "  Run server:      ./scripts/run_mcp.sh"
    echo ""
}

main
