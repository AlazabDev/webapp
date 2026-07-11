# Alazab Website

تطبيق Frappe للموقع الرسمي لشركة العزب. الفرع `develop` هو فرع التطوير، والفرع `version-16` هو خط Frappe v16.

## الوظائف الحالية

- صفحة رئيسية عربية ومتجاوبة.
- خدمات ديناميكية مبنية على DocType باسم `Service`.
- صفحات فعلية للخدمات والمشروعات والتواصل وطلب عرض السعر.
- صفحة مولدة لكل خدمة منشورة.
- تكامل مع مدونة Frappe القياسية.
- اختبار سلامة للقوالب والأصول ومسارات الصفحات.

## التثبيت

```bash
bench get-app webapp https://github.com/AlazabDev/webapp.git --branch develop
bench --site <site-name> install-app webapp
bench --site <site-name> migrate
bench build --app webapp
bench --site <site-name> clear-cache
```

## التطوير والفحص

```bash
ruff check webapp
bench --site <site-name> run-tests --app webapp
```

## البنية النشطة

- `webapp/www/`: صفحات الموقع القابلة للوصول مباشرة.
- `webapp/templates/webapp_base.html`: القالب الأساسي الوحيد للموقع.
- `webapp/templates/generators/service.html`: صفحة الخدمة الديناميكية.
- `webapp/public/css/webapp.css`: تنسيق الموقع.
- `webapp/webapp/doctype/service/`: نموذج الخدمة وقواعد التحقق.

المحتوى التشغيلي للخدمات يُدار من Frappe Desk، ولا يُكتب داخل القوالب إلا المحتوى الهيكلي الثابت.
