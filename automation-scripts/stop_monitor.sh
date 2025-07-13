#!/bin/bash

# Archive Automation System - Stop Script
# This script stops the automated archive monitoring system

echo "🛑 Stopping Archive Automation System..."

# Find and kill the automation process
AUTOMATION_PID=$(pgrep -f "auto_github.py")

if [ -z "$AUTOMATION_PID" ]; then
    echo "ℹ️ No automation process found running"
    exit 0
fi

echo "📋 Found automation process (PID: $AUTOMATION_PID)"

# Try graceful shutdown first
echo "🔄 Attempting graceful shutdown..."
kill -TERM $AUTOMATION_PID

# Wait a few seconds for graceful shutdown
sleep 3

# Check if process is still running
if kill -0 $AUTOMATION_PID 2>/dev/null; then
    echo "⚠️ Process still running, forcing shutdown..."
    kill -KILL $AUTOMATION_PID
    sleep 1
fi

# Final check
if kill -0 $AUTOMATION_PID 2>/dev/null; then
    echo "❌ Failed to stop automation process"
    exit 1
else
    echo "✅ Automation system stopped successfully"
fi

# Show final status
echo ""
echo "📊 Final Status:"
echo "   - Automation process: Stopped"
echo "   - Logs available in: automation-scripts/logs/"
echo "   - To restart: ./automation-scripts/start_monitor.sh" 