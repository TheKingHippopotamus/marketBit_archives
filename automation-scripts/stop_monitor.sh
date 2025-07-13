#!/bin/bash

# סקריפט עצירה לניטור ארכיון
# Stop Archive Monitor Script

echo "🛑 עוצר ניטור ארכיון..."

# חיפוש תהליכי Python שמריצים את הסקריפט
PIDS=$(pgrep -f "auto_github.py")

if [ -z "$PIDS" ]; then
    echo "✅ לא נמצאו תהליכי ניטור פעילים"
else
    echo "🔍 נמצאו תהליכים: $PIDS"
    echo "🔄 עוצר תהליכים..."
    
    for PID in $PIDS; do
        echo "עוצר תהליך $PID..."
        kill $PID
    done
    
    echo "✅ כל תהליכי הניטור הופסקו"
fi

echo ""
echo "📊 לוגים זמינים ב: automation-scripts/archive_monitor.log" 