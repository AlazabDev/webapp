#!/bin/bash
# make_public_v2.sh - جعل الفيديوهات عامة بدون Policy

BUCKET="alazab-storage-media"

echo "🔓 جعل الفيديوهات عامة باستخدام ACL..."
echo "════════════════════════════════════════════════════════════"

# 1. تعطيل Block Public Access
echo "1️⃣ تعطيل منع الوصول العام..."
aws s3api put-public-access-block --bucket $BUCKET --public-access-block-configuration '{
  "BlockPublicAcls": false,
  "IgnorePublicAcls": false,
  "BlockPublicPolicy": false,
  "RestrictPublicBuckets": false
}' 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ تم تعطيل منع الوصول العام"
else
    echo "   ⚠️  قد يكون معطل بالفعل"
fi

# 2. جعل الملفات عامة
echo ""
echo "2️⃣ جعل الفيديوهات عامة..."

SUCCESS=0
FAILED=0

for file in $(aws s3 ls s3://$BUCKET/videos/ --recursive | awk '{print $4}'); do
    echo -n "   📄 $file ... "
    
    aws s3api put-object-acl --bucket $BUCKET --key "$file" --acl public-read 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "❌ (قد يكون عاماً بالفعل)"
        FAILED=$((FAILED + 1))
    fi
done

# 3. اختبار الروابط
echo ""
echo "3️⃣ اختبار الروابط:"
echo "────────────────────────────────────────────────────────────"

for file in $(aws s3 ls s3://$BUCKET/videos/ --recursive | awk '{print $4}' | head -3); do
    URL="https://$BUCKET.s3.amazonaws.com/$file"
    STATUS=$(curl -I "$URL" 2>/dev/null | head -1 | awk '{print $2}')
    if [ "$STATUS" = "200" ]; then
        echo "   ✅ $file (HTTP $STATUS)"
    else
        echo "   ❌ $file (HTTP $STATUS)"
    fi
done

# 4. عرض الروابط
echo ""
echo "4️⃣ روابط الفيديوهات:"
echo "────────────────────────────────────────────────────────────"
aws s3 ls s3://$BUCKET/videos/ --recursive | awk '{print "https://'$BUCKET'.s3.amazonaws.com/" $4}'

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ تم جعل $SUCCESS فيديو عاماً"
if [ $FAILED -gt 0 ]; then
    echo "⚠️  فشل $FAILED فيديو (قد يكون عاماً بالفعل)"
fi
