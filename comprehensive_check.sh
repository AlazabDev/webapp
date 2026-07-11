#!/bin/bash
# comprehensive_check.sh - فحص شامل للمشروع

# الألوان للعرض الجميل
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              🔍 الفحص الشامل للمشروع                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ================================================================
# 1. معلومات المشروع الأساسية
# ================================================================
echo -e "${BLUE}📁 1. معلومات المشروع الأساسية${NC}"
echo "────────────────────────────────────────────────────────────"
echo -e "${CYAN}المسار الحالي:${NC} $(pwd)"
echo -e "${CYAN}تاريخ الفحص:${NC} $(date)"
echo -e "${CYAN}المستخدم:${NC} $(whoami)"
echo ""

# ================================================================
# 2. هيكل الملفات
# ================================================================
echo -e "${BLUE}📂 2. هيكل الملفات${NC}"
echo "────────────────────────────────────────────────────────────"

# عدد الملفات حسب النوع
HTML_COUNT=$(find . -name "*.html" -type f | wc -l)
CSS_COUNT=$(find . -name "*.css" -type f | wc -l)
JS_COUNT=$(find . -name "*.js" -type f | wc -l)
PHP_COUNT=$(find . -name "*.php" -type f | wc -l)
PY_COUNT=$(find . -name "*.py" -type f | wc -l)
JSON_COUNT=$(find . -name "*.json" -type f | wc -l)
IMG_COUNT=$(find . -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" -o -name "*.gif" | wc -l)
VIDEO_COUNT=$(find . -name "*.mp4" -o -name "*.webm" -o -name "*.mov" | wc -l)

echo -e "${CYAN}📄 HTML:${NC} $HTML_COUNT ملف"
echo -e "${CYAN}🎨 CSS:${NC} $CSS_COUNT ملف"
echo -e "${CYAN}⚡ JavaScript:${NC} $JS_COUNT ملف"
echo -e "${CYAN}🐘 PHP:${NC} $PHP_COUNT ملف"
echo -e "${CYAN}🐍 Python:${NC} $PY_COUNT ملف"
echo -e "${CYAN}📋 JSON:${NC} $JSON_COUNT ملف"
echo -e "${CYAN}🖼️  صور:${NC} $IMG_COUNT ملف"
echo -e "${CYAN}🎬 فيديو:${NC} $VIDEO_COUNT ملف"
echo ""

# ================================================================
# 3. المجلدات الرئيسية
# ================================================================
echo -e "${BLUE}📁 3. المجلدات الرئيسية${NC}"
echo "────────────────────────────────────────────────────────────"

# مجلدات Frappe
if [ -d "webapp" ]; then
    echo -e "${GREEN}✅${NC} مجلد webapp موجود"
    
    if [ -d "webapp/public" ]; then
        echo -e "${GREEN}✅${NC} webapp/public موجود"
        PUBLIC_FILES=$(find webapp/public -type f | wc -l)
        echo -e "   📦 عدد الملفات: $PUBLIC_FILES"
    else
        echo -e "${RED}❌${NC} webapp/public غير موجود"
    fi
    
    if [ -d "webapp/templates" ]; then
        echo -e "${GREEN}✅${NC} webapp/templates موجود"
        TEMPLATE_FILES=$(find webapp/templates -name "*.html" | wc -l)
        echo -e "   📄 عدد القوالب: $TEMPLATE_FILES"
    else
        echo -e "${RED}❌${NC} webapp/templates غير موجود"
    fi
else
    echo -e "${RED}❌${NC} مجلد webapp غير موجود"
fi

# مجلد assets (للموقع الثابت)
if [ -d "assets" ]; then
    echo -e "${GREEN}✅${NC} مجلد assets موجود (موقع ثابت)"
elif [ -d "../alazab.com/assets" ]; then
    echo -e "${YELLOW}⚠️${NC} مجلد assets موجود في alazab.com/"
else
    echo -e "${RED}❌${NC} مجلد assets غير موجود"
fi
echo ""

# ================================================================
# 4. فحص الملفات المهمة
# ================================================================
echo -e "${BLUE}🔍 4. فحص الملفات المهمة${NC}"
echo "────────────────────────────────────────────────────────────"

# ملفات Frappe المهمة
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
    else
        echo -e "${RED}❌${NC} $1 (غير موجود)"
    fi
}

