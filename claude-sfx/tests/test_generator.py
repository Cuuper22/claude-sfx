"""Tests for sound generator module."""

import os
import wave
import tempfile
import pytest

from sfx.generator import (
    generate_all,
    get_sound_path,
    SOUND_NAMES,
    SOUNDS_DIR,
    _write_wav,
    _fade,
)


def test_sound_names_defined():
    """Verify SOUND_NAMES is defined and not empty."""
    assert SOUND_NAMES
    assert isinstance(SOUND_NAMES, list)
    assert len(SOUND_NAMES) == 5
    assert set(SOUND_NAMES) == {"faah", "ding", "yay", "bruh", "whoosh"}


def test_generate_all():
    """Test generating all sounds."""
    paths = generate_all(force=True)
    
    assert isinstance(paths, dict)
    assert len(paths) == len(SOUND_NAMES)
    
    for name in SOUND_NAMES:
        assert name in paths
        assert os.path.isfile(paths[name])
        assert paths[name].endswith(f"{name}.wav")


def test_get_sound_path_existing():
    """Test getting path to existing sound."""
    # Generate first
    generate_all(force=True)
    
    for name in SOUND_NAMES:
        path = get_sound_path(name)
        assert os.path.isfile(path)
        assert path.endswith(f"{name}.wav")


def test_get_sound_path_generates_missing():
    """Test that get_sound_path generates missing sounds."""
    # Remove one sound file if it exists
    test_sound = "faah"
    sound_path = os.path.join(SOUNDS_DIR, f"{test_sound}.wav")
    if os.path.exists(sound_path):
        os.remove(sound_path)
    
    # Should auto-generate
    path = get_sound_path(test_sound)
    assert os.path.isfile(path)


def test_get_sound_path_invalid_name():
    """Test getting path for invalid sound name."""
    with pytest.raises(FileNotFoundError):
        get_sound_path("nonexistent_sound")


def test_generated_wav_format():
    """Test that generated WAV files have correct format."""
    paths = generate_all(force=True)
    
    for name, path in paths.items():
        with wave.open(path, "r") as wf:
            assert wf.getnchannels() == 1  # mono
            assert wf.getsampwidth() == 2  # 16-bit
            assert wf.getframerate() == 22050  # 22.05 kHz
            assert wf.getnframes() > 0  # has content


def test_sounds_have_reasonable_duration():
    """Test that sounds are between 0.2 and 1.0 seconds."""
    paths = generate_all(force=True)
    
    for name, path in paths.items():
        with wave.open(path, "r") as wf:
            duration = wf.getnframes() / wf.getframerate()
            assert 0.2 <= duration <= 1.0, f"{name} duration {duration}s out of range"


def test_write_wav():
    """Test _write_wav helper function."""
    # Create simple test samples
    samples = [int(32767 * 0.5) for _ in range(1000)]
    
    # Write to temp location
    with tempfile.TemporaryDirectory() as tmpdir:
        old_sounds_dir = os.environ.get('SOUNDS_DIR')
        
        try:
            # Temporarily change SOUNDS_DIR
            import sfx.generator as gen_module
            original_dir = gen_module.SOUNDS_DIR
            gen_module.SOUNDS_DIR = tmpdir
            
            path = _write_wav("test.wav", samples, sample_rate=22050)
            
            assert os.path.isfile(path)
            with wave.open(path, "r") as wf:
                assert wf.getnframes() == len(samples)
        finally:
            # Restore original
            gen_module.SOUNDS_DIR = original_dir


def test_fade():
    """Test _fade function applies fade in/out."""
    samples = [1000] * 1000
    
    faded = _fade(samples.copy(), fade_in=100, fade_out=100)
    
    # First sample should be 0 (full fade in)
    assert faded[0] == 0
    
    # Last sample should be 0 (full fade out)
    assert faded[-1] == 0
    
    # Middle samples should be unchanged
    assert faded[500] == 1000


def test_sounds_dir_created():
    """Test that SOUNDS_DIR is created when needed."""
    from sfx.generator import _ensure_dir
    
    _ensure_dir()
    assert os.path.isdir(SOUNDS_DIR)
