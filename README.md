# Alazab Website

تطبيق الموقع الرسمي لشركة العزب، مجهز للعمل كتطبيق قياسي داخل **Frappe Framework v16** من خلال دورة Bench الأصلية فقط.

## الفروع

- `develop`: التطوير والتكامل.
- `version-16`: خط الإصدار المتوافق مع Frappe v16.
- الإصدارات النهائية تُقفل على Tag مثل `v16.0.1`.

## عقد Bench المعتمد

عند إضافة التطبيق إلى Bench:

1. `bench get-app` يستنسخ المستودع، يثبت حزمة Python داخل بيئة Bench، يثبت تبعيات الواجهة عند وجودها، يسجل التطبيق ويبني الأصول.
2. `bench --site <site-name> install-app webapp` ينشئ Module Def ويزامن DocTypes القياسية من ملفات JSON.
3. `before_install` يفحص بيانات الخدمات وملف الفروع كاملًا قبل تعديل Schema الموقع.
4. `after_install` يعمل بعد إنشاء DocTypes ويضيف الخدمات والفروع الناقصة فقط.
5. `bench update` يتولى النسخ الاحتياطي والسحب والمتطلبات والبناء والترحيل وإعادة التشغيل ضمن دورة Bench.

لا يحتاج التطبيق إلى تشغيل `pip` أو `npm` أو `yarn` أو سكربت نشر مستقل خارج Bench.

## الوظائف

- صفحات الموقع العامة والقالب الموحد لهوية العزب.
- خدمات ديناميكية من DocType باسم `Service` وصفحة مولدة لكل خدمة منشورة.
- نموذج تواصل عام يُسجل الطلب داخل `Communication` القياسي في Frappe.
- نموذج طلب عرض سعر يُنشئ سجلًا في `Quote Request` ثم يفتح محادثة WhatsApp برقم الطلب.
- خريطة مرافق وفروع مبنية على DocType باسم `Facility` وتعرض السجلات المنشورة فقط.
- Seed آمن للخدمات لا يعيد الكتابة فوق بيانات Desk.
- استيراد متحقق منه لبيانات الفروع أثناء التثبيت الجديد والترقيات.
- تحديد معدل الطلبات والتحقق من البريد والهاتف والحقول العامة.

## المتطلبات

- Frappe Framework `>=16.0.0,<17.0.0`
- Python `>=3.14,<3.15`
- Node.js `24`
- MariaDB وRedis وفق متطلبات Frappe v16

## التثبيت على Bench

نفذ من داخل مجلد Bench:

```bash
bench get-app --branch version-16 webapp https://github.com/AlazabDev/webapp.git
```

ثم أضف التطبيق إلى الموقع:

```bash
bench --site <site-name> install-app webapp
```

إن نجح الأمر الثاني تكون DocTypes التالية قد أُنشئت تلقائيًا:

- `Service`
- `Quote Request`
- `Facility`

كما تكون بيانات Seed الآمنة قد أضيفت دون الكتابة فوق سجلات موجودة.

## تحديث نسخة مثبتة

من داخل مجلد Bench:

```bash
bench update --apps webapp
```

هذا هو مسار التحديث المعتمد. لا يتم سحب الفرع أو تثبيت التبعيات أو تشغيل الترحيل بأوامر منفصلة خارج Bench.

## إعداد Google Maps

```bash
bench --site <site-name> set-config google_maps_api_key '<GOOGLE_MAPS_API_KEY>'
```

ثم:

```bash
bench --site <site-name> clear-cache
```

## الفحص والاختبارات

```bash
bench --site <site-name> set-config allow_tests true
```

```bash
bench --site <site-name> run-tests --app webapp
```

## البنية المسؤولة عن التلقائية

- `pyproject.toml`: تعريف حزمة Python وتوافق Frappe v16 الذي يفحصه Bench عند `get-app`.
- `webapp/hooks.py`: ربط `before_install` و`after_install` ودورة الموقع.
- `webapp/modules.txt`: تعريف Module الذي ينشئه Bench داخل الموقع.
- `webapp/webapp/doctype/`: ملفات DocType القياسية التي يزامنها `install-app` تلقائيًا.
- `webapp/setup/install.py`: دورة التثبيت الجديدة.
- `webapp/setup/services.py`: فحص وإضافة خدمات Seed دون Overwrite.
- `webapp/setup/facilities.py`: فحص CSV كاملًا ثم إضافة الفروع الناقصة.
- `webapp/patches.txt`: ترحيلات المواقع المثبتة سابقًا بعد مزامنة Schema.
- `webapp/public/`: الأصول التي يبنيها Bench ويعرضها تحت `/assets/webapp/`.

## إدارة البيانات

- `webapp/fixtures/service.json` غير تشغيلي ويحتوي قائمة فارغة حتى لا يعيد Frappe استيراد بيانات الخدمات فوق الإنتاج.
- النسخة المحفوظة للخدمات موجودة في `webapp/setup/data/services.json`.
- الخدمات والفروع الموجودة مسبقًا لا يتم تعديلها أو استبدالها أثناء Seed أو Patch.
- بيانات `Service` و`Quote Request` و`Facility` تُدار بعد التثبيت من Frappe Desk.

## الترخيص

MIT — Copyright (c) 2026 AlazabDev.
