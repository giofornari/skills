---
name: discipline
description: "Coding discipline: think first, keep it simple, change only what was asked, verify, simplify safely. Not for: review-change."
---
> Source: multica-ai/andrej-karpathy-skills (MIT), read 2026-11-02; addyosmani/agent-skills (MIT), read 2026-11-02; wondelai/skills (MIT), read 2026-11-02

# Discipline

Habits that stop the usual agent mistakes: silent assumptions, overbuilt code, drive-by edits, "done" without proof. They lean towards caution over speed; for a trivial task use judgment. Code is read far more than written, so optimise for the reader.

## 1. Think before coding

- State your assumptions. If something is unclear, stop, name what confuses you, ask.
- Several readings of the request: present them, do not pick one silently.
- A simpler way exists, or the request looks wrong: say so and push back.
- Surface the trade-off before you commit to a design.

## 2. Simplicity first

- The least code that solves the stated problem. Nothing speculative: no extra features, no abstraction for one use, no flexibility or configuration nobody asked for, no handling of impossible cases.
- Write 200 lines where 50 would do? Rewrite. Test: would a senior engineer call it overcomplicated?
- DRY means one authoritative home for each piece of **knowledge**, not text that merely looks alike: two identical blocks serving different business rules are not duplication. Do not generalise before the third use.
- Keep components orthogonal: if the requirement behind a function changes drastically, one module should be affected. Avoid global state; inject collaborators (a `Notifier`, not a `SlackClient`).

## 3. Surgical changes

- Touch only what the request needs; match the existing style even if you would do it differently; do not "improve" adjacent code, comments or formatting; do not refactor what is not broken.
- Clean up **your own** orphans (imports, variables, functions your change made unused). Unrelated dead code: mention it, do not delete it.
- Every changed line must trace back to the request. Refactoring and feature work go in separate changes.
- Broken windows: do not add a hack that "we'll fix later". If a fix is out of scope, board it up (a TODO tied to a ticket, a stub, a flag) and say so.

## 4. Goal-driven execution

Turn the task into a verifiable goal and loop until it passes: "add validation" → tests for invalid inputs, then make them pass; "fix the bug" → a test that reproduces it, then pass; "refactor X" → tests green before and after. For several steps, state a short plan, each step with its check:

```
1. <step> → verify: <check>
2. <step> → verify: <check>
```

Strong criteria let you work alone; "make it work" needs constant questions. Nothing is done without the check having run.

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
