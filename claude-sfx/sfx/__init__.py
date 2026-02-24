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

from sfx.engine import play, trigger
from sfx.config import load_config, save_config, toggle, is_enabled
from sfx.generator import generate_all, SOUND_NAMES

__version__ = "0.1.0"

# ── quick-fire aliases ──────────────────────────────────────────────
def faah():
    """the FAAAAH — play on errors/failures"""
    trigger("faah")

def ding():
    """subtle ding — play when waiting for input"""
    trigger("ding")

def yay():
    """success chime — task completed"""
    trigger("yay")

def bruh():
    """bruh moment — warnings"""
    trigger("bruh")

def whoosh():
    """whoosh — thinking/loading"""
    trigger("whoosh")

__all__ = [
    "faah", "ding", "yay", "bruh", "whoosh",
    "play", "trigger", "toggle", "is_enabled",
    "load_config", "save_config", "generate_all",
]
