# Tests

This directory contains the unit and smoke tests for the mcp-osxphotos project.

## What is covered

- Arg builder unit tests (`test_arg_builders.py`)
  - Pairs (List[Tuple[str, str]]):
    `--field`, `--regex`, `--exif`, `--xattr-template`, `--post-command`
    - Accept both list-of-tuples and flat list inputs, and verify
      correct CLI expansion
    - Verify error handling for odd-length flat list or invalid
      sublist arity
  - Triples (List[Tuple[str, str, str]]): `--sidecar-template`
    - Accept both list-of-tuples and flat list inputs
    - Verify error handling for invalid arity
  - Location pairs: `--location`
    - Accept `(lat, lon)` tuples and `[lat, lon]` lists
    - Reject invalid shapes/types; return value indicates whether the flag was appended
- Smoke tests (`test_smoke.py`)
  - Basic sanity for the MCP runtime and environment discovery
    (no `osxphotos` invocation required)

- Schema shape tests (`test_schema_shapes.py`)
  - Guard against tuple-based annotations that could produce JSON Schema
    `prefixItems` (e.g., List[Tuple[...]]). Ensures multi-arg params use
    list-of-objects (TypedDict) in tool signatures.
  - Verifies helpers accept object-form inputs for pairs and triples.

## How to run tests

We use Python's built-in `unittest` to avoid external dependencies.

- Recommended options:
  - VS Code: Run the task "unittest: discover" from the Command Palette.
  - Makefile: `make test`
  - Direct (fish shell): run the command below.

```fish
# Run all tests discovered under tests/
./.venv/bin/python \
  -m unittest discover -s tests -p 'test*.py' -q
```

If you have a different virtual environment or interpreter,
adjust the Python path accordingly.

## Adding new tests

- Create a new file named `test_*.py` under this `tests/` folder.
- Prefer focused unit tests for internal helpers and parameter builders.
- For MCP tools that call `osxphotos`, prefer smoke tests that do not
  require a Photos library; consider invoking
  `osxphotos help <command>` in a separate test module guarded by an
  environment check when you add those later.

## Notes

- Tests are intentionally decoupled from pytest; if you want to add
  pytest later, we can include it behind optional tooling.
- The existing VS Code task for pytest was removed/adjusted because the
  matcher was unsupported. You can add a task for the unittest command
  if desired.
