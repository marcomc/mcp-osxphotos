# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to
Semantic Versioning.

## [Unreleased]

### Added

- Generalized multi-argument option handling for MCP tools:
  - New internal helper to append grouped arguments of arbitrary arity
    (for example, pairs and triples) when building osxphotos CLI commands.
  - Support for pair options across tools:
    `--field FIELD TEMPLATE`, `--regex REGEX TEMPLATE`,
    `--exif EXIF_TAG VALUE`, `--xattr-template ATTRIBUTE TEMPLATE`,
    `--post-command CATEGORY COMMAND`.
  - Support for triple option in export:
    `--sidecar-template MAKO_TEMPLATE_FILE SIDECAR_FILENAME_TEMPLATE OPTIONS`.
  - Location pairs for commands that accept coordinates:
    `--location LATITUDE LONGITUDE` (for example, import and batch-edit).

### Changed

- Refactored export_photos tool implementation to use the generalized
  N-arity argument helper for `--sidecar-template` and continue using pair
  handling for other multi-arg flags.
- Standardized language and formatting in documentation sections
  (indentation and list consistency).

### Fixed

- Correct handling of export `--sidecar-template` which requires three
  positional values per occurrence.
- Fixed markdown list indentation issues in the `export_photos`
  documentation that previously rendered inconsistently.

## [0.1.0] - 2025-08-30

<!-- markdownlint-disable MD024 -->
### Added
<!-- markdownlint-enable MD024 -->

- Initial release of mcp-osxphotos exposing common osxphotos CLI commands
  as MCP tools.

[Unreleased]: https://github.com/marcocmc/mcp-osxphotos/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/marcocmc/mcp-osxphotos/releases/tag/v0.1.0
