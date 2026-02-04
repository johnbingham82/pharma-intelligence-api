#!/bin/bash
# Start script for Pharma Intelligence API

set -e

echo "========================================"
echo "Pharma Intelligence API - Starting"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Run: ./api/setup.sh first"
    exit 1
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Start server
echo "🚀 Starting API server..."
echo ""
python main.py
