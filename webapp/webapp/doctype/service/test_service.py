from pathlib import Path
from unittest import TestCase

APP_ROOT = Path(__file__).resolve().parents[3]
REPOSITORY_ROOT = APP_ROOT.parent


class TestServiceWebsiteIntegrity(TestCase):
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
			APP_ROOT / "www" / "facilities.html",
		]
		for template in active_templates:
			self.assertTrue(template.is_file(), template)
			content = template.read_text(encoding="utf-8-sig")
			self.assertIn('extends "webapp/templates/webapp_base.html"', content)
			self.assertNotIn("webapp/templates/base.html", content)

	def test_referenced_local_assets_exist(self):
		assets = [
			APP_ROOT / "public" / "css" / "webapp.css",
			APP_ROOT / "public" / "images" / "logo" / "logo.png",
			APP_ROOT / "public" / "data" / "abuauf_branches_310.csv",
		]
		for asset in assets:
			self.assertTrue(asset.is_file(), asset)

	def test_templates_do_not_query_missing_production_line_doctype(self):
		for template_name in ("header.html", "footer.html"):
			content = (APP_ROOT / "templates" / "includes" / template_name).read_text(encoding="utf-8")
			self.assertNotIn("Production Line", content)
			self.assertNotIn("frappe.db.get_all", content)

	def test_public_forms_use_whitelisted_api_routes(self):
		contact = (APP_ROOT / "www" / "contact.html").read_text(encoding="utf-8")
		quote = (APP_ROOT / "www" / "request-quote.html").read_text(encoding="utf-8")
		facilities = (APP_ROOT / "www" / "facilities.html").read_text(encoding="utf-8")

		self.assertIn("/api/method/webapp.api.submit_contact_form", contact)
		self.assertIn("/api/method/webapp.api.submit_quote_form", quote)
		self.assertIn("/api/method/webapp.api.get_facilities", facilities)
		self.assertNotIn("webapp.webapp.api", facilities)
		self.assertNotIn("AIza", facilities)

	def test_release_metadata_is_ready(self):
		version_file = (APP_ROOT / "__init__.py").read_text(encoding="utf-8")
		license_file = (REPOSITORY_ROOT / "license.txt").read_text(encoding="utf-8")
		readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

		self.assertIn('__version__ = "16.0.0"', version_file)
		self.assertIn("Copyright (c) 2026 AlazabDev", license_file)
		self.assertNotIn("[year]", license_file)
		self.assertIn("--branch version-16", readme)
