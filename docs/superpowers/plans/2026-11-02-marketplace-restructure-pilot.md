# Marketplace restructure, phase 1 (Fundamentals pilot) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `restructure` branch, build the `fundamentals` essential plugin and the new `1-pack-fundamentals`, and inventory Content & Media and Learning, so the method is validated before it is repeated.

**Architecture:** `marketplace.json` stays the single source of truth. The essential is a local plugin in `plugins/fundamentals/` with fused skills; the pack stays a dependencies-only plugin. Verification is `jq`/`grep` assertions plus `claude plugin validate .` and `claude plugin details` for token cost.

**Tech Stack:** git, jq, the `claude plugin` CLI, Markdown skills.

**Spec:** `docs/superpowers/specs/2026-11-02-marketplace-restructure-design.md`

**Scope:** spec §6 phase 1 and §6.3 only. The other categories (§6.2) and the docs sync (§6.4, §8) are separate plans, written after this pilot is approved: their donors and fused skills depend on analysis that does not exist yet, and the spec makes the pilot the validation of the method.

## Global Constraints

- All work on branch `restructure`; one merge to `main`, at the end of all phases, not in this plan.
- No `version` in `marketplace.json` or any `plugin.json`; sources unpinned. "No version specified" validator warnings are expected.
- Packs hold only `dependencies`; pack names start with a digit (`1-pack-fundamentals`); the essential has the clean name `fundamentals`.
- Only sources with MIT, Apache-2.0, BSD or CC0 licences may be fused. GPL/AGPL, CC-BY-SA, CC-BY-NC and repos without a licence file stay pointers.
- Every fused skill carries a source line (repo, licence, date read); the plugin carries a `NOTICE`.
- Essential cost must be below the sum of the donor plugins that left the pack; new pack cost below the current pack cost.
- A fused skill's `description` must trigger distinctly from the originals (the owner accepts the duplication, not the competition).
- Existing ids break cleanly: no stub packs. READMEs and PNGs are not touched in this plan.
- Entries in `plugins[]` of donors that leave the pack stay in `marketplace.json`.

## Review Focus

1. A donor with a missing or odd licence file (none, dual, custom): must be classified non-fusable, never blank. Pinned in Task 2.
2. A fused skill named like a donor skill (`grill-me`, `grilling`): two skills with one name in the same session. Pinned in Task 4.
3. A "fusion" that is a concatenation: fused body costing more on invoke than the donors it replaces. Pinned in Task 4.
4. A pack dependency left dangling after donors leave the pack. Pinned in Task 5.
5. A fused skill without its source line or `NOTICE` entry. Pinned in Task 4.

---

### Task 1: Branch and CLAUDE.md rule

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Produces: the source-line format every fused skill uses, defined exactly once, here: `> Source: <owner/repo> (<SPDX id>), read <YYYY-MM-DD>` placed on the line after the frontmatter; several sources are separated by `; `. Allowed SPDX ids: `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `CC0-1.0`.

- [ ] **Step 1: Create the branch.** Run `git switch -c restructure`. Expected: `Switched to a new branch 'restructure'`. The untracked `docs/superpowers/` carries over.
- [ ] **Step 2: Failing check.** Run `grep -c '^## Essentials' CLAUDE.md`. Expected: `0`.
- [ ] **Step 3: Edit `CLAUDE.md`.** (a) In "Add a plugin" step 1, change "Reference upstream; copy nothing." to "Reference upstream; copy nothing, except inside an essential (see Essentials)." (b) In Conventions, change the local-code bullet to list "the pack manifests, the essentials, `camoufox`, `graphify`". (c) Add a section `## Essentials` of at most 10 lines stating: an essential is a local plugin named like its category in `plugins/<category>/`, holding skills fused from several donor plugins; the permissive-licence rule; the source-line format from this task's Interfaces; the `NOTICE` file; the two cost rules; the single-line `description` ending with `Not for: <sibling skill>.` (my call: it makes trigger separation checkable); fused skill names never equal a donor skill name.
- [ ] **Step 4: Verify.** Run `grep -c '^## Essentials' CLAUDE.md` (expect `1`) and `grep -c 'copy nothing, except' CLAUDE.md` (expect `1`).
- [ ] **Step 5: Commit CLAUDE.md, then the docs.**

