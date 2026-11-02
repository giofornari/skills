# Content & Media and Learning — donor inventory
Read: 2026-11-02

## Content & Media
| plugin | skills | licence | always-on | on-invoke | class |
|---|---|---|---|---|---|
| openmontage | 91 skills (abbreviated: 3d-asset-generation, acestep, ai-video-gen, create-video, elevenlabs, ffmpeg, gsap-*, heygen, hyperframes*, media-use, remotion, remotion-best-practices, remotion-to-hyperframes, threejs-*, video-*, website-to-video) | AGPL-3.0 | 11462 | 298980 | indivisible |
| hyperframes | figma, hyperframes, hyperframes-cli, hyperframes-registry, media-use, remotion-to-hyperframes, reverse-any-video, slideshow | Apache-2.0 | 888 | 15900 | indivisible |
| remotion | remotion-best-practices, remotion-captions, remotion-create, remotion-docs, remotion-interactivity, remotion-license, remotion-maps, remotion-markup, remotion-multimedia, remotion-render, remotion-saas, remotion-studio, remotion-upgrade | none | 310 | 15840 | fusable |
| ppt-master | ppt-master | MIT | 206 | 3500 | indivisible |
| diagram-design | diagram-design, doctor, export-diagram, import-drawio, import-excalidraw, import-mermaid, profile | MIT | 600 | 17140 | indivisible |
| anatomy | anatomy | MIT | 367 | 12000 | indivisible |
| academic-pptx-skill | academic-pptx | MIT | 289 | 2300 | fusable |

Overlap by function: video generation overlaps across openmontage, hyperframes and remotion (openmontage vendors copies of the hyperframes, remotion and gsap skills).
Diagrams overlap between diagram-design and anatomy, and slides between ppt-master and academic-pptx-skill.
Only remotion and academic-pptx-skill are Markdown-only, and they do not overlap each other (video vs. slides).
Recommendation: pack only
Reason: only two fusable donors exist, remotion has no licence and academic-pptx-skill overlaps with no other fusable donor (slides vs. video and diagrams).
The overlapping video and diagram donors are indivisible (hyperframes, anatomy, diagram-design, ppt-master) or AGPL (openmontage), so there is nothing permissive to fuse.

## Learning
| plugin | skills | licence | always-on | on-invoke | class |
|---|---|---|---|---|---|
| understand-anything | understand, understand-chat, understand-dashboard, understand-diff, understand-domain, understand-explain, understand-figma, understand-knowledge, understand-onboard | MIT | 1148 | 41600 | indivisible |
| education-agent-skills | 165 skills in 20 categories (abbreviated: backwards-design-unit-planner, kud-chart-author, retrieval-practice-generator, ...) | CC-BY-SA-4.0 | 13026 | 1030600 | fusable |
| i-have-adhd | i-have-adhd | MIT | 106 | 2400 | indivisible |

Overlap by function: none. understand-anything explains codebases, education-agent-skills supports teachers with lesson and assessment design, i-have-adhd shapes response style.
teach (mattpocock/skills) is also a Learning member but lives in Fundamentals today; it is a pointer and not analysed here.
Recommendation: pack only
Reason: understand-anything (hooks, agents, Node) and i-have-adhd (hook) are indivisible, and the only Markdown donor, education-agent-skills, is CC-BY-SA-4.0 and stays a pointer.
The three donors do different jobs, so no two permissive Markdown donors overlap in function.

## Notes
- Method: `claude --plugin-dir <dir> plugin details <name>` (claude 2.1.316), run from the repo root. Figures are rounded by the tool. On-invoke is the sum of the per-skill rounded figures. Always-on is the plugin's reported figure.
- Directories measured: synthetic wrapper plugins for anatomy, academic-pptx-skill and openmontage (their marketplace entries use `strict: false` with custom skill paths; openmontage wraps `.agents/skills`); the `skills` subdirectory for ppt-master (plugin name `ppt-master`); the `understand-anything-plugin` subdirectory for understand-anything; the repo root for the others.
- No measurement failed, so no character-count estimates were used.
- understand-anything: on-invoke counts the 9 skills only. Its 10 agents add about 50370 (91970 across all 19 components).
- Skill lists for openmontage and education-agent-skills are abbreviated for readability; the counts are exact.
- Class rule: fusable means Markdown-only skills with no bundled runtime, scripts, hooks, agents or MCP. indivisible means hooks, agents, a bundled Node or Python runtime or toolchain, or a methodology that works only whole.
- diagram-design: indivisible is borderline (no hooks, but scripts and templates are bundled). The recommendation is the same either way, because no other fusable permissive diagram donor exists (anatomy needs a Node/Chrome kit).
- hyperframes: `.codex/hooks.json` is Codex-only. The Claude plugin has 0 hooks. Its skills are Markdown but drive the repo's own CLI and runtime (`packages/`), so they work only with that toolchain; classified indivisible. Even if reclassified fusable, it would still be the only permissive video donor, so the recommendation does not change.
- Licence caveats:
  - remotion has no LICENSE file (plugin.json says MIT). The Remotion library has its own licence, and the plugin ships a `remotion-license` skill pointing at it. Treat as a pointer.
  - academic-pptx-skill: the LICENSE file is MIT, but the SKILL.md frontmatter says "Proprietary. LICENSE.txt has complete terms". The two conflict. Confirm with the author before fusing.
  - education-agent-skills is CC-BY-SA-4.0, a pointer. openmontage is AGPL-3.0, a pointer.
  - diagram-design bundles third-party assets: Tabler (MIT), Simple Icons (CC0), log-z (MIT), Devicon (MIT), Instrument Serif (OFL 1.1).
- academic-pptx resolution: the exact name `academic-pptx` is not a marketplace entry. It is the skill inside the entry `academic-pptx-skill` (github Gabberflast/academic-pptx-skill, category Learning, bonus). Classified by function into Content & Media.
- Classification by function, not by current marketplace category: ppt-master, diagram-design and anatomy sit under Learning in the current marketplace but are counted in Content & Media.
