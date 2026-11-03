"""PreToolUse gate that makes the model load fundamentals:discipline.

A description alone does not make a model load a skill before small edits
(measured 2026-11-03: 0 of 8 runs). So the first code edit of a session is
blocked, with a message telling the model to load the skill first.

- "mark": runs before every Skill call; records that discipline was loaded.
- "gate": runs before Edit/Write/MultiEdit/NotebookEdit. Blocks (exit 2, the
  message on stderr goes to the model) until the skill is loaded, at most
  twice per session, so a broken install can never lock editing.
  Prose files (.md, .mdx, .txt, .rst) are never blocked.

Fails open: any error, a missing python3 or an unexpected input exits non-2,
which lets the tool call through.
"""
import json
import os
import sys
import tempfile

SKILL = "fundamentals:discipline"
PROSE = {".md", ".mdx", ".txt", ".rst"}
MAX_BLOCKS = 2
MESSAGE = (
    "Blocked: load the discipline skill before editing code. Call the Skill "
    f'tool with skill "{SKILL}", read it, then repeat this edit. '
    "This check ends once the skill is loaded."
)


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "gate"
    try:
        data = json.load(sys.stdin)
        sid = str(data["session_id"])
    except Exception:
        return 0
    if not sid or not sid.replace("-", "").replace("_", "").isalnum():
        return 0
    state = os.path.join(tempfile.gettempdir(), f"fundamentals-discipline-{sid}")
    tool_input = data.get("tool_input") or {}

    if mode == "mark":
        if tool_input.get("skill") == SKILL:
            with open(state, "w") as f:
                f.write("loaded")
        return 0

    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if os.path.splitext(path)[1].lower() in PROSE:
        return 0
    try:
        with open(state) as f:
            seen = f.read().strip()
    except FileNotFoundError:
        seen = ""
    if seen == "loaded":
        return 0
    blocks = int(seen) if seen.isdigit() else 0
    if blocks >= MAX_BLOCKS:
        return 0
    with open(state, "w") as f:
        f.write(str(blocks + 1))
    print(MESSAGE, file=sys.stderr)
    return 2


try:
    sys.exit(main())
except SystemExit:
    raise
except Exception:
    sys.exit(0)