```bash
git add CLAUDE.md && git commit -m "docs: allow fused skills in essentials, with licence and attribution rule"
git add docs/superpowers && git commit -m "docs: marketplace restructure design and pilot plan"
```

### Task 2: Fundamentals analysis (read-only)

**Files:**
- Create: `docs/superpowers/analysis/2026-11-02-fundamentals.md`

**Interfaces:**
- Produces: a table with exactly these columns, one row per donor, used by Tasks 3-5: `| plugin | skills | licence | always-on | on-invoke | class |`. `class` is `indivisible` (hooks, daemon, MCP, or a methodology that only works whole) or `fusable` (Markdown skills). `licence` is an SPDX id or `none`; never empty. Also a `## Baseline` section with the current pack cost: the sum of `always-on` over the 12 current dependencies of `1-pack-fundamentals`.

Donors: the 12 dependencies of `1-pack-fundamentals` (`superpowers`, `andrej-karpathy-skills`, `humanizer`, `ponytail`, `grill-me`, `grill-with-docs`, `grilling`, `teach`, `improve-codebase-architecture`, `triage`, `retro`, `writing-for-agents`) plus the other `category == "Fundamentals"` entries (`mattpocock-skills`, `interview-me`, `idea-refine`, `debugging-and-error-recovery`, `shipping-and-launch`, `agent-skills`). **Fan-out:** run about 3 subagents in parallel, split by upstream repo (`mattpocock/skills`; `addyosmani/agent-skills`; everything else). Each writes a partial `docs/superpowers/analysis/fundamentals-<group>.md` with the same columns and reads nothing else of the analysis. The executor merges the partials into `2026-11-02-fundamentals.md`, computes `## Baseline` and writes Steps 3-4 itself. Task 2 runs in parallel with Task 6.

- [ ] **Step 1: Clone each distinct upstream repo** (shallow) into the scratchpad `clones/` directory. Source repos are in `jq -r '.plugins[]|select(.category=="Fundamentals")|.source' .claude-plugin/marketplace.json`.
- [ ] **Step 2: Fill the table.** Licence from the repo's `LICENSE*` file (SPDX id; `none` if absent). Costs: for an installed plugin `claude plugin details <name>`; otherwise `claude --plugin-dir <clone-or-subdir> plugin details <dir-name>` (works on a bare skill directory). Take "Always-on" and the sum of on-invoke per skill.
- [ ] **Step 3: Group the fusable skills by job** (interview/grill, planning, debugging, review, architecture, writing, retro/triage). For each group write one line: `fuse`, `keep best (name)` or `drop`, and whether every donor in it has a fusable licence.
- [ ] **Step 4: Add `## Questions for the owner`** with these three, which the spec and the repo disagree on: (a) the spec lists `claude-mem` as a Fundamentals indivisible, but in the repo it is `session-memory`, in Context & Memory; (b) the spec table puts `teach` in Learning, the repo has it in Fundamentals; (c) are the non-pack Fundamentals plugins donors too.
- [ ] **Step 5: Verify no empty licence cell.** Run `awk -F'|' '/^\| [a-z]/ && $4 ~ /^ *$/ {print "MISSING: "$2}' docs/superpowers/analysis/2026-11-02-fundamentals.md`. Expected: no output. Also expect `grep -c '^## Baseline'` to print `1`.
- [ ] **Step 6: Commit** `git add docs/superpowers/analysis && git commit -m "docs: fundamentals donor analysis"`.

### Task 3: Owner review gate

