#!/bin/bash

# סקריפט הפעלה לניטור ארכיון אוטומטי
# Start Archive Monitor Script

echo "🚀 מתחיל ניטור ארכיון אוטומטי..."
echo "📁 תיקייה: /Users/kinghippo/Documents/rssFeed/marketBit_archives"
echo "⏰ הסקריפט יבדוק קבצים חדשים כל 30 שניות"
echo "💾 לוגים יישמרו ב: automation-scripts/archive_monitor.log"
echo ""
echo "לעצירה: לחץ Ctrl+C"
echo ""

# שינוי לתיקיית הפרויקט
cd /Users/kinghippo/Documents/rssFeed/marketBit_archives

# הפעלת הסקריפט
python3 automation-scripts/auto_github.py 