---
name: idea-to-tickets
description: "Turn an idea into a spec, an ordered task plan and tracer-bullet tickets, one gate per stage. Not for: sharpen-intent."
---
> Source: addyosmani/agent-skills (MIT), read 2026-11-02; mattpocock/skills (MIT), read 2026-11-02

# Idea to Tickets

One pipeline, four stages, each ending in an artifact the human approves before the next starts: **Refine → Spec → Plan → Tickets**. Code without a spec is guessing; a plan without vertical slices is a tangle.

## Use when

A new project, feature or change that touches several files or takes over ~30 minutes, and no spec exists. Start at the stage the work is in: vague idea → Refine; chosen direction → Spec; approved spec → Plan; plan → Tickets. Skip for one-line fixes and unambiguous self-contained changes. If the user does not yet know what they want at all, run `sharpen-intent` first.

## Gates (all stages)

- Each stage writes a file (`docs/ideas/<name>.md`, `SPEC.md`, `tasks/plan.md` + `tasks/todo.md`, tickets) only after the user confirms.
- After saving an artifact, summarise it with its open questions, ask for approval, and **stop the turn**. The next stage starts in a later turn, never in the same one.
- If the project already uses a spec or tracker system (OpenSpec, GitHub, Linear, Jira, `bd`), keep its format and storage instead of creating a duplicate; this skill owns the questions, the content and the gates.
- Never overwrite a `plan.md` or `todo.md` that still has unchecked tasks for different work: stop and ask.

## 1. Refine (divergent, then convergent)

1. Restate the idea as one "How Might We" sentence.
2. Ask 3-5 sharpening questions, no more: who exactly, what success looks like, real constraints, what was tried, why now. Do not proceed without who and success.
3. Generate 5-8 variations, not 20, through lenses: inversion, constraint removal, audience shift, combination, simplification (10x simpler), 10x scale, expert lens. In a codebase, scan it first and ground variations in what exists.
4. After the user reacts, cluster into 2-3 genuinely different directions and stress-test each on user value (painkiller or vitamin), feasibility (hardest part), differentiation (would anyone switch).
5. Name hidden assumptions per direction: what you bet is true, what could kill it, what you ignore for now. Be honest, not a yes-machine.
6. One-pager: Problem, Recommended Direction, Assumptions to validate (with how to test each), MVP Scope, **Not Doing and why** (the most valuable part), Open Questions.

## 2. Spec

1. **Scope check.** If one request bundles several independently testable capabilities (own consumers, acceptance criteria that cluster, one could be cut alone), first propose a small capability map: kebab-case module ids chosen once, responsibility, depends-on, build order, no cycles. Gate it. Then spec each module in dependency order (`SPEC-<id>.md`). Single capability: skip.
2. **List assumptions first** (stack, auth, database, platform, browsers) and ask for corrections before writing.
3. If the conversation already holds the content, synthesise it without a new interview; ask only what is missing.
4. **Sketch the test seams**: prefer existing seams, use the highest one possible, ideal count is one; confirm with the user.
5. Write the spec: Objective (who, why, success; user stories as "As a…, I want…, so that…"), Tech stack, full Commands (build, test, lint, dev), Project structure, Code style (one real snippet beats three paragraphs), Testing strategy and what makes a good test (external behaviour only), Boundaries (Always / Ask first / Never), Success criteria, Out of scope, Open questions.
6. Reframe vague asks into measurable criteria ("faster" → LCP < 2.5s on 4G, load < 500ms) and ask if the targets are right. Use the project's glossary and respect existing ADRs. Name no file paths or code in decisions; they rot. Exception: a prototype snippet that encodes a decision more exactly than prose (state machine, schema, type shape).
7. The spec is living: update it before the code when a decision changes; commit it; link it from PRs.

## 3. Plan and tasks

Read-only: no code in this stage.

1. Read the spec and code; map the dependency graph; note risks and unknowns. Build foundations first.
2. **Slice vertically**: each task is one complete path through every layer (schema, API, UI, tests) that works and verifies on its own. Never "all the schema, then all the API".
3. **Wide refactor exception** (one mechanical change whose blast radius spans the codebase): sequence expand → migrate in batches sized by blast radius (one ticket per package) → contract (delete the old form, blocked by every batch). Prefactor first: make the change easy, then make the easy change.
4. Each task: description, acceptance criteria (specific, testable, ≤3 bullets), verification (test, build, manual check), dependencies, files likely touched, size.

   | Size | Files | Rule |
   |---|---|---|
   | XS / S | 1 / 1-2 | fine |
   | M | 3-5 | fine, agents do best here |
   | L | 5-8 | break down |
   | XL | 8+ | too large |

   Split when it needs more than one focused session (~2h), the acceptance criteria take more than 3 bullets, it touches two independent subsystems, or the title says "and".
5. Order by dependency, high risk early, a checkpoint (tests, build, core flow, human review) after every 2-3 tasks.
6. Parallelism: independent slices, tests of finished features and docs can run in parallel; migrations, shared state and dependency chains stay sequential; define a shared API contract first, then parallelise.
7. Save `tasks/plan.md` (overview, architecture decisions, phased task list with checkpoints, risks, open questions) and the list to `tasks/todo.md`, or to the designated tracker (one item per task; plan keeps an index of ids).

## 4. Tickets

1. Work from the plan or spec in context, or fetch the issue or spec the user points to, with its comments.
2. Draft **tracer-bullet** tickets: each a narrow but complete path, demoable or verifiable alone, sized for a single fresh context window, prefactoring first. Each declares its **blocking edges**; a ticket with no blockers can start now.
3. **Quiz the user** with a numbered list (title, blocked by, what it delivers): is the granularity right, does each ticket depend only on what truly gates it, merge or split anything? Iterate to approval.
4. Publish in dependency order (blockers first): local files as one file per ticket (`<NN>-<slug>.md`, numbered from 01, never one combined file), or one tracker issue per ticket using native blocking links (sub-issues if the source was an issue). Each ticket: What to build (end-to-end behaviour, not a layer list), Acceptance criteria, Blocked by. Add the project's agent-ready label if it has one. Do not close or edit the parent issue.
5. Work the frontier: any ticket whose blockers are done.

## Red flags

- Code, plan or tickets started in the same turn as the spec; an approval taken from silence.
- A spec that spans several capabilities with no capability map; boundaries decided during implementation.
- Horizontal slices; tasks with no acceptance criteria or verification; every task XL; no checkpoints.
- 20+ shallow variations; no "who is this for"; no Not Doing list; assumptions never named.
- Overwriting an incomplete plan; writing `todo.md` when a tracker is designated.
