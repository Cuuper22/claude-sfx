"""
Tests for claude-sfx package.

Run with: python -m pytest claude-sfx/tests/
or: python -m unittest discover -s claude-sfx/tests/
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

# Import from the package
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from sfx.generator import generate_all, get_sound_path, SOUND_NAMES
from sfx.config import load_config, save_config, toggle, get_settings


class TestSoundGeneration(unittest.TestCase):
    """Test that all sounds generate valid WAV files."""

    def test_all_sounds_generate_valid_wav(self):
        """Test that all 5 sounds generate valid WAV files with RIFF header."""
        paths = generate_all(force=True)

        # Check we got all 5 sounds
        self.assertEqual(len(paths), 5)
        for name in SOUND_NAMES:
            self.assertIn(name, paths)

        # Check each file has valid RIFF header
        for name, path in paths.items():
            self.assertTrue(os.path.exists(path), f"{name}.wav was not created")

            with open(path, "rb") as f:
                header = f.read(12)
                self.assertGreaterEqual(len(header), 12, f"{name}.wav is too small")

                # Check RIFF header
                self.assertEqual(header[0:4], b"RIFF", f"{name}.wav missing RIFF header")
                self.assertEqual(header[8:12], b"WAVE", f"{name}.wav missing WAVE format")

    def test_get_sound_path_generates_if_missing(self):
        """Test that get_sound_path generates sounds on demand."""
        # This should work even if file doesn't exist
        path = get_sound_path("ding")
        self.assertTrue(os.path.exists(path))

        # Verify it's a valid WAV
        with open(path, "rb") as f:
            header = f.read(4)
            self.assertEqual(header, b"RIFF")


class TestConfig(unittest.TestCase):
    """Test configuration loading and saving."""

    def setUp(self):
        """Set up a temporary config directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "settings.json")
        os.environ["CLAUDE_SFX_CONFIG"] = self.config_path

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
        if "CLAUDE_SFX_CONFIG" in os.environ:
            del os.environ["CLAUDE_SFX_CONFIG"]

    def test_load_config_defaults(self):
        """Test that load_config returns defaults when no file exists."""
        cfg = load_config()

        self.assertIn("enabled", cfg)
        self.assertIn("volume", cfg)
        self.assertIn("events", cfg)
        self.assertIn("custom_sounds", cfg)

        # Check defaults
        self.assertTrue(cfg["enabled"])
        self.assertEqual(cfg["volume"], 0.8)
        self.assertIn("error", cfg["events"])

    def test_save_and_load_config(self):
        """Test that config can be saved and loaded correctly."""
        test_config = {
            "enabled": False,
            "volume": 0.5,
            "events": {"error": "custom"},
            "custom_sounds": {}
        }

        save_config(test_config)
        loaded = load_config()

        self.assertEqual(loaded["enabled"], False)
        self.assertEqual(loaded["volume"], 0.5)
        self.assertEqual(loaded["events"]["error"], "custom")

    def test_get_settings(self):
        """Test that get_settings returns config."""
        settings = get_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn("volume", settings)


class TestToggle(unittest.TestCase):
    """Test toggle on/off functionality."""

    def setUp(self):
        """Set up a temporary config directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "settings.json")
        os.environ["CLAUDE_SFX_CONFIG"] = self.config_path

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
        if "CLAUDE_SFX_CONFIG" in os.environ:
            del os.environ["CLAUDE_SFX_CONFIG"]

    def test_toggle_on(self):
        """Test turning sounds on."""
        result = toggle(on=True)
        self.assertTrue(result)

        cfg = load_config()
        self.assertTrue(cfg["enabled"])

    def test_toggle_off(self):
        """Test turning sounds off."""
        result = toggle(on=False)
        self.assertFalse(result)

        cfg = load_config()
        self.assertFalse(cfg["enabled"])

    def test_toggle_flip(self):
        """Test toggling without arguments flips the state."""
        # Start with on
        toggle(on=True)

        # Flip to off
        result = toggle()
        self.assertFalse(result)

        # Flip back to on
        result = toggle()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
