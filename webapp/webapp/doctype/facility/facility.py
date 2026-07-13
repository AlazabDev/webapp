from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import strip_html


class Facility(Document):
	def validate(self):
		self.facility_id = strip_html(self.facility_id or "").strip().upper()
		self.facility_name = strip_html(self.facility_name or "").strip()
		self.facility_type = strip_html(self.facility_type or "").strip()
		self.address = strip_html(self.address or "").strip()
		self.map_link = str(self.map_link or "").strip()

		if not self.facility_id:
			frappe.throw(_("Facility ID is required"), frappe.ValidationError)
		if not self.facility_name:
			frappe.throw(_("Facility name is required"), frappe.ValidationError)
		if not self.facility_type:
			frappe.throw(_("Facility type is required"), frappe.ValidationError)

		if self.latitude not in (None, "") and not -90 <= float(self.latitude) <= 90:
			frappe.throw(_("Latitude must be between -90 and 90"), frappe.ValidationError)
		if self.longitude not in (None, "") and not -180 <= float(self.longitude) <= 180:
			frappe.throw(_("Longitude must be between -180 and 180"), frappe.ValidationError)

		if self.map_link:
			parsed = urlparse(self.map_link)
			if parsed.scheme not in {"http", "https"} or not parsed.netloc:
				frappe.throw(_("Map link must be a valid HTTP or HTTPS URL"), frappe.ValidationError)
