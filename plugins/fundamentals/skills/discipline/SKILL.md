---
name: discipline
description: "Use before writing or changing any code. Not for: interview."
---
> Source: multica-ai/andrej-karpathy-skills (MIT), read 2026-11-02; addyosmani/agent-skills (MIT), read 2026-11-02; wondelai/skills (MIT), read 2026-11-02

# Discipline

Habits that stop the usual agent mistakes: silent assumptions, overbuilt code, drive-by edits, "done" without proof. They lean towards caution over speed. Code is read far more than written, so optimise for the reader.

## Use when (always, at any size)

Load this before the first edit of any task that creates or changes code, config, tests or scripts: a feature, a fix, a refactor, a simplification, a rename, a one-line tweak. "It is a one-liner" is not an exemption: here the habits cost seconds and save the rework. Skip it only for reading, questions and prose. Once per task is enough; read it again only when the scope changes.

A request too vague to start on is not this skill's job: stop and use `interview`.

## 1. Think before coding

- State your assumptions. Anything unclear: pause, say what is confusing, and ask before going on.
- Several readings of the request: present them, do not pick one silently.
- A simpler way exists, or the request looks wrong: say so and push back.
- Surface the trade-off before you commit to a design.

## 2. Simplicity first

- The least code that solves the stated problem. Nothing speculative: no extra features, no abstraction for one use, no flexibility or configuration nobody asked for, no handling of impossible cases.
- If the same result fits in a quarter of the code, rewrite it. Ask whether an experienced reviewer would call it overbuilt.
- DRY means one authoritative home for each piece of **knowledge**, not text that merely looks alike: two identical blocks serving different business rules are not duplication. Do not generalise before the third use.
- Keep components orthogonal: if the requirement behind a function changes drastically, one module should be affected. Avoid global state; inject collaborators (a `Notifier`, not a `SlackClient`).

## 3. Minimal footprint

- Edit only what the request requires; follow the existing style even where you would choose another; leave neighbouring code, comments and formatting alone; do not refactor what works.
- Clean up **your own** orphans (imports, variables, functions your change made unused). Dead code you did not create: report it and leave it.
- Every changed line must trace back to the request. Refactoring and feature work go in separate changes.
- Broken windows: do not add a hack that "we'll fix later". If a fix is out of scope, board it up (a TODO tied to a ticket, a stub, a flag) and say so.

## 4. Goal-driven execution

Convert each task into a goal you can check, then iterate until the check passes. A new validation rule starts as failing cases for bad input. A bug starts as a failing test that captures it. A refactor needs the same tests green on both sides. For several steps, write a short plan that pairs every step with the command or observation that proves it.

Sharp criteria let you work unattended; "make it work" forces constant questions. Nothing is done until the check has run.

## 5. Write the code well

- **Names** reveal intent and answer why, what, how: `elapsedTimeInDays`, `isActive`, `calculateMonthlyRevenue()`. No encodings or type prefixes; one word per concept (not `fetch`, `retrieve` and `get`); longer scope, longer name.
- **Functions** small, one thing, one level of abstraction, read top-down. Zero to two arguments; three or more needs a reason or a parameter object. A flag argument means two functions. Change state or return a value, not both. The name tells the whole truth, side effects included. Guard clauses first, one happy path.
- **Comments** say *why* (an invariant, a constraint, a rejected alternative), never *what*; the best comment is a well-named extracted function. Delete commented-out code and journal comments.
- **Errors**: separate from business logic; exceptions over return codes, with operation and state in the message; do not return or pass `null` (empty collection, Optional, Null Object); wrap third-party APIs. Fail early and loudly at a broken contract (precondition, postcondition, invariant); assertions are for what must never happen, error handling for what might.
- **Tests** are first-class code: one concept each, named for scenario and expectation, fast, independent, repeatable, arranged as set-up, act, assert.
- **Reversibility**: keep database, vendor and framework choices behind a seam you can change later.
- **Tracer bullet** (a thin end-to-end slice you keep) when requirements or architecture are unproven; **prototype** (a throwaway probe of one risky aspect) when one thing is uncertain, labelled throwaway and never promoted.

## 6. Simplify existing code

1. **Preserve behaviour exactly**: same outputs, errors, side effects and ordering; existing tests pass without edits. Unsure it preserves? Do not.
2. **Follow project conventions**; read `CLAUDE.md` and neighbouring code. Consistency beats your taste.
3. **Clarity over cleverness**: a named helper or an if-chain beats a dense ternary or chained `reduce`. Fewer lines is not the goal; faster comprehension is.
4. **Keep balance**: do not inline a helper that names a concept, merge unrelated logic, strip an abstraction that exists for testing, or optimise for line count.
5. **Scope** to what changed unless asked wider.
6. **Chesterton's fence**: before removing or changing anything, know its responsibility, callers, edge cases, tests and why it exists (`git blame`).
7. Signals: nesting of 3+ levels (guard clauses), functions over ~50 lines, nested ternaries, boolean flags, repeated conditionals (a named predicate), generic or misleading names, comments restating code, factories with one product.
8. One simplification at a time, tests after each, revert if red. Past ~500 touched lines use a codemod, not hands. Compare before and after: if it is not easier to read and review, revert.

## Red flags

- A test edited to make a "simplification" pass: you changed behaviour.
- A diff line you cannot trace to the request; reformatting unrelated files.
- An abstraction, option or error path added "just in case".
- Silent assumption; "done" with no verification output.
- Error handling removed because it "cleans up" the code.
