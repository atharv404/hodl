#!/usr/bin/env bash

# HODL Platform Setup Script
# This script automates the setup process for local development

set -e  # Exit on error

echo "======================================"
echo "HODL Platform Setup Script"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Warning: Running as root is not recommended.${NC}"
    echo "Consider running without sudo and installing in a virtual environment."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    else
        echo -e "${YELLOW}⚠ Python $PYTHON_VERSION found, but 3.11+ is recommended${NC}"
    fi
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.11 or higher.${NC}"
    exit 1
fi

# Check for virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠ Not running in a virtual environment${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment created and activated${NC}"
else
    echo -e "${GREEN}✓ Already in virtual environment: $VIRTUAL_ENV${NC}"
fi

# Update pip
echo ""
echo "Updating pip..."
pip install --upgrade pip

# Install system dependencies (if on Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "Checking system dependencies..."
    
    if command -v apt-get &> /dev/null; then
        echo "Detected Debian/Ubuntu system"
        echo "You may need to install: sqlite3, python3-dev, build-essential"
        read -p "Install system dependencies? (requires sudo) (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo apt-get update
            sudo apt-get install -y sqlite3 python3-dev build-essential
        fi
    fi
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt || {
    echo -e "${YELLOW}⚠ Some packages failed to install. Trying minimal installation...${NC}"
    pip install flask sqlalchemy werkzeug pycryptodome json5 mmh3 twisted coloredlogs dpath attrs
}

# Install HODL package
echo ""
echo "Installing HODL package..."
python setup.py develop

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p db
mkdir -p logs
mkdir -p tmp
echo -e "${GREEN}✓ Directories created${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env and configure your settings${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Initialize database
echo ""
echo "Initializing database..."
python3 -c "from hodl.block.Blockchain import Blockchain; bch = Blockchain(); print('Database initialized successfully')" || {
    echo -e "${YELLOW}⚠ Database initialization had issues but may work at runtime${NC}"
}

# Run basic test
echo ""
echo "Running basic test..."
python3 -c "
from hodl import cryptogr as cg
keys = cg.gen_keys()
print('✓ Cryptography module works')
print(f'Generated test keypair')
" || {
    echo -e "${RED}✗ Basic test failed${NC}"
    exit 1
}

echo ""
echo "======================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Configure your settings in .env file"
echo "2. Start the daemon: python -m hodl.daemon"
echo "3. Access the API at: http://localhost:8001"
echo "4. Check status: curl http://localhost:8001/status"
echo ""
echo "For more information, see:"
echo "- SETUP.md for detailed setup instructions"
echo "- DEPLOYMENT.md for production deployment"
echo "- TROUBLESHOOTING.md for common issues"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
