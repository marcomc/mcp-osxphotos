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

## How to run tests

We use Python's built-in `unittest` to avoid external dependencies.

- If your editor integrates a Python environment, use it to run the discovery command.
- From a terminal (fish shell), you can run:

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
