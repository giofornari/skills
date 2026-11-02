---
name: sharpen-intent
description: "Interview or grill the user until intent is clear. Not for: idea-to-tickets."
---
> Source: addyosmani/agent-skills (MIT), read 2026-11-02; mattpocock/skills (MIT), read 2026-11-02

# Sharpen Intent

What people ask for and what they want differ ("a dashboard" because that is what one asks for). The cheapest moment to close the gap is before any plan, spec or code exists; afterwards switching costs lock the misfit in. Deliverable: a **confirmed statement of intent**.

## Use when

- The ask lacks **who**, **why now**, **success** or the binding **constraint**, or is conventional ("build me X", "make it faster").
- The user brings a plan or decision to stress-test ("grill me", "interview me", "are we sure?").
- You catch yourself filling gaps silently, or two values are in tension (simplicity vs flexibility, cost vs speed) and nobody picked.

Skip when the ask is unambiguous and mechanical (rename, typo), a pure information question, the user asked for speed, or you already predict their answers. Needs a live user: in CI, `/loop` or autonomous runs, flag the gap as a blocker instead of guessing.

## Process

1. **Hypothesis.** One sentence on what you think they want, plus an honest confidence %. Under ~70%, add what is missing. If you cannot predict their reaction to your next three questions, the number is too high.
2. **Pick the mode.**
   - *Interview*: vague ask, little structure. One question per turn; the next depends on the answer.
   - *Grill*: a plan or decision whose parts depend on each other. Map it as a **design tree**; the **frontier** is every decision whose prerequisites are settled. Ask the whole frontier in one numbered round. A question that depends on another still open waits for a later round. Each answer reshapes the tree: recompute the frontier and go again.
   - Switch to grill when an interview reveals a tree; back to interview when the user stalls.
3. **Every question carries your recommended answer**, worded so "yes" accepts it:
   ```
   Q1 <title>: <question, with options if useful>
   → <your recommended answer and why>
   ```
   A wrong guess is reacted to faster than an empty question is answered. Be visibly willing to be wrong, and sometimes guess against what you expect, so a polite user cannot just agree.
4. **Facts are your job, decisions are theirs.** Never ask for what the filesystem, docs or tools can tell you; look it up, or hand it to a fresh-context sub-agent and keep asking the questions that do not depend on it.
5. **Listen for "should want".** Best-practice talk ("scalable", "clean", "the standard way", "I should probably…") is not intent. Probe: *"If you didn't have to justify this to anyone, what would you actually want?"*
6. **Restate** in their words, 5-8 lines, correctable line by line:
   ```
   Outcome / User / Why now / Success / Constraint / Out of scope
   Yes, no, or refine?
   ```
   "Out of scope" is mandatory: half of misalignment is silent disagreement about what is not built.
7. **Wait for an explicit yes.** "Whatever you think", "sounds good", "sure, let's go" and silence are not yes: re-ask with two concrete options, or ask "anything to refine?". Fold corrections in, restate, loop.
8. **Stop the turn.** After the yes, deliver the statement, offer next steps (save to `docs/intent/<topic>.md`, hand to `idea-to-tickets`), and stop. Start no downstream work and call no tools until they choose.

## Done

You are done when the frontier is empty, nothing is silently assumed, and you can predict their reaction to the next three questions. After several rounds with no rise in confidence, say so: "Something foundational is missing. Want to step back?"

## Red flags

- Several unrelated questions in one message in interview mode, or a grill round with questions that depend on each other.
- A question with no recommended answer; a confidence below 70% with no reason.
- Accepting a hollow yes; drafting a spec or plan before the yes; saving the intent doc before it.
- Skipping "Out of scope"; asking the user for something you could look up.
