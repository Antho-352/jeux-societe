#!/usr/bin/env python3
"""Convert data/sources-batch-*.json into src/content/games/<slug>.md (+ creators).
Mirror mode only when rehosting_allowed starts with "yes": the first PDF is copied to public/pdf/<slug>/.
Run with python3 -I from the repo root. Re-running overwrites generated files but keeps hand-edited bodies
when a file contains the marker `<!-- hand-edited -->`.
"""
import json, os, re, shutil, pathlib, datetime, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'src/content/games'; OUT.mkdir(parents=True, exist_ok=True)
CRE = ROOT / 'src/content/creators'; CRE.mkdir(parents=True, exist_ok=True)
PDF = ROOT / 'public/pdf'; PDF.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return re.sub(r'-+', '-', s)[:60].strip('-')

TYPE = {'board': 'board', 'card': 'card', 'dice': 'dice', 'roll-and-write': 'roll-and-write', 'escape': 'escape', 'party': 'party',
        'scavenger-hunt': 'scavenger-hunt', 'puzzle': None, 'template': None, 'other': None, 'rpg': None}
CREATORS = {
  'Jellybean Games': ('jellybean-games', 'https://jellybean.games', 'Jellybean Games is a small Australian studio that publishes quick, colourful card and party games and shares print-and-play versions of most of them for free.', 'https://jellybean.games', 'Buy the boxed games'),
  'Unfair (2am Gameworks)': ('2am-gameworks', 'https://www.unfair-game.com', '2am Gameworks is the studio behind Unfair, a theme-park building card game, which offers the whole game as a free print and play for personal use.', 'https://www.unfair-game.com', 'Buy the boxed game'),
  'secrethitler.com': ('goat-wolf-cabbage', 'https://www.secrethitler.com', 'Goat, Wolf, & Cabbage designed Secret Hitler and released the full game under a Creative Commons licence.', 'https://www.secrethitler.com', 'Buy the boxed game'),
  'PnP Paradise (Tuesday Knight Games)': ('tuesday-knight-games', 'https://www.tuesdayknightgames.com', 'Tuesday Knight Games publishes Two Rooms and a Boom and keeps its print-and-play edition free forever.', 'https://www.tuesdayknightgames.com', 'Buy the boxed game'),
  'Outlandish Games': ('outlandish-games', 'https://outlandishgames.com', 'Outlandish Games is the collective behind Bloc by Bloc, a cooperative game of urban uprising released under a Creative Commons licence.', 'https://outlandishgames.com', 'Buy the boxed game'),
  'PrintablePaper.net': ('printablepaper', 'https://www.printablepaper.net', 'PrintablePaper.net, by Savetz Publishing, offers hundreds of free printable templates, including game boards, dice nets, logic grids and sudoku.', None, None),
}

def yaml_str(s):
    return json.dumps(str(s), ensure_ascii=False)

def write_creator(site):
    for k in CREATORS:
        if site and (site.lower().startswith(k.lower()[:8]) or k.lower().split(' (')[0] in site.lower()): site = k; break
    if site not in CREATORS: return None
    cid, url, bio, sup, label = CREATORS[site]
    p = CRE / f'{cid}.json'
    if not p.exists():
        data = {'name': site.split(' (')[0] if '(' not in site or site.startswith('Unfair') else site, 'url': url, 'bio': bio}
        if site.startswith('Unfair'): data['name'] = '2am Gameworks'
        if site == 'secrethitler.com': data['name'] = 'Goat, Wolf, & Cabbage'
        if site.startswith('PnP Paradise'): data['name'] = 'Tuesday Knight Games'
        if sup: data['support_url'] = sup; data['support_label'] = label
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return cid

def pick_pdf(paths):
    pdfs = [p for p in paths if p.lower().endswith('.pdf') and os.path.exists(p)]
    # prefer the full print pack over the rules booklet, then the biggest file
    pdfs.sort(key=lambda p: (not re.search(r'print|pnp|card|full|kit|component', p, re.I), -os.path.getsize(p)))
    return pdfs

