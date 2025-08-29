import json
import os
import sys
import unittest

# Ensure src/ is on sys.path so we can import the package in editable/dev mode
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from mcp_osxphotos import server  # noqa: E402


class SmokeTests(unittest.TestCase):
    def test_python_version_tool(self):
        out = server.python_version()
        data = json.loads(out)
        self.assertIn('version', data)
        self.assertIn('executable', data)
        # Basic sanity: the running executable path should exist
        self.assertTrue(os.path.exists(data['executable']))

    def test_osxphotos_health_tool(self):
        out = server.osxphotos_health()
        data = json.loads(out)
        # Should always return a dict with at least 'found' (bool)
        self.assertIn('found', data)
        self.assertIsInstance(data['found'], bool)
        # If found, ensure path exists
        if data['found']:
            self.assertTrue(os.path.exists(data['path']))


if __name__ == '__main__':
    unittest.main()