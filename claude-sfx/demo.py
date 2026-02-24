#!/usr/bin/env python3
"""
claude-sfx demo — run this to hear all the sounds and see the system in action.

    python3 demo.py

Generates sounds on first run, then plays them all with descriptions.
Works on macOS, Linux, and Windows (wherever a CLI audio player exists).
"""

import sys
import time

# ensure the local package is importable
sys.path.insert(0, ".")

import sfx
from sfx.generator import generate_all, SOUNDS_DIR
from sfx.config import load_config, save_config


DEMO_SCRIPT = [
    ("faah",    "error",      "FAAAH — when your build explodes 💥"),
    ("ding",    "prompt",     "ding — claude needs your attention 🔔"),
    ("yay",     "completion", "yay — task completed, dopamine hit ✓"),
    ("bruh",    "warning",    "bruh — something's sus ⚠"),
    ("whoosh",  "thinking",   "whoosh — claude is cooking 🌀"),
]


def main():
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║           claude-sfx  demo  v0.1             ║")
    print("  ║    meme sounds for your cli sessions         ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    # step 1: generate sounds
    print("  [1/3] generating .wav files...")
    paths = generate_all(force=True)
    for name, path in paths.items():
        print(f"        {name:8s} → {path}")
    print()

    # step 2: initialize config
    print("  [2/3] initializing config...")
    cfg = load_config()
    cfg["enabled"] = True
    save_config(cfg)
    print(f"        saved to: ~/.claude-sfx/settings.json")
    print()

    # step 3: play each sound
    print("  [3/3] playing sounds:\n")
    for sound_name, event_name, description in DEMO_SCRIPT:
        print(f"        ♪ {description}")
        sfx.trigger(event_name)
        time.sleep(1.2)  # wait for playback + pause
    print()

    print("  ────────────────────────────────────────────────")
    print("  all sounds generated in:  " + SOUNDS_DIR)
    print()
    print("  quick commands:")
    print("    python3 -m sfx play faah    # play the FAAAH")
    print("    python3 -m sfx test         # hear all sounds")
    print("    python3 -m sfx off          # mute everything")
    print("    python3 -m sfx on           # unmute")
    print("    python3 -m sfx status       # show config")
    print()
    print("  to integrate with claude code:")
    print("    python3 -m sfx install-hooks")
    print("  ────────────────────────────────────────────────")
    print()


if __name__ == "__main__":
    main()
