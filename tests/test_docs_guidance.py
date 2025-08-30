import os
import sys
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import mcp_osxphotos.server as server  # noqa: E402


class TestDocsGuidance(unittest.TestCase):
    def test_query_photos_doc_mentions_label_singular(self):
        doc = server.query_photos.__doc__ or ""
        self.assertIn("Use 'label' (singular)", doc)
        self.assertIn('Example: label=["Welsh Terrier"]', doc)


if __name__ == "__main__":
    unittest.main()
