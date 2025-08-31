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


class TestBatchEditByUUID(unittest.TestCase):
    def test_smoke_invocation(self):
        # Dry run to avoid real changes; expect JSON array string
        out = server.batch_edit_by_uuid(uuid=["FAKE-UUID-1", "FAKE-UUID-2"], metadata="all", dry_run=True)
        self.assertIsInstance(out, str)
        # Should be valid JSON (list of objects with uuid/result)
        try:
            data = json.loads(out)
        except Exception as e:
            self.fail(f"Output is not valid JSON: {e}\nRaw: {out[:200]}")
        self.assertIsInstance(data, list)
        # If two UUIDs were provided, expect two entries
        self.assertEqual(len(data), 2)
        for entry in data:
            self.assertIn("uuid", entry)
            self.assertIn("result", entry)


if __name__ == '__main__':
    unittest.main()
