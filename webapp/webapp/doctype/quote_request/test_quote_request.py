import frappe
from frappe.tests import IntegrationTestCase

from webapp.api import submit_contact_form, submit_quote_form


class TestQuoteRequest(IntegrationTestCase):
	def test_public_quote_submission_creates_record(self):
		result = submit_quote_form(
			name="Production Test",
			phone="+201001234567",
			service_name="Other request",
			location="Cairo",
			message="Request details for the production test.",
			email="production-test@example.com",
		)

		self.assertEqual(result["status"], "success")
		self.assertTrue(result["request_id"])

		doc = frappe.get_doc("Quote Request", result["request_id"])
		self.assertEqual(doc.customer_name, "Production Test")
		self.assertEqual(doc.source, "Website")
		self.assertEqual(doc.status, "New")

	def test_honeypot_does_not_create_quote_request(self):
		before = frappe.db.count("Quote Request")
		result = submit_quote_form(
			name="Bot",
			phone="+201001234567",
			service_name="Other request",
			location="Cairo",
			message="Automated spam",
			website="https://spam.invalid",
		)
		self.assertEqual(result, {"status": "success"})
		self.assertEqual(frappe.db.count("Quote Request"), before)

	def test_contact_submission_creates_communication(self):
		result = submit_contact_form(
			name="Website Visitor",
			email="visitor@example.com",
			subject="Website enquiry",
			message="Please contact me about a project.",
		)

		self.assertEqual(result["status"], "success")
		communication = frappe.get_doc("Communication", result["communication_id"])
		self.assertEqual(communication.sender, "visitor@example.com")
		self.assertEqual(communication.sent_or_received, "Received")

	def test_invalid_phone_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			submit_quote_form(
				name="Invalid Phone",
				phone="123",
				service_name="Other request",
				location="Cairo",
				message="Invalid phone test.",
			)