count = 0
for batch in sorted(ROOT.glob('data/sources-batch-*.json')):
    for r in json.load(open(batch)):
        t = TYPE.get(r.get('game_type'))
        if not t or not r.get('players_min'): continue
        sid = slug(r['title'])
        if not sid: continue
        out = OUT / f'{sid}.md'
        if out.exists() and '<!-- hand-edited -->' in out.read_text(): continue
        allowed = str(r.get('rehosting_allowed') or '').lower().startswith('yes')
        local = r.get('local_paths') or r.get('local_path(s)') or []
        pdfs = pick_pdf(local) if allowed else []
        download_url = None; size = None
        if pdfs:
            dest = PDF / sid; dest.mkdir(exist_ok=True)
            src = pathlib.Path(pdfs[0]); dst = dest / (slug(src.stem) + '.pdf')
            if not dst.exists(): shutil.copy2(src, dst)
            download_url = f'/pdf/{sid}/{dst.name}'; size = round(os.path.getsize(dst) / 1048576, 1)
        cid = write_creator(r.get('source_site') or '')
        fm = {
            'title': r['title'].split(' (')[0].strip(), 'type': t, 'summary': (r.get('description_short') or '')[:218].rsplit('.', 1)[0] + '.',
            'players_min': r['players_min'], 'players_max': r.get('players_max') or r['players_min'],
        }
        if r.get('age_min'): fm['age_min'] = r['age_min']
        if r.get('play_time_min'): fm['time_min'] = r['play_time_min']
        if r.get('play_time_max'): fm['time_max'] = r['play_time_max']
        fm['themes'] = [slug(x) for x in (r.get('themes') or []) if slug(x)][:6]
        fm['mechanics'] = [slug(x) for x in (r.get('mechanics') or []) if slug(x)][:6]
        fm['languages'] = [l.lower()[:2] for l in (r.get('languages') or ['en'])]
        fm['components_included'] = (r.get('components_included') or [])[:8] if isinstance(r.get('components_included'), list) else ([r['components_included']] if r.get('components_included') else [])
        fm['components_needed'] = (r.get('components_needed') or [])[:8] if isinstance(r.get('components_needed'), list) else ([r['components_needed']] if r.get('components_needed') else [])
        if r.get('pages'): fm['pages'] = r['pages']
        ps = (r.get('paper_size') or '').lower()
        if 'a4' in ps and 'letter' in ps: fm['paper'] = 'both'
        elif 'a4' in ps: fm['paper'] = 'a4'
        elif 'letter' in ps: fm['paper'] = 'letter'
        if r.get('colour') in ('colour', 'bw', 'both'): fm['colour'] = r['colour']
        if cid: fm['creator'] = cid
        fm['designers'] = [d for d in (r.get('designers') or []) if d] if isinstance(r.get('designers'), list) else ([r['designers']] if r.get('designers') else [])
        fm['artists'] = [a for a in (r.get('artists') or []) if a] if isinstance(r.get('artists'), list) else []
        if r.get('publisher'): fm['publisher'] = r['publisher']
        if r.get('year') and str(r['year']).isdigit(): fm['year'] = int(r['year'])
        fm['licence'] = (r.get('licence') or 'Free for personal use, all rights reserved')[:120]
        if r.get('licence_url') and str(r['licence_url']).startswith('http'): fm['licence_url'] = r['licence_url']
        fm['hosting_mode'] = 'mirror' if download_url else 'link'
        fm['source_url'] = r['source_url']
        if download_url: fm['download_url'] = download_url; fm['download_size_mb'] = size
        fm['status'] = 'draft'  # pages go live after a human-written body is added
        fm['date_added'] = TODAY
        lines = ['---']
        for k, v in fm.items():
            if isinstance(v, list): lines.append(f'{k}: [' + ', '.join(yaml_str(x) for x in v) + ']')
            elif isinstance(v, (int, float)): lines.append(f'{k}: {v}')
            else: lines.append(f'{k}: {yaml_str(v)}')
        lines.append('---'); lines.append('')
        lines.append(f"## About {fm['title']}"); lines.append(''); lines.append(r.get('description_short') or ''); lines.append('')
        if r.get('notes'): lines.append(f"<!-- notes from the catalogue: {str(r['notes'])[:400].replace('-->', '')} -->")
        out.write_text('\n'.join(lines) + '\n'); count += 1
print('games written:', count)
