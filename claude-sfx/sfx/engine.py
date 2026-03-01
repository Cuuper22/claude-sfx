"""
Core engine — ties generator, player, and config together.
"""

import os

from sfx.config import is_enabled, get_sound_for_event
from sfx.generator import get_sound_path, SOUNDS_DIR
from sfx.player import play_file


def play(sound_name: str, blocking: bool = False) -> bool:
    """
    Play a sound by name (e.g., 'faah', 'ding').

    Respects the enabled setting from configuration.

    Args:
        sound_name: Name of the sound to play.
        blocking: If True, blocks until playback completes.

    Returns:
        True if sound played successfully, False otherwise.
    """
    if not is_enabled():
        return False

    try:
        path = get_sound_path(sound_name)
    except FileNotFoundError:
        return False

    return play_file(path, blocking=blocking)


def trigger(event_or_sound: str, blocking: bool = False) -> bool:
    """
    Trigger a sound by event name or direct sound name.

    Accepts either:
    - Event name: 'error', 'prompt', 'completion', etc.
    - Direct sound name: 'faah', 'ding', 'yay', etc.

    If event_or_sound maps to a custom file path in config, plays that directly.

    Args:
        event_or_sound: Event name or sound name.
        blocking: If True, blocks until playback completes.

    Returns:
        True if sound played successfully, False otherwise.
    """
    if not is_enabled():
        return False

    # check if it's an event name that maps to something
    resolved = get_sound_for_event(event_or_sound)
    if resolved is None:
        # maybe it's a direct sound name
        resolved = event_or_sound

    # if resolved is an absolute path to a file, play it directly
    if os.path.isfile(resolved):
        return play_file(resolved, blocking=blocking)

    # otherwise treat as a built-in sound name
    return play(resolved, blocking=blocking)
