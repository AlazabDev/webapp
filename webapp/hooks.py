app_name = "webapp"
app_title = "Alazab Website"
app_publisher = "AlazabDev"
app_description = "Official Alazab company website built on Frappe Framework"
app_email = "info@alazab.com"
app_license = "mit"

fixtures = [{"doctype": "Service", "filters": [["published", "=", 1]]}]

website_generators = ["Service"]
update_website_context = "webapp.overrides.website_context"
homepage = "site"

add_to_apps_screen = [
    {
        "name": "webapp",
        "logo": "/assets/webapp/images/logo/logo.png",
        "title": "Alazab Website",
        "route": "/site",
    }
]

web_include_css = "/assets/webapp/css/webapp.css"
