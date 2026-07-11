from pathlib import Path
from unittest import TestCase


APP_ROOT = Path(__file__).resolve().parents[1]


class TestTemplateIntegrity(TestCase):
	def test_active_templates_use_existing_base(self):
		base_path = APP_ROOT / "templates" / "webapp_base.html"
		self.assertTrue(base_path.is_file())

		active_templates = [
			APP_ROOT / "templates" / "generators" / "service.html",
			APP_ROOT / "www" / "site.html",
			APP_ROOT / "www" / "about.html",
			APP_ROOT / "www" / "services.html",
			APP_ROOT / "www" / "projects.html",
			APP_ROOT / "www" / "contact.html",
			APP_ROOT / "www" / "request-quote.html",
		]
		for template in active_templates:
			self.assertTrue(template.is_file(), template)
			content = template.read_text(encoding="utf-8")
			self.assertIn('extends "webapp/templates/webapp_base.html"', content)
			self.assertNotIn("webapp/templates/base.html", content)

	def test_referenced_local_assets_exist(self):
		assets = [
			APP_ROOT / "public" / "css" / "webapp.css",
			APP_ROOT / "public" / "images" / "logo" / "logo.png",
		]
		for asset in assets:
			self.assertTrue(asset.is_file(), asset)

	def test_templates_do_not_query_missing_production_line_doctype(self):
		for template_name in ("header.html", "footer.html"):
			content = (APP_ROOT / "templates" / "includes" / template_name).read_text(encoding="utf-8")
			self.assertNotIn("Production Line", content)
			self.assertNotIn("frappe.db.get_all", content)
