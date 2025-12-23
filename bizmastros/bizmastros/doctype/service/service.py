import frappe
from frappe.website.website_generator import WebsiteGenerator

class Service(WebsiteGenerator):
  website = frappe._dict(
        template = "templates/generators/service.html",
        condition_field = "published",
        page_title_field = "service_name",
    )
