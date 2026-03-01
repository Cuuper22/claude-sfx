"""
Configuration management for claude-sfx.

Settings live in ~/.claude-sfx/settings.json (or a custom path).
Lightweight, human-editable JSON.
"""

import json
import os

DEFAULT_CONFIG_DIR = os.path.expanduser("~/.claude-sfx")
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_DIR, "settings.json")

DEFAULT_CONFIG = {
    "enabled": True,
    "volume": 0.8,
    "events": {
        "error": "faah",
        "prompt": "ding",
        "completion": "yay",
        "warning": "bruh",
        "thinking": "whoosh",
    },
    "custom_sounds": {
        # users can map event names to custom .wav file paths:
        # "error": "/path/to/my-custom-faah.wav"
    },
}


def _config_path() -> str:
    return os.environ.get("CLAUDE_SFX_CONFIG", DEFAULT_CONFIG_PATH)


def load_config() -> dict:
    """Load config from disk, falling back to defaults."""
    path = _config_path()
    if os.path.isfile(path):
        try:
            with open(path) as f:
                user_cfg = json.load(f)
            # merge with defaults so new keys are always present
            merged = {**DEFAULT_CONFIG, **user_cfg}
            merged["events"] = {**DEFAULT_CONFIG["events"], **user_cfg.get("events", {})}
            merged["custom_sounds"] = {
                **DEFAULT_CONFIG["custom_sounds"],
                **user_cfg.get("custom_sounds", {}),
            }
            return merged
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> str:
    """Save config to disk. Returns the file path."""
    path = _config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    return path


def toggle(on: bool | None = None) -> bool:
    """Toggle sounds on/off. Returns the new state."""
    cfg = load_config()
    if on is None:
        cfg["enabled"] = not cfg["enabled"]
    else:
        cfg["enabled"] = on
    save_config(cfg)
    return cfg["enabled"]


def is_enabled() -> bool:
    return load_config().get("enabled", True)


def get_sound_for_event(event: str) -> str | None:
    """
    Resolve which sound to play for a given event.
    Checks custom_sounds first, then built-in mappings.
    Returns a sound name (like 'faah') or a file path.
    """
    cfg = load_config()
    # custom path takes priority
    custom = cfg.get("custom_sounds", {}).get(event)
    if custom and os.path.isfile(custom):
        return custom
    return cfg.get("events", {}).get(event)


def get_settings() -> dict:
    """Get current settings (alias for load_config)."""
    return load_config()
