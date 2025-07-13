#!/usr/bin/env python3
"""
אוטומציה לעדכון GitHub ארכיון
מנטר תיקיית הארכיון ומבצע עדכון אוטומטי ל-GitHub
"""

import os
import time
import subprocess
import json
import hashlib
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Set

# הגדרת לוגים
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
            logging.FileHandler('automation-scripts/archive_monitor.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
)

class ArchiveMonitor:
    def __init__(self, archive_dir: str, repo_path: str):
        self.archive_dir = Path(archive_dir)
        self.repo_path = Path(repo_path)
        self.metadata_file = self.repo_path / "automation-scripts" / "archive_metadata.json"
        self.known_files: Set[str] = set()
        self.load_metadata()
        
    def load_metadata(self):
        """טוען מטא-דאטה של קבצים ידועים"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.known_files = set(data.get('files', []))
                logging.info(f"נטענו {len(self.known_files)} קבצים ידועים")
            except Exception as e:
                logging.error(f"שגיאה בטעינת מטא-דאטה: {e}")
                self.known_files = set()
        else:
            logging.info("לא נמצא קובץ מטא-דאטה, מתחיל עם רשימה ריקה")
    
    def save_metadata(self):
        """שומר מטא-דאטה של קבצים"""
        try:
            metadata = {
                'last_updated': datetime.now().isoformat(),
                'files': list(self.known_files),
                'total_files': len(self.known_files)
            }
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            logging.info(f"נשמר מטא-דאטה עם {len(self.known_files)} קבצים")
        except Exception as e:
            logging.error(f"שגיאה בשמירת מטא-דאטה: {e}")
    
    def get_current_files(self) -> Set[str]:
        """מחזיר את כל הקבצים הנוכחיים בתיקיית הארכיון"""
        if not self.archive_dir.exists():
            logging.warning(f"תיקיית הארכיון לא קיימת: {self.archive_dir}")
            return set()
        
        files = set()
        for file_path in self.archive_dir.glob("*.html"):
            files.add(file_path.name)
        return files
    
    def check_for_new_files(self) -> List[str]:
        """בודק אם יש קבצים חדשים"""
        current_files = self.get_current_files()
        new_files = current_files - self.known_files
        
        if new_files:
            logging.info(f"נמצאו {len(new_files)} קבצים חדשים: {list(new_files)}")
            return list(new_files)
        
        return []
    
    def update_known_files(self, new_files: List[str]):
        """מעדכן את רשימת הקבצים הידועים"""
        for file_name in new_files:
            self.known_files.add(file_name)
        self.save_metadata()
    
    def run_git_commands(self):
        """מריץ פקודות Git"""
        try:
            # שינוי לתיקיית הריפוזיטורי
            os.chdir(self.repo_path)
            logging.info(f"שינוי לתיקייה: {self.repo_path}")
            
            # git add
            logging.info("מריץ git add...")
            result = subprocess.run(['git', 'add', '.'], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                logging.error(f"שגיאה ב-git add: {result.stderr}")
                return False
            
            # בדיקה אם יש שינויים
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, encoding='utf-8')
            if not result.stdout.strip():
                logging.info("אין שינויים חדשים")
                return True
            
            # git commit
            commit_message = f"עדכון ארכיון אוטומטי - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            logging.info(f"מריץ git commit עם הודעה: {commit_message}")
            result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                logging.error(f"שגיאה ב-git commit: {result.stderr}")
                return False
            
            # git push
            logging.info("מריץ git push...")
            result = subprocess.run(['git', 'push'], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                logging.error(f"שגיאה ב-git push: {result.stderr}")
                return False
            
            logging.info("העדכון ל-GitHub הושלם בהצלחה!")
            return True
            
        except Exception as e:
            logging.error(f"שגיאה בהרצת פקודות Git: {e}")
            return False
    
    def countdown(self, seconds: int):
        """ספירה לאחור"""
        for i in range(seconds, 0, -1):
            print(f"\rספירה לאחור: {i} שניות...", end='', flush=True)
            time.sleep(1)
        print("\r", end='', flush=True)
    
    def monitor_and_update(self):
        """הפונקציה הראשית שמנטרת ועדכנת"""
        logging.info("מתחיל ניטור תיקיית הארכיון...")
        
        while True:
            try:
                # בדיקה לקבצים חדשים
                new_files = self.check_for_new_files()
                
                if new_files:
                    logging.info(f"נמצאו {len(new_files)} קבצים חדשים!")
                    
                    # ספירה לאחור של דקה
                    print(f"נמצאו {len(new_files)} קבצים חדשים. מתחיל ספירה לאחור...")
                    self.countdown(60)
                    
                    # עדכון רשימת הקבצים הידועים
                    self.update_known_files(new_files)
                    
                    # הרצת פקודות Git
                    success = self.run_git_commands()
                    
                    if success:
                        print("✅ העדכון ל-GitHub הושלם בהצלחה!")
                    else:
                        print("❌ שגיאה בעדכון ל-GitHub")
                
                # המתנה לפני הבדיקה הבאה
                time.sleep(30)  # בדיקה כל 30 שניות
                
            except KeyboardInterrupt:
                logging.info("הניטור הופסק על ידי המשתמש")
                break
            except Exception as e:
                logging.error(f"שגיאה בניטור: {e}")
                time.sleep(60)  # המתנה ארוכה יותר במקרה של שגיאה

def main():
    """הפונקציה הראשית"""
    # הגדרת נתיבים
    repo_path = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives")
    archive_dir = repo_path / "public" / "archive"
    
    print("🚀 מתחיל ניטור ארכיון אוטומטי...")
    print(f"📁 תיקיית ארכיון: {archive_dir}")
    print(f"📂 תיקיית ריפוזיטורי: {repo_path}")
    print("⏰ הניטור יתחיל בעוד 5 שניות...")
    
    time.sleep(5)
    
    # יצירת מוניטור
    monitor = ArchiveMonitor(str(archive_dir), str(repo_path))
    
    # התחלת ניטור
    monitor.monitor_and_update()

if __name__ == "__main__":
    main()
