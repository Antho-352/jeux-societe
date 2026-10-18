#!/usr/bin/env python3
"""Petit client DataForSEO en ligne de commande.

Identifiants : variables d'environnement DFS_LOGIN et DFS_PASS.

Usage :
  python3 -I scripts/dfs.py volume [--loc 2840] [--lang en] [--out f.json] "kw 1" "kw 2" ...
      → volumes Google Ads (max 1000 mots-clés par appel, l'outil découpe tout seul)
  python3 -I scripts/dfs.py ideas  [--loc 2840] [--lang en] [--out f.json] "seed 1" "seed 2" ...
      → idées de mots-clés Google Ads (max 20 seeds par appel)
  python3 -I scripts/dfs.py serp   [--loc 2840] [--lang en] [--out f.json] "requête"
      → top 10 Google organique (DataForSEO SERP live advanced)
  python3 -I scripts/dfs.py domain [--loc 2840] [--lang en] [--out f.json] example.com
      → mots-clés classés d'un domaine (DataForSEO Labs ranked_keywords, 300 max)

Codes pays : US 2840, UK 2826, FR 2250, CA 2124. Sortie : tableau TSV trié par volume
sur stdout, JSON brut complet dans --out.
"""
import argparse, base64, json, os, sys, urllib.request

login, pwd = os.environ.get("DFS_LOGIN"), os.environ.get("DFS_PASS")
if not login or not pwd:
    sys.exit("DFS_LOGIN / DFS_PASS manquants")
AUTH = base64.b64encode(f"{login}:{pwd}".encode()).decode()

def post(path, payload):
    req = urllib.request.Request("https://api.dataforseo.com/v3/" + path, data=json.dumps(payload).encode(),
                                 method="POST", headers={"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    for t in data.get("tasks", []):
        if t.get("status_code") != 20000:
            sys.exit(f"Erreur DataForSEO {t.get('status_code')}: {t.get('status_message')}")
    return data

def chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]

ap = argparse.ArgumentParser()
ap.add_argument("mode", choices=["volume", "ideas", "serp", "domain"])
ap.add_argument("--loc", type=int, default=2840)
ap.add_argument("--lang", default="en")
ap.add_argument("--out")
ap.add_argument("--limit", type=int, default=300)
ap.add_argument("args", nargs="+")
a = ap.parse_args()

results, raw = [], []
if a.mode == "volume":
    for c in chunks(a.args, 1000):
        d = post("keywords_data/google_ads/search_volume/live",
                 [{"keywords": c, "location_code": a.loc, "language_code": a.lang, "search_partners": False}])
        raw.append(d); results += d["tasks"][0].get("result") or []
elif a.mode == "ideas":
    for c in chunks(a.args, 20):
        d = post("keywords_data/google_ads/keywords_for_keywords/live",
                 [{"keywords": c, "location_code": a.loc, "language_code": a.lang, "search_partners": False, "sort_by": "search_volume"}])
        raw.append(d); results += d["tasks"][0].get("result") or []
elif a.mode == "serp":
    d = post("serp/google/organic/live/advanced",
             [{"keyword": a.args[0], "location_code": a.loc, "language_code": a.lang, "depth": 10}])
    raw.append(d)
    for it in (d["tasks"][0]["result"][0].get("items") or []):
        if it.get("type") == "organic":
            print(f"{it.get('rank_absolute')}\t{it.get('domain')}\t{it.get('url')}\t{it.get('title')}")
elif a.mode == "domain":
    d = post("dataforseo_labs/google/ranked_keywords/live",
             [{"target": a.args[0], "location_code": a.loc, "language_code": a.lang, "limit": a.limit,
               "order_by": ["keyword_data.keyword_info.search_volume,desc"]}])
    raw.append(d)
    for it in (d["tasks"][0]["result"][0].get("items") or []):
        kd, se = it["keyword_data"], it["ranked_serp_element"]["serp_item"]
        print(f"{kd['keyword_info'].get('search_volume')}\t{se.get('rank_absolute')}\t{kd['keyword']}\t{se.get('url')}")

if a.mode in ("volume", "ideas"):
    seen = set()
    rows = []
    for r in results:
        k = r.get("keyword")
        if k in seen: continue
        seen.add(k); rows.append(r)
    rows.sort(key=lambda r: -(r.get("search_volume") or 0))
    for r in rows:
        print(f"{r.get('search_volume') if r.get('search_volume') is not None else '-'}\t{r.get('competition') or '-'}\t{r.get('cpc') if r.get('cpc') is not None else '-'}\t{r['keyword']}")
if a.out:
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)
