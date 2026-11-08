#!/usr/bin/env python3
"""Render the README images in docs/ (EN) and docs/it/ (IT) from marketplace.json.

Usage: python3 scripts/docs/build.py [banner|cat|map ...]   (default: all)
Needs google-chrome-stable. Pack token totals are read from the README pack tables.
"""
import json, re, subprocess, sys, tempfile, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FONTS = Path(__file__).parent / "fonts"
CHROME = "google-chrome-stable"

# colour, text on it, per pack number
PACKS = {1: ("#929292", "#141416"), 2: ("#761717", "#f4f4f5"), 3: ("#ff8c38", "#141416"),
         4: ("#3cbc36", "#141416"), 5: ("#fb7081", "#141416"), 6: ("#1c70a5", "#f4f4f5"),
         7: ("#6b0065", "#f4f4f5"), 8: ("#e8b923", "#141416")}
BG, PANEL, CARD, LINE, TEXT, MUTED = "#0e0e10", "#17171a", "#232328", "#2c2c33", "#f0f0f2", "#9a9aa3"

L = {
    "en": dict(sub="Claude Code & Desktop marketplace · {packs} packs · {plugins} plugins", also="Also available",
               inpack="in the pack", avail="also available", tokens="tokens always-on", entries="{n} entries · {p} packs",
               plug="plugins", num=lambda n: f"{n:,}", readme="README.md", out=ROOT / "docs",
               use={1: "Working method, planning, debugging, code intelligence", 2: "Memory across sessions, lighter context",
                    3: "Interface design, taste, copy that sticks", 4: "3D, UX heuristics, design review",
                    5: "Understand codebases, make slides and diagrams", 6: "Web search, scraping, browsing",
                    7: "Video, motion graphics, platform content", 8: "SEO, conversion, sales, marketing"}),
    "it": dict(sub="Marketplace Claude Code & Desktop · {packs} pack · {plugins} plugin", also="Altri disponibili",
               inpack="nel pack", avail="anche disponibili", tokens="token sempre attivi", entries="{n} voci · {p} pack",
               plug="plugin", num=lambda n: f"{n:,}".replace(",", "."), readme="README.it.md", out=ROOT / "docs" / "it",
               use={1: "Metodo di lavoro, pianificazione, debug, intelligenza sul codice", 2: "Memoria tra le sessioni, contesto più leggero",
                    3: "Design di interfacce, gusto, testi che restano", 4: "3D, euristiche UX, design review",
                    5: "Capire codebase, creare slide e diagrammi", 6: "Ricerca web, scraping, navigazione",
                    7: "Video, motion graphics, contenuti dalle piattaforme", 8: "SEO, conversione, vendite, marketing"}),
}

def load():
    plugins = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())["plugins"]
    by = {p["name"]: p for p in plugins}
    packs = sorted((p for p in plugins if "pack" in (p.get("tags") or [])), key=lambda p: p["name"])
    return plugins, by, packs

def repo_of(p):
    s = p["source"] if isinstance(p, dict) else p
    if isinstance(s, str):
        return "giofornari/skills"
    if s.get("repo"):
        return s["repo"]
    if s.get("package"):
        return s["package"]
    m = re.search(r"github\.com/([^/]+/[^/.]+)", s.get("url", ""))
    return m.group(1) if m else s.get("url", "")

def pretty(name):
    return name.replace("-", " ").upper()

def tokens(lang):
    t = {}
    for line in (ROOT / L[lang]["readme"]).read_text().splitlines():
        m = re.match(r"\| `(\d)-pack-[\w-]+` \|.*\| ~([\d.,]+) \|$", line)
        if m:
            t[int(m[1])] = int(re.sub(r"\D", "", m[2]))
    return t

def css(w, h):
    f = lambda n, file, wt="400": f"@font-face{{font-family:'{n}';src:url('file://{FONTS / file}');font-weight:{wt}}}"
    return f"""{f('Bebas','BebasNeue-Regular.ttf')}{f('Inter','Inter.ttf','100 900')}
*{{box-sizing:border-box;margin:0}}html,body{{width:{w}px;height:{h}px;background:{BG};color:{TEXT};
font-family:Inter,sans-serif;overflow:hidden;-webkit-font-smoothing:antialiased}}
.d{{font-family:Bebas,sans-serif;letter-spacing:.01em;line-height:.92}}
.m{{font-family:'DejaVu Sans Mono',monospace}}"""

def shot(body, w, h, out, extra=""):
    page = f"<!doctype html><meta charset=utf-8><style>{css(w, h)}{extra}</style><body>{body}"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(page)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=3000",
                    f"--window-size={w},{h}", f"--screenshot={out}", f"file://{fh.name}"],
                   check=True, capture_output=True)
    Path(fh.name).unlink()

