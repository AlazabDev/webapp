# Changelog

All notable changes to the Alazab Website application are documented here.

## [16.0.0] - Unreleased

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
- Operational `Service` records are no longer exported as fixtures.
- Header quote action now points to `/request-quote`.

### Fixed

- Corrected the facilities API method path.
- Corrected the facilities base template and script block names.
- Added filtering so only published facilities are returned publicly.
- Completed MIT license metadata.
