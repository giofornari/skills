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
        f"<div class=d style='font-size:48px;margin-bottom:14px'>{i+1}</div><div><div class=d style='font-size:32px;line-height:1;min-height:64px'>{html.escape(p['category'].upper())}</div>"
        f"<div style='font-size:14px;line-height:1.3;margin-top:8px;opacity:.85'>{html.escape(t['use'][i+1])}</div></div></div>"
        for i, p in enumerate(packs))
    body = f"""<div style='height:232px;padding:0 70px;position:relative'>
<div class=d style='font-size:190px;position:absolute;left:70px;top:26px'>SKILLS</div>
<div class=m style='position:absolute;right:70px;top:62px;background:{PANEL};border:1px solid {LINE};border-radius:10px;padding:20px 24px;font-size:28px'>/plugin marketplace add giofornari/skills</div>
<div style='position:absolute;left:78px;top:190px;font-size:26px;color:{MUTED}'>{t['sub'].format(packs=len(packs), plugins=n_plug)}</div></div>
<div style='display:grid;grid-template-columns:repeat(8,minmax(0,1fr));height:188px'>{tiles}</div>"""
    shot(body, 1600, 420, t["out"] / "banner.png")

def cat(lang, plugins, by, packs):
    t, tok = L[lang], tokens(lang)
    for i, p in enumerate(packs, 1):
        deps = {d.split("@")[0] for d in p["dependencies"]}
        others = [q for q in plugins if q["category"] == p["category"] and "pack" not in (q.get("tags") or []) and q["name"] not in deps]
        c, fg = PACKS[i]
        body = f"""<div style='display:flex;height:190px'>
<div style='width:640px;background:{c};color:{fg};padding:34px 50px'><div class=d style='font-size:{96 if len(p['category'])<=14 else 62}px;white-space:nowrap'>{html.escape(p['category'].upper())}</div>
<div class=m style='font-size:24px;margin-top:14px;opacity:.75'>{p['name']}</div></div>
<div style='flex:1;background:{PANEL};padding:0 50px;display:flex;flex-direction:column;justify-content:center'><div style='font-size:30px;line-height:1.25;max-width:760px'>{html.escape(t['use'][i])}</div>
<div class=m style='margin-top:26px;font-size:20px;color:{MUTED}'>{len(deps)} {t['inpack']} · {(str(len(others)) + ' ' + t['avail'] + ' · ') if others else ''}~{t['num'](tok[i])} {t['tokens']}</div></div></div>"""
        shot(body, 1600, 190, t["out"] / f"cat-{i}-{re.sub(r'[^a-z]+', '-', p['category'].lower()).strip('-')}.png")

def card(name, repo):
    return (f"<div style='background:{CARD};border:1px solid {LINE};border-radius:8px;padding:14px 16px;min-height:104px;gap:6px;display:flex;flex-direction:column;justify-content:space-between'>"
            f"<div class=d style='font-size:28px;line-height:1'>{html.escape(name)}</div>"
            f"<div style='font-size:17px;color:{MUTED};white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{html.escape(repo)}</div></div>")

def mapimg(lang, plugins, by, packs):
    t = L[lang]
    W, rows, H = 2400, [], 190
    for i, p in enumerate(packs, 1):
        c, fg = PACKS[i]
        deps = [d for d in p["dependencies"]]
        members = []
        for d in deps:
            n, _, mk = d.partition("@")
            members.append(card(pretty(n), repo_of(by[n]) if n in by else f"{mk}/{n}"))
        others = [q for q in plugins if q["category"] == p["category"] and "pack" not in (q.get("tags") or []) and q["name"] not in {d.split("@")[0] for d in deps}]
        oc = [card(pretty(q["name"]), repo_of(q)) for q in others]
        mr, orow = -(-len(members) // 4), -(-len(oc) // 3)
        h = max(mr, orow, 1) * 116 + 28
        right = (f"<div style='border-left:1px solid {LINE};padding-left:22px;flex:1;min-width:0'><div style='font-size:16px;letter-spacing:.12em;color:{MUTED};margin-bottom:12px;text-transform:uppercase'>{t['also']}</div>"
                 f"<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:12px'>{''.join(oc)}</div></div>") if oc else ""
        rows.append(f"""<div style='display:flex;background:{PANEL};border-radius:10px;overflow:hidden;min-height:{h + (36 if oc else 0)}px;margin-bottom:14px'>
<div style='width:360px;flex:none;background:{c};color:{fg};padding:0 34px;display:flex;flex-direction:column;justify-content:center'>
<div class=d style='font-size:54px'>{html.escape(p['category'].upper())}</div><div class=m style='font-size:18px;margin-top:10px;opacity:.75'>{p['name']}</div></div>
<div style='flex:1;padding:18px;display:flex;gap:22px;align-items:flex-start'><div style='display:grid;grid-template-columns:repeat(4,1fr);gap:12px;width:1010px;flex:none'>{''.join(members)}</div>{right}</div></div>""")
        H += h + (36 if oc else 0) + 14
    H += 70
    body = f"""<div style='padding:44px 50px 0'><div style='display:flex;align-items:baseline;gap:28px;margin-bottom:34px'>
<div class=d style='font-size:96px'>SKILLS</div><div class=m style='font-size:28px;color:{MUTED}'>/plugin marketplace add giofornari/skills</div></div>{''.join(rows)}
<div style='text-align:right;color:{MUTED};font-size:22px;padding-top:6px'>{t['entries'].format(n=len(plugins), p=len(packs))}</div></div>"""
    shot(body, W, H, t["out"] / "map.png" if lang == "en" else t["out"].parent / "map.it.png")

if __name__ == "__main__":
    what = set(sys.argv[1:]) or {"banner", "cat", "map"}
    plugins, by, packs = load()
    for lang in L:
        if "banner" in what: banner(lang, plugins, packs)
        if "cat" in what: cat(lang, plugins, by, packs)
        if "map" in what: mapimg(lang, plugins, by, packs)
