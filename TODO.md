# TODO

Project-wide tasks and ideas. Use checkboxes for easy tracking.

## Testing

- [ ] Unit tests for CLI arg builders
  - [ ] Pairs: `--field`, `--regex`, `--exif`, `--xattr-template`, `--post-command`
  - [ ] Triples: `--sidecar-template`
  - [ ] Location pairs: `--location` validation (lat/lon shape and numeric types)
- [ ] Smoke tests for each MCP tool invoking `osxphotos --help` to ensure
  command availability
- [ ] End-to-end test running a no-op export to a temp dir
  (use a tiny Photos library fixture)

## Documentation

- [ ] Normalize "Usage: --regex REGEX TEMPLATE" note across all relevant tools
- [ ] Add examples for complex flags (pairs/triples) with both flat list and
  list-of-lists input forms
- [ ] Document error messages for malformed multi-arg input

## Developer Experience

- [ ] Makefile or `uv` scripts for common tasks (lint, test, typecheck)
- [ ] Type hints for helper functions and public tool signatures
- [ ] Pre-commit hooks (black, isort, ruff, markdownlint)

## Enhancements

- [ ] Better error mapping: parse `osxphotos` stderr and return structured MCP errors
- [ ] Timeout and cancellation support for long-running CLI operations
- [ ] Optional dry-run mode where available
- [ ] Cache CLI `--help` outputs to speed up schema generation
