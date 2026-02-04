#!/bin/bash
# Setup script for Pharma Intelligence API

set -e

echo "========================================"
echo "Pharma Intelligence API - Setup"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "To start the API server:"
echo "  source venv/bin/activate"
echo "  python api/main.py"
echo ""
echo "Or run: ./api/start.sh"
echo ""
