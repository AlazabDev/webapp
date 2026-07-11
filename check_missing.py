#!/usr/bin/env python3
# check_missing.py

import os
import re
from pathlib import Path

PROJECT_PATH = "/mnt/d/site/site-html/webapp"

def check_file_exists(path):
    """تتحقق من وجود ملف"""
    # لو المسار بيبدأ بـ /assets/webapp/
    if path.startswith('/assets/webapp/'):
        rel_path = path.replace('/assets/webapp/', 'public/')
        full_path = os.path.join(PROJECT_PATH, rel_path)
        return os.path.exists(full_path)
    return True

def main():
    print("🔍 البحث عن ملفات ناقصة...")
    print("="*60)
    
    missing = []
    
    for root, dirs, files in os.walk(os.path.join(PROJECT_PATH, 'webapp/templates')):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن مسارات /assets/webapp/
                paths = re.findall(r'["\'](/assets/webapp/[^"\']+)["\']', content)
                
                for path in paths:
                    if not check_file_exists(path):
                        missing.append({
                            'file': file_path,
                            'path': path
                        })
    
    if missing:
        print("❌ الملفات الناقصة:")
        for m in missing:
            print(f"   - {m['path']} (في {m['file']})")
    else:
        print("✅ كل المسارات صحيحة!")
    
    print("="*60)

if __name__ == "__main__":
    main()
