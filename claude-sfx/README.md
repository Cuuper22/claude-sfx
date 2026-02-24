# claude-sfx

hey, i made this — sfx memes for taking cli ux to the next level lol.

or just to feel *something* while waiting for the freshest quota session to come through.

---

**what is this:** lightweight sound effects that play during your Claude Code (or any CLI) sessions.
zero dependencies. pure python stdlib. works on mac, linux, windows.

| event | sound | vibe |
|-------|-------|------|
| error / failure | **FAAAH** | that descending tone of pure disappointment |
| prompt / question | **ding** | clean bell, claude wants your attention |
| task complete | **yay** | ascending chime, dopamine delivered |
| warning | **bruh** | low buzz, something's off |
| thinking | **whoosh** | noise sweep, claude is cooking |

sounds are generated programmatically as `.wav` files — no bundled audio, no downloads, no ffmpeg.

## quickstart

```bash
cd claude-sfx

# generate all sounds + hear them
python3 demo.py

# or individually
python3 -m sfx play faah
python3 -m sfx play ding
python3 -m sfx test          # all sounds in sequence
```

## use it in code

```python
import sfx

sfx.faah()      # play the FAAAH
sfx.ding()      # attention ding
sfx.yay()       # success!
sfx.bruh()      # warning
sfx.whoosh()    # thinking...

sfx.trigger("error")       # trigger by event name
sfx.toggle(on=False)       # mute
sfx.toggle(on=True)        # unmute
```

## integrate with claude code

two options:

### option a: hooks config (recommended)

copy `hooks/claude_code_settings.json` into your `~/.claude/settings.json` under the `"hooks"` key. done. now every failed bash command plays FAAAH and every completion plays yay.

```bash
python3 -m sfx install-hooks   # prints the config to paste
```

### option b: shell hook scripts

```bash
chmod +x hooks/*.sh

# then reference in your claude code settings:
# "command": "./hooks/on_error.sh"
```

## configure

settings live in `~/.claude-sfx/settings.json`:

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
    "error": "/path/to/my-custom-faaah.wav"
  }
}
```

```bash
python3 -m sfx on       # enable
python3 -m sfx off      # disable
python3 -m sfx status   # show config
```

## how it works

1. `sfx/generator.py` — synthesizes .wav files from math (sin waves, harmonics, noise). no samples, no assets
2. `sfx/player.py` — detects your OS audio player (afplay/aplay/paplay/pw-play/powershell)
3. `sfx/engine.py` — maps events → sounds, respects config
4. `sfx/config.py` — json settings, toggle, custom sound paths
5. plays audio in a background thread so it never blocks your cli

## file structure

```
claude-sfx/
├── sfx/
│   ├── __init__.py      # public api + aliases
│   ├── __main__.py      # python3 -m sfx
│   ├── cli.py           # CLI commands
│   ├── config.py        # settings management
│   ├── engine.py        # event→sound dispatcher
│   ├── generator.py     # programmatic wav synthesis
│   └── player.py        # cross-platform audio playback
├── hooks/
│   ├── claude_code_settings.json   # ready-to-paste hooks config
│   ├── on_error.sh
│   ├── on_prompt.sh
│   ├── on_complete.sh
│   └── on_thinking.sh
├── sounds/              # generated .wav files (after first run)
├── demo.py              # interactive demo
├── pyproject.toml
├── NEXT_STEPS.md
└── README.md
```

## contributing

this is a fun side thing. if you want to add sounds, tweak the synthesis, or wire up more events — PRs welcome. see `NEXT_STEPS.md` for ideas.

---

*built because staring at a terminal waiting for a response shouldn't be silent.*
