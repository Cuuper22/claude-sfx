# Osint_app

Described as an "OSINT investigation toolkit" but let's be honest -- the OSINT part is still on the drawing board. What actually lives here is **claude-sfx**, a zero-dependency Python library that plays sound effects during CLI sessions.

The OSINT stuff is planned. For now, enjoy the beeps.

## What's Actually Here

### claude-sfx

A Python package that plays sounds when things happen in your terminal. Errors get a descending tone. Completions get a little chime. Questions get a ding. All sounds are math-generated (sine waves, harmonics) -- no bundled audio files.

| Event | Sound | Meaning |
|-------|-------|---------|
| Error | descending tone | Something broke |
| Prompt | ding | Pay attention |
| Complete | ascending chime | It worked |
| Warning | flat tone | Heads up |
| Thinking | whoosh | Working on it |

### Quick Start

```bash
cd claude-sfx
python demo.py        # hear all sounds
python -m sfx test    # individual test
```

### Claude Code Integration

Copy the hooks config from `claude-sfx/hooks/` into your Claude Code settings. Failed commands play the error sound, completions play the chime.

## Stack

- Python 3.10+, stdlib only (no external dependencies)
- Cross-platform: macOS, Linux, Windows
- Non-blocking (sounds play in background threads)

## What About the OSINT Part?

It is what it is. The repo name will make more sense eventually.
