---
name: idea-to-tickets
description: "Turn an idea into a spec, plan and tickets. Not for: interview."
---
> Source: addyosmani/agent-skills (MIT), read 2026-11-02; mattpocock/skills (MIT), read 2026-11-02

# Idea to Tickets

One pipeline, three stages: **Refine → Spec → Plan**, the plan's tasks being the tickets. Each stage ends in an artifact the human approves before the next starts. Code without a spec is guessing; a plan without vertical slices is a tangle.

**Stance.** Every artifact is concrete: each line is something another person could check, each benefit is a change for a named person, never "better", "cleaner" or "maybe later". Judge the idea, the spec and the plan as an impartial critic, not a supporter: no praise, no going along. Say once what is weak, why, and what would fix it. If the user decides otherwise, the call is theirs and your objection goes into the artifact (Dissent, Open questions).

**No production code is written in any stage.** The codebase is read-only here; the only things you write are the artifacts.

## Where to start

Use it for a new project, feature or change that touches several files or takes over ~30 minutes. Skip it for one-line fixes and unambiguous self-contained changes. A stage starts only when its input exists and is approved:

- **Refine** needs the brief from `interview`. A message that already holds Goal, Done when and Out of scope counts as one; a vague idea with none means run `interview` first.
- **Spec** needs the approved one-pager, or the user's word that the direction is already chosen.
- **Plan** needs the approved spec.

Input missing: go back one stage. Never invent it.

## Gates (all stages)

- One approval per stage, no more, placed where the next step is costly: the direction (end of Refine), the spec (before Plan), the plan (before it is published or built). Write a local file (`docs/ideas/<name>.md`, `SPEC.md`, `tasks/plan.md` + `tasks/todo.md`, ticket files) as a draft without asking first, then summarise it with its open questions, ask for approval, and **stop the turn**. The next stage starts in a later turn, never in the same one, even when the request sounds like "do it all".
- What leaves the machine (publishing tasks to a tracker) or overwrites existing work needs explicit approval before it happens.
- A decision among discrete options (direction, stack, auth, database, test seams) goes through `AskUserQuestion`, your recommendation first with its cost. A list to review and edit (assumptions, capability map, tasks) stays a numbered list in chat: the user edits items rather than picking one.
- If the project already uses a spec or tracker system (OpenSpec, GitHub, Linear, Jira, `bd`), keep its format and storage instead of creating a duplicate; this skill owns the questions, the content and the gates.
- Never overwrite a `plan.md` or `todo.md` that still has unchecked tasks for different work, and never close or delete another plan's open items in a tracker: stop and ask.

## 1. Refine (diverge, argue, converge)

Input: the brief from `interview`. Ask nothing it already answers.

1. **State the problem as one "How Might We" sentence**: how might we [outcome] for [specific user] without [key constraint]. Narrow enough to act on, broad enough to leave options, no solution inside it ("…build a chatbot" is a solution). Check it against the brief's Goal and Done when. In a codebase, scan it first and ground everything in what exists.
2. **Pick 4-6 lenses (default 5).** Each reasons in a different way, not a different job title for the same thinking. Cover at least:
   - the person who has the pain, framed as a job ("when I…, I want…, so I can…": functional, emotional, social), and what they do today instead: that workaround is the real competitor;
   - a pre-mortem (the project failed a year on: why?);
   - the economist (cost, who pays, and the alternatives: do nothing, buy, reuse);
   - an outsider from an unrelated field, who matches on structure and not on surface ("Uber for X" is surface; "trust between strangers in a market" is structure);
   - the subtractor (the smallest thing that still delivers the value: one feature, one day).

   Swap in sharper ones when the domain offers them: the first-principles skeptic (what is actually true, what is only how it has always been done), the abuser, whoever inherits it in two years, a regulator, the third party who never uses it but pays for its side effects. Name each as a concrete person with a stake ("the on-call engineer at 3 a.m."), not a title.
