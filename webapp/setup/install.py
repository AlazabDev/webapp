import frappe

from webapp.setup.facilities import import_facilities, validate_facilities_source
from webapp.setup.services import ensure_default_services, validate_default_services


def before_install():
	"""Validate repository-managed seed data before Bench changes the site schema."""
	validate_default_services()
	validate_facilities_source()


def after_install():
	"""Populate safe defaults after Bench has synchronized the standard DocTypes."""
	ensure_default_services()
	import_facilities()
	frappe.clear_cache()