check_file "webapp/__init__.py"
check_file "webapp/hooks.py"
check_file "webapp/modules.txt"
check_file "webapp/templates/base.html"

# مجلدات الصور المهمة
check_dir() {
    if [ -d "$1" ]; then
        COUNT=$(find "$1" -type f 2>/dev/null | wc -l)
        echo -e "${GREEN}✅${NC} $1 (عدد الملفات: $COUNT)"
    else
        echo -e "${RED}❌${NC} $1 (غير موجود)"
    fi
}

echo ""
echo -e "${CYAN}📸 مجلدات الصور:${NC}"
check_dir "webapp/public/images"
check_dir "webapp/public/images/logo"
check_dir "webapp/public/images/projects"
check_dir "webapp/public/images/team"
check_dir "webapp/public/images/banners"

echo ""
echo -e "${CYAN}🎨 مجلدات CSS و JS:${NC}"
check_dir "webapp/public/css"
check_dir "webapp/public/js"
check_dir "webapp/public/vendor"

echo ""

# ================================================================
# 5. فحص المسارات في HTML
# ================================================================
echo -e "${BLUE}🔗 5. فحص المسارات في ملفات HTML${NC}"
echo "────────────────────────────────────────────────────────────"

# البحث عن مسارات خاطئة
echo -e "${CYAN}البحث عن مسارات خاطئة...${NC}"

# مسارات alazab بدل webapp
WRONG_ALAZAB=$(grep -r "/assets/alazab/" webapp/templates/ 2>/dev/null | wc -l)
if [ $WRONG_ALAZAB -eq 0 ]; then
    echo -e "${GREEN}✅${NC} لا توجد مسارات /assets/alazab/"
else
    echo -e "${RED}❌${NC} يوجد $WRONG_ALAZAB مسار /assets/alazab/"
    grep -r "/assets/alazab/" webapp/templates/ 2>/dev/null | head -5
fi

# مسارات css/ بدون assets
WRONG_CSS=$(grep -r 'href="css/' webapp/templates/ 2>/dev/null | wc -l)
if [ $WRONG_CSS -eq 0 ]; then
    echo -e "${GREEN}✅${NC} لا توجد مسارات css/ بدون assets"
else
    echo -e "${RED}❌${NC} يوجد $WRONG_CSS مسار css/"
fi

# مسارات js/ بدون assets
WRONG_JS=$(grep -r 'src="js/' webapp/templates/ 2>/dev/null | wc -l)
if [ $WRONG_JS -eq 0 ]; then
    echo -e "${GREEN}✅${NC} لا توجد مسارات js/ بدون assets"
else
    echo -e "${RED}❌${NC} يوجد $WRONG_JS مسار js/"
fi

# مسارات images/ بدون assets
WRONG_IMAGES=$(grep -r 'src="images/' webapp/templates/ 2>/dev/null | wc -l)
if [ $WRONG_IMAGES -eq 0 ]; then
    echo -e "${GREEN}✅${NC} لا توجد مسارات images/ بدون assets"
else
    echo -e "${RED}❌${NC} يوجد $WRONG_IMAGES مسار images/"
fi

echo ""

# ================================================================
# 6. فحص وجود الملفات المشار إليها
# ================================================================
echo -e "${BLUE}📂 6. فحص وجود الملفات المشار إليها${NC}"
echo "────────────────────────────────────────────────────────────"

