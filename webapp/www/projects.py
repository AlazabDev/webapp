import frappe

def get_context(context):
    if frappe.db.exists("DocType", "Project"):
        # Fetch all published projects ordered by creation date
        context.projects = frappe.get_all(
            "Project",
            fields=["name", "project_name", "category", "short_description", "project_image", "route"],
            filters={"published": 1},
            order_by="creation desc"
        )
    else:
        context.projects = []