def banner(lang, plugins, packs):
    t = L[lang]
    n_plug = len(plugins) - len(packs)
    tiles = "".join(
        f"<div style='background:{PACKS[i+1][0]};color:{PACKS[i+1][1]};padding:18px 18px 16px;display:flex;flex-direction:column'>"
        f"<div class=d style='font-size:56px;margin-bottom:6px'>{i+1}</div><div class=d style='font-size:33px;line-height:.95'>{html.escape(p['category'].upper())}</div></div>"
        for i, p in enumerate(packs))
    body = f"""<div style='height:232px;padding:0 70px;position:relative'>
<div class=d style='font-size:190px;position:absolute;left:70px;top:26px'>SKILLS</div>
<div class=m style='position:absolute;right:70px;top:62px;background:{PANEL};border:1px solid {LINE};border-radius:10px;padding:20px 24px;font-size:28px'>/plugin marketplace add giofornari/skills</div>
<div style='position:absolute;left:78px;top:190px;font-size:26px;color:{MUTED}'>{t['sub'].format(packs=len(packs), plugins=n_plug)}</div></div>
<div style='display:grid;grid-template-columns:repeat(8,minmax(0,1fr));height:150px'>{tiles}</div>"""
    shot(body, 1600, 382, t["out"] / "banner.png")

def cat(lang, plugins, by, packs):
    t, tok = L[lang], tokens(lang)
    for i, p in enumerate(packs, 1):
        deps = {d.split("@")[0] for d in p["dependencies"]}
        others = [q for q in plugins if q["category"] == p["category"] and "pack" not in (q.get("tags") or []) and q["name"] not in deps]
        c, fg = PACKS[i]
        body = f"""<div style='display:flex;height:190px'>
<div style='width:640px;background:{c};color:{fg};padding:34px 50px'><div class=d style='font-size:{96 if len(p['category'])<=14 else 62}px;white-space:nowrap'>{html.escape(p['category'].upper())}</div>
<div class=m style='font-size:24px;margin-top:14px;opacity:.75'>{p['name']}</div></div>
<div style='flex:1;background:{PANEL};padding:0 50px;display:flex;flex-direction:column;justify-content:center'><div style='font-size:34px;line-height:1.25;max-width:820px'>{html.escape(t['use'][i])}</div>
<div class=m style='margin-top:26px;font-size:24px;color:{MUTED}'>{len(deps)} {t['inpack']} · {(str(len(others)) + ' ' + t['avail'] + ' · ') if others else ''}~{t['num'](tok[i])} {t['tokens']}</div></div></div>"""
        shot(body, 1600, 190, t["out"] / f"cat-{i}-{re.sub(r'[^a-z]+', '-', p['category'].lower()).strip('-')}.png")

def mapimg(lang, plugins, by, packs):
    """Pack board: one row per pack, the plugin names it installs. Sized to stay readable at README width."""
    t, W, rows, H = L[lang], 1200, [], 0
    for i, p in enumerate(packs, 1):
        c, fg = PACKS[i]
        names = [d.split("@")[0] for d in p["dependencies"]]
        chips = "".join(f"<span style='background:{CARD};border:1px solid {LINE};border-radius:8px;padding:9px 16px;font-size:24px;font-weight:600'>{html.escape(n)}</span>" for n in names)
        lines, x = 1, 0  # greedy wrap with an estimated chip width (24px semibold ~ 12.8px/char + padding)
        for n in names:
            w = len(n) * 12.8 + 34 + 10
            if x + w > 836 and x:
                lines, x = lines + 1, 0
            x += w
        h = max(110, 36 + 59 * lines)
        H += h + 12
        rows.append(f"""<div style='display:flex;min-height:{h}px;background:{PANEL};border-radius:10px;overflow:hidden;margin-bottom:12px'>
<div style='width:320px;flex:none;background:{c};color:{fg};padding:0 28px;display:flex;align-items:center;gap:18px'>
<div class=d style='font-size:72px'>{i}</div><div class=d style='font-size:42px;line-height:.95'>{html.escape(p['category'].upper())}</div></div>
<div style='flex:1;padding:18px 22px;display:flex;flex-wrap:wrap;gap:10px;align-content:center'>{chips}</div></div>""")
    shot(f"<div style='padding:0'>{''.join(rows)}</div>", W, H - 12, t["out"] / "map.png" if lang == "en" else t["out"].parent / "map.it.png")

if __name__ == "__main__":
    what = set(sys.argv[1:]) or {"banner", "cat", "map"}
    plugins, by, packs = load()
    for lang in L:
        if "banner" in what: banner(lang, plugins, packs)
        if "cat" in what: cat(lang, plugins, by, packs)
        if "map" in what: mapimg(lang, plugins, by, packs)
