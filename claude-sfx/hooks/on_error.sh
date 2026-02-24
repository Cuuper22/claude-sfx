#!/bin/bash
# Claude Code hook: play FAAAH on errors
# Add to your Claude Code settings as a post-tool hook for Bash failures
python3 -c "import sfx; sfx.faah()" 2>/dev/null || printf '\a'