3. **Round 1, independent.** Launch one fresh read-only subagent per lens, all in one message (see `orchestrate-agents`), and tell the user in one line how many. Give each only the brief and its lens, and: argue the lens at full strength; do not balance, do not be agreeable; report in at most 10 lines: verdict (build / reshape / do not build), strongest argument, the one fact you would want checked, what this lens sees that others will miss, the version of the project you would build, what you would kill. Never show them your preferred direction or each other's work: shared context makes them agree. No web search unless the user approved it. Without a subagent tool, write each lens in turn from the brief alone, and say that independence is weaker.
4. **Round 2, dialogue.** Send each agent the other lenses' verdict and strongest argument (SendMessage, so each keeps its own reasoning) and ask, in at most 6 lines: which other view is most wrong and why; what you concede; your position now. A position that survives the challenge is a real conflict.
5. **Converge.** Read every report yourself. Map where the lenses agree, where they truly conflict (not in wording) and what moved in round 2. Do not average them: a direction is a bet that settles the conflicts in one specific way, and it exists for a reason you can state in one line. Build 2-3 directions that differ genuinely, always including "do nothing or reuse what exists". At least one must come from a lens far from the user's own field: a view they would not have reached by thinking alone. Five to eight ideas that each have a reason beat twenty shallow ones.
6. **Judge each direction** as an impartial critic, not a diplomat:
   - **Value is evidence, not belief.** Can you name three specific people who have this problem now? Do they pull (ask for it) or do you push? How often does it bite (daily beats monthly)? A painkiller is described with emotion and already has workarounds; a vitamin gets a polite nod and no change in behaviour. "Everyone could use it", "like X but better" and "real but rare" all fail. And: what happens if nobody builds it.
   - **Feasibility:** the hardest part, dependencies you do not control, the minimum stack, time to first value. An MVP that still takes months is not minimal.
   - **Differentiation**, strongest to weakest: new capability, 10x on one dimension, new audience, new context, better UX, cheaper. Could a rival copy it in a week? Do users care, or only builders?
   - **Assumptions**, sorted: dealbreakers (if false the idea dies: validate before building), important (adjust if false), nice-to-have (leave until the core is proven).
   - **Rank**: high value and high feasibility first; high value and low feasibility only if worth the risk; low value only if trivial; otherwise drop. Differentiation breaks ties. A direction whose value is only potential is not recommended.

   Recommend one; say which lenses it satisfies and which it overrules, and why.
7. Show the user one line per lens, the conflicts and the directions with your verdict, then ask which direction with `AskUserQuestion` (the directions as options, your recommendation first). Their pick is this stage's approval: write the one-pager, report its path and stop the turn. The one-pager: Problem, Recommended Direction, Concrete value (what changes, for whom, how measured), Why this one (lenses that won, lenses overruled), Dissent (the strongest unresolved objection and whose it is), Assumptions to validate (sorted as above, each with how to test it), MVP Scope (one job done well; the riskiest assumption tested first; sized by time, not by feature list; a first version that does not feel incomplete is over-built), **Not Doing and why** (mandatory, the most valuable part), Open Questions.

**Done when:** the one-pager exists, the user picked the direction, value is stated as a change for a named person, every assumption has a test, and Not Doing is not empty.

## 2. Spec

