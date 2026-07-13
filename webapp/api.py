from __future__ import annotations

import re
from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import escape_html, strip_html, validate_email_address

_PHONE_DIGITS_MIN = 8
_PHONE_DIGITS_MAX = 15


def _clean_text(value, label: str, max_length: int, *, required: bool = False) -> str:
	text = strip_html(str(value or "")).strip()
	if required and not text:
		frappe.throw(_("{0} is required").format(_(label)), frappe.ValidationError)
	if len(text) > max_length:
		frappe.throw(
			_("{0} must not exceed {1} characters").format(_(label), max_length),
			frappe.ValidationError,
		)
	return text


def _clean_phone(value) -> str:
	phone = _clean_text(value, "Phone", 30, required=True)
	digits = re.sub(r"\D", "", phone)
	if not _PHONE_DIGITS_MIN <= len(digits) <= _PHONE_DIGITS_MAX:
		frappe.throw(_("Please enter a valid phone number"), frappe.ValidationError)
	return phone


def _safe_url(value) -> str:
	url = str(value or "").strip()
	if not url:
		return ""
	parsed = urlparse(url)
	return url if parsed.scheme in {"http", "https"} and parsed.netloc else ""


def _request_metadata() -> tuple[str, str]:
	request_ip = str(getattr(frappe.local, "request_ip", "") or "")[:140]
	user_agent = ""
	if frappe.request:
		user_agent = str(frappe.request.headers.get("User-Agent") or "")[:500]
	return request_ip, user_agent


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=10, seconds=15 * 60, methods="POST")
def submit_contact_form(name, email, subject, message, website=""):
	"""Persist a public contact request as a standard Frappe Communication."""
	if website:
		return {"status": "success"}

	name = _clean_text(name, "Name", 140, required=True)
	email = validate_email_address(_clean_text(email, "Email", 140, required=True), throw=True)
	subject = _clean_text(subject, "Subject", 200, required=True)
	message = _clean_text(message, "Message", 5000, required=True)

	communication = frappe.get_doc(
		{
			"doctype": "Communication",
			"sender": email,
			"sender_full_name": name,
			"subject": subject,
			"sent_or_received": "Received",
			"communication_medium": "Email",
			"content": f'<div style="white-space: pre-wrap">{escape_html(message)}</div>',
			"status": "Open",
		}
	).insert(ignore_permissions=True)

	return {"status": "success", "communication_id": communication.name}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=10, seconds=15 * 60, methods="POST")
def submit_quote_form(
	name,
	phone,
	service="",
	service_name="",
	location="",
	message="",
	email="",
	website="",
):
	"""Create a controlled Quote Request record from the public website."""
	if website:
		return {"status": "success"}
	if not frappe.db.table_exists("Quote Request"):
		frappe.throw(_("Quote requests are temporarily unavailable"), frappe.ValidationError)

	customer_name = _clean_text(name, "Name", 140, required=True)
	phone = _clean_phone(phone)
	location = _clean_text(location, "Location", 300, required=True)
	details = _clean_text(message, "Request details", 5000, required=True)
	service = _clean_text(service, "Service", 140)
	service_name = _clean_text(service_name, "Service name", 140)

	if email:
		email = validate_email_address(_clean_text(email, "Email", 140), throw=True)

	if service:
		if not frappe.db.exists("Service", {"name": service, "published": 1}):
			frappe.throw(_("The selected service is not available"), frappe.ValidationError)
		service_name = frappe.db.get_value("Service", service, "service_name") or service_name

	if not service_name:
		service_name = _("Other request")

	request_ip, user_agent = _request_metadata()
	quote_request = frappe.get_doc(
		{
			"doctype": "Quote Request",
			"naming_series": "AZ-QR-.YYYY.-.#####",
			"customer_name": customer_name,
			"phone": phone,
			"email": email,
			"service": service or None,
			"service_name": service_name,
			"project_location": location,
			"details": details,
			"source": "Website",
			"status": "New",
			"request_ip": request_ip,
			"user_agent": user_agent,
		}
	).insert(ignore_permissions=True)

	return {"status": "success", "request_id": quote_request.name}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=120, seconds=60, methods="GET")
def get_facilities():
	"""Return only published facilities and public map fields."""
	if not frappe.db.table_exists("Facility"):
		return []

	facilities = frappe.get_all(
		"Facility",
		filters={"published": 1},
		fields=[
			"facility_id",
			"facility_name",
			"facility_type",
			"address",
			"latitude",
			"longitude",
			"map_link",
		],
		order_by="facility_name asc",
		limit_page_length=1000,
	)

	for facility in facilities:
		facility.map_link = _safe_url(facility.map_link)

	return facilities
