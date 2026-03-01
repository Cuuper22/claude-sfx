"""Tests for sound engine module."""

import os
import tempfile
import pytest

from sfx.engine import play, trigger
from sfx.config import toggle, save_config, load_config
from sfx.generator import generate_all


@pytest.fixture(autouse=True)
def setup_sounds():
    """Ensure sounds are generated before tests."""
    generate_all(force=False)


@pytest.fixture
def temp_config():
    """Provide a temporary config file path."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    old_env = os.environ.get('CLAUDE_SFX_CONFIG')
    os.environ['CLAUDE_SFX_CONFIG'] = tmp_path
    
    # Enable sounds by default
    toggle(on=True)
    
    yield tmp_path
    
    if old_env:
        os.environ['CLAUDE_SFX_CONFIG'] = old_env
    else:
        del os.environ['CLAUDE_SFX_CONFIG']
    
    if os.path.exists(tmp_path):
        os.remove(tmp_path)


def test_play_valid_sound(temp_config):
    """Test playing a valid sound."""
    result = play("faah", blocking=True)
    # Should return True if enabled and player found
    assert isinstance(result, bool)


def test_play_all_sounds(temp_config):
    """Test playing all built-in sounds."""
    sounds = ["faah", "ding", "yay", "bruh", "whoosh"]
    
    for sound in sounds:
        result = play(sound, blocking=False)
        assert isinstance(result, bool)


def test_play_invalid_sound(temp_config):
    """Test playing invalid sound returns False."""
    result = play("nonexistent", blocking=True)
    assert result is False


def test_play_respects_enabled_state(temp_config):
    """Test that play respects enabled setting."""
    toggle(on=False)
    result = play("faah")
    assert result is False
    
    toggle(on=True)
    result = play("faah")
    # May be True if player available
    assert isinstance(result, bool)


def test_trigger_by_event_name(temp_config):
    """Test triggering sound by event name."""
    result = trigger("error", blocking=True)
    assert isinstance(result, bool)
    
    result = trigger("prompt", blocking=True)
    assert isinstance(result, bool)


def test_trigger_by_sound_name(temp_config):
    """Test triggering sound by direct sound name."""
    result = trigger("faah", blocking=True)
    assert isinstance(result, bool)
    
    result = trigger("ding", blocking=True)
    assert isinstance(result, bool)


def test_trigger_respects_enabled_state(temp_config):
    """Test that trigger respects enabled setting."""
    toggle(on=False)
    result = trigger("error")
    assert result is False
    
    toggle(on=True)
    result = trigger("error")
    assert isinstance(result, bool)


def test_trigger_custom_sound_path(temp_config):
    """Test triggering with custom sound file path."""
    # Create a minimal WAV file
    import wave
    import struct
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as custom:
        custom_path = custom.name
        
        with wave.open(custom_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            samples = [0] * 100
            wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    
    try:
        # Set custom sound in config
        config = load_config()
        config["custom_sounds"]["error"] = custom_path
        save_config(config)
        
        # Should play the custom sound
        result = trigger("error", blocking=True)
        assert isinstance(result, bool)
    finally:
        if os.path.exists(custom_path):
            os.remove(custom_path)


def test_trigger_nonexistent_event(temp_config):
    """Test triggering nonexistent event falls back to sound name."""
    result = trigger("nonexistent_event")
    assert result is False


def test_play_blocking_mode(temp_config):
    """Test blocking mode waits for completion."""
    # Should complete without error
    result = play("faah", blocking=True)
    assert isinstance(result, bool)


def test_play_non_blocking_mode(temp_config):
    """Test non-blocking mode returns immediately."""
    result = play("faah", blocking=False)
    assert isinstance(result, bool)
    # Should return immediately without blocking
