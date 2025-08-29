# Publish to PyPI (real release)

This guide covers releasing a versioned package to the Python Package Index (PyPI).

## Prerequisites

- PyPI account: <https://pypi.org/account/register/>
- PyPI API token: <https://pypi.org/manage/account/token/>
- Clean working tree and a unique version in `pyproject.toml` (versions are immutable).
- Optional: tag the release (see below).

## Build artifacts

```sh
python -m pip install --upgrade build
python -m build  # creates ./dist/*.tar.gz and ./dist/*.whl
```

## Upload to PyPI

```sh
python -m pip install --upgrade twine
# Use a token; prefer environment variables to avoid leaking secrets
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-AgEIcHlwaS5vcmc..."  # from PyPI
python -m twine upload dist/*
```

After upload, your project page will be live on PyPI (e.g., <https://pypi.org/project/mcp-osxphotos/>).

## Try it (no install needed)

Users can run your server directly with uvx:

```sh
uvx mcp-osxphotos
```

or pin a specific version:

```sh
uvx mcp-osxphotos==0.1.0
```

## Optional: Git tags

```sh
git tag -a v0.1.0 -m "release v0.1.0"
git push --tags
```

## Optional: GitHub Actions (publish on tag)

Create `.github/workflows/publish.yml` and store your token as
`PYPI_API_TOKEN` in repo secrets.

```yaml
name: Publish to PyPI
on:
  push:
    tags:
      - "v*"

jobs:
  build-and-publish:
    name: Build and Publish
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          python -m pip install build
      - name: Build
        run: python -m build
      - name: Publish
        uses: pypa/gh-action-pypi-publish@v1.10.3
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## Bumping versions

- Update `[project].version` in `pyproject.toml` before each build.
- PyPI will reject re-uploads of the same version.
