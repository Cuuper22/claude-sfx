#!/usr/bin/env python3
"""
claude-sfx CLI — generate sounds, test them, toggle on/off.

Usage:
    claude-sfx generate          # generate all built-in .wav files
    claude-sfx play <name>       # play a sound (faah, ding, yay, bruh, whoosh)
    claude-sfx test              # play all sounds in sequence
    claude-sfx on                # enable sounds
    claude-sfx off               # disable sounds
    claude-sfx status            # show current config
    claude-sfx trigger <event>   # trigger by event name (error, prompt, etc.)
    claude-sfx install-hooks     # print Claude Code hook configs
"""

from typing import List, Optional, Dict, Any
import json
import sys
import time


def main(args: Optional[List[str]] = None) -> None:
    """
    Main CLI entry point.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:]).
    """
    if args is None:
        args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return

    cmd = args[0]

    if cmd == "generate":
        from sfx.generator import generate_all
        print("generating sounds...")
        paths = generate_all(force="--force" in args)
        for name, path in paths.items():
            print(f"  {name:8s} -> {path}")
        print("done.")

    elif cmd == "play":
        if len(args) < 2:
            print("usage: claude-sfx play <name>")
            print("names: faah, ding, yay, bruh, whoosh")
            return
        from sfx.engine import play
        name = args[1]
        print(f"playing '{name}'...")
        play(name, blocking=True)

    elif cmd == "test":
        from sfx.engine import play
        from sfx.generator import SOUND_NAMES
        print("playing all sounds:\n")
        for name in SOUND_NAMES:
            print(f"  * {name}...", end=" ", flush=True)
            play(name, blocking=True)
            print("done")
            time.sleep(0.3)
        print("\nall sounds tested.")

    elif cmd == "on":
        from sfx.config import toggle
        toggle(on=True)
        print("sounds: ON")

    elif cmd == "off":
        from sfx.config import toggle
        toggle(on=False)
        print("sounds: OFF")

    elif cmd == "status":
        from sfx.config import load_config
        cfg = load_config()
        print(json.dumps(cfg, indent=2))

    elif cmd == "trigger":
        if len(args) < 2:
            print("usage: claude-sfx trigger <event>")
            print("events: error, prompt, completion, warning, thinking")
            return
        from sfx.engine import trigger
        event = args[1]
        print(f"triggering '{event}'...")
        trigger(event, blocking=True)

    elif cmd == "install-hooks":
        _print_hook_config()

    else:
        print(f"unknown command: {cmd}")
        print("run 'claude-sfx help' for usage")


def _print_hook_config() -> None:
    """Print the Claude Code hooks configuration for user to paste."""
    hooks: Dict[str, Any] = {
        "hooks": {
            "Bash": [
                {
                    "matcher": "exit_code != 0",
                    "event": "on_error",
                    "command": "python3 -m sfx.cli trigger error"
                }
            ],
            "AskUserQuestion": [
                {
                    "event": "on_invoke",
                    "command": "python3 -m sfx.cli trigger prompt"
                }
            ],
            "TaskComplete": [
                {
                    "event": "on_complete",
                    "command": "python3 -m sfx.cli trigger completion"
                }
            ]
        }
    }
    print("add this to your ~/.claude/settings.json:\n")
    print(json.dumps(hooks, indent=2))
    print("\nor see hooks/ directory for ready-made hook scripts.")


if __name__ == "__main__":
    main()
