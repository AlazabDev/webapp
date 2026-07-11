#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fix_paths.py - إصلاح المسارات التلقائي

import os
import re
from pathlib import Path

PROJECT_PATH = "/mnt/d/site/site-html/webapp"

# ================================================================
# قائمة التحويلات (من → إلى)
# ================================================================

FIXES = [
    # ====== إصلاح مسار alazab → webapp ======
    (r'/assets/alazab/', '/assets/webapp/'),
    
    # ====== إصلاح مسار css/webapp.css → css/main.css ======
    (r'/assets/webapp/css/webapp\.css', '/assets/webapp/css/main.css'),
    
    # ====== إصلاح مسار webapp-logo.jpeg → logo.png ======
    (r'/assets/webapp/images/webapp-logo\.jpeg', '/assets/webapp/images/logo/logo.png'),
    
    # ====== إصلاح مسارات الصور الناقصة ======
    (r'/assets/webapp/images/projects/', '/assets/webapp/images/projects/'),
    
    # ====== إضافة مسار images إذا كان ناقص ======
    (r'src="/assets/webapp/(?!images/)logo\.png', 'src="/assets/webapp/images/logo/logo.png'),
]

def fix_file(file_path):
    """إصلاح المسارات في ملف واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        for old, new in FIXES:
            if re.search(old, content):
                content = re.sub(old, new, content)
                changes.append(f"{old} → {new}")
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
    except Exception as e:
        print(f"❌ خطأ في {file_path}: {e}")
    return False, []

def main():
    print("🔧 بدء إصلاح المسارات...")
    print("="*60)
    
    fixed_files = []
    total_changes = 0
    
    # الملفات المستهدفة
    target_files = [
        "webapp/templates/base.html",
        "webapp/templates/includes/header.html",
        "webapp/templates/includes/hero-carousel.html",
        "webapp/templates/includes/slide_show.html",
        "webapp/www/about.html",
    ]
    
    for file_rel in target_files:
        file_path = os.path.join(PROJECT_PATH, file_rel)
        if os.path.exists(file_path):
            success, changes = fix_file(file_path)
            if success:
                fixed_files.append(file_path)
                total_changes += len(changes)
                print(f"✅ تم إصلاح: {file_rel}")
                for change in changes:
                    print(f"   📝 {change}")
            else:
                print(f"⏭️  لا توجد تغييرات: {file_rel}")
        else:
            print(f"❌ الملف غير موجود: {file_rel}")
    
    print("="*60)
    print(f"✨ تم إصلاح {len(fixed_files)} ملفات")
    print(f"📝 إجمالي التغييرات: {total_changes}")
    
    # ============================================================
    # التحقق من مجلدات الصور
    # ============================================================
    print("\n🔍 التحقق من مجلدات الصور...")
    
    # قائمة المجلدات اللي لازم تتأكد من وجودها
    required_dirs = [
        "public/images/logo",
        "public/images/projects",
        "public/images/team",
        "public/images/banners",
    ]
    
    for dir_rel in required_dirs:
        dir_path = os.path.join(PROJECT_PATH, dir_rel)
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            print(f"   ✅ {dir_rel} (عدد الملفات: {len(files)})")
        else:
            print(f"   ❌ {dir_rel} غير موجود")
    
    # ============================================================
    # اقتراحات إضافية
    # ============================================================
    print("\n💡 اقتراحات:")
    print("   1. تأكد من وجود ملف logo.png في: public/images/logo/")
    print("   2. تأكد من وجود صور المشاريع في: public/images/projects/")
    print("   3. إذا كانت الصور ناقصة، انقلها من مجلد alazab.com/assets/img/")

if __name__ == "__main__":
    main()
