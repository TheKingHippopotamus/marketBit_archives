#!/usr/bin/env python3
"""
Full Automation System for MarketBit Archives
Handles HTML generation, date updates, documentation, and Git operations automatically.
"""

import os
import time
import subprocess
import json
import re
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Set, Optional
import requests
import hashlib
from dataclasses import dataclass
import shutil

# Logging setup with rotation
from logging.handlers import RotatingFileHandler

# Setup comprehensive logging
def setup_logging():
    log_dir = Path("automation-scripts/logs")
    log_dir.mkdir(exist_ok=True)
    
    # Main log file with rotation
    main_handler = RotatingFileHandler(
        log_dir / "archive_monitor.log", 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # Error log file
    error_handler = RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    for handler in [main_handler, error_handler, console_handler]:
        handler.setFormatter(formatter)
    
    # Root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[main_handler, error_handler, console_handler]
    )

@dataclass
class ArchiveFile:
    """Represents an archive file with metadata."""
    filename: str
    ticker: str
    date: str
    file_path: Path
    size: int
    modified_time: float
    hash: str

class LLMProcessor:
    """Handles LLM operations using Ollama."""
    
    def __init__(self, model_name: str = "codellama:7b-instruct"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        self.check_ollama_availability()
    
    def check_ollama_availability(self):
        """Check if Ollama is running and model is available."""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                if self.model_name in available_models:
                    logging.info(f"✅ Ollama model {self.model_name} is available")
                    return True
                else:
                    logging.warning(f"⚠️ Model {self.model_name} not found. Available: {available_models}")
                    return False
        except Exception as e:
            logging.error(f"❌ Ollama not available: {e}")
            return False
    
    def generate_content(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """Generate content using Ollama."""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logging.error(f"LLM API error: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"LLM generation error: {e}")
            return None

class HTMLGenerator:
    """Handles HTML generation and updates."""
    
    def __init__(self, archive_dir: Path, index_file: Path):
        self.archive_dir = archive_dir
        self.index_file = index_file
        self.template_file = Path("automation-scripts/templates/index_template.html")
        self.backup_dir = Path("automation-scripts/backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def parse_filename(self, filename: str) -> Optional[Dict[str, str]]:
        """Parse filename to extract ticker and date."""
        # Pattern: TICKER_YYYYMMDD.html
        pattern = r'^([A-Z]+)_(\d{8})\.html$'
        match = re.match(pattern, filename)
        if match:
            ticker, date_str = match.groups()
            # Convert YYYYMMDD to DD/MM/YYYY
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            formatted_date = date_obj.strftime('%d/%m/%Y')
            return {
                'ticker': ticker,
                'date': formatted_date,
                'original_date': date_str
            }
        return None
    
    def get_archive_files(self) -> List[ArchiveFile]:
        """Get all archive files with metadata."""
        files = []
        for file_path in self.archive_dir.glob("*.html"):
            if file_path.name == "test.html":  # Skip test files
                continue
                
            parsed = self.parse_filename(file_path.name)
            if parsed:
                stat = file_path.stat()
                # Calculate file hash
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                files.append(ArchiveFile(
                    filename=file_path.name,
                    ticker=parsed['ticker'],
                    date=parsed['date'],
                    file_path=file_path,
                    size=stat.st_size,
                    modified_time=stat.st_mtime,
                    hash=file_hash
                ))
        
        # Sort by date (newest first)
        files.sort(key=lambda x: x.modified_time, reverse=True)
        return files
    
    def group_files_by_date(self, files: List[ArchiveFile]) -> Dict[str, List[ArchiveFile]]:
        """Group files by date."""
        grouped = {}
        for file in files:
            date_key = file.date
            if date_key not in grouped:
                grouped[date_key] = []
            grouped[date_key].append(file)
        return grouped
    
    def generate_archive_cards(self, files: List[ArchiveFile]) -> str:
        """Generate HTML for archive cards."""
        cards_html = []
        grouped_files = self.group_files_by_date(files)
        
        for date in sorted(grouped_files.keys(), reverse=True):
            cards_html.append(f'                    <!-- {date} -->')
            for file in grouped_files[date]:
                cards_html.append(
                    f'                    <a class="archive-link" href="archive/{file.filename}">'
                    f'<div class="archive-card"><div class="archive-ticker">{file.ticker}</div>'
                    f'<div class="archive-date">{file.date}</div></div></a>'
                )
        
        return '\n'.join(cards_html)
    
    def backup_current_index(self):
        """Create backup of current index file."""
        if self.index_file.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f"index_backup_{timestamp}.html"
            shutil.copy2(self.index_file, backup_path)
            logging.info(f"📦 Created backup: {backup_path}")
    
    def update_index_html(self, files: List[ArchiveFile]) -> bool:
        """Update the index.html file with new archive data."""
        try:
            self.backup_current_index()
            
            # Read current index file
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new archive cards
            new_cards = self.generate_archive_cards(files)
            
            # Update archive grid section
            pattern = r'(<div class="archive-grid">\s*<!--.*?-->.*?)(</div>\s*</div>\s*</div>)'
            replacement = r'\1' + new_cards + r'\2'
            
            updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # Update last modified date
            current_date = datetime.now().strftime('%d/%m/%Y')
            date_pattern = r'(עודכן לאחרונה: )\d{2}/\d{2}/\d{4}'
            updated_content = re.sub(date_pattern, r'\1' + current_date, updated_content)
            
            # Write updated content
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logging.info(f"✅ Updated index.html with {len(files)} archive files")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error updating index.html: {e}")
            return False

class DocumentationGenerator:
    """Handles documentation generation."""
    
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.docs_dir.mkdir(exist_ok=True)
    
    def generate_update_report(self, new_files: List[ArchiveFile], 
                             total_files: int, success: bool) -> str:
        """Generate update report."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# Archive Update Report - {timestamp}

## Summary
- **Status**: {'✅ Success' if success else '❌ Failed'}
- **New Files Added**: {len(new_files)}
- **Total Files**: {total_files}
- **Update Time**: {timestamp}

## New Files
"""
        
        for file in new_files:
            report += f"- **{file.ticker}** ({file.date}) - {file.filename}\n"
        
        report += f"""
## Technical Details
- File sizes: {[f"{file.size/1024:.1f}KB" for file in new_files]}
- Processing time: {datetime.now().strftime('%H:%M:%S')}

---
*Generated automatically by Archive Automation System*
"""
        
        return report
    
    def save_report(self, report: str, filename: str):
        """Save report to file."""
        report_path = self.docs_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        logging.info(f"📄 Saved report: {report_path}")

class ArchiveMonitor:
    """Main archive monitoring and automation system."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.archive_dir = repo_path / "archive"
        self.index_file = repo_path / "index.html"
        
        # Initialize components
        self.html_generator = HTMLGenerator(self.archive_dir, self.index_file)
        self.docs_generator = DocumentationGenerator(repo_path / "docs")
        self.llm_processor = LLMProcessor()
        
        # Metadata
        self.metadata_file = repo_path / "automation-scripts" / "archive_metadata.json"
        self.known_files: Set[str] = set()
        self.load_metadata()
        
        logging.info("🚀 Archive Monitor initialized")
    
    def load_metadata(self):
        """Load known files metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.known_files = set(data.get('files', []))
                logging.info(f"📋 Loaded {len(self.known_files)} known files")
            except Exception as e:
                logging.error(f"❌ Error loading metadata: {e}")
                self.known_files = set()
    
    def save_metadata(self, files: List[ArchiveFile]):
        """Save metadata with file hashes."""
        try:
            metadata = {
                'last_updated': datetime.now().isoformat(),
                'files': {file.filename: file.hash for file in files},
                'total_files': len(files),
                'file_details': [
                    {
                        'filename': file.filename,
                        'ticker': file.ticker,
                        'date': file.date,
                        'size': file.size,
                        'hash': file.hash,
                        'modified': file.modified_time
                    } for file in files
                ]
            }
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logging.info(f"💾 Saved metadata for {len(files)} files")
            
        except Exception as e:
            logging.error(f"❌ Error saving metadata: {e}")
    
    def check_for_new_files(self) -> List[ArchiveFile]:
        """Check for new files and return them."""
        current_files = self.html_generator.get_archive_files()
        current_filenames = {file.filename for file in current_files}
        
        # Find new files
        new_files = []
        for file in current_files:
            if file.filename not in self.known_files:
                new_files.append(file)
        
        if new_files:
            logging.info(f"🆕 Found {len(new_files)} new files")
            for file in new_files:
                logging.info(f"   📄 {file.ticker} ({file.date}) - {file.filename}")
        
        return new_files
    
    def run_git_operations(self) -> bool:
        """Run git add, commit, and push operations."""
        try:
            os.chdir(self.repo_path)
            logging.info(f"📁 Changed to directory: {self.repo_path}")
            
            # git add
            logging.info("📤 Running git add...")
            result = subprocess.run(['git', 'add', '.'], 
                                   capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                logging.error(f"❌ git add failed: {result.stderr}")
                return False
            
            # Check for changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                   capture_output=True, text=True, encoding='utf-8')
            if not result.stdout.strip():
                logging.info("ℹ️ No changes to commit")
                return True
            
            # git commit
            commit_message = f"🤖 Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            logging.info(f"💾 Running git commit: {commit_message}")
            result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                   capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                logging.error(f"❌ git commit failed: {result.stderr}")
                return False
            
            # git push
            logging.info("🚀 Running git push...")
            result = subprocess.run(['git', 'push'], 
                                   capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                logging.error(f"❌ git push failed: {result.stderr}")
                return False
            
            logging.info("✅ Successfully pushed to GitHub!")
            return True
            
        except Exception as e:
            logging.error(f"❌ Git operations error: {e}")
            return False
    
    def countdown(self, seconds: int):
        """Display countdown timer."""
        for i in range(seconds, 0, -1):
            print(f"\r⏰ Countdown: {i} seconds...", end='', flush=True)
            time.sleep(1)
        print("\r", end='', flush=True)
    
    def process_update(self, new_files: List[ArchiveFile]) -> bool:
        """Process a complete update cycle."""
        try:
            logging.info("🔄 Starting update process...")
            
            # Get all current files
            all_files = self.html_generator.get_archive_files()
            
            # Update HTML
            logging.info("📝 Updating index.html...")
            if not self.html_generator.update_index_html(all_files):
                return False
            
            # Generate documentation
            logging.info("📄 Generating documentation...")
            report = self.docs_generator.generate_update_report(
                new_files, len(all_files), True
            )
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.docs_generator.save_report(report, f"update_report_{timestamp}.md")
            
            # Update metadata
            self.save_metadata(all_files)
            
            # Wait before git operations
            logging.info("⏳ Waiting 60 seconds before git operations...")
            self.countdown(60)
            
            # Git operations
            success = self.run_git_operations()
            
            if success:
                # Update known files
                for file in new_files:
                    self.known_files.add(file.filename)
                
                logging.info("🎉 Update process completed successfully!")
                return True
            else:
                logging.error("❌ Update process failed at git operations")
                return False
                
        except Exception as e:
            logging.error(f"❌ Update process error: {e}")
            return False
    
    def monitor_and_update(self):
        """Main monitoring loop."""
        logging.info("🔍 Starting continuous monitoring...")
        print("🚀 Archive automation system is running!")
        print("📁 Monitoring directory:", self.archive_dir)
        print("⏰ Check interval: 30 seconds")
        print("💤 Press Ctrl+C to stop")
        
        while True:
            try:
                new_files = self.check_for_new_files()
                
                if new_files:
                    print(f"\n🆕 {len(new_files)} new files detected!")
                    success = self.process_update(new_files)
                    
                    if success:
                        print("✅ Update completed successfully!")
                    else:
                        print("❌ Update failed - check logs for details")
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                logging.info("🛑 Monitoring stopped by user")
                print("\n🛑 Monitoring stopped")
                break
            except Exception as e:
                logging.error(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait longer on error

def main():
    """Main entry point."""
    setup_logging()
    
    repo_path = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives")
    archive_dir = repo_path / "public" / "archive"
    
    # Validate paths
    if not repo_path.exists():
        logging.error(f"❌ Repository path does not exist: {repo_path}")
        return
    
    if not archive_dir.exists():
        logging.error(f"❌ Archive directory does not exist: {archive_dir}")
        return
    
    print("🚀 Starting Archive Automation System...")
    print(f"📂 Repository: {repo_path}")
    print(f"📁 Archive: {archive_dir}")
    print("⏰ Starting in 5 seconds...")
    
    time.sleep(5)
    
    monitor = ArchiveMonitor(repo_path)
    monitor.monitor_and_update()

if __name__ == "__main__":
    main()
