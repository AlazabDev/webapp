# Fixtures policy

Frappe imports every `.json` file in this directory during `install-app` and `migrate` and may overwrite matching records.

For that reason:

- Operational `Service`, `Facility`, and `Quote Request` records must not be stored here.
- `service.json` intentionally contains an empty JSON list so the historical path remains present without importing records.
- Default services are preserved in `webapp/setup/data/services.json`.
- Fresh installations use `webapp.setup.install.after_install`.
- Existing sites use the idempotent patches declared in `webapp/patches.txt`.
- Seed and patch code only creates missing records and never overwrites existing production records.
