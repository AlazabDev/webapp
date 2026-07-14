import csv

import frappe


CSV_HEADERS = {
	"facility_id": "ID",
	"facility_name": "اسم الفرع / المنفذ",
	"facility_type": "نوع المرفق",
	"address": "العنوان",
	"map_link": "رابط الاتجاهات",
	"latitude": "خط العرض (Latitude)",
	"longitude": "خط الطول (Longitude)",
}


def _to_float(value):
	value = str(value or "").strip()
	return float(value) if value else None


def execute():
	csv_path = frappe.get_app_path("webapp", "public", "data", "abuauf_branches_310.csv")

	with open(csv_path, encoding="utf-8-sig", newline="") as csv_file:
		reader = csv.DictReader(csv_file, delimiter=";")
		for row in reader:
			facility_id = str(row.get(CSV_HEADERS["facility_id"]) or "").strip().upper()
			if not facility_id:
				continue

			values = {
				"facility_id": facility_id,
				"facility_name": str(row.get(CSV_HEADERS["facility_name"]) or "").strip(),
				"facility_type": str(row.get(CSV_HEADERS["facility_type"]) or "").strip(),
				"address": str(row.get(CSV_HEADERS["address"]) or "").strip(),
				"map_link": str(row.get(CSV_HEADERS["map_link"]) or "").strip(),
				"latitude": _to_float(row.get(CSV_HEADERS["latitude"])),
				"longitude": _to_float(row.get(CSV_HEADERS["longitude"])),
				"published": 1,
				"source": "abuauf_branches_310.csv",
			}

			if frappe.db.exists("Facility", facility_id):
				doc = frappe.get_doc("Facility", facility_id)
				doc.update(values)
				doc.save(ignore_permissions=True)
			else:
				frappe.get_doc({"doctype": "Facility", **values}).insert(ignore_permissions=True)
