#!/bin/bash
# Claude Code hook: play success chime on task completion
python3 -c "import sfx; sfx.yay()" 2>/dev/null || printf '\a'
