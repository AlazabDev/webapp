from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse

import frappe
from frappe import _

CSV_HEADERS = {
	"facility_id": "ID",
	"facility_name": "اسم الفرع / المنفذ",
	"facility_type": "نوع المرفق",
	"address": "العنوان",
	"map_link": "رابط الاتجاهات",
	"latitude": "خط العرض (Latitude)",
	"longitude": "خط الطول (Longitude)",
}


def _source_path() -> Path:
	return Path(frappe.get_app_path("webapp", "public", "data", "abuauf_branches_310.csv"))


def _parse_coordinate(value, label: str, line_number: int, minimum: float, maximum: float) -> float | None:
	text = str(value or "").strip()
	if not text:
		return None
	try:
		number = float(text)
	except ValueError:
		frappe.throw(
			_("Invalid {0} at CSV line {1}: {2}").format(label, line_number, text),
			frappe.ValidationError,
		)
	if not minimum <= number <= maximum:
		frappe.throw(
			_("{0} is out of range at CSV line {1}: {2}").format(label, line_number, text),
			frappe.ValidationError,
		)
	return number


def _validate_map_link(value, line_number: int) -> str:
	url = str(value or "").strip()
	if not url:
		return ""
	parsed = urlparse(url)
	if parsed.scheme not in {"http", "https"} or not parsed.netloc:
		frappe.throw(
			_("Invalid map link at CSV line {0}: {1}").format(line_number, url),
			frappe.ValidationError,
		)
	return url


def load_facilities() -> list[dict]:
	path = _source_path()
	if not path.is_file():
		frappe.throw(_("Facility CSV file is missing: {0}").format(path), frappe.ValidationError)

	with path.open(encoding="utf-8-sig", newline="") as csv_file:
		reader = csv.DictReader(csv_file, delimiter=";")
		fieldnames = set(reader.fieldnames or [])
		missing_headers = [header for header in CSV_HEADERS.values() if header not in fieldnames]
		if missing_headers:
			frappe.throw(
				_("Facility CSV is missing required columns: {0}").format(", ".join(missing_headers)),
				frappe.ValidationError,
			)

		facilities: list[dict] = []
		seen_ids: set[str] = set()
		for line_number, row in enumerate(reader, start=2):
			facility_id = str(row.get(CSV_HEADERS["facility_id"]) or "").strip().upper()
			if not facility_id:
				continue
			if facility_id in seen_ids:
				frappe.throw(
					_("Duplicate facility ID at CSV line {0}: {1}").format(line_number, facility_id),
					frappe.ValidationError,
				)

			facility_name = str(row.get(CSV_HEADERS["facility_name"]) or "").strip()
			facility_type = str(row.get(CSV_HEADERS["facility_type"]) or "").strip()
			if not facility_name or not facility_type:
				frappe.throw(
					_("Facility name and type are required at CSV line {0}").format(line_number),
					frappe.ValidationError,
				)

			seen_ids.add(facility_id)
			facilities.append(
				{
					"doctype": "Facility",
					"facility_id": facility_id,
					"facility_name": facility_name,
					"facility_type": facility_type,
					"address": str(row.get(CSV_HEADERS["address"]) or "").strip(),
					"map_link": _validate_map_link(row.get(CSV_HEADERS["map_link"]), line_number),
					"latitude": _parse_coordinate(
						row.get(CSV_HEADERS["latitude"]), "latitude", line_number, -90, 90
					),
					"longitude": _parse_coordinate(
						row.get(CSV_HEADERS["longitude"]), "longitude", line_number, -180, 180
					),
					"published": 1,
					"source": "abuauf_branches_310.csv",
				}
			)

	if not facilities:
		frappe.throw(_("Facility CSV does not contain any valid rows"), frappe.ValidationError)
	return facilities


def validate_facilities_source() -> None:
	load_facilities()


def import_facilities() -> int:
	created = 0
	for facility in load_facilities():
		if frappe.db.exists("Facility", facility["facility_id"]):
			continue
		frappe.get_doc(facility).insert(ignore_permissions=True)
		created += 1
	return created
