#!/bin/bash

# Archive Automation System - Start Script
# This script starts the automated archive monitoring system

echo "🚀 Starting Archive Automation System..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import requests, psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required packages..."
    pip3 install requests psutil
fi

# Check if Ollama is running
echo "🤖 Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️ Warning: Ollama is not running. LLM features will be disabled."
    echo "   To start Ollama, run: ollama serve"
fi

# Change to the repository directory
cd /Users/kinghippo/Documents/rssFeed/marketBit_archives

# Create necessary directories
mkdir -p automation-scripts/logs
mkdir -p automation-scripts/backups
mkdir -p automation-scripts/docs

# Check if automation is already running
if pgrep -f "auto_github.py" > /dev/null; then
    echo "⚠️ Automation is already running!"
    echo "   Process ID: $(pgrep -f auto_github.py)"
    echo "   To stop, run: ./automation-scripts/stop_monitor.sh"
    exit 1
fi

# Start the automation system
echo "🔄 Starting automation monitor..."
echo "📁 Monitoring directory: archive"
echo "⏰ Check interval: 30 seconds"
echo "💤 Press Ctrl+C to stop"
echo ""

# Run the automation script
python3 automation-scripts/auto_github.py 