**Files:**
- Modify: `docs/superpowers/analysis/2026-11-02-fundamentals.md` (append `## Decisions`)

No building before this task is done. Present the analysis to the owner: the table, the groups with licence verdicts, the three questions, the baseline.

- [ ] **Step 1: Ask the owner** to decide, per group: fuse / keep best / drop; the answers to (a)-(c); the names of the fused skills (the builder proposes, none may equal a donor skill name); the list of indivisible plugins that stay in the pack.
- [ ] **Step 2: Append `## Decisions`** with one line per fused skill: `<fused-name>: <donor skills>` and one line `pack: <dependency list, in order, fundamentals first>`.
- [ ] **Step 3: Verify.** Run `grep -c '^pack: fundamentals' docs/superpowers/analysis/2026-11-02-fundamentals.md`. Expected: `1`.
- [ ] **Step 4: Commit** `git commit -am "docs: fundamentals decisions"`.

### Task 4: The `fundamentals` essential

**Files:**
- Create: `plugins/fundamentals/.claude-plugin/plugin.json`
- Create: `plugins/fundamentals/skills/<fused-name>/SKILL.md` (one per `## Decisions` line)
- Create: `plugins/fundamentals/NOTICE`
- Modify: `.claude-plugin/marketplace.json` (new entry)

**Interfaces:**
- Consumes: the fused-skill list and donors from `## Decisions`; the source-line format from Task 1; the table from Task 2.
- Produces: plugin `fundamentals`, with a marketplace entry `{"name":"fundamentals","source":"./plugins/fundamentals","category":"Fundamentals","tags":["essential"],"description":...}` (the `essential` tag is my call: it lets later plans and the README tell essentials from plugins).

- [ ] **Step 1: Write the checks first** into `$SCRATCH/check-fundamentals.sh` (`SCRATCH` = the scratchpad dir), as five assertions, each printing `FAIL: <what>`:
  1. manifest: `jq -e '.name=="fundamentals"' plugins/fundamentals/.claude-plugin/plugin.json`
  2. every `SKILL.md` has a `^> Source: .+ \(.+\), read [0-9]{4}-[0-9]{2}-[0-9]{2}$` line, and every licence in those lines is one of the five allowed ids
  3. `NOTICE` contains each skill directory name
  4. no skill directory name appears in the `skills` column of the Task 2 table (`awk -F'|' '/^\| [a-z]/{print $3}' ... | tr ',' '\n' | tr -d ' ' | sort -u`, then `comm -12` with `ls plugins/fundamentals/skills | sort`; expect empty)
  5. each `SKILL.md` has a single-line `description:` that contains `Not for:`
- [ ] **Step 2: Run the checks.** Expected: FAILs (the plugin does not exist yet).
- [ ] **Step 3: Write `plugin.json`** (`name`, `description`, `author` as in `plugins/graphify/.claude-plugin/plugin.json`; no `version`).
- [ ] **Step 4: Write each fused `SKILL.md`.** Frontmatter `name` equals the directory; the source line right after it. Fuse, do not concatenate: the shared core appears once; each donor's distinct technique stays as a named option or section; drop what only repeats. Body budget: on-invoke cost at most the sum of the on-invoke costs of the donor skills it replaces, as measured in Task 2.
- [ ] **Step 5: Write `NOTICE`:** per fused skill, its name and the same source info as its source line (repo, licence, date).
- [ ] **Step 6: Add the marketplace entry** with `jq` or `Edit`; place it first among the Fundamentals entries.
- [ ] **Step 7: Run the checks and validate.** Expected: the script prints nothing; `claude plugin validate .` ends with `Validation passed with warnings`, warnings only about versions.
- [ ] **Step 8: Measure.** Run `claude --plugin-dir plugins/fundamentals plugin details fundamentals`. Expected: (a) Always-on below the sum of the always-on of the donors that leave the pack; (b) for each fused skill, on-invoke at most the sum of the on-invoke of the donor skills it replaces (the Review Focus 3 check: a body above that sum is a concatenation). Write the numbers under `## Result` in the analysis file, one line per skill. If a bound fails, shorten the descriptions and bodies, or drop a skill, and re-measure.
- [ ] **Step 9: Commit** `git add plugins/fundamentals .claude-plugin/marketplace.json docs && git commit -m "feat: fundamentals essential"`.

