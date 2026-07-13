# Changelog

All notable changes to the Alazab Website application are documented here.

## [16.0.1] - 2026-07-13

### Added

- Bench-native `before_install` validation for service seed data and the facility CSV source.
- Bench-native `after_install` seeding after standard DocType synchronization.
- Shared, idempotent service and facility importers used by fresh installs and migrations.
- Frappe v16 dependency contract in `pyproject.toml`.
- Tests covering the complete Bench installation contract and automatic DocType creation.

### Changed

- Operational service data is preserved under `webapp/setup/data/services.json` and inserted only when missing.
- Facility migrations validate the complete CSV before writing and no longer overwrite existing records.
- Website context and public APIs tolerate partial installation states without querying missing tables.
- Application and desktop icons use a valid non-empty local asset.
- Production instructions now use Bench commands for installation and updates.

### Security

- Service rich text is sanitized before public rendering.
- Service routes are normalized and protected from reserved Frappe routes.
- Quote requests accept only published services.

### Fixed

- Prevented Frappe fixture synchronization from overwriting operational service records.
- Ensured fresh `install-app` executions populate facilities even though migration patches are marked completed on first installation.
- Removed the fragile duplicate facility-import implementation from the migration patch.

## [16.0.0] - 2026-07-13

### Added

- `Quote Request` DocType with production naming, workflow status, source and request metadata.
- `Facility` DocType with published filtering, coordinate validation and public map fields.
- Migration patch to import the Abu Auf branch dataset from the repository CSV file.
- Rate-limited public endpoints for contact, quote requests and facilities.
- Integration tests for quote requests, contact messages and facilities.
- Production installation, configuration and upgrade documentation.

### Changed

- Application version aligned to `16.0.0`.
- Contact messages are stored as standard Frappe `Communication` records.
- Quote requests are registered before the WhatsApp handoff.
- Google Maps API key is loaded from site configuration instead of source code.
- Header quote action now points to `/request-quote`.

### Fixed

- Corrected the facilities API method path.
- Corrected the facilities base template and script block names.
- Added filtering so only published facilities are returned publicly.
- Completed MIT license metadata.
