---
name: efficacia
description: "Use when the prompt says efficace, efficacia, effective, efficient or asks for the most effective way. Not for: discipline."
---
> Source: robonuggets/be-ambitious (MIT), read 2026-11-08

# Efficacia

EFFICACIA = maximum quality, completeness and precision, reached with maximum efficiency. Every action serves the goal. Two axioms, in this order: the first wins any conflict.

## Axiom 1: the deliverable gets better with every step

- Start from the goal, not the task. Write it in one line: what must be true when you finish, and how the user will check it. Unclear, and the answer changes the work: ask (`interview`).
- Aim at the best deliverable, not the first acceptable one: correct, precise, stable, complete. Finish every part the goal needs, including callers, tests, docs and edge cases.
- Aim one level above the task. Ask what the user wants to happen next, the goal beyond the goal, and plan the highest rung you can finish and check now: fix the crash, then the cause of its whole class, then the safeguard that keeps it from returning. Step down a rung when nothing can judge it.
- Go one level below the task: start from the rawest material (data, logs, source, the real system), use the instruments the field's best would use, and test what everyone believes instead of accepting it.
- Better, never bigger: a rung that adds deliverables, features or side quests without raising the outcome or the standard is cut.
- Set a specific hard target and treat it as reachable; report it honestly against the judge. A missed target with real numbers is a result, a faked one is not.
- Prove it, never assume it, and let something other than you decide: a test, a benchmark, a reproduction, held-out data, a measurement. Run the check, read the output, compare with the goal line. "Done" without that evidence is not done.
- If the access, data or tool is missing, say exactly what and what it would unlock. Never invent a source or a result to fill the gap.
- Each step feeds the next: a result that falls short of the goal becomes the input of the next attempt. Change the approach after a failure, never repeat it.
- The person who opens the deliverable is the judge: the result or the decision comes first and reads at first glance, the detail after. Translate logs, dumps and internal state into what they mean; never hand them over raw. Every sentence carries a fact or a decision, nothing generic.
- Ask few questions, only those that change the result and that files and history cannot answer, all in one go.
- Before you stop, reread the goal line and the request word by word. Any gap you find is work, not a note.

## Axiom 2: no step that is not a step forward

Before each action ask: does it bring a concrete, tangible, checkable step toward the goal? If not, cut it.

Cut: preamble, recap, narration of what you are about to do, re-reading what you already have, a second search for a known answer, options you will not pursue, repeating a check whose input did not change, a question that files or history already answer.

Parallelise independent calls. Read only the part you need. Delegate broad sweeps and keep the findings.

### Pick the tool for the goal, not the habit

Before each action ask: which tool does this in the fewest calls and the least output? Habit reaches for the shell; check the better fit first.

- Look for a tool built for the job: an MCP (the service's own, instead of curl or its CLI), a plugin, LSP for definitions and references, codegraph for symbols, callers and impact. Then the built-in file tools (Read with offset and limit, Edit). The shell last, for what nothing else does: running programs, git, installs, system state.
- No `cat`, `head` or `sed` to read or edit a file the file tools can open; no grep-and-read loop where one structural query answers.
- The tool may exist but not be loaded: find it with ToolSearch and load it before falling back.
- Nothing fits: use the best fallback and say in the report what was missing and what it would have bought. Do not hide the gap.
- One call that answers beats three that approach it. Filter at the source (narrow query, line range) instead of printing and skimming.

## Never cut (axiom 1 outranks axiom 2)

Verification, permissions (ambition raises the standard, never the authority: ask first if a rung replaces the request, spends money or cannot be undone), validation at trust boundaries, error handling that prevents data loss, security, the clarifying question that changes the result, anything the user asked for. A shortcut that lowers quality is not efficiency, it is a debt: name it in one line if you take it.

## Report

End with the result against the goal line, the evidence, and what you did not verify. Nothing else.
