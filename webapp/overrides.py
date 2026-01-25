import frappe


def website_context(context):
	context.services = frappe.get_all(
		"Service",
		filters={"published": 1},
		fields=["name", "service_name", "short_description", "service_image", "route"],
		order_by="creation asc",
	)
	context.all_blogs = frappe.get_all(
		"Blog Post",		
		order_by="creation asc",
	)
	return context
