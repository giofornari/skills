# skills

Claude Code and Desktop marketplace `giofornari`. `.claude-plugin/marketplace.json` is the single source of truth: one pack per category, every plugin also installable alone.

## Add a plugin

1. Add an entry to `plugins[]`, grouped by category, with `source` pointing at the upstream repo (`github`, `git-subdir`, `url`, `npm`). Reference upstream; copy nothing.
2. Add its name to its pack's `dependencies` in `marketplace.json`, unless it is a bonus (`tags: ["bonus"]`).
3. Run `claude plugin validate .`.

## Conventions

- Entry `name` equals the plugin's manifest name. Names starting with `claude-` are reserved: name it for what it does (`session-memory`).
- Extract one skill from a larger repo with `git-subdir` plus `"strict": false, "skills": ["./"]`.
- Keep sources unpinned and set no `version` in `marketplace.json` or any `plugin.json`: updates then follow upstream. The validator's "No version specified" warnings are expected.
- Packs hold dependencies only. Local code lives in `plugins/`: the pack manifests, `camoufox`, `graphify`.
