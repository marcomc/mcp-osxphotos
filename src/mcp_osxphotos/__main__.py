import asyncio

from . import server


def _run_async() -> None:
    # FastMCP-based servers are run by the MCP CLI, so we provide a tiny shim
    # that mirrors `mcp dev` behavior for stdio operation.
    # Import here in case future async setup is needed.
    pass


def main() -> None:
    # Run the FastMCP server over stdio using the MCP CLI dev launcher when invoked via console script
    # Equivalent to: uvx mcp dev /path/to/server.py
    import subprocess
    import sys as _sys
    _cmd = [
        _sys.executable,
        "-m",
        "mcp",
        "dev",
        server.__file__,
    ]
    subprocess.run(_cmd, check=True)
