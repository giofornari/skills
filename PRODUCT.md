# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Claude Code and Claude Desktop users who want a curated set of skills, MCP servers and tools without hunting through repos. They arrive from a GitHub link and either install a pack in a minute or scan the catalog and token costs before choosing. The owner (a developer and student) uses it as his own setup.

## Product Purpose

`giofornari/skills` is a Claude Code/Desktop marketplace: one pack per category (8), every plugin also installable alone. `.claude-plugin/marketplace.json` is the single source of truth; entries point at upstream repos and follow their latest version. Success: a reader installs a pack, or picks plugins knowing what each adds to every session.

## Positioning

Curated by use, not exhaustive: every entry is something the owner runs. Token cost is shown per plugin and per pack. Only the `fundamentals` essential carries rewritten (permissively licensed) code; everything else is a pointer.

## Brand and voice

Direct, concise, useful. Lean text, no filler. The existing identity is the commitment: dark ground, condensed display face (Bebas Neue), Inter for text, monospace only for commands, one color per pack (grey, maroon, orange, green, pink, blue, purple, yellow). Bilingual: English and Italian sets mirror each other.

## Constraints

- README.md, README.it.md and every PNG in docs/ (docs/it/ and map.it.png are the Italian set) mirror marketplace.json: names, descriptions, categories, token costs.
- Images are static PNG (GitHub README). A new plugin needs its Italian description.
- Open decisions: none recorded.
