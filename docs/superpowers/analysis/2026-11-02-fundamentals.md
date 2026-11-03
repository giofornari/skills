# Fundamentals — donor analysis
Read: 2026-11-02; upstream commits: addyosmani/agent-skills=301b02b, mattpocock/skills=4ae2317, obra/superpowers=2ce8aa1, multica-ai/andrej-karpathy-skills=2c60614, blader/humanizer=0ef9fe5, DietrichGebert/ponytail=96608e0

Figures: `claude --plugin-dir <dir> plugin details <name>`, rounded by the tool. On-invoke counts SKILL.md only, not sibling reference files. Hook-injected context is not counted in always-on.

| plugin | skills | licence | always-on | on-invoke | class |
|---|---|---|---|---|---|
| superpowers | brainstorming, diagnosing-superpowers, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills | MIT | 848 | 49700 | indivisible |
| andrej-karpathy-skills | karpathy-guidelines | none | 105 | 850 | fusable |
| humanizer | humanizer | MIT | 144 | 10700 | fusable |
| ponytail | ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review | MIT | 641 | 6880 | indivisible |
| grill-me | grill-me | MIT | 34 | 20 | fusable |
| grill-with-docs | grill-with-docs | MIT | 60 | 30 | fusable |
| grilling | grilling | MIT | 70 | 600 | fusable |
| teach | teach | MIT | 32 | 3000 | fusable |
| improve-codebase-architecture | improve-codebase-architecture | MIT | 68 | 2100 | fusable |
| triage | triage | MIT | 57 | 2300 | fusable |
| retro | retro | MIT | 28 | 1400 | fusable |
| writing-for-agents | writing-for-agents | MIT | 64 | 3400 | fusable |
| interview-me | interview-me | MIT | 173 | 4900 | fusable |
| idea-refine | idea-refine | MIT | 124 | 3300 | fusable |
| debugging-and-error-recovery | debugging-and-error-recovery | MIT | 131 | 3600 | fusable |
| shipping-and-launch | shipping-and-launch | MIT | 108 | 4200 | fusable |
| agent-skills | api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, code-simplification, constraint-driven-development, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, interview-me, observability-and-instrumentation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, source-driven-development, spec-driven-development, test-driven-development, using-agent-skills | MIT | 3779 | 118400 | indivisible |
| mattpocock-skills | ask-matt, code-review, codebase-design, diagnosing-bugs, domain-modeling, grill-me, grill-with-docs, grilling, handoff, implement, implement-spec, improve-codebase-architecture, pr, prototype, research, retro, setup-matt-pocock-skills, tdd, teach, to-questionnaire, to-spec, to-tickets, triage, wait-what, wayfinder, wizard, writing-for-agents | MIT | 1651 | 42110 | fusable |

Class `fusable` = Markdown-only skills, no bundled runtime, scripts, hooks, agents or MCP. `agent-skills` is indivisible as a package (router meta-skill, 4 agents, 9 commands, unwired hook scripts); its single skills are plain Markdown and can be fused one by one. `mattpocock-skills` is fusable by class, but its skills cross-call each other (see Notes).

Per-skill on-invoke, the skills only reachable through a whole-repo plugin:
- agent-skills: using-agent-skills 3400, spec-driven-development 4500, planning-and-task-breakdown 3600, incremental-implementation 3200, test-driven-development 5800, source-driven-development 3500, constraint-driven-development 7600, doubt-driven-development 5800, context-engineering 5300, code-review-and-quality 7400, code-simplification 4700, api-and-interface-design 5200, frontend-ui-engineering 4100, browser-testing-with-devtools 4900, security-and-hardening 6000, performance-optimization 5800, observability-and-instrumentation 4800, ci-cd-and-automation 3900, git-workflow-and-versioning 4800, documentation-and-adrs 3800, deprecation-and-migration 4400. Standalone: interview-me 4900, idea-refine 3300, debugging-and-error-recovery 3600, shipping-and-launch 4200.
- mattpocock-skills: ask-matt 4200, code-review 2100, codebase-design 2000, diagnosing-bugs 2900, domain-modeling 1000, handoff 250, implement 170, implement-spec 920, pr 1300, prototype 920, research 190, setup-matt-pocock-skills 2500, tdd 1200, to-questionnaire 930, to-spec 960, to-tickets 1900, wait-what 90, wayfinder 4100, wizard 1300.
- superpowers: brainstorming 4800, diagnosing-superpowers 2400, dispatching-parallel-agents 2100, executing-plans 6400, finishing-a-development-branch 2700, receiving-code-review 2100, requesting-code-review 1000, subagent-driven-development 7000, systematic-debugging 3400, test-driven-development 3400, using-git-worktrees 2400, using-superpowers 1100, verification-before-completion 1200, writing-plans 3700, writing-skills 6000.
- ponytail: ponytail 1100, ponytail-audit 1800, ponytail-debt 540, ponytail-gain 640, ponytail-help 1100, ponytail-review 1700.

