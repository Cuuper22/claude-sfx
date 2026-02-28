# Osint_app

Described as an "OSINT investigation toolkit" but let's be real -- there's no OSINT here yet. What actually lives in this repo is **claude-sfx**, a lightweight Python library that plays meme sound effects during CLI sessions.

OSINT stuff is planned. Someday. For now, enjoy the sound effects.

## What's Actually Here

### claude-sfx

A zero-dependency Python package that plays sounds when things happen in your terminal. Errors get a descending FAAAH. Completions get a little yay. Claude asking you a question gets a ding. You get the idea.

All sounds are synthesized from math (sin waves, harmonics) -- no bundled audio files, no ffmpeg, no external downloads.

| Event | Sound | What It Means |
|-------|-------|---------------|
| Error | FAAAH | Something broke |
| Prompt | ding | Pay attention |
| Complete | yay | It worked |
| Warning | bruh | Heads up |
| Thinking | whoosh | Working on it |

### Quick Start

```bash
cd claude-sfx

# generate sounds and hear them all
python demo.py

# play individual sounds
python -m sfx play faah
python -m sfx test
```

### Use in Code

```python
import sfx

sfx.faah()       # disappointment
sfx.ding()       # attention
sfx.yay()        # dopamine
sfx.bruh()       # concern
sfx.whoosh()     # patience

sfx.toggle(on=False)   # mute
```

### Claude Code Integration

Paste the hooks config from `claude-sfx/hooks/claude_code_settings.json` into your `~/.claude/settings.json`. Failed commands play FAAAH, completions play yay.

```bash
python -m sfx install-hooks   # prints the config to paste
```

## Stack

- Python 3.10+, stdlib only
- Works on macOS, Linux, Windows
- Sounds play in background threads (non-blocking)

## What About OSINT?

It's on the list. The repo name will make more sense eventually.
