#!/bin/bash
# upload_to_s3.sh - رفع الفيديوهات إلى AWS S3

# ================================================================
# الإعدادات
# ================================================================

S3_BUCKET="alazab-storage-media"  # غير الـ bucket حسب رغبتك
S3_PATH="videos/"                   # المسار داخل الـ bucket
LOCAL_VIDEO_PATH="/mnt/d/site/site-html/webapp/webapp/public/video"
TEMPLATES_PATH="/mnt/d/site/site-html/webapp/webapp/templates"

# الألوان
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              📤 رفع الفيديوهات إلى AWS S3                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# ================================================================
# عرض الفيديوهات الموجودة
# ================================================================

echo -e "${BLUE}🎬 الفيديوهات الموجودة محلياً:${NC}"
echo "────────────────────────────────────────────────────────────"

VIDEO_FILES=()
TOTAL_SIZE=0

for video in "$LOCAL_VIDEO_PATH"/*.mp4 "$LOCAL_VIDEO_PATH"/*.webm "$LOCAL_VIDEO_PATH"/*.mov; do
    if [ -f "$video" ]; then
        SIZE=$(du -h "$video" | cut -f1)
        SIZE_BYTES=$(stat -c%s "$video" 2>/dev/null || stat -f%z "$video" 2>/dev/null)
        TOTAL_SIZE=$((TOTAL_SIZE + SIZE_BYTES))
        VIDEO_FILES+=("$video")
        echo -e "   📄 $(basename "$video") (حجم: $SIZE)"
    fi
done

if [ ${#VIDEO_FILES[@]} -eq 0 ]; then
    echo -e "${YELLOW}⚠️  لا توجد فيديوهات للرفع${NC}"
    exit 0
fi

echo ""
echo -e "${CYAN}إجمالي عدد الفيديوهات:${NC} ${#VIDEO_FILES[@]}"
echo -e "${CYAN}الحجم الإجمالي:${NC} $(($TOTAL_SIZE / 1024 / 1024))MB"

# ================================================================
# تأكيد الرفع
# ================================================================

echo ""
read -p "هل تريد رفع الفيديوهات إلى S3 وحذفها محلياً؟ (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${YELLOW}⏹️  تم الإلغاء${NC}"
    exit 0
fi

# ================================================================
# رفع الفيديوهات
# ================================================================

echo ""
echo -e "${BLUE}📤 جارٍ رفع الفيديوهات إلى S3...${NC}"
echo "────────────────────────────────────────────────────────────"

UPLOADED=0
FAILED=0
declare -A UPLOAD_URLS

for video in "${VIDEO_FILES[@]}"; do
    FILENAME=$(basename "$video")
    echo -n "   📤 رفع $FILENAME ... "
    
    # رفع الفيديو إلى S3
    aws s3 cp "$video" "s3://$S3_BUCKET/$S3_PATH$FILENAME" \
        --acl public-read \
        --quiet
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ تم الرفع${NC}"
        UPLOADED=$((UPLOADED + 1))
        
        # الحصول على الرابط
        URL="https://$S3_BUCKET.s3.amazonaws.com/$S3_PATH$FILENAME"
        UPLOAD_URLS["$FILENAME"]="$URL"
        
        # حفظ الرابط في ملف
        echo "$FILENAME -> $URL" >> s3_uploaded_urls.txt
        
        # حذف الفيديو محلياً
        rm "$video"
        echo -e "   ${YELLOW}🗑️  تم حذف الملف المحلي${NC}"
    else
        echo -e "${RED}❌ فشل الرفع${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo -e "${GREEN}✅ تم رفع $UPLOADED فيديو إلى S3${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}❌ فشل رفع $FAILED فيديو${NC}"
fi

# ================================================================
# عرض الروابط
# ================================================================

if [ ${#UPLOAD_URLS[@]} -gt 0 ]; then
    echo ""
    echo -e "${BLUE}🔗 روابط الفيديوهات المرفوعة:${NC}"
    echo "────────────────────────────────────────────────────────────"
    
    for filename in "${!UPLOAD_URLS[@]}"; do
        echo "   📄 $filename"
        echo "      ${UPLOAD_URLS[$filename]}"
        echo ""
    done
    
    echo -e "${YELLOW}📝 تم حفظ الروابط في ملف: s3_uploaded_urls.txt${NC}"
fi

# ================================================================
# تحديث المسارات في ملفات HTML
# ================================================================

echo ""
read -p "هل تريد تحديث مسارات الفيديوهات في ملفات HTML؟ (y/n): " UPDATE_HTML

if [ "$UPDATE_HTML" == "y" ] || [ "$UPDATE_HTML" == "Y" ]; then
    echo -e "${BLUE}🔄 تحديث المسارات في ملفات HTML...${NC}"
    echo "────────────────────────────────────────────────────────────"
    
    UPDATED=0
    for filename in "${!UPLOAD_URLS[@]}"; do
        OLD_PATH="/assets/webapp/video/$filename"
        NEW_URL="${UPLOAD_URLS[$filename]}"
        
        # استبدال المسار القديم بالرابط الجديد في جميع ملفات HTML
        find "$TEMPLATES_PATH" -name "*.html" -exec sed -i "s|$OLD_PATH|$NEW_URL|g" {} \;
        
        if [ $? -eq 0 ]; then
            echo -e "   ✅ $filename -> تم التحديث"
            UPDATED=$((UPDATED + 1))
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ تم تحديث $UPDATED فيديو في ملفات HTML${NC}"
fi

# ================================================================
# الملخص النهائي
# ================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   📊 ملخص العملية                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ تم رفع $UPLOADED فيديو إلى S3${NC}"
echo -e "${GREEN}🗑️  تم حذف $UPLOADED فيديو من السيرفر المحلي${NC}"
echo -e "${CYAN}📁 المساحة المحررة: ~$(($TOTAL_SIZE / 1024 / 1024))MB${NC}"
echo ""
echo -e "${CYAN}📦 الـ Bucket المستخدم:${NC} $S3_BUCKET"
echo -e "${CYAN}📁 المسار في S3:${NC} $S3_PATH"
echo ""
echo -e "${CYAN}🔗 الروابط محفوظة في:${NC} s3_uploaded_urls.txt"

if [ $FAILED -gt 0 ]; then
    echo -e "${RED}⚠️  فشل رفع $FAILED فيديو. تحقق من الاتصال والمجلدات.${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   ✅ انتهت العملية                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