## Baseline
Always-on of the 12 current `1-pack-fundamentals` dependencies: superpowers 848 + andrej-karpathy-skills 105 + humanizer 144 + ponytail 641 + grill-me 34 + grill-with-docs 60 + grilling 70 + teach 32 + improve-codebase-architecture 68 + triage 57 + retro 28 + writing-for-agents 64 = **2151** tokens.
The tool does not count hook injection: superpowers' SessionStart hook adds about 1100 (true always-on about 3250 for the pack), ponytail's three hooks add an unmeasured amount.
Adjusted baseline (Task 5 comparison): the owner moved `claudemem` (always-on 2873) into this pack, so the cost relocates from Context & Memory rather than appearing. Adjusted baseline = 2151 + 2873 = **5024**. Task 5 records the new pack against both numbers.

## Groups
One line per job. Verdict is my proposal: `fuse`, `keep best (<name>)` or `drop`. "Licences" says whether every donor named in the verdict is fusable (MIT/Apache-2.0/BSD/CC0, licence file present).
- interview/grill: interview-me (addy), grilling, grill-me, grill-with-docs, to-questionnaire, wait-what (matt); superpowers:brainstorming overlaps but stays in its pack — fuse interview-me + grilling into one skill; grill-me and grill-with-docs are 20/30-token stubs, drop them; to-questionnaire and wait-what drop — licences: all MIT, yes.
- ideation/planning: idea-refine, spec-driven-development, planning-and-task-breakdown (addy), to-spec, to-tickets, wayfinder, implement, implement-spec, prototype, research (matt); superpowers:writing-plans overlaps but stays — fuse idea-refine + spec-driven-development + planning-and-task-breakdown + to-spec + to-tickets (refine → spec → tickets); wayfinder, implement, implement-spec, prototype, research drop — licences: all MIT, yes.
- debugging: debugging-and-error-recovery, browser-testing-with-devtools (addy), diagnosing-bugs (matt); superpowers:systematic-debugging overlaps but stays — fuse debugging-and-error-recovery + diagnosing-bugs; browser-testing-with-devtools drop (needs the external chrome-devtools MCP) — licences: all MIT, yes.
- review: code-review-and-quality, constraint-driven-development, doubt-driven-development (addy), code-review (matt), pr (matt), karpathy-guidelines; superpowers requesting/receiving-code-review and ponytail-review overlap but stay — fuse code-review-and-quality + code-review + doubt-driven-development; constraint-driven-development drop (7600, niche); pr and karpathy-guidelines are not fusable (pr is derived from a `show-me` skill of unchecked licence, karpathy has no licence file) — licences: yes for the three fused, no for pr and karpathy.
- architecture/domain: improve-codebase-architecture, codebase-design, domain-modeling (matt), api-and-interface-design, deprecation-and-migration (addy) — fuse improve-codebase-architecture + codebase-design + domain-modeling into one self-contained skill (the standalone plugin calls the other two, which are not extracted); api-and-interface-design and deprecation-and-migration drop — licences: all MIT, yes.
- retro/triage: retro, triage (matt), diagnosing-superpowers (stays in superpowers) — keep best (retro): fuse retro with writing-for-agents (retro calls it); triage drop from the essential (needs `setup-matt-pocock-skills` tracker config, calls grilling and domain-modeling) and stays a pointer — licences: all MIT, yes.
- writing: writing-for-agents (matt), humanizer, documentation-and-adrs, git-workflow-and-versioning (addy) — fuse writing-for-agents into the retro skill (above); humanizer is a different job (prose for humans, 10700 on-invoke): keep as its own plugin in the pack, not fused; documentation-and-adrs and git-workflow-and-versioning drop — licences: all MIT, yes.
- shipping/ops: shipping-and-launch, ci-cd-and-automation, observability-and-instrumentation (addy) — keep best (shipping-and-launch); the others drop — licences: MIT, yes.
- coding discipline: karpathy-guidelines, ponytail (+ ponytail-audit/debt/gain/help), code-simplification, test-driven-development (addy), tdd (matt); superpowers:test-driven-development overlaps — karpathy and ponytail stay as plugins in the pack; code-simplification, addy TDD and matt tdd drop (superpowers covers TDD) — licences: karpathy no, others MIT.
- learning: teach (matt) — owner decision, see question (b) — licences: MIT, yes.
- other: ask-matt, handoff, wizard, setup-matt-pocock-skills (matt), using-agent-skills, context-engineering, source-driven-development, incremental-implementation, security-and-hardening, performance-optimization, frontend-ui-engineering (addy) — drop: routers, config, or outside the pack's job — licences: MIT, yes.

