#!/usr/bin/env python3
"""
Test script for Archive Automation System
Tests all components to ensure they work correctly.
"""

import sys
import os
from pathlib import Path
import requests
import subprocess
import json
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import requests
        import psutil
        from pathlib import Path
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_paths():
    """Test that all required paths exist."""
    print("📁 Testing paths...")
    
    repo_path = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives")
    required_paths = [
        repo_path,
        repo_path / "archive",
        repo_path / "index.html",
        repo_path / "automation-scripts"
    ]
    
    for path in required_paths:
        if path.exists():
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - NOT FOUND")
            return False
    
    return True

def test_archive_files():
    """Test archive file parsing."""
    print("📄 Testing archive file parsing...")
    
    archive_dir = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives/archive")
    html_files = list(archive_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in archive")
        return False
    
    print(f"✅ Found {len(html_files)} HTML files")
    
    # Test filename parsing
    import re
    from datetime import datetime
    
    valid_files = 0
    for file in html_files[:5]:  # Test first 5 files
        pattern = r'^([A-Z]+)_(\d{8})\.html$'
        match = re.match(pattern, file.name)
        if match:
            ticker, date_str = match.groups()
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                formatted_date = date_obj.strftime('%d/%m/%Y')
                print(f"   ✅ {file.name} -> {ticker} ({formatted_date})")
                valid_files += 1
            except ValueError:
                print(f"   ❌ {file.name} - Invalid date format")
        else:
            print(f"   ❌ {file.name} - Invalid filename format")
    
    print(f"✅ {valid_files} valid archive files found")
    return valid_files > 0

def test_ollama():
    """Test Ollama connection."""
    print("🤖 Testing Ollama...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            # Test model availability
            required_model = "codellama:7b-instruct"
            available_models = [model['name'] for model in models]
            if required_model in available_models:
                print(f"✅ Required model {required_model} is available")
                return True
            else:
                print(f"⚠️ Required model {required_model} not found")
                print(f"   Available: {available_models}")
                return False
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama not available: {e}")
        return False

def test_git():
    """Test Git configuration."""
    print("📝 Testing Git...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            
            # Check remote
            result = subprocess.run(['git', 'remote', '-v'], 
                                   capture_output=True, text=True)
            if result.stdout.strip():
                print("✅ Git remote configured")
                return True
            else:
                print("⚠️ No Git remote configured")
                return False
        else:
            print("❌ Not a Git repository")
            return False
    except Exception as e:
        print(f"❌ Git error: {e}")
        return False

def test_html_generation():
    """Test HTML generation functionality."""
    print("🌐 Testing HTML generation...")
    
    try:
        # Import the HTML generator
        sys.path.append(str(Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives/automation-scripts")))
        from auto_github import HTMLGenerator
        
        repo_path = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives")
        archive_dir = repo_path / "archive"
        index_file = repo_path / "index.html"
        
        generator = HTMLGenerator(archive_dir, index_file)
        files = generator.get_archive_files()
        
        if files:
            print(f"✅ HTML generator working - {len(files)} files found")
            
            # Test card generation
            cards_html = generator.generate_archive_cards(files[:5])  # First 5 files
            if cards_html and len(cards_html) > 100:
                print("✅ Archive cards generation working")
                return True
            else:
                print("❌ Archive cards generation failed")
                return False
        else:
            print("❌ No archive files found")
            return False
            
    except Exception as e:
        print(f"❌ HTML generation error: {e}")
        return False

def test_metadata():
    """Test metadata functionality."""
    print("📊 Testing metadata...")
    
    metadata_file = Path("/Users/kinghippo/Documents/rssFeed/marketBit_archives/automation-scripts/archive_metadata.json")
    
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            print(f"✅ Metadata file exists with {metadata.get('total_files', 0)} files")
            print(f"   Last updated: {metadata.get('last_updated', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Metadata file error: {e}")
            return False
    else:
        print("⚠️ No metadata file found (will be created on first run)")
        return True

def run_all_tests():
    """Run all tests."""
    print("🧪 Archive Automation System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Paths", test_paths),
        ("Archive Files", test_archive_files),
        ("Ollama", test_ollama),
        ("Git", test_git),
        ("HTML Generation", test_html_generation),
        ("Metadata", test_metadata)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! System is ready to run.")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before running automation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 