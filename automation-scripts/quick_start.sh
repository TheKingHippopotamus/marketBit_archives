#!/bin/bash

# Quick Start Script for Archive Automation System
# Runs tests and starts the automation system

echo "🚀 Archive Automation System - Quick Start"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "index.html" ] || [ ! -d "archive" ]; then
    echo "❌ Error: Please run this script from the marketBit_archives directory"
    exit 1
fi

# Run system tests
echo "🧪 Running system tests..."
python3 automation-scripts/test_system.py

if [ $? -ne 0 ]; then
    echo "❌ System tests failed. Please fix issues before starting automation."
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo ""

# Ask user if they want to start automation
read -p "🤔 Do you want to start the automation system now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting automation system..."
    echo "💤 Press Ctrl+C to stop"
    echo ""
    
    # Start the automation system
    python3 automation-scripts/auto_github.py
else
    echo "ℹ️ To start later, run: ./automation-scripts/start_monitor.sh"
    echo "ℹ️ To check status: python3 automation-scripts/manage_automation.py status"
fi 