#!/bin/bash

# SmartAdvisor Frontend Startup Script

echo "Starting SmartAdvisor Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the development server
echo "Starting Vite development server on http://localhost:5173"
npm run dev

