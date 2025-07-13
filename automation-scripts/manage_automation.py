#!/usr/bin/env python3
"""
Archive Automation Management System
Provides management interface for the automation system.
"""

import os
import sys
import json
import time
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
import argparse
import requests
from typing import Dict, List, Optional

class AutomationManager:
    """Manages the automation system."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.archive_dir = repo_path / "archive"
        self.metadata_file = repo_path / "automation-scripts" / "archive_metadata.json"
        self.log_dir = repo_path / "automation-scripts" / "logs"
        self.docs_dir = repo_path / "docs"
        
    def get_system_status(self) -> Dict:
        """Get comprehensive system status."""
        status = {
            'timestamp': datetime.now().isoformat(),
            'archive_files': 0,
            'total_size': 0,
            'last_update': None,
            'ollama_status': False,
            'git_status': 'unknown',
            'disk_space': 0,
            'recent_errors': []
        }
        
        # Archive files count
        if self.archive_dir.exists():
            html_files = list(self.archive_dir.glob("*.html"))
            status['archive_files'] = len(html_files)
            status['total_size'] = sum(f.stat().st_size for f in html_files)
        
        # Last update from metadata
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
                    status['last_update'] = metadata.get('last_updated')
            except:
                pass
        
        # Ollama status
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            status['ollama_status'] = response.status_code == 200
        except:
            status['ollama_status'] = False
        
        # Git status
        try:
            os.chdir(self.repo_path)
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                if result.stdout.strip():
                    status['git_status'] = 'dirty'
                else:
                    status['git_status'] = 'clean'
        except:
            status['git_status'] = 'error'
        
        # Disk space
        try:
            disk_usage = psutil.disk_usage(str(self.repo_path))
            status['disk_space'] = disk_usage.free / (1024**3)  # GB
        except:
            status['disk_space'] = 0
        
        # Recent errors
        error_log = self.log_dir / "errors.log"
        if error_log.exists():
            try:
                with open(error_log, 'r') as f:
                    lines = f.readlines()
                    status['recent_errors'] = lines[-10:]  # Last 10 error lines
            except:
                pass
        
        return status
    
    def display_status(self):
        """Display system status in a nice format."""
        status = self.get_system_status()
        
        print("🔍 Archive Automation System Status")
        print("=" * 50)
        print(f"📅 Timestamp: {status['timestamp']}")
        print(f"📁 Archive Files: {status['archive_files']}")
        print(f"💾 Total Size: {status['total_size'] / (1024**2):.1f} MB")
        print(f"🔄 Last Update: {status['last_update'] or 'Never'}")
        print(f"🤖 Ollama Status: {'✅ Running' if status['ollama_status'] else '❌ Stopped'}")
        print(f"📝 Git Status: {status['git_status']}")
        print(f"💿 Free Disk Space: {status['disk_space']:.1f} GB")
        
        if status['recent_errors']:
            print("\n❌ Recent Errors:")
            for error in status['recent_errors'][-5:]:
                print(f"   {error.strip()}")
        
        print("\n" + "=" * 50)
    
    def manual_update(self):
        """Perform manual update of the system."""
        print("🔄 Starting manual update...")
        
        # Import the main automation module
        sys.path.append(str(self.repo_path / "automation-scripts"))
        from auto_github import ArchiveMonitor
        
        monitor = ArchiveMonitor(self.repo_path)
        new_files = monitor.check_for_new_files()
        
        if new_files:
            print(f"🆕 Found {len(new_files)} new files")
            success = monitor.process_update(new_files)
            if success:
                print("✅ Manual update completed successfully!")
            else:
                print("❌ Manual update failed!")
        else:
            print("ℹ️ No new files found")
    
    def check_ollama(self):
        """Check Ollama status and available models."""
        print("🤖 Checking Ollama status...")
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"✅ Ollama is running")
                print(f"📋 Available models ({len(models)}):")
                for model in models:
                    print(f"   - {model['name']} ({model['size'] / (1024**3):.1f} GB)")
            else:
                print("❌ Ollama API error")
        except Exception as e:
            print(f"❌ Ollama not available: {e}")
    
    def show_logs(self, lines: int = 20):
        """Show recent logs."""
        log_file = self.log_dir / "archive_monitor.log"
        if log_file.exists():
            print(f"📋 Recent logs (last {lines} lines):")
            print("-" * 50)
            try:
                with open(log_file, 'r') as f:
                    lines_content = f.readlines()
                    for line in lines_content[-lines:]:
                        print(line.strip())
            except Exception as e:
                print(f"❌ Error reading logs: {e}")
        else:
            print("❌ Log file not found")
    
    def cleanup_old_backups(self, days: int = 7):
        """Clean up old backup files."""
        backup_dir = self.repo_path / "automation-scripts" / "backups"
        if not backup_dir.exists():
            print("ℹ️ No backup directory found")
            return
        
        cutoff_time = time.time() - (days * 24 * 3600)
        deleted_count = 0
        
        for backup_file in backup_dir.glob("*.html"):
            if backup_file.stat().st_mtime < cutoff_time:
                try:
                    backup_file.unlink()
                    deleted_count += 1
                    print(f"🗑️ Deleted: {backup_file.name}")
                except Exception as e:
                    print(f"❌ Error deleting {backup_file.name}: {e}")
        
        print(f"✅ Cleanup completed: {deleted_count} files deleted")
    
    def generate_report(self):
        """Generate a comprehensive system report."""
        status = self.get_system_status()
        
        report = f"""# Archive Automation System Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Overview
