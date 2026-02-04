#!/bin/bash

# Pharma Intelligence API - Local Deployment Script (without Docker)
# This script helps deploy the API using pyenv or system Python 3.12

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "======================================"
echo "  Pharma Intelligence API Deployment"
echo "======================================"
echo ""

# Check Python version
log_info "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

log_info "Current Python version: $PYTHON_VERSION"

if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 11 ] && [ "$MINOR" -le 13 ]; then
    log_success "Python version is compatible ($PYTHON_VERSION)"
elif [ "$MAJOR" -eq 3 ] && [ "$MINOR" -eq 14 ]; then
    log_error "Python 3.14 detected - pydantic-core compatibility issue!"
    echo ""
    echo "Options:"
    echo "1. Use Docker (recommended): ./deploy.sh"
    echo "2. Install Python 3.12 with pyenv:"
    echo "   $ brew install pyenv"
    echo "   $ pyenv install 3.12.0"
    echo "   $ cd api && pyenv local 3.12.0"
    echo "   $ python3 --version  # should show 3.12.0"
    echo "   $ ./deploy_local.sh"
    echo ""
    echo "3. Use conda:"
    echo "   $ conda create -n pharma python=3.12"
    echo "   $ conda activate pharma"
    echo "   $ cd api && ./deploy_local.sh"
    exit 1
else
    log_error "Python 3.11-3.13 required. Found: $PYTHON_VERSION"
    exit 1
fi

# Navigate to API directory
cd api

# Check if virtual environment exists
if [ -d "venv_312" ]; then
    log_info "Using existing virtual environment..."
else
    log_info "Creating virtual environment with Python 3.12..."
    python3 -m venv venv_312
    log_success "Virtual environment created!"
fi

# Activate virtual environment
log_info "Activating virtual environment..."
source venv_312/bin/activate

# Upgrade pip
log_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
log_info "Installing dependencies..."
pip install -r requirements.txt

log_success "Dependencies installed!"

# Check if data files exist
log_info "Checking data files..."
if [ -f "../pbs_data/pbs_metformin_real_data.json" ]; then
    log_success "PBS data found!"
else
    log_warning "PBS data not found at ../pbs_data/pbs_metformin_real_data.json"
fi

# Start the server
echo ""
log_success "Setup complete! Starting API server..."
echo ""
log_info "API will be available at: http://localhost:8000"
log_info "API documentation at: http://localhost:8000/docs"
log_info "Press Ctrl+C to stop the server"
echo ""
sleep 2

uvicorn main:app --reload --host 0.0.0.0 --port 8000
