"""
Cross-platform audio playback — zero dependencies.

Tries platform-native commands in order:
  macOS  → afplay
  Linux  → aplay / paplay / pw-play / ffplay
  Windows → powershell (System.Media.SoundPlayer)

Falls back to printing a bell character (\\a) if nothing works.
"""

import os
import platform
import shutil
import subprocess
import sys
import threading


def _find_player() -> list[str] | None:
    """Detect the best available audio player command."""
    system = platform.system()

    if system == "Darwin":
        if shutil.which("afplay"):
            return ["afplay"]

    elif system == "Linux":
        for cmd in ("pw-play", "paplay", "aplay", "ffplay"):
            if shutil.which(cmd):
                if cmd == "ffplay":
                    return ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]
                return [cmd]

    elif system == "Windows":
        return [
            "powershell", "-c",
            "(New-Object System.Media.SoundPlayer('{path}')).PlaySync()"
        ]

    return None


_PLAYER_CMD: list[str] | None = None
_PLAYER_RESOLVED = False


def _get_player() -> list[str] | None:
    global _PLAYER_CMD, _PLAYER_RESOLVED
    if not _PLAYER_RESOLVED:
        _PLAYER_CMD = _find_player()
        _PLAYER_RESOLVED = True
    return _PLAYER_CMD


def play_file(filepath: str, blocking: bool = False) -> bool:
    """
    Play a .wav file. Returns True if playback started successfully.

    blocking=False (default) plays in a background thread so it
    never stalls the CLI.
    """
    if not os.path.isfile(filepath):
        return False

    player = _get_player()
    if player is None:
        # last resort: terminal bell
        sys.stdout.write("\a")
        sys.stdout.flush()
        return False

    def _do_play():
        try:
            cmd = [part.replace("{path}", filepath) for part in player]
            if "{path}" not in " ".join(player):
                cmd.append(filepath)
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

    if blocking:
        _do_play()
    else:
        t = threading.Thread(target=_do_play, daemon=True)
        t.start()

    return True
