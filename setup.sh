#!/bin/bash

# Agentic Commerce Toolkit - Setup Script
# This script initializes the repository and installs dependencies

set -e

echo "=========================================="
echo "Agentic Commerce Toolkit - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Check Node version (optional)
echo "[2/5] Checking Node.js (optional for Shopify app)..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✓ Found Node.js $node_version"
else
    echo "⚠ Node.js not found. Shopify app will not work without Node.js"
fi
echo ""

# Create virtual environment
echo "[3/5] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install Python dependencies
echo "[4/5] Installing Python dependencies..."
pip install --upgrade pip

# Install SDK
pip install -e sdk-python/
echo "✓ SDK installed"

# Install gateway requirements
pip install -r gateway/requirements.txt
echo "✓ Gateway dependencies installed"

# Install MCP server requirements
pip install -r mcp-server/requirements.txt
echo "✓ MCP Server dependencies installed"
echo ""

# Install Node dependencies (skip if Node not available)
echo "[5/5] Installing Node.js dependencies (if available)..."
if command -v npm &> /dev/null; then
    cd shopify-app
    npm install
    cd ..
    echo "✓ Shopify app dependencies installed"
else
    echo "⚠ Skipping Shopify app (Node.js not found)"
fi
echo ""

echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""

echo "Next steps:"
echo "1. Start with Docker: docker-compose up"
echo "   OR"
echo "2. Start services manually:"
echo "   - Gateway: uvicorn gateway.app:app --port 8000"
echo "   - MCP Server: uvicorn mcp-server.server:app --port 9000"
echo "   - Shopify App: cd shopify-app && npm start"
echo ""
echo "3. Test the installation:"
echo "   python example_agent.py"
echo ""
echo "For more information:"
echo "- Installation: cat INSTALLATION.md"
echo "- Usage: cat USAGE.md"
echo "- API Docs: cat API.md"
echo ""
