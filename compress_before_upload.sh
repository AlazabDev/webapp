#!/bin/bash
# compress_before_upload.sh - ضغط الفيديوهات قبل الرفع

VIDEO_PATH="/mnt/d/site/site-html/webapp/webapp/public/video"

echo "🎬 ضغط الفيديوهات قبل الرفع..."
echo "────────────────────────────────────────────────────────────"

for video in "$VIDEO_PATH"/*.mp4; do
    if [ -f "$video" ]; then
        SIZE_BEFORE=$(du -h "$video" | cut -f1)
        echo "📄 $(basename "$video") (قبل: $SIZE_BEFORE)"
        
        # ضغط باستخدام ffmpeg (CRF 28 = جودة مقبولة، حجم صغير)
        ffmpeg -i "$video" -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 128k "${video%.mp4}_compressed.mp4" -y 2>/dev/null
        
        if [ -f "${video%.mp4}_compressed.mp4" ]; then
            SIZE_AFTER=$(du -h "${video%.mp4}_compressed.mp4" | cut -f1)
            rm "$video"
            mv "${video%.mp4}_compressed.mp4" "$video"
            echo -e "   ✅ بعد الضغط: $SIZE_AFTER"
        else
            echo -e "   ❌ فشل الضغط"
        fi
    fi
done

echo "✅ تم ضغط الفيديوهات!"
