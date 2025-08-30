import unittest

# Ensure we can import from src
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from mcp_osxphotos.server import (  # noqa: E402
    _append_multi_arg_pairs,
    _append_multi_arg_group,
    _append_location_pair,
)


class TestArgBuilders(unittest.TestCase):
    def test_pairs_list_of_tuples(self):
        cases = [
            ("regex", [("a", "{name}"), ("b", "{uuid}")], ["--regex", "a", "{name}", "--regex", "b", "{uuid}"]),
            ("exif", [("Make", "Apple"), ("Model", "iPhone")], ["--exif", "Make", "Apple", "--exif", "Model", "iPhone"]),
            ("field", [("uuid", "{uuid}")], ["--field", "uuid", "{uuid}"]),
            ("xattr_template", [("com.example.attr", "{name}")], ["--xattr-template", "com.example.attr", "{name}"]),
            ("post_command", [("exported", "echo hi")], ["--post-command", "exported", "echo hi"]),
        ]
        for name, value, expected in cases:
            cmd: list[str] = []
            _append_multi_arg_pairs(cmd, name, value)  # type: ignore[arg-type]
            self.assertEqual(cmd, expected, f"failed for {name}")

    def test_pairs_flat_list(self):
        cmd: list[str] = []
        _append_multi_arg_pairs(cmd, "regex", ["a", "{name}", "b", "{uuid}"])  # type: ignore[arg-type]
        self.assertEqual(cmd, ["--regex", "a", "{name}", "--regex", "b", "{uuid}"])

    def test_pairs_invalid_odd_flat_list_raises(self):
        with self.assertRaises(ValueError):
            _append_multi_arg_pairs([], "regex", ["a"])  # type: ignore[arg-type]

    def test_pairs_invalid_sublist_length_raises(self):
        with self.assertRaises(ValueError):
            _append_multi_arg_pairs([], "regex", [["a", "b", "c"]])  # type: ignore[arg-type]

    def test_triples_list_of_tuples(self):
        cmd: list[str] = []
        triples = [("tmpl.mako", "{name}.json", "--foo=1"), ("t2.mako", "{uuid}.json", "--bar")] 
        _append_multi_arg_group(cmd, "sidecar_template", triples, 3)  # type: ignore[arg-type]
        self.assertEqual(cmd, [
            "--sidecar-template", "tmpl.mako", "{name}.json", "--foo=1",
            "--sidecar-template", "t2.mako", "{uuid}.json", "--bar",
        ])

    def test_triples_flat_list(self):
        cmd: list[str] = []
        flat = ["tmpl.mako", "{name}.json", "--foo=1", "t2.mako", "{uuid}.json", "--bar"]
        _append_multi_arg_group(cmd, "sidecar_template", flat, 3)  # type: ignore[arg-type]
        self.assertEqual(cmd, [
            "--sidecar-template", "tmpl.mako", "{name}.json", "--foo=1",
            "--sidecar-template", "t2.mako", "{uuid}.json", "--bar",
        ])

    def test_triples_invalid_arity_raises(self):
        with self.assertRaises(ValueError):
            _append_multi_arg_group([], "sidecar_template", ["a", "b"], 3)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            _append_multi_arg_group([], "sidecar_template", [["a", "b"]], 3)  # type: ignore[arg-type]

    def test_location_pair_tuple(self):
        cmd: list[str] = []
        handled = _append_location_pair(cmd, "location", (10.5, 20.25))
        self.assertTrue(handled)
        self.assertEqual(cmd, ["--location", "10.5", "20.25"])

    def test_location_pair_list(self):
        cmd: list[str] = []
        handled = _append_location_pair(cmd, "location", [10.0, 20.0])
        self.assertTrue(handled)
        self.assertEqual(cmd, ["--location", "10.0", "20.0"])

    def test_location_none(self):
        cmd: list[str] = []
        handled = _append_location_pair(cmd, "location", None)
        self.assertFalse(handled)
        self.assertEqual(cmd, [])

    def test_location_invalid_shapes_raise(self):
        with self.assertRaises(ValueError):
            _append_location_pair([], "location", (10.0,))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            _append_location_pair([], "location", (10.0, 20.0, 30.0))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            _append_location_pair([], "location", "10,20")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
