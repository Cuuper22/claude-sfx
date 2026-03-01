"""
claude-sfx: meme sound effects for your CLI sessions.

    pip install claude-sfx   (or just drop this folder in)

    >>> import sfx
    >>> sfx.faah()          # error / failure
    >>> sfx.ding()          # prompt / question
    >>> sfx.yay()           # success / completion
    >>> sfx.bruh()          # warning
    >>> sfx.whoosh()        # thinking / loading
"""

from typing import Dict, List

from sfx.engine import play, trigger
from sfx.config import load_config, save_config, toggle, is_enabled
from sfx.generator import generate_all, SOUND_NAMES

__version__ = "0.1.0"

# ── quick-fire aliases ──────────────────────────────────────────────
def faah() -> bool:
    """
    Play the FAAAAH sound - descending tone for errors/failures.

    Returns:
        True if sound played successfully, False otherwise.
    """
    return trigger("faah")

def ding() -> bool:
    """
    Play a subtle ding - bell sound for prompts/waiting for input.

    Returns:
        True if sound played successfully, False otherwise.
    """
    return trigger("ding")

def yay() -> bool:
    """
    Play success chime - ascending tone for task completion.

    Returns:
        True if sound played successfully, False otherwise.
    """
    return trigger("yay")

def bruh() -> bool:
    """
    Play bruh sound - low buzz for warnings.

    Returns:
        True if sound played successfully, False otherwise.
    """
    return trigger("bruh")

def whoosh() -> bool:
    """
    Play whoosh sound - noise sweep for thinking/loading.

    Returns:
        True if sound played successfully, False otherwise.
    """
    return trigger("whoosh")

__all__ = [
    "faah", "ding", "yay", "bruh", "whoosh",
    "play", "trigger", "toggle", "is_enabled",
    "load_config", "save_config", "generate_all",
    "SOUND_NAMES",
]
