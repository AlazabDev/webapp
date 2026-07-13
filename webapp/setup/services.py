from __future__ import annotations

import json
import re
from pathlib import Path

import frappe
from frappe import _

_RESERVED_ROUTES = {
	"api",
	"app",
	"assets",
	"desk",
	"files",
	"login",
	"logout",
	"private",
	"services",
}


def normalize_route(value: str) -> str:
	value = (value or "").strip().strip("/").lower()
	value = re.sub(r"\s+", "-", value)
	value = re.sub(r"[^a-z0-9-]+", "-", value)
	value = re.sub(r"-+", "-", value)
	return value.strip("-")


def validate_route(value: str) -> str:
	route = normalize_route(value)
	if not route:
		frappe.throw(_("Route is required and must contain Latin letters or numbers"), frappe.ValidationError)
	if route in _RESERVED_ROUTES:
		frappe.throw(_("Route {0} is reserved").format(route), frappe.ValidationError)
	return route


def _seed_path() -> Path:
	return Path(frappe.get_app_path("webapp", "setup", "data", "services.json"))


def load_default_services() -> list[dict]:
	path = _seed_path()
	if not path.is_file():
		frappe.throw(_("Service seed file is missing: {0}").format(path), frappe.ValidationError)

	with path.open(encoding="utf-8") as seed_file:
		services = json.load(seed_file)

	if not isinstance(services, list) or not services:
		frappe.throw(_("Service seed file must contain at least one service"), frappe.ValidationError)

	validated: list[dict] = []
	seen_names: set[str] = set()
	seen_routes: set[str] = set()

	for index, service in enumerate(services, start=1):
		if not isinstance(service, dict):
			frappe.throw(_("Invalid service seed record at position {0}").format(index), frappe.ValidationError)

		name = str(service.get("name") or "").strip()
		service_name = str(service.get("service_name") or "").strip()
		route = validate_route(str(service.get("route") or ""))

		if not name or not service_name:
			frappe.throw(
				_("Service seed record {0} requires name and service_name").format(index),
				frappe.ValidationError,
			)
		if name in seen_names:
			frappe.throw(_("Duplicate service name in seed data: {0}").format(name), frappe.ValidationError)
		if route in seen_routes:
			frappe.throw(_("Duplicate service route in seed data: {0}").format(route), frappe.ValidationError)

		seen_names.add(name)
		seen_routes.add(route)

		payload = dict(service)
		payload["doctype"] = "Service"
		payload["name"] = name
		payload["service_name"] = service_name
		payload["route"] = route
		validated.append(payload)

	return validated


def validate_default_services() -> None:
	load_default_services()


def ensure_default_services() -> int:
	created = 0
	for service in load_default_services():
		if frappe.db.exists("Service", service["name"]):
			continue
		if frappe.db.exists("Service", {"route": service["route"]}):
			continue
		frappe.get_doc(service).insert(ignore_permissions=True)
		created += 1
	return created
