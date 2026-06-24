import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from Flappybird import resolve_asset_path, sanitize_high_score


class SecurityHardeningTests(unittest.TestCase):
    def test_sanitize_high_score(self):
        self.assertEqual(sanitize_high_score("42"), 42)
        self.assertEqual(sanitize_high_score("-10"), 0)
        self.assertEqual(sanitize_high_score("abc"), 0)
        self.assertEqual(sanitize_high_score(999), 999)

    def test_resolve_asset_path_rejects_directory_escape(self):
        with self.assertRaises(ValueError):
            resolve_asset_path("../README.md")

    def test_resolve_asset_path_for_existing_asset(self):
        resolved = resolve_asset_path("player.png")
        self.assertTrue(resolved.exists())
        self.assertEqual(resolved.name, "player.png")


if __name__ == "__main__":
    unittest.main()
