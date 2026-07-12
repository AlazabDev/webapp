import frappe

def get_context(context):
    # Fetch Services if DocType exists
    if frappe.db.exists("DocType", "Service"):
        context.services = frappe.get_all(
            "Service",
            fields=["name", "service_name", "short_description", "icon", "route"],
            filters={"published": 1},
            order_by="creation asc",
            limit_page_length=6
        )
    else:
        context.services = []

    # Fetch Projects if DocType exists
    if frappe.db.exists("DocType", "Project"):
        context.projects = frappe.get_all(
            "Project",
            fields=["name", "project_name", "category", "project_image", "route"],
            filters={"published": 1},
            order_by="creation desc",
            limit_page_length=6
        )
    else:
        context.projects = []
