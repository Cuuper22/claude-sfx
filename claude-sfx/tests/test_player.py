"""Tests for audio player module."""

import os
import platform
import tempfile
import wave
import struct
import pytest

from sfx.player import play_file, _find_player, _get_player


def test_find_player():
    """Test that _find_player returns something on all platforms."""
    player = _find_player()
    
    # Should find a player on most systems, or None
    assert player is None or isinstance(player, list)
    
    if player is not None:
        assert len(player) > 0


def test_get_player_caches_result():
    """Test that _get_player caches the result."""
    import sfx.player as player_module
    
    # Reset cache
    player_module._PLAYER_RESOLVED = False
    player_module._PLAYER_CMD = None
    
    first_call = _get_player()
    second_call = _get_player()
    
    # Should return same result
    assert first_call == second_call


def test_play_file_nonexistent():
    """Test playing nonexistent file returns False."""
    result = play_file("/nonexistent/path/to/file.wav")
    assert result is False


def test_play_file_with_valid_wav():
    """Test playing a valid WAV file."""
    # Create a minimal valid WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
        
        # Write a minimal WAV (silence)
        with wave.open(tmp_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            samples = [0] * 1000
            wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    
    try:
        # Should not crash, returns True if player found
        result = play_file(tmp_path, blocking=False)
        assert isinstance(result, bool)
        
        # If we have a player, should return True
        if _get_player() is not None:
            assert result is True
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_play_file_blocking():
    """Test blocking playback mode."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
        
        with wave.open(tmp_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            samples = [0] * 100  # Very short
            wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    
    try:
        result = play_file(tmp_path, blocking=True)
        assert isinstance(result, bool)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_platform_specific_player():
    """Test that platform-specific player command is reasonable."""
    player = _find_player()
    system = platform.system()
    
    if system == "Darwin" and player:
        assert "afplay" in player[0]
    elif system == "Linux" and player:
        assert any(cmd in player[0] for cmd in ["aplay", "paplay", "pw-play", "ffplay"])
    elif system == "Windows" and player:
        assert "powershell" in player[0].lower()
