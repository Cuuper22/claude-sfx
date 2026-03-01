"""Tests for public API module."""

import pytest
import sfx


def test_module_version():
    """Test that __version__ is defined."""
    assert hasattr(sfx, "__version__")
    assert isinstance(sfx.__version__, str)


def test_sound_names_exported():
    """Test that SOUND_NAMES is exported."""
    assert hasattr(sfx, "SOUND_NAMES")
    assert isinstance(sfx.SOUND_NAMES, list)
    assert len(sfx.SOUND_NAMES) > 0


def test_faah_function():
    """Test faah() function."""
    result = sfx.faah()
    assert isinstance(result, bool)


def test_ding_function():
    """Test ding() function."""
    result = sfx.ding()
    assert isinstance(result, bool)


def test_yay_function():
    """Test yay() function."""
    result = sfx.yay()
    assert isinstance(result, bool)


def test_bruh_function():
    """Test bruh() function."""
    result = sfx.bruh()
    assert isinstance(result, bool)


def test_whoosh_function():
    """Test whoosh() function."""
    result = sfx.whoosh()
    assert isinstance(result, bool)


def test_play_function():
    """Test play() function."""
    result = sfx.play("faah")
    assert isinstance(result, bool)


def test_trigger_function():
    """Test trigger() function."""
    result = sfx.trigger("error")
    assert isinstance(result, bool)


def test_toggle_function():
    """Test toggle() function."""
    # Turn off
    result = sfx.toggle(on=False)
    assert result is False
    
    # Turn on
    result = sfx.toggle(on=True)
    assert result is True


def test_is_enabled_function():
    """Test is_enabled() function."""
    sfx.toggle(on=True)
    assert sfx.is_enabled() is True
    
    sfx.toggle(on=False)
    assert sfx.is_enabled() is False


def test_load_config_function():
    """Test load_config() function."""
    config = sfx.load_config()
    assert isinstance(config, dict)
    assert "enabled" in config
    assert "events" in config


def test_save_config_function():
    """Test save_config() function."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    old_env = os.environ.get('CLAUDE_SFX_CONFIG')
    os.environ['CLAUDE_SFX_CONFIG'] = tmp_path
    
    try:
        config = sfx.load_config()
        saved_path = sfx.save_config(config)
        assert os.path.isfile(saved_path)
    finally:
        if old_env:
            os.environ['CLAUDE_SFX_CONFIG'] = old_env
        else:
            del os.environ['CLAUDE_SFX_CONFIG']
        
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_generate_all_function():
    """Test generate_all() function."""
    paths = sfx.generate_all(force=False)
    assert isinstance(paths, dict)
    assert len(paths) > 0


def test_all_exports():
    """Test that __all__ contains expected exports."""
    expected = [
        "faah", "ding", "yay", "bruh", "whoosh",
        "play", "trigger", "toggle", "is_enabled",
        "load_config", "save_config", "generate_all",
        "SOUND_NAMES",
    ]
    
    for name in expected:
        assert name in sfx.__all__, f"{name} not in __all__"
        assert hasattr(sfx, name), f"{name} not exported"
