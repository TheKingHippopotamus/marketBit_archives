# Archive Automation System - System Summary

## 🎯 מטרת המערכת

מערכת אוטומציה מלאה לניהול ארכיון קבצי HTML עם אינטגרציה אוטומטית ל-GitHub, עדכון HTML, תיעוד מלא ותמיכה ב-LLM.

## 🏗️ ארכיטקטורת המערכת

### רכיבים עיקריים:

1. **ArchiveMonitor** - הרכיב הראשי שמנהל את כל התהליך
2. **HTMLGenerator** - מטפל בעדכון index.html
3. **DocumentationGenerator** - יוצר דוחות ותיעוד
4. **LLMProcessor** - אינטגרציה עם Ollama
5. **AutomationManager** - כלי ניהול המערכת

### תהליך העבודה:

```
📁 ניטור תיקייה (30 שניות)
    ↓
🔍 זיהוי קבצים חדשים
    ↓
📝 עדכון index.html
    ↓
📦 גיבוי אוטומטי
    ↓
📄 יצירת דוח עדכון
    ↓
⏳ המתנה (60 שניות)
    ↓
🚀 Git operations (add, commit, push)
    ↓
💾 עדכון מטא-דאטה
```

## 📁 מבנה קבצים

```
automation-scripts/
├── auto_github.py              # הסקריפט הראשי
├── manage_automation.py        # כלי ניהול
├── test_system.py              # בדיקות מערכת
├── start_monitor.sh            # הפעלה
├── stop_monitor.sh             # עצירה
├── quick_start.sh              # הפעלה מהירה
├── requirements.txt            # תלויות
├── README.md                   # תיעוד
├── SYSTEM_SUMMARY.md           # סיכום זה
├── logs/                       # לוגים
│   ├── archive_monitor.log
│   └── errors.log
├── backups/                    # גיבויים
├── docs/                       # דוחות
└── templates/                  # תבניות
```

## 🚀 תכונות עיקריות

### ✅ אוטומציה מלאה
- ניטור רציף של תיקיית הארכיון
- זיהוי אוטומטי של קבצים חדשים
- עדכון HTML אוטומטי
- עדכון תאריכים לפורמט d/m/y
- Git operations אוטומטי

### ✅ ניהול מתקדם
- גיבוי אוטומטי לפני כל עדכון
- לוגים מפורטים עם רוטציה
- דוחות עדכון אוטומטיים
- מטא-דאטה עם hash של קבצים
- ניהול שגיאות מקיף

### ✅ אינטגרציה עם LLM
- תמיכה ב-Ollama
- מודל ברירת מחדל: codellama:7b-instruct
- בדיקת זמינות אוטומטית
- המשך עבודה גם ללא LLM

### ✅ כלי ניהול
- בדיקת סטטוס מערכת
- עדכון ידני
- הצגת לוגים
- ניקוי גיבויים ישנים
- יצירת דוחות מערכת

## 🔧 הגדרות טכניות

### דרישות מערכת:
- Python 3.7+
- Git מותקן ומוגדר
- Ollama (אופציונלי)
- 100MB+ מקום פנוי

### תלויות Python:
- requests>=2.28.0
- psutil>=5.9.0
- pathlib2>=2.3.7

### זמנים:
- בדיקת קבצים: כל 30 שניות
- המתנה לפני Git: 60 שניות
- רוטציית לוגים: 10MB
- גיבוי לוגים: 5 קבצים

## 📊 סטטיסטיקות נוכחיות

- **קבצים בארכיון**: 678
- **גודל כולל**: 20.5 MB
- **עדכון אחרון**: 2025-07-13T03:59:48
- **סטטוס Ollama**: ✅ פעיל
- **סטטוס Git**: dirty (יש שינויים)
- **מקום פנוי**: 356.3 GB

## 🛠️ פקודות שימוש

### הפעלה מהירה:
```bash
./automation-scripts/quick_start.sh
```

### הפעלה רגילה:
```bash
./automation-scripts/start_monitor.sh
```

### עצירה:
```bash
./automation-scripts/stop_monitor.sh
```

### בדיקת סטטוס:
```bash
python3 automation-scripts/manage_automation.py status
```

### עדכון ידני:
```bash
python3 automation-scripts/manage_automation.py update
```

### בדיקת מערכת:
```bash
python3 automation-scripts/test_system.py
```

## 🔍 ניטור ותיעוד

### קבצי לוג:
- `logs/archive_monitor.log` - לוג כללי
- `logs/errors.log` - לוג שגיאות בלבד

### דוחות אוטומטיים:
- דוחות עדכון ב-`docs/`
- דוחות מערכת ב-`docs/`
- מטא-דאטה ב-`archive_metadata.json`

### גיבויים:
- גיבוי index.html לפני כל עדכון
- שמירה ב-`backups/` עם timestamp

## 🚨 פתרון בעיות

### בעיות נפוצות:

1. **המערכת לא מתחילה**
   - בדוק Python 3: `python3 --version`
   - התקן תלויות: `pip3 install -r requirements.txt`
   - בדוק הרשאות: `chmod +x automation-scripts/*.sh`

2. **שגיאות Git**
   - בדוק הגדרות: `git config --list`
   - בדוק remote: `git remote -v`
   - בדוק הרשאות push

3. **בעיות Ollama**
   - הפעל שירות: `ollama serve`
   - בדוק מודלים: `ollama list`
   - המערכת תמשיך ללא Ollama

## 🔮 תכונות עתידיות

### מתוכנן לפיתוח:
- [ ] Dashboard web interface
- [ ] Email notifications
- [ ] Slack/Discord integration
- [ ] Advanced LLM analysis
- [ ] Backup to cloud storage
- [ ] Performance metrics
- [ ] API endpoints

### שיפורים אפשריים:
- [ ] Multi-threading for faster processing
- [ ] Database integration
- [ ] Advanced file validation
- [ ] Custom templates support
- [ ] Plugin system

## 📞 תמיכה

### לבעיות דחופות:
1. בדוק לוגים: `python3 automation-scripts/manage_automation.py logs`
2. בדוק סטטוס: `python3 automation-scripts/manage_automation.py status`
3. הרץ בדיקות: `python3 automation-scripts/test_system.py`

### תיעוד נוסף:
- `README.md` - מדריך מפורט
- `logs/` - לוגים מפורטים
- `docs/` - דוחות מערכת

---

**מערכת אוטומציה לארכיון MarketBit - גרסה 2.0**  
*נוצר ב: 2025-07-13*  
*סטטוס: פעיל ומוכן לשימוש* 