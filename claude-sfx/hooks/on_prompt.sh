#!/bin/bash
# Claude Code hook: play ding when waiting for user input
python3 -c "import sfx; sfx.ding()" 2>/dev/null || printf '\a'
