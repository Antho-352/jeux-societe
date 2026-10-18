#!/usr/bin/env python3
"""Récupère les volumes de recherche Google Ads via DataForSEO pour les mots-clés
listés dans docs/01-mots-cles.md et écrit docs/01-mots-cles-volumes.md + data/keywords.json.

Identifiants lus dans les variables d'environnement DFS_LOGIN et DFS_PASS
(jamais stockés dans le dépôt).

Usage : DFS_LOGIN=... DFS_PASS=... python3 -I scripts/dataforseo_volumes.py
"""
import base64, json, os, re, sys, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "01-mots-cles.md"
OUT_MD = ROOT / "docs" / "01-mots-cles-volumes.md"
OUT_JSON = ROOT / "data" / "keywords.json"

login, pwd = os.environ.get("DFS_LOGIN"), os.environ.get("DFS_PASS")
if not login or not pwd:
    sys.exit("DFS_LOGIN / DFS_PASS manquants")
auth = base64.b64encode(f"{login}:{pwd}".encode()).decode()

# Parse les deux tableaux du fichier markdown
text = SRC.read_text(encoding="utf-8")
sections = {"en": [], "fr": []}
current = None
for line in text.splitlines():
    if line.startswith("## Anglais"):
        current = "en"
    elif line.startswith("## Français"):
        current = "fr"
    elif line.startswith("## "):
        current = None
    m = re.match(r"^\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
    if current and m:
        sections[current].append({"keyword": m.group(1), "intent": m.group(2), "target": m.group(3)})

# Marchés : anglais sur US + UK, français sur France
MARKETS = {
    "en": [("US", 2840, "en"), ("UK", 2826, "en")],
    "fr": [("FR", 2250, "fr")],
}

def call(keywords, location_code, language_code):
    body = json.dumps([{
        "keywords": keywords,
        "location_code": location_code,
        "language_code": language_code,
        "search_partners": False,
    }]).encode()
    req = urllib.request.Request(
        "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live",
        data=body, method="POST",
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    task = data["tasks"][0]
    if task.get("status_code") != 20000:
        sys.exit(f"Erreur DataForSEO {task.get('status_code')}: {task.get('status_message')}")
    return {it["keyword"]: it for it in (task.get("result") or [])}

results = {}
for lang, rows in sections.items():
    kws = [r["keyword"] for r in rows]
    for market, loc, lc in MARKETS[lang]:
        res = call(kws, loc, lc)
        for r in rows:
            it = res.get(r["keyword"], {})
            r.setdefault("volumes", {})[market] = {
                "search_volume": it.get("search_volume"),
                "competition": it.get("competition"),
                "cpc": it.get("cpc"),
            }
    results[lang] = rows

OUT_JSON.parent.mkdir(exist_ok=True)
OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

def fmt(v):
    return "–" if v is None else f"{v:,}".replace(",", " ")

lines = ["# Volumes de recherche (DataForSEO, Google Ads, moyenne mensuelle)", ""]
for lang, title, cols in (("en", "Anglais", ["US", "UK"]), ("fr", "Français", ["FR"])):
    rows = sorted(results[lang], key=lambda r: -(r["volumes"][cols[0]]["search_volume"] or 0))
    lines += [f"## {title}", "", "| Mot-clé | " + " | ".join(f"Volume {c}" for c in cols) + " | Concurrence | Intention | Page cible |",
              "|---|" + "---|" * (len(cols) + 3)]
    for r in rows:
        vols = " | ".join(fmt(r["volumes"][c]["search_volume"]) for c in cols)
        comp = r["volumes"][cols[0]]["competition"] or "–"
        lines.append(f"| {r['keyword']} | {vols} | {comp} | {r['intent']} | {r['target']} |")
    lines.append("")
OUT_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"OK : {sum(len(v) for v in results.values())} mots-clés → {OUT_MD.relative_to(ROOT)}")
