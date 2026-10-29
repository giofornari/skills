---
name: graphify-setup
description: Set up Graphify, the codebase knowledge-graph CLI, when `graphify` is missing or the user asks to install or register it.
---

# Graphify setup

Graphify installs itself into Claude Code through its own installer, so this skill runs that installer and nothing else.

1. Run `graphify --version`. A printed version means Graphify is installed: skip to step 3.
2. Run `uv tool install graphifyy` (or `pipx install graphifyy`). Done when `graphify --version` prints a version; if the shell cannot find it, run `uv tool update-shell` and check again.
3. Run `graphify install` once. Done when `/graphify` is listed as a skill after the session restarts.
4. Offer `graphify claude install` for the current project: it writes a graphify section to `CLAUDE.md` and a PreToolUse hook. Run it only after the user agrees.

Source: https://github.com/Graphify-Labs/graphify