- **Archive Files**: {status['archive_files']}
- **Total Size**: {status['total_size'] / (1024**2):.1f} MB
- **Last Update**: {status['last_update'] or 'Never'}
- **Ollama Status**: {'Running' if status['ollama_status'] else 'Stopped'}
- **Git Status**: {status['git_status']}
- **Free Disk Space**: {status['disk_space']:.1f} GB

## Archive Statistics
"""
        
        # Get archive statistics
        if self.archive_dir.exists():
            files = list(self.archive_dir.glob("*.html"))
            if files:
                # Group by date
                from collections import defaultdict
                date_groups = defaultdict(list)
                
                for file in files:
                    # Extract date from filename
                    import re
                    match = re.match(r'^[A-Z]+_(\d{8})\.html$', file.name)
                    if match:
                        date_str = match.group(1)
                        date_obj = datetime.strptime(date_str, '%Y%m%d')
                        date_groups[date_obj.strftime('%Y-%m-%d')].append(file)
                
                report += "\n### Files by Date\n"
                for date in sorted(date_groups.keys(), reverse=True):
                    report += f"- **{date}**: {len(date_groups[date])} files\n"
        
        # Recent activity
        report += "\n## Recent Activity\n"
        if status['recent_errors']:
            report += "\n### Recent Errors\n"
            for error in status['recent_errors'][-5:]:
                report += f"- {error.strip()}\n"
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.docs_dir / f"system_report_{timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"📄 System report saved: {report_file}")
        return report_file

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Archive Automation Management")
    parser.add_argument('command', choices=[
        'status', 'update', 'ollama', 'logs', 'cleanup', 'report'
    ], help='Command to execute')
    parser.add_argument('--lines', type=int, default=20, help='Number of log lines to show')
    parser.add_argument('--days', type=int, default=7, help='Days to keep backups')
    
    args = parser.parse_args()
    
    repo_path = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives")
    manager = AutomationManager(repo_path)
    
    if args.command == 'status':
        manager.display_status()
    elif args.command == 'update':
        manager.manual_update()
    elif args.command == 'ollama':
        manager.check_ollama()
    elif args.command == 'logs':
        manager.show_logs(args.lines)
    elif args.command == 'cleanup':
        manager.cleanup_old_backups(args.days)
    elif args.command == 'report':
        manager.generate_report()

if __name__ == "__main__":
    main() 