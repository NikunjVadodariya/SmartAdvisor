#!/bin/bash

# SmartAdvisor Backend Startup Script

echo "Starting SmartAdvisor Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    # Ensure activate script has execute permissions
    chmod +x venv/bin/activate
fi

# Ensure activate script has execute permissions (in case venv was created externally)
chmod +x venv/bin/activate 2>/dev/null || true

# Activate virtual environment
source venv/bin/activate

# Upgrade pip first
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating from env.example..."
    cp env.example .env
    echo "Please edit .env and add your API keys before running."
    exit 1
fi

# Create logs directory
mkdir -p logs

# Start the server
echo "Starting FastAPI server on http://0.0.0.0:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

