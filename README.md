# claude-sfx

Meme sound effects for your CLI sessions. Zero dependencies, pure Python stdlib.

[![Tests](https://github.com/Cuuper22/claude-sfx/actions/workflows/test.yml/badge.svg)](https://github.com/Cuuper22/claude-sfx/actions/workflows/test.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why

Terminals are silent by default. You stare at text, text stares back. I wanted my CLI sessions to have personality — a sound when something fails, a different sound when something works, a little whoosh while it's thinking.

The constraint I set: zero dependencies. Every sound is synthesized from scratch using `math.sin()`, `struct.pack()`, and `wave.open()`. Three stdlib calls. That's the entire audio pipeline.

The FAAH (error sound) is a descending sawtooth wave from 520Hz to 140Hz with increasing vibrato and soft clipping for that crunchy distortion feel. The ding is bell harmonics at A5 with an inharmonic 4.2x overtone — that's what makes it sound like a bell instead of an organ pipe. The whoosh is seeded random noise through a moving-average filter whose width sweeps across the duration.

Building audio synthesis from sine waves teaches you things about sound that no library can. Why does a bell sound different from an organ? Inharmonic overtone ratios. Why does a descending tone feel dramatic? The human ear tracks frequency sweeps as urgency signals. Why does filtered noise sound like wind? Because wind literally is filtered noise.

## Sounds

| Sound | Trigger | What it sounds like |
|-------|---------|--------------------|
| **FAAAH** | errors, failures | Descending sawtooth, 520Hz→140Hz, vibrato + soft clipping |
| **ding** | prompts, attention | Bell at A5 (880Hz), 4.2x inharmonic overtone |
| **yay** | task completion | Ascending chime C6→E6, dopamine delivered |
| **bruh** | warnings | Low F# buzz, light saturation |
| **whoosh** | thinking, loading | Seeded noise through a moving-average filter |

Every sound is synthesized from `math.sin()`, `struct.pack()`, and `wave.open()`. No bundled audio files.

<!-- TODO: Add waveform visualization of each sound -->

*Waveform visualization — to be added.*

## Quick start

```bash
git clone https://github.com/Cuuper22/claude-sfx.git
cd claude-sfx/claude-sfx
pip install -e .
```

### CLI

```bash
claude-sfx generate      # synthesize all WAV files
claude-sfx play faah     # play a sound
claude-sfx test          # play all sounds in sequence
claude-sfx on            # enable
claude-sfx off           # disable
claude-sfx status        # show config
```

### Python API

```python
import sfx

sfx.faah()              # error/failure
sfx.ding()              # attention/prompt
sfx.yay()               # success/completion
sfx.bruh()              # warning
sfx.whoosh()            # thinking/loading

sfx.trigger("error")    # trigger by event name
sfx.toggle(on=False)    # mute
```

## Claude Code integration

Automatically play sounds on CLI events:

```bash
claude-sfx install-hooks
```

This prints the hook configuration to paste into `~/.claude/settings.json`. Failed bash commands get a FAAH, prompts get a ding, task completions get a yay.

See `claude-sfx/hooks/` for the shell scripts and settings template.

## How it works

```
Event ("error")
  → engine.py    maps event → sound name, checks config
  → generator.py synthesizes WAV from math.sin()
  → player.py    detects platform audio, plays in background thread
```

All sounds are WAV files (16-bit mono PCM, 22.05 kHz) generated at runtime. No bundled audio files — the math is the source.

Platform detection chain: macOS `afplay` → Linux `pw-play`/`paplay`/`aplay`/`ffplay` → Windows `SoundPlayer` → terminal bell `\a` fallback.

Sounds play in background threads so they never block your shell.

## Configuration

Settings live at `~/.claude-sfx/settings.json`:

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
    "error": "/path/to/custom-faah.wav"
  }
}
```

Override location with `CLAUDE_SFX_CONFIG` env var.

## Testing

62 tests across 6 modules. CI runs on every push — 9-matrix (Ubuntu, macOS, Windows × Python 3.10, 3.11, 3.12) plus mypy type checking.

```bash
cd claude-sfx && pytest
```

| Module | Tests | Covers |
|--------|------:|--------|
| test_sfx.py | 8 | Integration — WAV generation, config round-trips, toggle |
| test_api.py | 15 | Public interface — `sfx.faah()`, `sfx.trigger()`, exports |
| test_config.py | 12 | Settings load/save, defaults, merge, corrupt JSON fallback |
| test_engine.py | 11 | Event→sound mapping, enable/disable, blocking modes |
| test_generator.py | 10 | WAV synthesis, format validation, fade, duration bounds |
| test_player.py | 6 | Platform detection, caching, background threading |

## Project structure

```
claude-sfx/
├── claude-sfx/               # package directory
│   ├── sfx/                  # the actual module
│   │   ├── generator.py      # all audio synthesis (math.sin → WAV)
│   │   ├── player.py         # cross-platform playback + threading
│   │   ├── engine.py         # event → sound mapping
│   │   ├── config.py         # JSON settings management
│   │   └── cli.py            # command-line interface
│   ├── hooks/                # Claude Code integration scripts
│   ├── tests/                # 62 tests
│   ├── demo.py               # interactive demo
│   └── pyproject.toml        # packaging config
├── .github/workflows/        # CI: 3 OS × 3 Python versions + mypy
└── README.md
```

## License

MIT

---

*Built with the same constraint-obsession as [ToaruOS-Arnold](https://github.com/Cuuper22/ToaruOS-Arnold) — artificial constraints make the engineering more interesting.*
