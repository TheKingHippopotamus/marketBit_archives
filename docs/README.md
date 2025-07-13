# Archive Automation System

מערכת אוטומציה מלאה לניהול ארכיון קבצי HTML עם אינטגרציה ל-GitHub ו-LLM.

## 🚀 תכונות עיקריות

- **ניטור אוטומטי**: בדיקת קבצים חדשים כל 30 שניות
- **עדכון HTML אוטומטי**: עדכון index.html עם קבצים חדשים
- **עדכון תאריכים**: המרה אוטומטית לפורמט d/m/y
- **גיבוי אוטומטי**: גיבוי קבצים לפני עדכון
- **תיעוד מלא**: דוחות עדכון ותיעוד שגיאות
- **אינטגרציה עם Git**: commit ו-push אוטומטי
- **תמיכה ב-LLM**: אינטגרציה עם Ollama
- **ניהול מערכת**: כלי ניהול וניטור

## 📁 מבנה התיקיות

```
automation-scripts/
├── auto_github.py          # הסקריפט הראשי
├── manage_automation.py    # כלי ניהול המערכת
├── start_monitor.sh        # סקריפט הפעלה
├── stop_monitor.sh         # סקריפט עצירה
├── requirements.txt        # תלויות Python
├── README.md              # תיעוד זה
├── logs/                  # קבצי לוג
│   ├── archive_monitor.log
│   └── errors.log
├── backups/               # גיבויים
├── docs/                  # דוחות ותיעוד
└── templates/             # תבניות HTML
```

## 🛠️ התקנה והפעלה

### 1. התקנת תלויות

```bash
cd automation-scripts
pip3 install -r requirements.txt
```

### 2. הפעלת המערכת

```bash
# הפעלה
./automation-scripts/start_monitor.sh

# עצירה
./automation-scripts/stop_monitor.sh
```

### 3. בדיקת סטטוס

```bash
python3 automation-scripts/manage_automation.py status
```

## 📋 פקודות ניהול

### בדיקת סטטוס המערכת
```bash
python3 automation-scripts/manage_automation.py status
```

### עדכון ידני
```bash
python3 automation-scripts/manage_automation.py update
```

### בדיקת Ollama
```bash
python3 automation-scripts/manage_automation.py ollama
```

### הצגת לוגים
```bash
python3 automation-scripts/manage_automation.py logs --lines 50
```

### ניקוי גיבויים ישנים
```bash
python3 automation-scripts/manage_automation.py cleanup --days 7
```

### יצירת דוח מערכת
```bash
python3 automation-scripts/manage_automation.py report
```

## 🔧 הגדרות

### Ollama (אופציונלי)
המערכת תומכת באינטגרציה עם Ollama לניתוח מתקדם:

```bash
# התקנת Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# הפעלת שירות
ollama serve

# הורדת מודל
ollama pull codellama:7b-instruct
```

### הגדרות Git
וודא שה-Git repository מוגדר נכון:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📊 ניטור ותיעוד

### קבצי לוג
- `logs/archive_monitor.log` - לוג כללי של המערכת
- `logs/errors.log` - לוג שגיאות בלבד

### דוחות אוטומטיים
- דוחות עדכון נשמרים ב-`docs/`
- דוחות מערכת נשמרים ב-`docs/`

### מטא-דאטה
- `archive_metadata.json` - מידע על כל הקבצים

## 🚨 פתרון בעיות

### המערכת לא מתחילה
1. בדוק שה-Python 3 מותקן
2. בדוק שהתלויות מותקנות: `pip3 install -r requirements.txt`
3. בדוק הרשאות לקבצים: `chmod +x automation-scripts/*.sh`

### שגיאות Git
1. בדוק שה-repository מוגדר נכון
2. בדוק הרשאות push ל-GitHub
3. בדוק חיבור לאינטרנט

### בעיות עם Ollama
1. בדוק ש-Ollama רץ: `ollama serve`
2. בדוק שהמודל מותקן: `ollama list`
3. המערכת תמשיך לעבוד גם ללא Ollama

## 🔄 תהליך העבודה

1. **ניטור**: המערכת בודקת קבצים חדשים כל 30 שניות
2. **זיהוי**: קבצים חדשים מזוהים לפי שם הקובץ
3. **עדכון HTML**: index.html מתעדכן עם הקבצים החדשים
4. **גיבוי**: גיבוי אוטומטי לפני עדכון
5. **תיעוד**: יצירת דוח עדכון
6. **המתנה**: המתנה של 60 שניות
7. **Git**: commit ו-push אוטומטי
8. **עדכון מטא-דאטה**: שמירת מידע על הקבצים

## 📈 סטטיסטיקות

המערכת מספקת סטטיסטיקות מפורטות:
- מספר קבצים בארכיון
- גודל כולל
- תאריך עדכון אחרון
- סטטוס Git
- מקום פנוי בדיסק
- שגיאות אחרונות

## 🔒 אבטחה

- גיבוי אוטומטי לפני כל עדכון
- לוגים מפורטים לכל פעולה
- בדיקת תקינות קבצים
- טיפול בשגיאות מקיף

## 📞 תמיכה

לבעיות או שאלות:
1. בדוק את הלוגים ב-`logs/`
2. השתמש בפקודת `status` לבדיקת המערכת
3. בדוק את הדוחות ב-`docs/`

---

*מערכת אוטומציה לארכיון MarketBit - גרסה 2.0* 