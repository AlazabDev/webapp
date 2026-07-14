import re

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import strip_html, validate_email_address


class QuoteRequest(Document):
	def validate(self):
		self.customer_name = strip_html(self.customer_name or "").strip()
		self.phone = strip_html(self.phone or "").strip()
		self.service_name = strip_html(self.service_name or "").strip()
		self.project_location = strip_html(self.project_location or "").strip()
		self.details = strip_html(self.details or "").strip()

		if not self.customer_name:
			frappe.throw(_("Customer name is required"), frappe.ValidationError)

		digits = re.sub(r"\D", "", self.phone)
		if not 8 <= len(digits) <= 15:
			frappe.throw(_("Please enter a valid phone number"), frappe.ValidationError)

		if self.email:
			self.email = validate_email_address(self.email.strip(), throw=True)

		if self.service and not frappe.db.exists("Service", self.service):
			frappe.throw(_("The selected service is not available"), frappe.ValidationError)

		if self.service and not self.service_name:
			self.service_name = frappe.db.get_value("Service", self.service, "service_name")
