"""Unit tests for configuration validation."""
import json
import tempfile
import unittest
from pathlib import Path

from parsing import Config


class ConfigTests(unittest.TestCase):
    def test_comments_are_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text('{\n # comment\n "lives": 4, // inline comment\n "seed": 9\n}')
            config = Config(str(path)).check_config()
            self.assertEqual(config["lives"], 4)
            self.assertEqual(config["seed"], 9)

    def test_invalid_values_use_defaults_and_at_least_ten_levels(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text(json.dumps({"lives": -2, "levels": [{"width": 2,
                                                                 "height": 4}]}))
            config = Config(str(path)).check_config()
            self.assertEqual(config["lives"], 3)
            self.assertEqual(len(config["levels"]), 10)
            self.assertEqual(config["levels"][0], {"width": 15, "height": 15})


if __name__ == "__main__":
    unittest.main()
