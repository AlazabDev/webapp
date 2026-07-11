#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكربت استخراج جميع المسارات والاستدعاءات من ملفات المشروع
الاستخدام: python3 extract_paths.py
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# ================================================================
# الإعدادات
# ================================================================

PROJECT_PATH = "/mnt/d/site/site-html/webapp"
OUTPUT_FILE = "extracted_paths.json"

# الامتدادات المدعومة
EXTENSIONS = {
    'html': ['.html', '.htm'],
    'css': ['.css', '.scss'],
    'js': ['.js'],
}

# ================================================================
# أنماط البحث (Regular Expressions)
# ================================================================

PATTERNS = {
    # HTML - روابط CSS
    'link_css': re.compile(r'<link[^>]*href=["\']([^"\']+\.css[^"\']*)["\']', re.IGNORECASE),
    
    # HTML - روابط JS
    'script_src': re.compile(r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']', re.IGNORECASE),
    
    # HTML - صور
    'img_src': re.compile(r'<img[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE),
    
    # HTML - روابط عامة (href)
    'link_href': re.compile(r'<a[^>]*href=["\']([^"\']+)["\']', re.IGNORECASE),
    
    # HTML - استدعاء include
    'include': re.compile(r'{%\s*include\s+["\']([^"\']+)["\']\s*%}', re.IGNORECASE),
    
    # HTML - extends
    'extends': re.compile(r'{%\s*extends\s+["\']([^"\']+)["\']\s*%}', re.IGNORECASE),
    
    # HTML - static files (Frappe)
    'static_url': re.compile(r'["\'](/assets/[^"\']+)["\']', re.IGNORECASE),
    
    # CSS - url() images
    'css_url': re.compile(r'url\(["\']?([^"\')\s]+)["\']?\)', re.IGNORECASE),
    
    # CSS - @import
    'css_import': re.compile(r'@import\s+["\']([^"\']+)["\']', re.IGNORECASE),
    
    # JS - import/require
    'js_import': re.compile(r'(?:import|require)\s*\(?["\']([^"\'()]+)["\']', re.IGNORECASE),
    
    # JS - fetch/ajax
    'js_fetch': re.compile(r'(?:fetch|ajax)\s*\(["\']([^"\'()]+)["\']', re.IGNORECASE),
    
    # JS - window.location
    'js_location': re.compile(r'window\.location\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE),
}

# ================================================================
# الدوال الرئيسية
# ================================================================

def get_file_type(file_path):
    """تحديد نوع الملف بناءً على الامتداد"""
    ext = Path(file_path).suffix.lower()
    for file_type, extensions in EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return 'other'

def extract_paths_from_file(file_path):
    """استخراج جميع المسارات من ملف واحد"""
    results = {
        'file': str(file_path),
        'type': get_file_type(file_path),
        'paths': defaultdict(list)
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, FileNotFoundError):
        # حاول بترميز آخر
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            results['error'] = 'Cannot read file'
            return results
    
    # البحث عن كل نمط
    for pattern_name, pattern in PATTERNS.items():
        matches = pattern.findall(content)
        if matches:
            # إزالة التكرارات
            unique_matches = list(set(matches))
            results['paths'][pattern_name] = unique_matches
    
    return results

def scan_project(project_path):
    """مسح جميع الملفات في المشروع"""
    all_results = []
    extensions_to_scan = ['.html', '.htm', '.css', '.scss', '.js']
    
    for root, dirs, files in os.walk(project_path):
        # تجاهل المجلدات المخفية والمجلدات غير المهمة
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'dist']]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in extensions_to_scan:
                file_path = os.path.join(root, file)
                result = extract_paths_from_file(file_path)
                all_results.append(result)
    
    return all_results

