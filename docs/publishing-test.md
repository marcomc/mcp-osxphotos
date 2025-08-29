# Publish to TestPyPI (dry run)

Use TestPyPI to validate packaging and metadata before a real release.

## Prerequisites

- Accounts and tokens:
  - TestPyPI account: <https://test.pypi.org/account/register/>
  - TestPyPI token: <https://test.pypi.org/manage/account/token/>
- Clean working tree and a unique version in `pyproject.toml`
  (PyPI/TestPyPI versions are immutable).
- Optional: create a fresh virtual environment to test installs.

## Build artifacts

```sh
python -m pip install --upgrade build
python -m build  # creates ./dist/*.tar.gz and ./dist/*.whl
```

## Upload to TestPyPI

```sh
python -m pip install --upgrade twine
# Use a token; use an environment variable to avoid leaking secrets
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-AgENdGVzdC5weXBpLm9yZy5..."  # from TestPyPI
python -m twine upload --repository testpypi dist/*
```

Expected result: the package appears on TestPyPI
(e.g., <https://test.pypi.org/project/mcp-osxphotos/>).

## Verify installation (optional)

Install from TestPyPI in a clean environment to ensure dependencies resolve:

```sh
python -m venv .venv-testpypi
. .venv-testpypi/bin/activate
python -m pip install --upgrade pip
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  mcp-osxphotos
# Quick smoke: ensure console script is present
mcp-osxphotos --help || true
```

Note: Some dependencies may only exist on PyPI; the `--extra-index-url`
fallback ensures they resolve.

## Cleanup / next steps

- If all looks good, repeat the steps with real PyPI (see `docs/publishing.md`).
- If you need to re-upload, bump `[project].version` in `pyproject.toml`,
  rebuild, and upload again.
