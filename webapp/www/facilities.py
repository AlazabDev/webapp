import frappe


def get_context(context):
	context.no_cache = 1
	context.google_maps_api_key = frappe.conf.get("google_maps_api_key") or ""
	return context
