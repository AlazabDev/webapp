import frappe
from frappe.model.document import Document

class Services(Document):

    website = frappe._dict({
        "condition_field": "is_published",
        "page_title_field": "service_name",
        "route": "services"
    })

    def autoname(self):
        if not self.route:
            self.route = frappe.scrub(self.service_name)

