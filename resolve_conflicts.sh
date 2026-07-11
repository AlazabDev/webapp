#!/bin/bash
# resolve_conflicts.sh - حل التعارضات تلقائياً

echo "🔧 حل التعارضات..."
echo "════════════════════════════════════════════════════════════"

# 1. عرض الملفات المتعارضة
echo "📄 الملفات المتعارضة:"
git status | grep "both modified"

echo ""
echo "────────────────────────────────────────────────────────────"

# 2. حل التعارضات (استخدام إصدار version-16)
echo "🔧 استخدام إصدار version-16 (الأحدث)..."
git checkout --theirs webapp/templates/includes/header.html
git checkout --theirs webapp/templates/generators/service.html

# 3. إضافة الملفات
echo "📤 إضافة الملفات..."
git add webapp/templates/includes/header.html
git add webapp/templates/generators/service.html

# 4. عمل commit
echo "📝 عمل commit..."
git commit -m "دمج version-16 مع develop وحل التعارضات"

# 5. دفع التغييرات
echo "📤 دفع التغييرات..."
git push origin develop

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ تم حل التعارضات ودفع التغييرات!"
