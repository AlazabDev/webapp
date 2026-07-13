import frappe
from frappe.website.website_generator import WebsiteGenerator

from webapp.setup.services import validate_route


class Service(WebsiteGenerator):
	website = frappe._dict(
		template="templates/generators/service.html",
		condition_field="published",
		page_title_field="service_name",
	)

	def validate(self):
		self.route = validate_route(self.route)
		if self.description:
			self.description = frappe.utils.sanitize_html(
				self.description,
				always_sanitize=True,
				disallowed_tags=["script", "style", "form", "input", "button", "iframe", "object", "embed"],
			)
