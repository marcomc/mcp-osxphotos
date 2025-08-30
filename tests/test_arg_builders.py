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
    _flag,
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

    def test_field_single_flat_token_raises(self):
        with self.assertRaises(ValueError):
            _append_multi_arg_pairs([], "field", ["uuid"])  # type: ignore[arg-type]

    def test_field_odd_length_flat_list_message(self):
        try:
            _append_multi_arg_pairs([], "field", ["uuid"])  # type: ignore[arg-type]
            self.fail("Expected ValueError for odd-length 'field' flat list")
        except ValueError as e:
            msg = str(e)
            self.assertIn("object form", msg)
            self.assertIn("FIELD", msg)
            self.assertIn("TEMPLATE", msg)

    def test_regex_odd_length_flat_list_message(self):
        with self.assertRaises(ValueError) as cm:
            _append_multi_arg_pairs([], "regex", ["a"])  # type: ignore[arg-type]
        msg = str(cm.exception)
        self.assertIn("object form", msg)
        self.assertIn("REGEX", msg)
        self.assertIn("TEMPLATE", msg)

    def test_exif_odd_length_flat_list_message(self):
        with self.assertRaises(ValueError) as cm:
            _append_multi_arg_pairs([], "exif", ["Make"])  # type: ignore[arg-type]
        msg = str(cm.exception)
        self.assertIn("object form", msg)
        self.assertIn("EXIF_TAG", msg)
        self.assertIn("VALUE", msg)

    def test_xattr_template_odd_length_flat_list_message(self):
        with self.assertRaises(ValueError) as cm:
            _append_multi_arg_pairs([], "xattr_template", ["com.example"])  # type: ignore[arg-type]
        msg = str(cm.exception)
        self.assertIn("object form", msg)
        self.assertIn("ATTRIBUTE", msg)
        self.assertIn("TEMPLATE", msg)

    def test_post_command_odd_length_flat_list_message(self):
        with self.assertRaises(ValueError) as cm:
            _append_multi_arg_pairs([], "post_command", ["exported"])  # type: ignore[arg-type]
        msg = str(cm.exception)
        self.assertIn("object form", msg)
        self.assertIn("CATEGORY", msg)
        self.assertIn("COMMAND", msg)

    def test_sidecar_template_wrong_group_size_message(self):
        with self.assertRaises(ValueError) as cm:
            _append_multi_arg_group([], "sidecar_template", [["t.mako", "{name}.json"]], 3)  # type: ignore[arg-type]
        msg = str(cm.exception)
        self.assertIn("object form", msg)
        self.assertIn("MAKO_TEMPLATE_FILE", msg)
        self.assertIn("SIDECAR_FILENAME_TEMPLATE", msg)
        self.assertIn("OPTIONS", msg)

    def test_sidecar_template_object_missing_keys_message(self):
        with self.assertRaises(ValueError) as cm:
            _append_multi_arg_group([], "sidecar_template", [{"mako_template": "t.mako"}], 3)  # type: ignore[arg-type]
        msg = str(cm.exception)
        self.assertIn("object form", msg)
        self.assertIn("mako_template", msg)
        self.assertIn("filename_template", msg)
        self.assertIn("options", msg)

    def test_flag_overrides(self):
        self.assertEqual(_flag("print_template"), "--print")
        self.assertEqual(_flag("exiftool_flag"), "--exiftool")


if __name__ == "__main__":
    unittest.main()
