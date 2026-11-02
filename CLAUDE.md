# skills

Claude Code and Desktop marketplace `giofornari`. `.claude-plugin/marketplace.json` is the single source of truth: one pack per category, every plugin also installable alone.

## Add a plugin

1. Add an entry to `plugins[]`, grouped by category, with `source` pointing at the upstream repo (`github`, `git-subdir`, `url`, `npm`). Reference upstream; copy nothing, except inside an essential (see Essentials).
2. Add its name to its pack's `dependencies` in `marketplace.json`, unless it is a bonus (`tags: ["bonus"]`).
3. Run `claude plugin validate .`.

## Conventions

- Entry `name` equals the plugin's manifest name. Names starting with `claude-` are reserved: name it for what it does (`session-memory`).
- Extract one skill from a larger repo with `git-subdir` plus `"strict": false, "skills": ["./"]`.
- Keep sources unpinned and set no `version` in `marketplace.json` or any `plugin.json`: updates then follow upstream. The validator's "No version specified" warnings are expected.
- Pack names start with a digit (`1-pack-…`): the `/plugin` list sorts alphabetically, and digits sort first.
- Packs hold dependencies only. Local code lives in `plugins/`: the pack manifests, the essentials, `camoufox`, `graphify`.
- `README.md`, `README.it.md` and every PNG in `docs/` (`docs/it/` and `map.it.png` are the Italian set) mirror `marketplace.json`: names, descriptions, categories, token costs. A new plugin needs its Italian description too. Update all of them in the same commit.

## Essentials

An essential is a local plugin named like its category (`plugins/<category>/`), holding skills fused from several donor plugins. Fusing copies and rewrites, so:

- Only permissive donors (`MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `CC0-1.0`). GPL/AGPL, CC-BY-SA, CC-BY-NC and no-licence repos stay pointers.
- Line after the frontmatter of each fused skill: `> Source: <owner/repo> (<SPDX id>), read <YYYY-MM-DD>`; several sources separated by `; `. List every skill in the plugin's `NOTICE`.
- Cost: the essential's always-on is below the sum of the donors that left the pack; each fused skill's on-invoke is at most the sum of the donor skills it replaces.
- `description` is one line ending `Not for: <sibling skill>.`. A fused skill's name never equals a donor skill's name.
