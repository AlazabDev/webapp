import frappe
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9أ-ي\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def create_doctypes():
    print("Setting up Alazab Webapp DocTypes...")
    
    # Check and create Project DocType
    if not frappe.db.exists("DocType", "Project"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "webapp",
            "custom": 1,
            "name": "Project",
            "naming_rule": "By fieldname",
            "autoname": "field:project_name",
            "fields": [
                {"fieldname": "project_name", "fieldtype": "Data", "label": "Project Name", "reqd": 1, "unique": 1},
                {"fieldname": "category", "fieldtype": "Data", "label": "Category"},
                {"fieldname": "short_description", "fieldtype": "Small Text", "label": "Short Description"},
                {"fieldname": "description", "fieldtype": "Text Editor", "label": "Description"},
                {"fieldname": "project_image", "fieldtype": "Attach Image", "label": "Project Image"},
                {"fieldname": "published", "fieldtype": "Check", "label": "Published", "default": "1"},
                {"fieldname": "route", "fieldtype": "Data", "label": "Route", "reqd": 1, "unique": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Project DocType Created.")

    # Check and create Client DocType
    if not frappe.db.exists("DocType", "Client"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "webapp",
            "custom": 1,
            "name": "Client",
            "naming_rule": "By fieldname",
            "autoname": "field:client_name",
            "fields": [
                {"fieldname": "client_name", "fieldtype": "Data", "label": "Client Name", "reqd": 1, "unique": 1},
                {"fieldname": "client_logo", "fieldtype": "Attach Image", "label": "Client Logo"},
                {"fieldname": "published", "fieldtype": "Check", "label": "Published", "default": "1"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Client DocType Created.")

    # Check and create Web Settings DocType (Single)
    if not frappe.db.exists("DocType", "Alazab Settings"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "webapp",
            "custom": 1,
            "name": "Alazab Settings",
            "issingle": 1,
            "fields": [
                {"fieldname": "company_email", "fieldtype": "Data", "label": "Company Email"},
                {"fieldname": "company_phone", "fieldtype": "Data", "label": "Company Phone"},
                {"fieldname": "company_address", "fieldtype": "Data", "label": "Company Address"},
                {"fieldname": "facebook", "fieldtype": "Data", "label": "Facebook Link"},
                {"fieldname": "instagram", "fieldtype": "Data", "label": "Instagram Link"},
                {"fieldname": "linkedin", "fieldtype": "Data", "label": "LinkedIn Link"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Alazab Settings DocType Created.")

    # Check and create Website Contact DocType
    if not frappe.db.exists("DocType", "Website Contact"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "webapp",
            "custom": 1,
            "name": "Website Contact",
            "naming_rule": "Expression",
            "autoname": "MSG-.YYYY.-.#####",
            "fields": [
                {"fieldname": "sender_name", "fieldtype": "Data", "label": "Name", "reqd": 1},
                {"fieldname": "email", "fieldtype": "Data", "label": "Email", "reqd": 1},
                {"fieldname": "subject", "fieldtype": "Data", "label": "Subject", "reqd": 1},
                {"fieldname": "message", "fieldtype": "Small Text", "label": "Message", "reqd": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Open\nClosed", "default": "Open"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Website Contact DocType Created.")

    # Check and create Quote Request DocType
    if not frappe.db.exists("DocType", "Quote Request"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "webapp",
            "custom": 1,
            "name": "Quote Request",
            "naming_rule": "Expression",
            "autoname": "QUOTE-.YYYY.-.#####",
            "fields": [
                {"fieldname": "customer_name", "fieldtype": "Data", "label": "Name", "reqd": 1},
                {"fieldname": "email", "fieldtype": "Data", "label": "Email", "reqd": 1},
                {"fieldname": "phone", "fieldtype": "Data", "label": "Phone", "reqd": 1},
                {"fieldname": "project_type", "fieldtype": "Data", "label": "Project Type"},
                {"fieldname": "timeline", "fieldtype": "Data", "label": "Timeline"},
                {"fieldname": "budget", "fieldtype": "Data", "label": "Budget"},
                {"fieldname": "message", "fieldtype": "Text", "label": "Message"},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "New\nContacted\nClosed", "default": "New"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Quote Request DocType Created.")

    # Check and create Facility DocType
    if not frappe.db.exists("DocType", "Facility"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "module": "webapp",
            "custom": 1,
            "name": "Facility",
            "naming_rule": "By fieldname",
            "autoname": "field:facility_id",
            "fields": [
                {"fieldname": "facility_id", "fieldtype": "Data", "label": "Facility ID", "reqd": 1, "unique": 1},
                {"fieldname": "facility_name", "fieldtype": "Data", "label": "Name", "reqd": 1},
                {"fieldname": "facility_type", "fieldtype": "Data", "label": "Type"},
                {"fieldname": "address", "fieldtype": "Data", "label": "Address"},
                {"fieldname": "latitude", "fieldtype": "Data", "label": "Latitude"},
                {"fieldname": "longitude", "fieldtype": "Data", "label": "Longitude"},
                {"fieldname": "map_link", "fieldtype": "Data", "label": "Map Link"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("Facility DocType Created.")

    frappe.db.commit()

def import_abuauf_projects():
    projects_data = [
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – المشاية 1", "desc": "المنصورة - إنشاء وتجهيز فرع أبو عوف – المشاية 1"},
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – المشاية 2", "desc": "المنصورة - إنشاء وتجهيز فرع أبو عوف – المشاية 2"},
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – شارع قناة السويس، المنصورة", "desc": "المنصورة - تجهيز فرع أبو عوف – شارع قناة السويس، المنصورة"},
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – شارع عبد السلام عارف، المنصورة", "desc": "المنصورة - تجهيز فرع أبو عوف – شارع عبد السلام عارف، المنصورة"},
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – شارع الترعة، المنصورة", "desc": "المنصورة - إنشاء وتجهيز فرع أبو عوف – شارع الترعة، المنصورة"},
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – الوكالة، المنصورة", "desc": "المنصورة - تجهيز فرع أبو عوف – الوكالة، المنصورة"},
        {"category": "المنصورة", "name": "تجهيز فرع أبو عوف – المنصورة مول", "desc": "المنصورة - تجهيز فرع أبو عوف – المنصورة مول"},

        {"category": "الدلتا", "name": "تجهيز فرع أبو عوف – طلبة عويضة، الزقازيق", "desc": "الدلتا - تجهيز فرع أبو عوف – طلبة عويضة، الزقازيق"},
        {"category": "الدلتا", "name": "تجهيز فرع أبو عوف – الاستاد، طنطا", "desc": "الدلتا - تجهيز فرع أبو عوف – الاستاد، طنطا"},
        {"category": "الدلتا", "name": "تجهيز فرع أبو عوف – الكورنيش، بنها", "desc": "الدلتا - تجهيز فرع أبو عوف – الكورنيش، بنها"},

        {"category": "أسيوط", "name": "تجهيز فرع أبو عوف – الأزهر، أسيوط", "desc": "أسيوط - تجهيز فرع أبو عوف – الأزهر، أسيوط"},
        {"category": "أسيوط", "name": "تجهيز فرع أبو عوف – الجمهورية، أسيوط", "desc": "أسيوط - تجهيز فرع أبو عوف – الجمهورية، أسيوط"},
        {"category": "أسيوط", "name": "تجهيز فرع أبو عوف – أسيوط الجديدة", "desc": "أسيوط - تجهيز فرع أبو عوف – أسيوط الجديدة"},

        {"category": "السويس", "name": "تجهيز فرع أبو عوف – الملاحات، السويس", "desc": "السويس - تجهيز فرع أبو عوف – الملاحات، السويس"},
        {"category": "السويس", "name": "تجهيز فرع أبو عوف – الأربعين، السويس", "desc": "السويس - تجهيز فرع أبو عوف – الأربعين، السويس"},

        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – محطة الرمل، الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – محطة الرمل، الإسكندرية"},
        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – لوران، الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – لوران، الإسكندرية"},
        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – جنكليز، الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – جنكليز، الإسكندرية"},
        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – الإقبال، الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – الإقبال، الإسكندرية"},
        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – البطاش، الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – البطاش، الإسكندرية"},
        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – كارفور الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – كارفور الإسكندرية"},
        {"category": "الإسكندرية", "name": "تجهيز فرع أبو عوف – كورنيش الإسكندرية", "desc": "الإسكندرية - تجهيز فرع أبو عوف – كورنيش الإسكندرية"},

        {"category": "نادي وادي دجلة", "name": "تجهيز فرع أبو عوف – نادي وادي دجلة أكتوبر", "desc": "نادي وادي دجلة - تجهيز فرع أبو عوف – نادي وادي دجلة أكتوبر"},
        {"category": "نادي وادي دجلة", "name": "تجهيز فرع أبو عوف – نادي وادي دجلة الشيخ زايد", "desc": "نادي وادي دجلة - تجهيز فرع أبو عوف – نادي وادي دجلة الشيخ زايد"},
        {"category": "نادي وادي دجلة", "name": "تجهيز فرع أبو عوف – نادي وادي دجلة التجمع", "desc": "نادي وادي دجلة - تجهيز فرع أبو عوف – نادي وادي دجلة التجمع"},
        {"category": "نادي وادي دجلة", "name": "تجهيز فرع أبو عوف – نادي وادي دجلة المعادي", "desc": "نادي وادي دجلة - تجهيز فرع أبو عوف – نادي وادي دجلة المعادي"},

        {"category": "القاهرة الكبرى", "name": "تجهيز فرع أبو عوف – المقطم", "desc": "القاهرة الكبرى - تجهيز فرع أبو عوف – المقطم"},
        {"category": "القاهرة الكبرى", "name": "تجهيز فرع أبو عوف – شارع 50، المعادي", "desc": "القاهرة الكبرى - تجهيز فرع أبو عوف – شارع 50، المعادي"},

        {"category": "التجمع الخامس", "name": "تجهيز فرع أبو عوف – أربيلا، التجمع الخامس", "desc": "التجمع الخامس - تجهيز فرع أبو عوف – أربيلا، التجمع الخامس"},
        {"category": "التجمع الخامس", "name": "تجهيز فرع أبو عوف – كونكورد، التجمع الخامس", "desc": "التجمع الخامس - تجهيز فرع أبو عوف – كونكورد، التجمع الخامس"},
        {"category": "التجمع الخامس", "name": "تجهيز فرع أبو عوف – داون تاون، التجمع الخامس", "desc": "التجمع الخامس - تجهيز فرع أبو عوف – داون تاون، التجمع الخامس"},
        {"category": "التجمع الخامس", "name": "تجهيز فرع أبو عوف – المستشفى الجوي، التجمع الخامس", "desc": "التجمع الخامس - تجهيز فرع أبو عوف – المستشفى الجوي، التجمع الخامس"},
        {"category": "التجمع الخامس", "name": "تجهيز فرع أبو عوف – الشريفات، التجمع الخامس", "desc": "التجمع الخامس - تجهيز فرع أبو عوف – الشريفات، التجمع الخامس"},

        {"category": "الزمالك", "name": "تجهيز فرع أبو عوف – شارع طه حسين، الزمالك", "desc": "الزمالك - تجهيز فرع أبو عوف – شارع طه حسين، الزمالك"},
        {"category": "الزمالك", "name": "تجهيز فرع أبو عوف – شارع البرازيل، الزمالك", "desc": "الزمالك - تجهيز فرع أبو عوف – شارع البرازيل، الزمالك"},
        {"category": "الزمالك", "name": "تجهيز فرع أبو عوف – نادي الزمالك", "desc": "الزمالك - تجهيز فرع أبو عوف – نادي الزمالك"},

        {"category": "الجيزة والمهندسين", "name": "تجهيز فرع أبو عوف – شارع مصدق", "desc": "الجيزة والمهندسين - تجهيز فرع أبو عوف – شارع مصدق، الدقي"},
        {"category": "الجيزة والمهندسين", "name": "تجهيز فرع أبو عوف – شارع سوريا", "desc": "الجيزة والمهندسين - تجهيز فرع أبو عوف – شارع سوريا، المهندسين"},
        {"category": "الجيزة والمهندسين", "name": "تجهيز فرع أبو عوف – جامعة القاهرة", "desc": "الجيزة والمهندسين - تجهيز فرع أبو عوف – جامعة القاهرة"},

        {"category": "الرحاب", "name": "تجهيز فرع أبو عوف – السوق الشرقي، الرحاب", "desc": "الرحاب - تجهيز فرع أبو عوف – السوق الشرقي، الرحاب"},
        {"category": "الرحاب", "name": "تجهيز فرع أبو عوف – أفنيو مول، الرحاب", "desc": "الرحاب - تجهيز فرع أبو عوف – أفنيو مول، الرحاب"},

        {"category": "البحر الأحمر", "name": "تجهيز فرع أبو عوف – شارع شيراتون، الغردقة", "desc": "البحر الأحمر - تجهيز فرع أبو عوف – شارع شيراتون، الغردقة"},

        {"category": "الساحل الشمالي", "name": "تجهيز فرع أبو عوف – مارينا، الساحل الشمالي", "desc": "الساحل الشمالي - تجهيز فرع أبو عوف – مارينا، الساحل الشمالي"},
        {"category": "الساحل الشمالي", "name": "تجهيز فرع أبو عوف – هاسيندا، الساحل الشمالي", "desc": "الساحل الشمالي - تجهيز فرع أبو عوف – هاسيندا، الساحل الشمالي"},

        {"category": "الشيخ زايد", "name": "تجهيز وتشطيب فرع أبو عوف – أركان مول، الشيخ زايد", "desc": "الشيخ زايد - تجهيز وتشطيب فرع أبو عوف – أركان مول، الشيخ زايد"}
    ]

    print(f"Starting import of {len(projects_data)} projects...")
    
    for idx, p in enumerate(projects_data):
        route = f"project/{slugify(p['name'])}"
        
        if not frappe.db.exists("Project", p["name"]):
            doc = frappe.get_doc({
                "doctype": "Project",
                "project_name": p["name"],
                "category": p["category"],
                "short_description": p["desc"],
                "description": p["desc"],
                "route": route,
                "published": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"[{idx+1}/{len(projects_data)}] Inserted: {p['name']}")
        else:
            print(f"[{idx+1}/{len(projects_data)}] Skipped (Already exists): {p['name']}")

    frappe.db.commit()

def import_facilities():
    import csv
    import os
    
    # Path to CSV file
    csv_path = frappe.get_app_path("webapp", "public", "data", "abuauf_branches_310.csv")
    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
        return
        
    print("Importing Facilities from CSV...")
    count = 0
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        
        for row in csv_reader:
            try:
                fid = row.get("ID", "").strip()
                if not fid: continue
                
                if not frappe.db.exists("Facility", fid):
                    doc = frappe.get_doc({
                        "doctype": "Facility",
                        "facility_id": fid,
                        "facility_name": row.get("اسم الفرع / المنفذ", "").strip(),
                        "facility_type": row.get("نوع المرفق", "").strip(),
                        "address": row.get("العنوان", "").strip(),
                        "map_link": row.get("رابط الاتجاهات", "").strip(),
                        "latitude": row.get("خط العرض (Latitude)", "").strip(),
                        "longitude": row.get("خط الطول (Longitude)", "").strip()
                    })
                    doc.insert(ignore_permissions=True)
                    count += 1
            except Exception as e:
                print(f"Failed to insert facility {fid}: {str(e)}")
                
    frappe.db.commit()
    print(f"Imported {count} new facilities successfully.")

def run_all():
    """
    This function should be executed via 'bench execute webapp.setup.run_all'.
    It securely initializes all required WebApp DocTypes and Imports Initial Data
    within the Frappe Environment.
    """
    create_doctypes()
    import_abuauf_projects()
    import_facilities()
    print("Done setting up webapp.")
