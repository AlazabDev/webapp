#!/bin/bash
# make_public.sh - جعل الفيديوهات عامة

BUCKET="alazab-storage-media"

echo "🔓 جعل الـ Bucket عاماً للقراءة..."

# 1. تطبيق الـ Policy
aws s3api put-bucket-policy --bucket $BUCKET --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::'$BUCKET'/*"
  }]
}'

if [ $? -eq 0 ]; then
    echo "✅ تم تطبيق الـ Policy بنجاح"
else
    echo "❌ فشل تطبيق الـ Policy"
    exit 1
fi

# 2. جعل الملفات عامة (احتياطي)
echo ""
echo "🔓 جعل الملفات عامة..."
for file in $(aws s3 ls s3://$BUCKET/videos/ --recursive | awk '{print $4}'); do
    echo "   📄 $file"
    aws s3api put-object-acl --bucket $BUCKET --key "$file" --acl public-read 2>/dev/null
done

# 3. اختبار الرابط
echo ""
echo "🧪 اختبار الرابط:"
TEST_URL="https://$BUCKET.s3.amazonaws.com/videos/video_01.mp4"
echo "   $TEST_URL"

# 4. اختبار الوصول
curl -I "$TEST_URL" 2>/dev/null | head -1

echo ""
echo "✅ تم جعل الفيديوهات عامة!"
echo "🔗 الروابط: https://$BUCKET.s3.amazonaws.com/videos/"
