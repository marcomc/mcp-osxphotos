# mcp-osxphotos

<!-- markdownlint-disable MD013 MD004 MD007 MD029 MD030 MD032 -->

An MCP server for interacting with the `osxphotos` CLI tool.

This project provides Model Context Protocol tools around the open source project [osxphotos](https://github.com/RhetTbull/osxphotos).

This server provides a way for AI tools that support the Model Context Protocol (MCP) to interact with your Apple Photos library through the powerful `osxphotos` command-line tool.

## Quick Index

- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Using uvx (alternative)](#using-uvx-alternative)
- [Testing](#testing)
- [Developer Documentation](#developer-documentation)
    - [Available Tools](./docs/available-tools.md)
- [Configure with common MCP clients](#configure-with-common-mcp-clients)
    - [Claude Desktop (macOS)](#claude-desktop-macos)
    - [VS Code – Continue extension](#vs-code--continue-extension)
    - [Zed editor](#zed-editor)
    - [gemini-cli (template)](#gemini-cli-template)
- [License](#license)
- [Publishing](#publishing)

## Prerequisites

This server executes the `osxphotos` CLI. The executable is discovered in this order:

1. If the environment variable `OSXPHOTOS_BIN` is set to an absolute path to the executable, that path is used.
2. Otherwise, the system `PATH` is searched (same environment as the process that launches this server).

If the executable cannot be found, tools will return a clear error message asking you to set `OSXPHOTOS_BIN` or update `PATH`.

Tip: Verify discovery with the `osxphotos_health` tool. It reports the resolved path, `--version`, and relevant environment variables. If you’re running this from an app that manages its own environment, ensure the directory that contains `osxphotos` is on `PATH` (use `which osxphotos` to find it), or set `OSXPHOTOS_BIN` to the absolute path explicitly.

Python version: This server targets Python >= 3.11. You can confirm the runtime with the `python_version` tool.

Environment configuration: This server loads a `.env` file if present (via python-dotenv). You can set `OSXPHOTOS_BIN=/absolute/path/to/osxphotos` there instead of wiring it into your client config.

## Installation and Setup

1. **Clone the repository (or create the project files):**

    ```bash
    # (If you have the project files, you can skip this step)
    git clone <repository_url>
    cd mcp-osxphotos
    ```

2. **Install dependencies with uv (optional for published usage):**

    This project uses `uv` for package management. For local development:

    ```bash
    uv sync
    ```

## Usage

To run the MCP server, execute the following command from the project's root directory:

Recommended (published package):

```bash
uvx mcp-osxphotos
```

This runs the published console script and starts the server over stdio.

Development (from local source):

```bash
uv run mcp dev src/mcp_osxphotos/server.py
```

## Using uvx (alternative)

If you prefer not to install anything locally, you can launch the server using uvx. This downloads and runs the package in an isolated environment (cached by uv).

```bash
uvx mcp-osxphotos
```

Notes:

- With `uvx`, you don’t need to install `mcp[cli]` into your venv. The `mcp` tool will be resolved automatically.
- For GUI clients (Claude, Continue, Zed, etc.), you can set the command to `uvx` and remove `run` from the args (see examples below).

## Testing

Once the server is running, you can test it using the MCP Inspector, a web-based interface for interacting with the server's tools.

1. When you start the server, it will print a URL in your terminal, usually `http://localhost:6274`.
2. Open this URL in your web browser.
3. You will see all the available tools and their parameters.
4. You can expand each tool to see its parameters, fill them with test values, and click the "Execute" button to run the tool and see the output.

## Configure with common MCP clients

Below are examples for wiring this server into popular MCP clients. For development, use an absolute path to `src/mcp_osxphotos/server.py`. For published usage, prefer the console script `mcp-osxphotos`. Set `OSXPHOTOS_BIN` if your client is a GUI app (it may not inherit your shell PATH).

Tip: After adding a server, run `python_version` and `osxphotos_health` from your client to verify the environment.

### Claude Desktop (macOS)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add an entry under `mcpServers`:

Dev config (local source):

```json
{
    "mcpServers": {
        "mcp-osxphotos": {
            "command": "uv",
            "args": ["run", "mcp", "dev", "/absolute/path/to/src/mcp_osxphotos/server.py"],
            "env": {
                "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos"
            }
        }
    }
}
```

Published config (recommended):

```json
{
    "mcpServers": {
        "mcp-osxphotos": {
            "command": "uvx",
            "args": ["mcp-osxphotos"],
            "env": {
                "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos"
            }
        }
    }
}
```

Then restart Claude Desktop.

### VS Code – Continue extension

Create or edit `~/.continue/config.json` (user-level) or `.continue/config.json` in your workspace:

Dev config (local source):

```json
{
    "mcpServers": {
        "mcp-osxphotos": {
            "command": "uv",
            "args": ["run", "mcp", "dev", "/absolute/path/to/src/mcp_osxphotos/server.py"],
            "env": {
                "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos"
            }
        }
    }
}
```

Or with published package:

```json
{
    "mcpServers": {
        "mcp-osxphotos": {
            "command": "uvx",
            "args": ["mcp-osxphotos"],
            "env": {
                "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos"
            }
        }
    }
}
```

Reload the Continue extension (or VS Code) and look for the server under Tools.

### Zed editor

Add a server entry to your Zed settings (e.g., `~/.config/zed/settings.json`). Insert under the root settings object:

Dev config (local source):

```json
{
    "mcp": {
        "servers": [
            {
                "name": "mcp-osxphotos",
                "binary": "uv",
                "args": ["run", "mcp", "dev", "/absolute/path/to/src/mcp_osxphotos/server.py"],
                "env": { "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos" }
            }
        ]
    }
}
```

Or with published package:

```json
{
    "mcp": {
        "servers": [
            {
                "name": "mcp-osxphotos",
                "binary": "uvx",
                "args": ["mcp-osxphotos"],
                "env": { "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos" }
            }
        ]
    }
}
```

Restart Zed to pick up changes.

### gemini-cli (template)

If your `gemini-cli` supports MCP servers via a config file, the entry typically follows the same pattern as above. Use this as a template and consult the `gemini-cli` documentation for the exact config path and schema:

Dev config (local source):

```json
{
    "mcpServers": {
        "mcp-osxphotos": {
            "command": "uv",
            "args": ["run", "mcp", "dev", "/absolute/path/to/src/mcp_osxphotos/server.py"],
            "env": { "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos" }
        }
    }
}
```

Or with published package:

```json
{
    "mcpServers": {
        "mcp-osxphotos": {
            "command": "uvx",
            "args": ["mcp-osxphotos"],
            "env": { "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos" }
        }
    }
}
```

Troubleshooting tips:

- GUI apps often have a minimal PATH. Prefer setting `OSXPHOTOS_BIN` to the absolute path of `osxphotos`.
- Ensure your Python matches the supported range (>= 3.12,< 3.14). Use the `python_version` tool to verify.
- Use `osxphotos_health` to confirm the resolved CLI path and version.

## Developer Documentation

See the full tool reference in docs: [docs/available-tools.md](./docs/available-tools.md).

### Notes on interactive commands

The osxphotos commands `inspect` and `repl` are intentionally not exposed as MCP tools because they require interactive terminal control and real-time user interaction with Photos or a shell session. MCP tools run as single, stateless invocations and return outputs, which is not compatible with the continuous interactive behavior expected by these commands. If you need their functionality:

- For `inspect`, run it in a local terminal while using Photos for interactive selection.
- For `repl`, open the REPL in a terminal for exploratory work, then script repeatable logic and run it via the `run` tool.

### How it Works

The tools in this server are wrappers around the `osxphotos` CLI tool. When you call a tool, the server constructs and executes the corresponding `osxphotos` command with the provided parameters. The output of the command is then returned to the client.

### Extending the Server

You can easily extend the server by adding new tools or modifying the existing ones in `src/mcp_osxphotos/server.py`.

To add a new tool, simply define a new function and decorate it with `@mcp.tool()`. The function's name will be the tool's name, and its parameters will be the tool's parameters. Inside the function, you can use the `subprocess` module to execute any `osxphotos` command you want.

### Debugging with MCP Inspector

For a great debugging experience, use the MCP Inspector:

- Published package:

    ```bash
    npx @modelcontextprotocol/inspector uvx mcp-osxphotos
    ```

- Local development:

    ```bash
    npx @modelcontextprotocol/inspector uv --directory /absolute/path/to/mcp-osxphotos run mcp dev src/mcp_osxphotos/server.py
    ```

The Inspector will display a URL you can open in your browser.

### Lockfile maintenance

If you change dependencies or project metadata, regenerate the lockfile:

```bash
uv sync
```

### Smoke tests

A tiny unittest-based smoke test suite is included to sanity-check the environment and a couple of tools:

- `python_version` returns the running Python version and executable path.
- `osxphotos_health` reports whether the `osxphotos` CLI is discoverable and, if so, where.

Run the tests with uv:

```bash
# Ensure a compatible Python is pinned (project requires >=3.11)
uv python pin 3.12

# Run unittest discovery
uv run python -m unittest discover -s tests -p 'test*.py' -q
```

Notes:

- The tests don’t require `osxphotos` to be installed; they only report discovery status. If `osxphotos` is not found, the test still passes as long as `osxphotos_health` returns the expected JSON shape.
- The tests add `src/` to `sys.path` so they work from a local checkout without installation.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Publishing

Looking to release a version users can run via `uvx mcp-osxphotos`?

- Dry run on TestPyPI: see [docs/publishing-test.md](./docs/publishing-test.md)
- Real release to PyPI: see [docs/publishing.md](./docs/publishing.md)