## Questions for the owner
- (a) claude-mem was listed as `claudemem` in Context & Memory, not in Fundamentals. You called it an indivisible Fundamentals plugin: does it move to the Fundamentals pack, or stay in Context & Memory?
- (b) `teach` is in the Fundamentals pack in the repo but listed under Learning in the spec §3. Moves it to Learning, or stays?
- (c) The six non-pack Fundamentals plugins (interview-me, idea-refine, debugging-and-error-recovery, shipping-and-launch, agent-skills, mattpocock-skills) are donors too in the verdicts above. Right? And do any of them join the new pack as plugins (as-is)?
- (d) andrej-karpathy-skills declares MIT in plugin.json, the SKILL.md frontmatter and the README, but ships no LICENSE file. Pointer (rule) or trust the declared MIT and fuse?

## Notes
- Hidden always-on: superpowers' SessionStart hook injects the full `using-superpowers` skill (about 1100 tokens) at every start/clear/compact; the tool labels it "harness-only, no model context cost". ponytail's SessionStart, SubagentStart and UserPromptSubmit hooks also inject its ruleset. Neither is in the figures above. A slimmer pack that keeps both gains nothing there.
- superpowers 7.0.1 upstream, 7.0.0 in the local cache (measured on the upstream clone). Its skills cross-reference each other by name, so it stays whole.
- ponytail also carries a mod UI, a `userConfig` CSV ledger at `~/.config/ponytail/band/<project>.csv` and an optional webhook that sends nothing unless the user sets one.
- agent-skills: the four standalone addy plugins are fusable MIT donors that are not in the current pack. The skills measure slightly different standalone vs inside the whole repo (interview-me 4900 vs 5200, shipping-and-launch 4200 vs 3900): tool rounding, not content. The router `using-agent-skills` is meaningless without the rest. `idea-refine` ships three reference .md files and a helper script (not run).
- mattpocock standalone plugins are not self-contained: grill-me and grill-with-docs are stubs calling `grilling` (and `domain-modeling`); improve-codebase-architecture needs `codebase-design`, `grilling`, `domain-modeling`; triage needs `grilling`, `domain-modeling` and the `setup-matt-pocock-skills` config; retro needs `writing-for-agents`. `domain-modeling` and `codebase-design` are not extracted, only reachable through the whole `mattpocock-skills` repo. A fused skill replaces the stubs and the missing links.
- The grill group's real cost is `grilling` at 600: `grill-me` (34 always-on / 20 on-invoke) and `grill-with-docs` (60 / 30) are near-empty stubs.
- Whole-repo `mattpocock-skills` always-on is 1651 against 413 for the 8 extracted plugins: the extraction already saves about 1240 per session.
- Licence: `pr` carries `metadata.credits` to Dex Horthy / humanlayer `show-me`; the upstream licence is unchecked, so treat `pr` as derived work and do not fuse it. Copyright lines for `NOTICE`: Matt Pocock (2026), Addy Osmani (2025), Siqi Chen (2025, humanizer), Jesse Vincent (2025, superpowers), DietrichGebert (2026, ponytail).
- On-invoke excludes sibling reference files read on demand: teach has 4 `*-FORMAT.md` files (SKILL.md 9.7 of 18 KB), triage `AGENT-BRIEF.md` + `OUT-OF-SCOPE.md` (6.6 of 19 KB), improve-codebase-architecture `HTML-REPORT.md` (6 of 12.7 KB), writing-for-agents `SKILL-MECHANICS.md` (10.9 of 13.5 KB). The real cost of a fully exercised skill is higher than the table.
- Many matt skills have `disable-model-invocation: true`; the tool still counts their description toward always-on.
- Whole-repo `mattpocock-skills` lists 27 skills; the clone holds 12 more unexposed SKILL.md directories (not measured).
- Measurement caveat: always-on of the pack in `## Result` (Task 5) is the sum of plugin-level figures, so it is comparable to the Baseline above, not to a hook-inclusive total.

