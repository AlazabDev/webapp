import frappe
from frappe.tests import IntegrationTestCase

from webapp.api import get_facilities


class TestFacility(IntegrationTestCase):
	def test_public_api_returns_only_published_facilities(self):
		published_id = f"TEST-{frappe.generate_hash(length=8).upper()}"
		hidden_id = f"TEST-{frappe.generate_hash(length=8).upper()}"

		frappe.get_doc(
			{
				"doctype": "Facility",
				"facility_id": published_id,
				"facility_name": "Published Facility",
				"facility_type": "Test",
				"latitude": 30.0,
				"longitude": 31.0,
				"published": 1,
			}
		).insert()
		frappe.get_doc(
			{
				"doctype": "Facility",
				"facility_id": hidden_id,
				"facility_name": "Hidden Facility",
				"facility_type": "Test",
				"latitude": 30.0,
				"longitude": 31.0,
				"published": 0,
			}
		).insert()

		facility_ids = {row.facility_id for row in get_facilities()}
		self.assertIn(published_id, facility_ids)
		self.assertNotIn(hidden_id, facility_ids)

	def test_invalid_coordinates_are_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Facility",
					"facility_id": f"TEST-{frappe.generate_hash(length=8).upper()}",
					"facility_name": "Invalid Coordinates",
					"facility_type": "Test",
					"latitude": 120,
					"longitude": 31,
				}
			).insert()
