# next steps

things to do if this gets traction, or if you're bored and want to contribute.

---

## immediate (v0.2)

- [ ] **volume control that actually works** — right now the `volume` config key is stored but not wired to playback. need to scale wav samples at generation time or use a player flag (`afplay -v`, `paplay --volume`)
- [ ] **npm/pip package publish** — make it `pip install claude-sfx` for real, push to PyPI
- [ ] **actual audio tests** — generate sounds in CI, validate wav headers + duration, no playback needed
- [ ] **env var quick-disable** — `CLAUDE_SFX=0` to mute without touching the config file

## sound improvements

- [ ] **better FAAAH** — the current one is synthesized from math. sample a real one, or improve the synthesis with FM modulation + formant filters for that vocal quality
- [ ] **sound packs / themes** — let users pick between "meme", "minimal", "retro arcade", "mechanical keyboard" etc.
- [ ] **user-submitted sounds** — community repo of `.wav` files people can drop in
- [ ] **adaptive sounds** — different FAAAH intensity based on how many errors in a row (escalating disappointment)

## integration

- [ ] **native claude code support** — open an issue/PR on `anthropics/claude-code` to add first-class sound effect hooks. the hooks system already supports `PostToolUse` and `PreToolUse` — native support would mean sounds ship with claude code itself
- [ ] **VS Code extension companion** — play sounds through the VS Code audio API when using Claude Code in the IDE
- [ ] **tmux/screen awareness** — detect if running in a background pane and skip playback (or route to system notification sound)
- [ ] **iTerm2 / kitty integration** — use terminal-specific escape sequences for inline audio where supported
- [ ] **webhook mode** — POST to a local server instead of playing audio, for custom integrations

## platform

- [ ] **Windows testing** — powershell `SoundPlayer` approach needs real-world testing
- [ ] **WSL audio passthrough** — may need `wslu` or PulseAudio bridge
- [ ] **docker/remote** — detect headless environments and skip gracefully (already falls back to `\a` bell)

## fun ideas

- [ ] **combo counter** — "5 successful commands in a row!" with escalating chimes
- [ ] **rare sounds** — 1-in-100 chance of a special sound variant (gacha mechanics for your terminal)
- [ ] **session stats** — "you triggered 47 FAAHs today" end-of-session summary
- [ ] **sound recording mode** — record your own sounds directly: `claude-sfx record error`
- [ ] **spatial audio on macOS** — because why not

---

## filing as a feature request

if you want this in claude code natively, here's a ready-to-file issue:

**repo:** https://github.com/anthropics/claude-code/issues

**title:** Feature Request: Customizable sound effects for CLI events (errors, prompts, completions)

**body:**

> Add support for customizable sound effects that play during Claude Code CLI events.
>
> **motivation:** when multitasking, there's no audible feedback for errors, prompts, or completions. short meme-inspired sounds (like the trending "FAAAH" for failures) make the experience more responsive and fun.
>
> **proposed:** a config option in settings.json to enable sounds per event type, with built-in defaults and custom .wav path support. a toggle flag (`--silent` or `/sounds`) to mute.
>
> **reference implementation:** https://github.com/Cuuper22/Osint_app/tree/claude/add-sound-effects-YLE2y/claude-sfx
>
> this could start minimal (just a system bell on errors) and grow from there. the hooks system already supports this pattern — native support would make it accessible to everyone.

---

*"the terminal doesn't have to be silent."*
