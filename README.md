## Why

Terminals are silent and soulless. Now mine goes "FAAAH" when something breaks and "yay" when a task completes. Pure Python, zero dependencies, synthesized from sine waves.

# claude-sfx

Meme sound effects for your CLI sessions. Zero dependencies, pure Python stdlib.

## What Is This?

A lightweight Python library that plays sound effects when things happen in your terminal:

- **FAAAH** - descending tone of pure disappointment (errors/failures)
- **ding** - clean bell, attention please (prompts/questions)
- **yay** - ascending chime, dopamine delivered (task completion)
- **bruh** - low buzz, something's off (warnings)
- **whoosh** - noise sweep, working on it (thinking/loading)

All sounds are synthesized programmatically using sine waves and harmonics. No bundled audio files, no external dependencies, no downloads required.

## Installation

### From PyPI (when published)

```bash
pip install claude-sfx
```

### From Source

```bash
git clone https://github.com/Cuuper22/claude-sfx.git
cd Osint_app/claude-sfx
pip install -e .
```

## Quick Start

### Command Line

```bash
# Generate all sound files
claude-sfx generate

# Play individual sounds
claude-sfx play faah
claude-sfx play ding

# Test all sounds in sequence
claude-sfx test

# Toggle on/off
claude-sfx on
claude-sfx off

# View current configuration
claude-sfx status
```

### Python API

```python
import sfx

# Direct sound playback
sfx.faah()       # error/failure sound
sfx.ding()       # attention/prompt sound
sfx.yay()        # success/completion sound
sfx.bruh()       # warning sound
sfx.whoosh()     # thinking/loading sound

# Trigger by event name
sfx.trigger("error")
sfx.trigger("prompt")
sfx.trigger("completion")

# Control playback
sfx.toggle(on=False)   # mute all sounds
sfx.toggle(on=True)    # unmute
```

## Claude Code Integration

Automatically play sounds on CLI events by adding hooks to your `~/.claude/settings.json`:

```bash
claude-sfx install-hooks
```

This will print the configuration to paste into your settings file. Events supported:
- Failed bash commands → FAAAH
- User prompts → ding
- Task completions → yay

See `claude-sfx/hooks/claude_code_settings.json` for the full configuration.

## Configuration

Settings are stored in `~/.claude-sfx/settings.json`:

```json
{
  "enabled": true,
  "volume": 0.8,
  "events": {
    "error": "faah",
    "prompt": "ding",
    "completion": "yay",
    "warning": "bruh",
    "thinking": "whoosh"
  },
  "custom_sounds": {
    "error": "/path/to/my-custom-faah.wav"
  }
}
```

You can override the config location with the `CLAUDE_SFX_CONFIG` environment variable.

## Platform Support

- **macOS**: Uses `afplay`
- **Linux**: Uses `pw-play`, `paplay`, `aplay`, or `ffplay` (whichever is available)
- **Windows**: Uses PowerShell's `System.Media.SoundPlayer`

Falls back to terminal bell (`\a`) if no audio player is found.

## Supported Audio Formats

The library generates and plays WAV files (16-bit mono PCM, 22.05 kHz sample rate). Custom sounds must also be in WAV format.

## Requirements

- Python 3.10 or higher
- No external dependencies (stdlib only)
- Platform-native audio player (automatically detected)

## Architecture

- `sfx/generator.py` - Synthesizes .wav files from mathematical formulas
- `sfx/player.py` - Detects and uses platform-native audio players
- `sfx/engine.py` - Maps events to sounds, respects configuration
- `sfx/config.py` - JSON settings management
- `sfx/cli.py` - Command-line interface

Sounds play in background threads so they never block your CLI.

## Development

```bash
# Clone the repository
git clone https://github.com/Cuuper22/claude-sfx.git
cd Osint_app/claude-sfx

# Install in editable mode
pip install -e .

# Run tests
pytest

# Run demo
python demo.py
```

## License

MIT License - see LICENSE file for details

