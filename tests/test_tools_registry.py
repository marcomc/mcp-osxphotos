import os
import sys
import unittest


# Ensure we can import from src
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import mcp_osxphotos.server as server  # noqa: E402


class TestToolsRegistry(unittest.TestCase):
    def test_batch_edit_tools_registered(self):
        mcp = server.mcp
        # Use the FastMCP tool manager; if not present, skip instead of poking lazy properties
        try:
            tm = getattr(mcp, "tool_manager")
        except Exception:
            raise unittest.SkipTest("FastMCP tool_manager not accessible; skipping registry smoke test")

        tools = getattr(tm, "tools", None)
        if not isinstance(tools, dict):
            raise unittest.SkipTest("FastMCP tool_manager.tools not available; skipping registry smoke test")

        names = set(k for k in tools.keys() if isinstance(k, str))

        # Must include canonical names and not include legacy alias
        self.assertIn("batch_edit", names, f"Registered tools did not include 'batch_edit'. Found: {sorted(names)}")
        self.assertIn("batch_edit_by_uuid", names, f"Registered tools did not include 'batch_edit_by_uuid'. Found: {sorted(names)}")
        self.assertNotIn(
            "osxphotos_batch_edit",
            names,
            f"Alias tool 'osxphotos_batch_edit' should not be registered. Found: {sorted(names)}",
        )


if __name__ == "__main__":
    unittest.main()