def analyze_results(results):
    """تحليل النتائج وإحصائيات"""
    stats = {
        'total_files': len(results),
        'file_types': defaultdict(int),
        'total_paths': 0,
        'path_types': defaultdict(int),
        'missing_files': [],
        'absolute_paths': [],
        'relative_paths': [],
    }
    
    for result in results:
        if result.get('error'):
            continue
        
        stats['file_types'][result['type']] += 1
        
        for path_type, paths in result.get('paths', {}).items():
            for path in paths:
                stats['total_paths'] += 1
                stats['path_types'][path_type] += 1
                
                # تحليل نوع المسار
                if path.startswith('/'):
                    stats['absolute_paths'].append({
                        'file': result['file'],
                        'type': path_type,
                        'path': path
                    })
                elif path.startswith('.'):
                    stats['relative_paths'].append({
                        'file': result['file'],
                        'type': path_type,
                        'path': path
                    })
                
                # التحقق من الملفات المفقودة (في المسارات المطلقة)
                if path.startswith('/assets/'):
                    check_path = PROJECT_PATH + path
                    if not os.path.exists(check_path):
                        stats['missing_files'].append({
                            'file': result['file'],
                            'type': path_type,
                            'path': path
                        })
    
    return stats

def generate_report(results, stats, output_file):
    """توليد تقرير مفصل"""
    report = {
        'summary': {
            'total_files_scanned': stats['total_files'],
            'file_types': dict(stats['file_types']),
            'total_paths_found': stats['total_paths'],
            'path_types': dict(stats['path_types']),
            'missing_files_count': len(stats['missing_files']),
            'absolute_paths_count': len(stats['absolute_paths']),
            'relative_paths_count': len(stats['relative_paths']),
        },
        'all_paths': results,
        'missing_files': stats['missing_files'],
        'absolute_paths': stats['absolute_paths'],
        'relative_paths': stats['relative_paths'],
        'path_summary': dict(stats['path_types']),
    }
    
    # حفظ التقرير كـ JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report

def print_summary(stats):
    """طباعة ملخص في الترمينال"""
    print("\n" + "="*60)
    print("📊 ملخص استخراج المسارات")
    print("="*60)
    print(f"📁 إجمالي الملفات الممسوحة: {stats['total_files']}")
    print(f"📄 أنواع الملفات:")
    for file_type, count in stats['file_types'].items():
        print(f"   - {file_type}: {count} ملف")
    print(f"🔗 إجمالي المسارات المستخرجة: {stats['total_paths']}")
    print(f"\n📂 توزيع المسارات حسب النوع:")
    for path_type, count in stats['path_types'].items():
        print(f"   - {path_type}: {count}")
    print(f"\n✅ المسارات المطلقة: {len(stats['absolute_paths'])}")
    print(f"📁 المسارات النسبية: {len(stats['relative_paths'])}")
    print(f"❌ الملفات المفقودة: {len(stats['missing_files'])}")
    
    if stats['missing_files']:
        print("\n⚠️ الملفات المفقودة (أول 10):")
        for i, missing in enumerate(stats['missing_files'][:10]):
            print(f"   {i+1}. {missing['path']} (في {missing['file']})")

# ================================================================
# التنفيذ
# ================================================================

def main():
    print("🚀 بدء استخراج المسارات من المشروع...")
    print(f"📂 المسار: {PROJECT_PATH}")
    print("="*60)
    
    # مسح المشروع
    results = scan_project(PROJECT_PATH)
    print(f"✅ تم مسح {len(results)} ملف")
    
    # تحليل النتائج
    stats = analyze_results(results)
    
    # طباعة الملخص
    print_summary(stats)
    
    # توليد التقرير
    report = generate_report(results, stats, OUTPUT_FILE)
    print(f"\n📄 تم حفظ التقرير في: {OUTPUT_FILE}")
    
    # عرض المسارات المفقودة بالتفصيل
    if stats['missing_files']:
        print("\n🔍 الملفات المفقودة بالتفصيل:")
        for missing in stats['missing_files']:
            print(f"   - {missing['path']}")
            print(f"     الملف: {missing['file']}")
            print(f"     النوع: {missing['type']}")
            print()
    
    print("="*60)
    print("✨ انتهى الاستخراج!")

if __name__ == "__main__":
    main()
