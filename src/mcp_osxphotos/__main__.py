from . import server


def main() -> None:
    """Console script entrypoint that runs the FastMCP server over stdio.

    This MUST NOT emit any non-JSON to stdout. Avoid `mcp dev` here because it prints
    banners/tooling helpers that will break clients expecting pure JSON-RPC over stdio.
    """
    server.mcp.run()
