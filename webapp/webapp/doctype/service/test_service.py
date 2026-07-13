import json
import tomllib
from pathlib import Path
from unittest import TestCase

import frappe

from webapp.setup.facilities import load_facilities
from webapp.setup.services import load_default_services

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

	def test_referenced_local_assets_exist_and_are_not_empty(self):
		assets = [
			APP_ROOT / "public" / "css" / "webapp.css",
			APP_ROOT / "public" / "images" / "logo_g.jpg",
			APP_ROOT / "public" / "data" / "abuauf_branches_310.csv",
		]
		for asset in assets:
			self.assertTrue(asset.is_file(), asset)
			self.assertGreater(asset.stat().st_size, 0, asset)

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

	def test_bench_install_contract(self):
		with (REPOSITORY_ROOT / "pyproject.toml").open("rb") as pyproject_file:
			pyproject = tomllib.load(pyproject_file)
		self.assertEqual(
			pyproject["tool"]["bench"]["frappe-dependencies"]["frappe"],
			">=16.0.0,<17.0.0",
		)

		hooks = (APP_ROOT / "hooks.py").read_text(encoding="utf-8")
		self.assertIn('before_install = "webapp.setup.install.before_install"', hooks)
		self.assertIn('after_install = "webapp.setup.install.after_install"', hooks)

		active_fixture = json.loads((APP_ROOT / "fixtures" / "service.json").read_text(encoding="utf-8"))
		self.assertEqual(active_fixture, [])

		for required_file in (
			APP_ROOT / "setup" / "install.py",
			APP_ROOT / "setup" / "services.py",
			APP_ROOT / "setup" / "facilities.py",
			APP_ROOT / "setup" / "data" / "services.json",
		):
			self.assertTrue(required_file.is_file(), required_file)

	def test_seed_sources_are_valid(self):
		services = load_default_services()
		facilities = load_facilities()
		self.assertGreaterEqual(len(services), 4)
		self.assertGreaterEqual(len(facilities), 300)
		self.assertEqual(len({service["route"] for service in services}), len(services))
		self.assertEqual(len({facility["facility_id"] for facility in facilities}), len(facilities))

	def test_bench_install_created_standard_doctypes(self):
		for doctype in ("Service", "Quote Request", "Facility"):
			self.assertTrue(frappe.db.table_exists(doctype), doctype)

	def test_release_metadata_is_ready(self):
		version_file = (APP_ROOT / "__init__.py").read_text(encoding="utf-8")
		license_file = (REPOSITORY_ROOT / "license.txt").read_text(encoding="utf-8")
		readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

		self.assertIn('__version__ = "16.0.1"', version_file)
		self.assertIn("Copyright (c) 2026 AlazabDev", license_file)
		self.assertNotIn("[year]", license_file)
		self.assertIn("--branch version-16", readme)
