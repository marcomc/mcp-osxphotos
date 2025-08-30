import inspect
import os
import sys
import types
import unittest
from typing import get_type_hints

# Ensure src on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import mcp_osxphotos.server as server  # noqa: E402


class TestSchemaShapes(unittest.TestCase):
    def test_no_tuple_annotations_for_multi_args(self):
        """
        Ensure multi-argument options are not annotated with Tuple[...] so
        downstream JSON Schema does not use 'prefixItems'. We expect TypedDict
        list forms instead.
        """
        funcs = [
            server.add_locations,
            server.dump,
            server.export_photos,
            server.push_exif,
            server.query_photos,
            server.sync,
        ]
        for fn in funcs:
            hints = get_type_hints(fn)
            for name, t in hints.items():
                if name in {"regex", "exif", "field", "xattr_template", "post_command", "sidecar_template"}:
                    # We expect List[TypedDict] style; no Tuple in the repr
                    rep = repr(t)
                    self.assertNotIn("Tuple", rep, f"{fn.__name__}.{name} should not be a Tuple-based type: {rep}")

    def test_helpers_accept_object_forms(self):
        cmd = []
        server._append_multi_arg_pairs(cmd, "regex", [{"pattern": "a", "template": "{name}"}])
        self.assertEqual(cmd, ["--regex", "a", "{name}"])
        cmd = []
        server._append_multi_arg_pairs(cmd, "exif", [{"tag": "Make", "value": "Apple"}])
        self.assertEqual(cmd, ["--exif", "Make", "Apple"])
        cmd = []
        server._append_multi_arg_pairs(cmd, "field", [{"field": "uuid", "template": "{uuid}"}])
        self.assertEqual(cmd, ["--field", "uuid", "{uuid}"])
        cmd = []
        server._append_multi_arg_pairs(cmd, "xattr_template", [{"attribute": "com.example", "template": "{name}"}])
        self.assertEqual(cmd, ["--xattr-template", "com.example", "{name}"])
        cmd = []
        server._append_multi_arg_pairs(cmd, "post_command", [{"category": "exported", "command": "echo hi"}])
        self.assertEqual(cmd, ["--post-command", "exported", "echo hi"])

    def test_triple_helper_accepts_object_form(self):
        cmd = []
        server._append_multi_arg_group(cmd, "sidecar_template", [{
            "mako_template": "t.mako",
            "filename_template": "{name}.json",
            "options": "--foo=1",
        }], 3)
        self.assertEqual(cmd, [
            "--sidecar-template", "t.mako", "{name}.json", "--foo=1",
        ])


if __name__ == "__main__":
    unittest.main()
