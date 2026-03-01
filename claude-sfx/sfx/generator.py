"""
Programmatic WAV sound generator — zero external dependencies.

Generates short meme-inspired sound effects as .wav files using
nothing but the stdlib `wave` + `struct` modules.
"""

from typing import List, Dict, Callable
import math
import os
import random
import struct
import wave

SAMPLE_RATE = 22050
SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")

SOUND_NAMES = ["faah", "ding", "yay", "bruh", "whoosh"]


def _ensure_dir() -> None:
    """Ensure the sounds directory exists."""
    os.makedirs(SOUNDS_DIR, exist_ok=True)


def _write_wav(filename: str, samples: List[int], sample_rate: int = SAMPLE_RATE) -> str:
    """
    Write raw 16-bit mono PCM samples to a .wav file.

    Args:
        filename: Name of the output file.
        samples: List of 16-bit PCM sample values.
        sample_rate: Sample rate in Hz.

    Returns:
        Path to the written file.
    """
    _ensure_dir()

    # Apply volume scaling from config
    try:
        from sfx.config import get_settings
        volume = get_settings().get("volume", 0.8)
        samples = [int(s * volume) for s in samples]
    except (ImportError, Exception):
        # Fallback if config isn't available during generation
        pass

    path = os.path.join(SOUNDS_DIR, filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    return path


def _fade(samples: List[int], fade_in: int = 200, fade_out: int = 800) -> List[int]:
    """
    Apply fade-in and fade-out to samples to avoid clicks.

    Args:
        samples: List of PCM samples to modify in-place.
        fade_in: Number of samples for fade-in.
        fade_out: Number of samples for fade-out.

    Returns:
        Modified samples list.
    """
    n = len(samples)
    for i in range(min(fade_in, n)):
        samples[i] = int(samples[i] * (i / fade_in))
    for i in range(min(fade_out, n)):
        idx = n - 1 - i
        samples[idx] = int(samples[idx] * (i / fade_out))
    return samples


# ── individual sound generators ─────────────────────────────────────

def _gen_faah() -> str:
    """
    THE FAAAH — a dramatic descending tone with vibrato and distortion.
    Inspired by the 2025-2026 fail meme sound.
    ~0.7 seconds of pure disappointment.
    """
    duration = 0.72
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n

        # descending frequency: 520 Hz → 140 Hz with a dramatic swoop
        freq = 520 - 380 * (progress ** 0.6)

        # add vibrato that increases over time
        vibrato = math.sin(2 * math.pi * 5.5 * t) * (12 * progress)
        freq += vibrato

        # main tone (slightly overdriven sawtooth-ish)
        phase = 2 * math.pi * freq * t
        raw = math.sin(phase) * 0.6 + math.sin(phase * 2) * 0.25 + math.sin(phase * 3) * 0.15

        # soft clip for that crunchy feel
        raw = max(-0.85, min(0.85, raw * 1.4))

        # volume envelope: quick attack, sustain, then fade
        if progress < 0.05:
            env = progress / 0.05
        elif progress < 0.7:
            env = 1.0
        else:
            env = (1.0 - progress) / 0.3

        val = int(raw * env * 28000)
        samples.append(max(-32767, min(32767, val)))

    return _write_wav("faah.wav", _fade(samples))


def _gen_ding() -> str:
    """
    Attention ding — clean bell-like tone for prompts/questions.
    ~0.4 seconds, bright and non-annoying.
    """
    duration = 0.4
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n

        freq = 880  # A5
        # bell harmonics
        raw = (
            math.sin(2 * math.pi * freq * t) * 0.5
            + math.sin(2 * math.pi * freq * 2.0 * t) * 0.3
            + math.sin(2 * math.pi * freq * 3.0 * t) * 0.12
            + math.sin(2 * math.pi * freq * 4.2 * t) * 0.08
        )

        # exponential decay
        env = math.exp(-6.0 * progress)

        val = int(raw * env * 26000)
        samples.append(max(-32767, min(32767, val)))

    return _write_wav("ding.wav", _fade(samples, fade_in=50, fade_out=200))


def _gen_yay() -> str:
    """
    Success chime — ascending two-tone with sparkle.
    ~0.5 seconds of dopamine.
    """
    duration = 0.5
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n

        # two-note ascend: C6 → E6
        if progress < 0.45:
            freq = 1047  # C6
            local_p = progress / 0.45
        else:
            freq = 1319  # E6
            local_p = (progress - 0.45) / 0.55

        raw = (
            math.sin(2 * math.pi * freq * t) * 0.55
            + math.sin(2 * math.pi * freq * 2.0 * t) * 0.25
            + math.sin(2 * math.pi * freq * 3.0 * t) * 0.1
        )

        # per-note envelope
        if local_p < 0.08:
            env = local_p / 0.08
        else:
            env = math.exp(-3.0 * (local_p - 0.08))

        val = int(raw * env * 24000)
        samples.append(max(-32767, min(32767, val)))

    return _write_wav("yay.wav", _fade(samples, fade_in=50, fade_out=300))


def _gen_bruh() -> str:
    """
    Bruh — low pitched buzzy tone. Warning energy.
    ~0.45 seconds.
    """
    duration = 0.45
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        progress = i / n

        freq = 185  # low F#
        # chunky square-ish wave
        phase = 2 * math.pi * freq * t
        raw = (
            math.sin(phase) * 0.5
            + math.sin(phase * 2) * 0.3
            + math.sin(phase * 3) * 0.2
            + math.sin(phase * 5) * 0.08
        )

        # slight pitch bend down
        freq_mod = freq - 25 * progress
        phase_mod = 2 * math.pi * freq_mod * t
        raw = raw * 0.7 + math.sin(phase_mod) * 0.3

        # envelope
        if progress < 0.06:
            env = progress / 0.06
        elif progress < 0.6:
            env = 1.0
        else:
            env = (1.0 - progress) / 0.4

        raw = max(-0.9, min(0.9, raw * 1.3))  # light saturation

        val = int(raw * env * 25000)
        samples.append(max(-32767, min(32767, val)))

    return _write_wav("bruh.wav", _fade(samples))


def _gen_whoosh() -> str:
    """
    Whoosh — filtered noise sweep for thinking/loading.
    ~0.35 seconds.
    """
    duration = 0.35
    n = int(SAMPLE_RATE * duration)
    samples = []

    rng = random.Random(42)  # deterministic noise

    # simple noise buffer
    noise = [rng.uniform(-1, 1) for _ in range(n)]

    # moving-average filter with sweep
    for i in range(n):
        progress = i / n

        # filter width sweeps from tight to wide (low→high freq)
        width = int(3 + 60 * (1 - progress))
        start = max(0, i - width)
        chunk = noise[start:i + 1]
        filtered = sum(chunk) / len(chunk) if chunk else 0

        # envelope: fade in, peak in middle, fade out
        if progress < 0.2:
            env = progress / 0.2
        elif progress < 0.5:
            env = 1.0
        else:
            env = (1.0 - progress) / 0.5

        val = int(filtered * env * 30000)
        samples.append(max(-32767, min(32767, val)))

    return _write_wav("whoosh.wav", _fade(samples, fade_in=100, fade_out=400))


# ── generate all sounds ─────────────────────────────────────────────

_GENERATORS = {
    "faah": _gen_faah,
    "ding": _gen_ding,
    "yay": _gen_yay,
    "bruh": _gen_bruh,
    "whoosh": _gen_whoosh,
}


def generate_all(force: bool = False) -> Dict[str, str]:
    """
    Generate all built-in sounds.

    Args:
        force: If True, regenerate even if files already exist.

    Returns:
        Dictionary mapping sound names to file paths.
    """
    paths: Dict[str, str] = {}
    for name, gen_fn in _GENERATORS.items():
        path = os.path.join(SOUNDS_DIR, f"{name}.wav")
        if force or not os.path.exists(path):
            paths[name] = gen_fn()
        else:
            paths[name] = path
    return paths


def get_sound_path(name: str) -> str:
    """
    Get path to a sound file, generating it if needed.

    Args:
        name: Name of the sound (e.g., 'faah', 'ding').

    Returns:
        Path to the sound file.

    Raises:
        FileNotFoundError: If the sound name is not recognized.
    """
    path = os.path.join(SOUNDS_DIR, f"{name}.wav")
    if not os.path.exists(path):
        if name in _GENERATORS:
            return _GENERATORS[name]()
        raise FileNotFoundError(f"No sound '{name}' — available: {list(_GENERATORS)}")
    return path
