---
name: deepen-architecture
description: "Find shallow modules, propose deepening refactors and keep the domain glossary and ADRs current. Not for: review-change."
---
> Source: mattpocock/skills (MIT), read 2026-11-02; wondelai/skills (MIT), read 2026-11-02

# Deepen Architecture

Design **deep modules**: a lot of behaviour behind a small interface, at a clean seam, tested through that interface. The aim is leverage for callers, locality for maintainers, testability for everyone, and a codebase an agent can navigate. Complexity is the enemy; judge every design move by whether it lowers or raises it.

## Vocabulary (use exactly; no "component", "service", "API", "boundary")

- **Module**: anything with an interface and an implementation; a function, class, package or slice.
- **Interface**: everything a caller must know: signature, invariants, ordering, error modes, config, performance. Not just the type surface.
- **Depth**: behaviour a caller can exercise per unit of interface learned. Deep: small interface, large implementation. Shallow: interface nearly as complex as the body.
- **Seam**: where behaviour can change without editing in place; where a module's interface lives. Where to put it is its own decision.
- **Adapter**: a concrete thing satisfying an interface at a seam; named by role, not content.
- **Leverage** (callers get more per interface learned) and **locality** (change, bugs and knowledge concentrate in one place).

## Principles

- Depth belongs to the interface, not the implementation: a deep module may be made of small swappable parts behind it. Internal seams stay private.
- **Deletion test**: delete the module in your head. Complexity vanishes → pass-through. It reappears across N callers → it earns its keep.
- **The interface is the test surface**; testing past it means the module has the wrong shape.
- **One adapter is a hypothetical seam, two a real one**; add a port only when two adapters are justified (usually production plus test).
- Testable shape: accept dependencies instead of creating them; return results instead of mutating; keep the surface small.
- **Hide information**: one design decision reflected in several modules is a leak (shared formats, protocols, "read then process then write" splits by time). Organise by knowledge, not by when things run. If two modules share knowledge, merge them or give it a new owner.
- **Classitis**: many small shallow classes each add an interface to learn; small is not good, deep is. A method harder to learn than to rewrite is net negative.
- Be **somewhat general-purpose**: the simplest interface that covers today's needs; generality nobody needs is speculative complexity. A config parameter is a decision pushed onto the caller; decide, and push complexity downward so upper layers stay simple.
- Interface comments record what code cannot: the abstraction, invariants, why this approach. A comment that is hard to write means the design is too complex.
- Strategic over tactical: spend 10-20% extra on structure with each change; refactoring belongs to every feature, not to a special event.
- Symptoms to name before fixing: change amplification (one edit, many places), cognitive load, unknown unknowns (not obvious what a change affects), the worst of the three.

## Process

1. **Scope before scanning (YAGNI).** Deepening pays off where change keeps happening: take the user's named module or pain point, else read `git log --oneline` for hot spots and weight those paths first; if changes are scattered, widen. Read `GLOSSARY.md` and the ADRs of the area.
2. **Explore** with a fresh-context sub-agent, organically, noting friction: understanding one concept means bouncing across many small modules; interfaces nearly as complex as their bodies; pure functions extracted only for testability while the bugs hide in how they are called; tightly coupled modules leaking across seams; parts that are untested or hard to test through their interface. Apply the deletion test to every suspect.
3. **Present candidates** (a markdown list, or a self-contained HTML report in the temp directory with before/after diagrams if the user wants visuals). Per candidate: files, problem, solution in plain English, benefits as locality, leverage and test improvement, strength (**Strong**, **Worth exploring**, **Speculative**). End with a top recommendation. Use the glossary's domain terms ("the Order intake module", not "FooBarHandler"). Surface a candidate that contradicts an ADR only when the friction justifies reopening it, and say so. **Propose no interfaces yet**; ask which to explore.
4. **Grill the chosen one** (see `sharpen-intent`, grill mode): constraints, dependencies, the shape of the deepened module, what sits behind the seam, which tests survive.
5. **Classify dependencies**; the category sets how the seam is tested:
   - *In-process* (pure, in-memory): merge and test through the new interface; no adapter.
   - *Local-substitutable* (a local stand-in exists, such as an in-memory DB): test with the stand-in; the seam stays internal.
   - *Remote but owned* (your own services): a port at the seam, an HTTP/queue adapter in production, an in-memory adapter in tests.
   - *True external* (Stripe, Twilio): inject as a port, mock adapter in tests.
6. **Design it twice** when the interface is not obvious: frame constraints, dependencies and a rough sketch for the user, then spawn 3+ fresh-context sub-agents in parallel, each with a different constraint (minimise to 1-3 entry points; maximise flexibility; optimise the most common caller; ports and adapters for cross-seam dependencies). Each returns interface (with invariants, ordering, errors), a usage example, what hides behind the seam, dependency strategy, trade-offs. Present sequentially, compare on depth, locality and seam placement, then recommend or propose a hybrid; be opinionated, not a menu.
7. **Tests: replace, do not layer.** Once tests exist at the deepened interface, delete the old unit tests on the shallow modules. Assert observable outcomes; a test that must change when the implementation changes is testing past the interface.

## Domain model, as decisions crystallise

- Challenge a term that conflicts with `GLOSSARY.md` the moment it appears ("the glossary says cancellation means X, you mean Y?").
- Sharpen fuzzy words into one canonical term ("account": Customer or User?); stress-test relationships with invented edge-case scenarios.
- Check the code agrees with what the user says and surface the contradiction ("code cancels whole Orders, but you said partial is possible").
- Update `GLOSSARY.md` at once, never batched; it holds terms only: no implementation details, no spec, no scratch notes. A `GLOSSARY-MAP.md` at the root means several contexts, each with its own glossary and `docs/adr/`. Create files lazily, at the first term or first ADR.
- Offer an **ADR** only when it is all three: hard to reverse, surprising without context, the result of a real trade-off. Also when the user rejects a candidate for a load-bearing reason a future explorer would need; skip ephemeral ones ("not now").

## Red flags

- Interfaces proposed before the user picked a candidate; "component/service/boundary" drifting back in.
- A new seam with one adapter; a port added "for flexibility".
- Old shallow-module tests kept beside the new interface tests.
- A refactor that relocates complexity without reducing the concepts a reader holds.
- Glossary or ADRs batched to the end, or filled with implementation detail.