# ملفات CSS المشار إليها
CSS_REFERENCED=$(grep -rh 'href=".*\.css"' webapp/templates/ 2>/dev/null | sed 's/.*href="//' | sed 's/".*//' | sort -u)
echo -e "${CYAN}ملفات CSS المذكورة في القوالب:${NC}"
for css in $CSS_REFERENCED; do
    if [[ $css == /assets/webapp/* ]]; then
        file_path="webapp/public/${css#/assets/webapp/}"
        if [ -f "$file_path" ]; then
            echo -e "   ${GREEN}✅${NC} $css"
        else
            echo -e "   ${RED}❌${NC} $css (غير موجود)"
        fi
    fi
done

echo ""

# ملفات JS المشار إليها
JS_REFERENCED=$(grep -rh 'src=".*\.js"' webapp/templates/ 2>/dev/null | sed 's/.*src="//' | sed 's/".*//' | sort -u)
echo -e "${CYAN}ملفات JS المذكورة في القوالب:${NC}"
for js in $JS_REFERENCED; do
    if [[ $js == /assets/webapp/* ]]; then
        file_path="webapp/public/${js#/assets/webapp/}"
        if [ -f "$file_path" ]; then
            echo -e "   ${GREEN}✅${NC} $js"
        else
            echo -e "   ${RED}❌${NC} $js (غير موجود)"
        fi
    fi
done

echo ""

# ================================================================
# 7. الصور المفقودة
# ================================================================
echo -e "${BLUE}🖼️ 7. فحص الصور المفقودة${NC}"
echo "────────────────────────────────────────────────────────────"

IMAGES_REFERENCED=$(grep -rh 'src=".*\.\(png\|jpg\|jpeg\|webp\|gif\|svg\)"' webapp/templates/ 2>/dev/null | sed 's/.*src="//' | sed 's/".*//' | sort -u)
MISSING_IMAGES=0

for img in $IMAGES_REFERENCED; do
    if [[ $img == /assets/webapp/* ]]; then
        file_path="webapp/public/${img#/assets/webapp/}"
        if [ ! -f "$file_path" ]; then
            echo -e "   ${RED}❌${NC} $img"
            MISSING_IMAGES=$((MISSING_IMAGES + 1))
        fi
    fi
done

if [ $MISSING_IMAGES -eq 0 ]; then
    echo -e "${GREEN}✅${NC} جميع الصور موجودة!"
else
    echo -e "${RED}❌${NC} يوجد $MISSING_IMAGES صورة مفقودة"
fi

echo ""

# ================================================================
# 8. فحص الملفات الكبيرة
# ================================================================
echo -e "${BLUE}📦 8. فحص الملفات الكبيرة (> 10MB)${NC}"
echo "────────────────────────────────────────────────────────────"

LARGE_FILES=$(find . -type f -size +10M -not -path "./.git/*" 2>/dev/null)
if [ -n "$LARGE_FILES" ]; then
    echo -e "${YELLOW}⚠️  ملفات كبيرة الحجم:${NC}"
    echo "$LARGE_FILES" | while read -r file; do
        SIZE=$(du -h "$file" | cut -f1)
        echo -e "   📄 $file (حجم: $SIZE)"
    done
else
    echo -e "${GREEN}✅${NC} لا توجد ملفات كبيرة (> 10MB)"
fi

echo ""

# ================================================================
# 9. الملخص النهائي
# ================================================================
echo -e "${BLUE}📊 9. الملخص النهائي${NC}"
echo "════════════════════════════════════════════════════════════"

# حساب الإحصائيات النهائية
TOTAL_FILES=$(find . -type f -not -path "./.git/*" -not -path "./node_modules/*" 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh . 2>/dev/null | cut -f1)

echo -e "${CYAN}إجمالي الملفات:${NC} $TOTAL_FILES"
echo -e "${CYAN}الحجم الإجمالي:${NC} $TOTAL_SIZE"
echo ""

# التقييم النهائي
ISSUES=0
if [ $WRONG_ALAZAB -gt 0 ]; then ISSUES=$((ISSUES + 1)); fi
if [ $WRONG_CSS -gt 0 ]; then ISSUES=$((ISSUES + 1)); fi
if [ $WRONG_JS -gt 0 ]; then ISSUES=$((ISSUES + 1)); fi
if [ $WRONG_IMAGES -gt 0 ]; then ISSUES=$((ISSUES + 1)); fi
if [ $MISSING_IMAGES -gt 0 ]; then ISSUES=$((ISSUES + 1)); fi

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}🎉 المشروع بحالة ممتازة! كل شيء صحيح.${NC}"
else
    echo -e "${YELLOW}⚠️  يوجد $ISSUES مشكلة/مشاكل تحتاج للإصلاح.${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ انتهى الفحص الشامل                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
