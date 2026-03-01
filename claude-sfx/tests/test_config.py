"""Tests for configuration module."""

import json
import os
import tempfile
import pytest

from sfx.config import (
    load_config,
    save_config,
    toggle,
    is_enabled,
    get_sound_for_event,
    DEFAULT_CONFIG,
)


@pytest.fixture
def temp_config():
    """Provide a temporary config file path."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    # Set environment variable to use temp path
    old_env = os.environ.get('CLAUDE_SFX_CONFIG')
    os.environ['CLAUDE_SFX_CONFIG'] = tmp_path
    
    yield tmp_path
    
    # Cleanup
    if old_env:
        os.environ['CLAUDE_SFX_CONFIG'] = old_env
    else:
        del os.environ['CLAUDE_SFX_CONFIG']
    
    if os.path.exists(tmp_path):
        os.remove(tmp_path)


def test_default_config_structure():
    """Test DEFAULT_CONFIG has expected structure."""
    assert "enabled" in DEFAULT_CONFIG
    assert "volume" in DEFAULT_CONFIG
    assert "events" in DEFAULT_CONFIG
    assert "custom_sounds" in DEFAULT_CONFIG
    
    assert isinstance(DEFAULT_CONFIG["events"], dict)
    assert isinstance(DEFAULT_CONFIG["custom_sounds"], dict)


def test_load_config_defaults(temp_config):
    """Test loading config returns defaults when no file exists."""
    # Remove temp file if created
    if os.path.exists(temp_config):
        os.remove(temp_config)
    
    config = load_config()
    
    assert config["enabled"] is True
    assert "events" in config
    assert config["events"]["error"] == "faah"


def test_save_and_load_config(temp_config):
    """Test saving and loading config."""
    test_config = {
        "enabled": False,
        "volume": 0.5,
        "events": DEFAULT_CONFIG["events"],
        "custom_sounds": {},
    }
    
    saved_path = save_config(test_config)
    assert os.path.isfile(saved_path)
    
    loaded = load_config()
    assert loaded["enabled"] is False
    assert loaded["volume"] == 0.5


def test_toggle_on(temp_config):
    """Test toggling sounds on."""
    result = toggle(on=True)
    assert result is True
    assert is_enabled() is True


def test_toggle_off(temp_config):
    """Test toggling sounds off."""
    result = toggle(on=False)
    assert result is False
    assert is_enabled() is False


def test_toggle_flip(temp_config):
    """Test toggling without argument flips state."""
    # Set to True
    toggle(on=True)
    assert is_enabled() is True
    
    # Flip to False
    result = toggle()
    assert result is False
    assert is_enabled() is False
    
    # Flip back to True
    result = toggle()
    assert result is True
    assert is_enabled() is True


def test_is_enabled_default(temp_config):
    """Test is_enabled returns True by default."""
    if os.path.exists(temp_config):
        os.remove(temp_config)
    
    assert is_enabled() is True


def test_get_sound_for_event_builtin(temp_config):
    """Test getting sound for built-in event."""
    sound = get_sound_for_event("error")
    assert sound == "faah"
    
    sound = get_sound_for_event("prompt")
    assert sound == "ding"


def test_get_sound_for_event_custom(temp_config):
    """Test getting custom sound file for event."""
    # Create a fake custom sound file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as custom:
        custom_path = custom.name
    
    try:
        config = load_config()
        config["custom_sounds"]["error"] = custom_path
        save_config(config)
        
        sound = get_sound_for_event("error")
        assert sound == custom_path
    finally:
        if os.path.exists(custom_path):
            os.remove(custom_path)


def test_get_sound_for_event_nonexistent(temp_config):
    """Test getting sound for nonexistent event."""
    sound = get_sound_for_event("nonexistent_event")
    assert sound is None


def test_config_merges_with_defaults(temp_config):
    """Test that partial config merges with defaults."""
    partial_config = {"enabled": False}
    
    with open(temp_config, 'w') as f:
        json.dump(partial_config, f)
    
    loaded = load_config()
    
    # Should have our override
    assert loaded["enabled"] is False
    
    # Should have defaults for missing keys
    assert "events" in loaded
    assert "custom_sounds" in loaded
    assert loaded["events"]["error"] == "faah"


def test_config_handles_corrupt_json(temp_config):
    """Test that corrupt JSON falls back to defaults."""
    with open(temp_config, 'w') as f:
        f.write("{ invalid json }")
    
    config = load_config()
    
    # Should return defaults
    assert config["enabled"] is True
    assert "events" in config
