import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator


class Service(WebsiteGenerator):
	website = frappe._dict(
		template="templates/generators/service.html",
		condition_field="published",
		page_title_field="service_name",
	)

	def validate(self):
		route = (self.route or "").strip().strip("/")
		if not route:
			frappe.throw(_("Route is required for website services"))
		self.route = "-".join(route.split())
