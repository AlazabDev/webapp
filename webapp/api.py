import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def submit_contact_form(name, email, subject, message):
    if not name or not email or not message:
        frappe.throw(_("Name, Email and Message are mandatory"))
        
    doc = frappe.get_doc({
        "doctype": "Website Contact",
        "sender_name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "status": "Open"
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return {"message": "success"}

@frappe.whitelist(allow_guest=True)
def submit_quote_form(name, email, phone, type="", timeline="", budget="", message=""):
    if not name or not email or not phone:
        frappe.throw(_("Name, Email and Phone are mandatory"))
        
    doc = frappe.get_doc({
        "doctype": "Quote Request",
        "customer_name": name,
        "email": email,
        "phone": phone,
        "project_type": type,
        "timeline": timeline,
        "budget": budget,
        "message": message,
        "status": "New"
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return {"message": "success"}

@frappe.whitelist(allow_guest=True)
def get_facilities():
    facilities = frappe.get_all("Facility", fields=[
        "facility_id", 
        "facility_name", 
        "facility_type", 
        "address", 
        "latitude", 
        "longitude", 
        "map_link"
    ])
    return facilities
