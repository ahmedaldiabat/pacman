"""Unit tests for persistent highscore handling."""
import json
import tempfile
import unittest
from pathlib import Path

from highscores import Highscores


class HighscoreTests(unittest.TestCase):
    def test_names_are_sanitized_and_top_ten_saved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "scores.json"
            scores = Highscores(str(path))
            for number in range(12):
                scores.add(f"player{number}!", number * 10)
            self.assertEqual(len(scores.entries), 10)
            self.assertEqual(scores.entries[0]["score"], 110)
            self.assertEqual(scores.entries[0]["name"], "player11")
            self.assertTrue(path.exists())
            self.assertEqual(len(json.loads(path.read_text())), 10)

    def test_corrupt_file_recovers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "scores.json"
            path.write_text("not json")
            self.assertEqual(Highscores(str(path)).entries, [])


if __name__ == "__main__":
    unittest.main()
