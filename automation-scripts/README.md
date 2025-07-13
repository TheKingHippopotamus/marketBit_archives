# אוטומציה לעדכון GitHub ארכיון

## תיאור
סקריפט Python שמנטר את תיקיית הארכיון ומבצע עדכון אוטומטי ל-GitHub כאשר מתגלים קבצים חדשים.

## תכונות
- 🔍 ניטור רציף של תיקיית הארכיון
- ⏰ ספירה לאחור של דקה לפני העלאה
- 📝 יצירת קובץ מטא-דאטה עם רשימת קבצים
- 🔄 ביצוע אוטומטי של `git add`, `commit`, ו-`push`
- 📊 לוגים מפורטים עם תיעוד מלא
- 🛡️ טיפול בשגיאות ומצבי חירום

## דרישות
- Python 3.7+
- Git מותקן ומוגדר
- הרשאות כתיבה לתיקיית הריפוזיטורי

## התקנה והפעלה

### 1. הגדרת הרשאות
```bash
chmod +x automation-scripts/auto_github.py
```

### 2. הפעלת הסקריפט (קל)
```bash
./automation-scripts/start_monitor.sh
```

### 3. עצירת הסקריפט
```bash
./automation-scripts/stop_monitor.sh
```

### 4. הפעלה ברקע (אופציונלי)
```bash
nohup python3 automation-scripts/auto_github.py > archive_monitor.log 2>&1 &
```

## איך זה עובד

### שלב 1: ניטור
הסקריפט בודק כל 30 שניות אם יש קבצים חדשים בתיקיית `public/archive/`

### שלב 2: זיהוי שינויים
כאשר מתגלים קבצים חדשים, הסקריפט:
- מעדכן את קובץ המטא-דאטה
- מתחיל ספירה לאחור של 60 שניות

### שלב 3: עדכון GitHub
לאחר הספירה לאחור:
- `git add .` - מוסיף את כל השינויים
- `git commit` - יוצר commit עם הודעה אוטומטית
- `git push` - מעלה את השינויים ל-GitHub

## קבצים שנוצרים

### automation-scripts/archive_metadata.json
קובץ JSON המכיל:
```json
{
  "last_updated": "2025-01-20T10:30:00",
  "files": ["AAPL_20250619.html", "MSFT_20250619.html"],
  "total_files": 2
}
```

### automation-scripts/archive_monitor.log
קובץ לוג עם כל הפעולות והשגיאות:
```
2025-01-20 10:30:00 - INFO - נטענו 150 קבצים ידועים
2025-01-20 10:30:30 - INFO - נמצאו 3 קבצים חדשים: ['NVDA_20250619.html', ...]
2025-01-20 10:31:30 - INFO - מריץ git add...
2025-01-20 10:31:31 - INFO - העדכון ל-GitHub הושלם בהצלחה!
```

## הגדרות מותאמות אישית

### שינוי זמני בדיקה
בקובץ `auto_github.py`, שינוי השורה:
```python
time.sleep(30)  # בדיקה כל 30 שניות
```

### שינוי זמן ספירה לאחור
```python
self.countdown(60)  # ספירה לאחור של 60 שניות
```

## פתרון בעיות

### שגיאת הרשאות Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### שגיאת Push
וודא שיש לך הרשאות push לריפוזיטורי:
```bash
git remote -v
git push origin main
```

### עצירת הסקריפט
לחץ `Ctrl+C` לעצירה בטוחה של הסקריפט.

## תמיכה
לשאלות או בעיות, בדוק את קובץ הלוג `archive_monitor.log` לפרטים נוספים.

---
**הערה**: הסקריפט מיועד לשימוש עם ריפוזיטורי Git תקין ומוגדר כראוי. 