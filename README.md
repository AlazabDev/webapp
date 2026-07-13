# Alazab Website

تطبيق Frappe للموقع الرسمي لشركة العزب، مخصص لخط **Frappe Framework v16**.

## الفروع

- `develop`: التطوير والتكامل والاختبارات.
- `version-16`: فرع الإنتاج المستقر المتوافق مع Frappe v16.
- الإصدارات المثبتة في الإنتاج تُقفل على Tag مثل `v16.0.0`.

## الوظائف

- صفحات الموقع العامة والقالب الموحد لهوية العزب.
- خدمات ديناميكية من DocType باسم `Service` وصفحة مولدة لكل خدمة منشورة.
- نموذج تواصل عام يُسجل الطلب داخل `Communication` القياسي في Frappe.
- نموذج طلب عرض سعر يُنشئ سجلًا في `Quote Request` ثم يفتح محادثة WhatsApp برقم الطلب.
- خريطة مرافق وفروع مبنية على DocType باسم `Facility` وتعرض السجلات المنشورة فقط.
- استيراد بيانات الفروع من `webapp/public/data/abuauf_branches_310.csv` أثناء الترحيل.
- تحديد معدل الطلبات والتحقق من البريد والهاتف والحقول العامة.
- اختبارات سلامة للقوالب والأصول ومسارات API واختبارات تكامل للنماذج والمرافق.

## متطلبات v16

- Python `>=3.14,<3.15`
- Node.js `>=24`
- Frappe Framework branch `version-16`
- MariaDB وRedis وفق متطلبات Frappe v16

## تثبيت بيئة التطوير

```bash
bench get-app webapp https://github.com/AlazabDev/webapp.git
```

```bash
bench --site <site-name> install-app webapp
```

```bash
bench --site <site-name> migrate
```

```bash
bench build --app webapp
```

```bash
bench --site <site-name> clear-cache
```

## تثبيت فرع الإنتاج

```bash
bench get-app webapp https://github.com/AlazabDev/webapp.git --branch version-16
```

بعد نشر `v16.0.0` يفضل تثبيت النسخة المقفلة:

```bash
bench get-app webapp https://github.com/AlazabDev/webapp.git --branch v16.0.0
```

## إعداد Google Maps

مفتاح Google Maps لا يُحفظ داخل المستودع. أضفه إلى إعدادات الموقع:

```bash
bench --site <site-name> set-config google_maps_api_key '<GOOGLE_MAPS_API_KEY>'
```

ثم نفذ:

```bash
bench --site <site-name> clear-cache
```

## ترقية نسخة موجودة

```bash
cd apps/webapp
```

```bash
git fetch origin --tags
```

```bash
git switch version-16
```

```bash
git pull --ff-only origin version-16
```

```bash
cd ../..
```

```bash
bench --site <site-name> migrate
```

```bash
bench build --app webapp
```

```bash
bench --site <site-name> clear-cache
```

## الفحص والاختبارات

```bash
ruff check webapp
```

```bash
bench --site <site-name> set-config allow_tests true
```

```bash
bench --site <site-name> run-tests --app webapp
```

## البنية النشطة

- `webapp/www/`: صفحات الموقع العامة.
- `webapp/templates/webapp_base.html`: القالب الأساسي.
- `webapp/templates/generators/service.html`: صفحة الخدمة الديناميكية.
- `webapp/webapp/doctype/service/`: الخدمات المنشورة.
- `webapp/webapp/doctype/quote_request/`: طلبات عروض الأسعار.
- `webapp/webapp/doctype/facility/`: المرافق والفروع.
- `webapp/api.py`: نقاط API العامة المراقبة.
- `webapp/patches/v16_0/`: ترحيلات إصدار v16.

## قواعد البيانات التشغيلية

بيانات `Service` و`Quote Request` و`Facility` تُدار من Frappe Desk. لا يتم تصدير الخدمات المنشورة كـFixtures حتى لا يعيد `migrate` الكتابة فوق المحتوى التشغيلي في الإنتاج.

## تجهيز الإصدار

قبل إنشاء Tag جديد:

1. نجاح GitHub Actions على Pull Request من `develop` إلى `version-16`.
2. تشغيل `migrate` و`build` واختبارات التطبيق على موقع اختبار.
3. مراجعة `CHANGELOG.md` ورقم `webapp/__init__.py`.
4. أخذ نسخة احتياطية من موقع الإنتاج.
5. إنشاء Tag على `version-16` بصيغة `v16.x.x`.

## الترخيص

MIT — Copyright (c) 2026 AlazabDev.
