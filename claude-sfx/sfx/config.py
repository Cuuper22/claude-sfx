"""
Configuration management for claude-sfx.

Settings live in ~/.claude-sfx/settings.json (or a custom path).
Lightweight, human-editable JSON.
"""

from typing import Dict, Optional, Any
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
    """Get the configuration file path from environment or use default."""
    return os.environ.get("CLAUDE_SFX_CONFIG", DEFAULT_CONFIG_PATH)


def load_config() -> Dict[str, Any]:
    """
    Load configuration from disk, falling back to defaults.

    Returns:
        Dictionary containing the merged configuration.
    """
    path = _config_path()
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
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


def save_config(config: Dict[str, Any]) -> str:
    """
    Save configuration to disk.

    Args:
        config: Configuration dictionary to save.

    Returns:
        The file path where config was saved.
    """
    path = _config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    return path


def toggle(on: Optional[bool] = None) -> bool:
    """
    Toggle sounds on/off.

    Args:
        on: True to enable, False to disable, None to toggle current state.

    Returns:
        The new enabled state.
    """
    cfg = load_config()
    if on is None:
        cfg["enabled"] = not cfg["enabled"]
    else:
        cfg["enabled"] = on
    save_config(cfg)
    return cfg["enabled"]


def is_enabled() -> bool:
    """
    Check if sounds are currently enabled.

    Returns:
        True if enabled, False otherwise.
    """
    return load_config().get("enabled", True)


def get_sound_for_event(event: str) -> Optional[str]:
    """
    Resolve which sound to play for a given event.

    Checks custom_sounds first, then built-in mappings.

    Args:
        event: Event name (e.g., 'error', 'prompt').

    Returns:
        Sound name (like 'faah') or file path, or None if not found.
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