1. **Scope check.** If one request bundles several independently testable capabilities (own consumers, acceptance criteria that cluster, one could be cut alone), first propose a capability map: a table of kebab-case module ids (chosen once, never renamed), responsibility and depends-on, plus the build order. Dependencies point one way; two modules that need each other are one module. The contract between two modules belongs in the provider's spec. Gate the map, save the approved map at the project root (it is the index of what exists), then spec each module in dependency order (`SPEC-<id>.md`). Single capability: skip.
2. **List assumptions first** (stack, auth, database, platform, browsers) as a numbered list and ask for corrections before writing; a point with several real candidates becomes an `AskUserQuestion` decision instead. Never fill an ambiguous requirement silently.
3. If the conversation already holds the content, synthesise it without a new interview; ask only what is missing.
4. **Sketch the test seams**: prefer existing seams, use the highest one possible, ideal count is one; confirm with the user through `AskUserQuestion`.
5. Write the spec: Objective (from the user's perspective: problem, solution, who, why, success; user stories "As a…, I want…, so that…" that cover every actor and every aspect of the behaviour, because a behaviour with no story is not specified), Tech stack, full Commands (build, test, lint, dev), Project structure, Code style (one real snippet beats three paragraphs), Testing strategy (what makes a good test: external behaviour only; which modules; prior art: similar tests already in the codebase), Boundaries (Always / Ask first / Never), Success criteria, Out of scope, Open questions. Save it where the project keeps specs: `SPEC.md`, or its tracker (with the agent-ready label, if it has one).
6. Reframe vague asks into measurable criteria ("faster" → LCP < 2.5s on 4G, load < 500ms) and ask if the targets are right. Use the project's glossary and respect existing ADRs. Name no file paths or code in decisions; they rot. Exception: a prototype snippet that encodes a decision more exactly than prose (state machine, schema, type shape).
7. The spec is living: update it before the code when a decision changes; commit it; link it from PRs.

**Done when:** every area above is covered, each success criterion is specific and testable, boundaries are set, the spec is saved, and the user approved it in a later turn.

## 3. Plan and tickets

Read-only: no code in this stage.

1. Read the spec and the code; use the project's glossary and respect its ADRs. Map the dependency graph; note risks and unknowns. Build foundations first.
2. **Slice vertically**: each task is one complete path through every layer (schema, API, UI, tests) that works and verifies on its own: narrow but complete, demoable alone, sized for a single fresh context window, and it leaves the system working. Never "all the schema, then all the API".
3. **Wide refactor exception** (one mechanical change whose blast radius spans the codebase): sequence expand → migrate in batches sized by blast radius (one ticket per package) → contract (delete the old form, blocked by every batch). If even the batches cannot stay green alone, let them share an integration branch and block a final integrate-and-verify ticket: green is promised only there. Prefactor first: make the change easy, then make the easy change.
4. Each task: description, acceptance criteria (specific, testable, ≤3 bullets), verification (test, build, manual check), dependencies, files likely touched, size.

   | Size | Files | Rule |
   |---|---|---|
   | XS / S | 1 / 1-2 | fine |
   | M | 3-5 | fine, agents do best here |
   | L | 5-8 | break down |
   | XL | 8+ | too large |

   Split when it needs more than one focused session (~2h), the acceptance criteria take more than 3 bullets, it touches two independent subsystems, or the title says "and".
5. Order by dependency, high risk early, a checkpoint (tests, build, core flow, human review) after every 2-3 tasks. Declare each task's blocking edges: a task with no open blockers can start now.
6. Parallelism: independent slices, tests of finished features and docs can run in parallel; migrations, shared state and dependency chains stay sequential; define a shared API contract first, then parallelise.
7. Save `tasks/plan.md` (overview, architecture decisions, phased task list with checkpoints, a risk table of risk, impact and mitigation, open questions) and `tasks/todo.md` as drafts. If the user points to an issue or spec, fetch it with its comments first. If the tasks live in a tracker, say so in `plan.md` and keep its task list as an ordered index of ids or links, never a second checklist.
8. **Quiz the user** with a numbered list (title, blocked by, what it delivers): is the granularity right, does each task depend only on what truly gates it, merge or split anything? Iterate to approval.
9. If the project has a tracker, or the user wants separate tickets, publish after approval, in dependency order (blockers first): one tracker issue per task using native blocking links (sub-issues if the source was an issue), or locally one file per ticket (`tasks/tickets/<NN>-<slug>.md`, numbered from 01, never one combined file). Each: What to build (end-to-end behaviour from the user's side, not a layer list), Acceptance criteria, Blocked by. Add the project's agent-ready label if it has one. Do not close or edit the parent issue. The plan keeps an index of ids.

**Done when:** every task has acceptance criteria and a verification step, dependencies and blocking edges are set, no task is larger than M, checkpoints exist, the tasks are recorded in their target, no incomplete plan was overwritten, and the user approved. The skill ends here: executing the plan is a separate step the user starts.

## Stop signs

- "This is simple, it needs no spec." A two-line spec with acceptance criteria is fine; none is not.
- "I'll write the spec after the code." That is documentation. A spec's value is forcing clarity first.
- "Requirements will change anyway." That is why the spec is living: update it before the code.
- "I'll split it into modules while planning." Module boundaries are decided before the spec exists, not after.
- "The tasks are obvious." Write them down: that surfaces hidden dependencies.
- "The old plan is stale, I'll replace it." Unchecked tasks may be mid-build in another session: stop and ask.
- "The idea sounds good and they seem set." Going along is not judging: say the weak point once, then record it.
- Also wrong: the next stage started in the same turn as an approval request; an approval taken from silence; tasks published to a tracker before the quiz is approved; a spec spanning several capabilities with no map; horizontal slices; tasks with no acceptance criteria or verification; every task XL; no checkpoints; lenses that are job titles repeating one view; round-1 agents shown your preferred direction or each other's work; views averaged into mush; no "do nothing or reuse" direction; a recommendation whose value is only potential; no Not Doing list; assumptions never named; `todo.md` written when a tracker is designated.