## Donors added at the gate
Owner asked for a discipline skill and a parallelisation skill that draw on wondelai. All MIT with a LICENSE file; on-invoke measured with `claude --plugin-dir <skill dir> plugin details <name>` on the local cache copy (wondelai/skills 1.8.0).

| plugin | skills | licence | always-on | on-invoke | class |
|---|---|---|---|---|---|
| wondelai clean-code | clean-code | MIT | 208 | 5100 | fusable |
| wondelai pragmatic-programmer | pragmatic-programmer | MIT | 238 | 5500 | fusable |
| wondelai software-design-philosophy | software-design-philosophy | MIT | 257 | 5100 | fusable |
| wondelai high-output-management | high-output-management | MIT | 281 | 6600 | fusable |
| wondelai team-topologies | team-topologies | MIT | 260 | 6000 | fusable |

- wondelai/skills: Copyright (c) 2025 Wondel.ai sp. z o.o. The skills summarise published books (Ousterhout, Hunt & Thomas, Martin, Grove, Skelton & Pais); a fused skill takes the ideas in fresh wording, not the text.
- addy `code-simplification` (MIT, 4700) and superpowers `dispatching-parallel-agents` (MIT, 2100) and `subagent-driven-development` (MIT, 7000) are also donors; their plugins stay where they are.
- `claudemem` (thedotmack/claude-mem 15.8.3, plugin.json says Apache-2.0): 30 skills, 9 hooks, 1 MCP server, **always-on 2873**. Measured on the installed cache copy. Stays whole, not a donor.
- `codegraph` is `@colbymchenry/codegraph` 0.9.5 (npm, MIT), a CLI with `serve --mcp`; it ships no Claude Code plugin manifest. A wrapper plugin (MCP only) measures ~0 always-on, like `plugins/camoufox`.

## Decisions
Owner decisions 2026-11-02. The proposals above stand except as corrected below.
- Owner: retro does not matter. `retro` and `writing-for-agents` are dropped, not fused.
- Owner: the coding-discipline group becomes one skill, fusing karpathy-guidelines with our other discipline skills, drawing on wondelai.
- Owner: a new skill explains whether, when and how to launch subagents, teammates or full agents (parallelisation), drawing heavily on wondelai.
- Owner: claude-mem stays its own plugin (entry `claudemem`), in the Fundamentals pack with ponytail and codegraph.
- Owner, during the file-by-file review: `deepen-architecture` is dropped, not fused (the owner would never use it). `improve-codebase-architecture` stays out of the pack and in `plugins[]`, like `retro`; the bound above no longer counts it. Its other donors (mattpocock `codebase-design`, `domain-modeling`; wondelai `software-design-philosophy`) were never in the pack.
- Owner, during the file-by-file review: `review-change` is dropped, not fused. It overlaps `/code-review`, `/security-review` and superpowers' `requesting-code-review`. What goes with it: a spec axis and a standards axis kept apart, the test-mutation check, the doubt loop with the author's claim withheld, and fixed report rules (severity, "zero findings is valid"). Its donors (addy `code-review-and-quality`, `doubt-driven-development`, mattpocock `code-review`) were never in the pack; their plugins stay as plain donors.
- Fused skills (one `SKILL.md` each, name never equals a donor skill):

