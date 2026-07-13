import frappe


def website_context(context):
	"""Provide shared, read-only website navigation data without breaking partial installs."""
	if not frappe.db.table_exists("Service"):
		context.services = []
		return context

	context.services = frappe.get_all(
		"Service",
		filters={"published": 1},
		fields=["name", "service_name", "short_description", "service_image", "route", "icon"],
		order_by="service_name asc",
		limit_page_length=50,
	)
	return context