### Task 5: Rewrite `1-pack-fundamentals`

**Files:**
- Modify: `.claude-plugin/marketplace.json` (entry `1-pack-fundamentals`: `dependencies`, `description`)

**Interfaces:**
- Consumes: the `pack:` line of `## Decisions`.

- [ ] **Step 1: Failing checks.** Run `jq -e '.plugins[]|select(.name=="1-pack-fundamentals")|.dependencies[0]=="fundamentals"' .claude-plugin/marketplace.json`. Expected: `false` (non-zero exit).
- [ ] **Step 2: Set `dependencies`** to the `pack:` list, `fundamentals` first; update `description` to list the members. Leave every donor entry in `plugins[]`.
- [ ] **Step 3: Dependencies resolve** (all packs):
  `jq -e '[.plugins[].name] as $n | [.plugins[]|select((.tags//[])|index("pack"))|.dependencies[]] | all(. as $d | $n|index($d))' .claude-plugin/marketplace.json`. Expected: `true`.
- [ ] **Step 4: Donors left.** For each fused donor, `jq -e '.plugins[]|select(.name=="1-pack-fundamentals")|.dependencies|index("<donor>")|not'`. Expected: `true`.
- [ ] **Step 5: Cost.** Sum the always-on of the new pack's dependencies (installed: `claude plugin details`; others as in Task 2). Expected: below the `## Baseline` figure. Add the two numbers to `## Result`.
- [ ] **Step 6: Validate.** `claude plugin validate .`. Expected: `Validation passed with warnings`.
- [ ] **Step 7: Commit** `git commit -am "feat: slim 1-pack-fundamentals around the essential"`.

### Task 6: Content & Media and Learning inventory (read-only)

**Files:**
- Create: `docs/superpowers/analysis/2026-11-02-content-learning-inventory.md`

Runs as one subagent, **in parallel with Task 2** (it shares nothing with it). `teach` is covered by Task 2; list it here only as a pointer.

- [ ] **Step 1: For each donor** in Content & Media (`openmontage`, `hyperframes`, `remotion`, `ppt-master`, `diagram-design`, `anatomy`, `academic-pptx`) and Learning (`understand-anything`, `education-agent-skills`, `i-have-adhd`, and `teach` if the owner answered (b) with Learning), record skills, licence, always-on cost and class, as in Task 2.
- [ ] **Step 2: Give each category** `Recommendation: essential` (at least two Markdown-skill donors that overlap in function, with permissive licences) or `Recommendation: pack only`, with two lines of reasoning.
- [ ] **Step 3: Verify.** Run `grep -c '^Recommendation:' docs/superpowers/analysis/2026-11-02-content-learning-inventory.md`. Expected: `2`.
- [ ] **Step 4: Commit** `git add docs && git commit -m "docs: content and learning inventory"`.

### Task 7: Pilot sign-off

- [ ] **Step 1: Run** `claude plugin validate .` and the Task 4 check script once more on the final tree. Expected: validation passes, script prints nothing.
- [ ] **Step 2: Show the owner** the cost table (essential vs donors left, new pack vs baseline), the Content & Media / Learning recommendations, and `git log --oneline main..restructure`.
- [ ] **Step 3: Stop for the owner's approval of the method.** Then write the follow-up plans: one per remaining category (Design first, then Marketing & Sales), each reusing Tasks 2-5; and one for the docs sync (READMEs, PNGs, Italian descriptions, "old id → new id" table, pack renumbering 1-7, category renames, the merge to `main`).