interview: interview-me, grilling
idea-to-tickets: idea-refine, spec-driven-development, planning-and-task-breakdown, to-spec, to-tickets
root-cause-debug: debugging-and-error-recovery, diagnosing-bugs
discipline: karpathy-guidelines, code-simplification, clean-code, pragmatic-programmer
orchestrate-agents: dispatching-parallel-agents, subagent-driven-development, high-output-management, team-topologies
launch-checklist: shipping-and-launch

pack: fundamentals, superpowers, ponytail, claudemem, codegraph, humanizer, teach

- Pack: superpowers, ponytail and claudemem stay whole (indivisible). humanizer stays a plugin (a different job). teach stays for the pilot; the Learning plan moves it. codegraph is a new local wrapper plugin (Task 5).
- `claudemem` is a dependency of both `1-pack-fundamentals` and `2-pack-context-memory` until the Context & Memory plan decides where it lives; its category stays "Context & Memory". The double membership is intentional and temporary.
- Out of the pack, still in `plugins[]`: grill-me, grill-with-docs, grilling, improve-codebase-architecture, retro, writing-for-agents, triage, andrej-karpathy-skills. The addy and mattpocock-skills plugins stay as plain donors, not in the pack.

## Result
Measured 2026-11-02 with `claude --plugin-dir plugins/fundamentals plugin details fundamentals` (tool rounds the figures). Six skills, 0 hooks, 0 MCP servers.

| fused skill | always-on | on-invoke | donors' on-invoke sum | within bound |
|---|---|---|---|---|
| interview | 50 | 3100 | 5500 (interview-me 4900 + grilling 600) | yes |
| idea-to-tickets | 40 | 5300 | 14260 (idea-refine 3300, spec-driven-development 4500, planning-and-task-breakdown 3600, to-spec 960, to-tickets 1900) | yes |
| root-cause-debug | 50 | 3400 | 6500 (debugging-and-error-recovery 3600 + diagnosing-bugs 2900) | yes |
| discipline | 40 | 2000 | 16150 (karpathy-guidelines 850, code-simplification 4700, clean-code 5100, pragmatic-programmer 5500) | yes |
| orchestrate-agents | 40 | 2000 | 21700 (dispatching-parallel-agents 2100, subagent-driven-development 7000, high-output-management 6600, team-topologies 6000) | yes |
| launch-checklist | 40 | 1600 | 4200 (shipping-and-launch) | yes |

Essential always-on: **265**. Bound (spec §6.3a, "somma dei soli plugin donatori usciti dal pack"): the plugins whose skills were fused and that left the pack, grill-me 34 + grill-with-docs 60 + grilling 70 + andrej-karpathy-skills 105 = **269**. `improve-codebase-architecture` (68) no longer counts: its skill was dropped, not fused. 265 is below it, by 4.
- The first build measured 458 (descriptions of 17-23 words, ~50-60 each) and failed this bound; the review caught a wider reading (486, counting retro, writing-for-agents and triage, which fused nothing) that does not follow the spec. The fix shortened each description to one clause (8-14 words, ~40 each), which keeps the `Not for:` sibling.
- The trade: shorter descriptions give the model less to match on when deciding to invoke a skill. Each still names its job.

### Pack
`1-pack-fundamentals` dependencies, in order: fundamentals 265, superpowers 848, ponytail 641, claudemem 2873, codegraph 0 (MCP wrapper, tool schemas resolved at runtime), humanizer 144, teach 32. Total **4803**.

| comparison | baseline | new pack | verdict |
|---|---|---|---|
| raw (old pack, no claudemem) | 2151 | 4803 | above: +2652, all of it `claudemem` (2873) |
| adjusted (old pack + claudemem moved in) | 5024 | 4803 | below by 221 |
| new pack without `claudemem` | 2151 | 1930 | below by 221 |

- The pack passes the cost rule only on the adjusted baseline. Moving claude-mem in is the owner's call; its 2873 is 30 skills (several look personal to its author: childhood, owner-goals, wowerpoint) and 9 hooks whose injected context the tool does not count.
- Hook-injected context is still uncounted: superpowers (~1100), ponytail, claudemem (9 hooks). True always-on is higher than 4803.
- The pack no longer depends on: grill-me, grill-with-docs, grilling, andrej-karpathy-skills (fused); improve-codebase-architecture, retro, writing-for-agents, triage (dropped). All stay in `plugins[]`.
