#!/bin/bash
# Claude Code hook: play whoosh when Claude starts thinking
python3 -c "import sfx; sfx.whoosh()" 2>/dev/null || printf '\a'
