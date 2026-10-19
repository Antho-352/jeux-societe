#!/usr/bin/env python3
"""Build the editorial calendar from data/blog-topics-*.json.

Rhythm: 1.5 articles per week on average, i.e. alternating weeks of 1 and 2 posts, never on the
same weekday or hour twice in a row. Seasonal topics are placed before their deadline; the rest is
ordered by priority (quick wins first), then by keyword difficulty, then volume, while alternating
silos so one silo never gets two posts in a row.

Writes data/blog-calendar.json and docs/14-calendrier-editorial.md.
Usage: python3 -I scripts/blog_calendar.py [start YYYY-MM-DD] [weeks]
"""
import datetime as dt, json, pathlib, random, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
start = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 10, 26)
weeks = int(sys.argv[2]) if len(sys.argv) > 2 else 26
rng = random.Random(352)  # deterministic

topics = []
for f in sorted((ROOT / 'data').glob('blog-topics-*.json')):
    for t in json.loads(f.read_text()):
        t['_src'] = f.stem
        topics.append(t)
seen, uniq = set(), []
for t in topics:
    k = t['target_keyword'].lower().strip()
    if k in seen: continue
    seen.add(k); uniq.append(t)
topics = uniq

# Slots: Monday-based weeks, 1 or 2 posts alternating, weekdays Mon-Sat, hours 12-21 UTC (morning to afternoon in the US)
slots, last_day, last_hour = [], None, None
for w in range(weeks):
    monday = start + dt.timedelta(weeks=w)
    n = 2 if w % 2 == 0 else 1
    days = sorted(rng.sample(range(0, 6), n))
    if n == 2 and days[1] - days[0] < 2: days = [days[0], min(5, days[0] + rng.choice([2, 3]))]
    for d in days:
        if last_day is not None and d == last_day and n == 1: d = (d + rng.choice([1, 2])) % 6
        h = rng.choice([12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
        while h == last_hour: h = rng.choice([12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
        m = rng.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        slots.append(dt.datetime.combine(monday + dt.timedelta(days=d), dt.time(h, m), tzinfo=dt.timezone.utc))
        last_day, last_hour = d, h
slots.sort()

# Hard deadlines only for real dated events (holidays); "peak season" hints from the games list are soft.
HARD = {'family-game-night-ideas'}
def deadline(t):
    if t.get('_src') == 'blog-topics-b' and t['slug'] not in HARD: return None
    s = t.get('season_deadline')
    return dt.datetime.fromisoformat(s + 'T23:59:00+00:00') if s else None

seasonal = sorted([t for t in topics if deadline(t)], key=deadline)
evergreen = sorted([t for t in topics if not deadline(t)], key=lambda t: (t.get('priority', 2), t.get('kd') if t.get('kd') is not None else 50, -(t.get('volume_us') or 0)))

plan, used = [], set()
# 1. seasonal: latest free slot before the deadline but not earlier than 8 weeks before it
for t in seasonal:
    dl = deadline(t)
    cands = [i for i, s in enumerate(slots) if i not in used and s <= dl and s >= dl - dt.timedelta(weeks=8)]
    if not cands: cands = [i for i, s in enumerate(slots) if i not in used and s <= dl]
    if not cands:  # deadline already passed: publish as early as possible
        cands = [i for i in range(len(slots)) if i not in used][:1]
        if not cands: t['_unplaced'] = 'no slot left'; continue
        used.add(cands[0]); plan.append((slots[cands[0]], t)); continue
    i = cands[-1] if len(cands) < 3 else cands[len(cands) // 2]
    used.add(i); plan.append((slots[i], t))
# 2. evergreen in remaining slots, avoiding the same silo twice in a row.
#    Growth targets (priority 3) take the last free slots: easy wins first, harder keywords later.
free = [i for i in range(len(slots)) if i not in used]
growth = [t for t in evergreen if t.get('priority') == 3][: max(0, len(free) // 6)]
others = [t for t in evergreen if t not in growth]
n_others = len(free) - len(growth)
def fill(slot_ids, queue):
    for i in slot_ids:
        if not queue: break
        prev = [t for s, t in sorted(plan, key=lambda x: x[0]) if s < slots[i]]
        last_silo = prev[-1]['silo'] if prev else None
        pick = next((t for t in queue if t['silo'] != last_silo), queue[0])
        queue.remove(pick); plan.append((slots[i], pick))
fill(free[:n_others], others[:])
fill(free[n_others:], growth[:])
plan.sort(key=lambda x: x[0])

out = [{'publish_at': s.strftime('%Y-%m-%dT%H:%M:00Z'), **{k: v for k, v in t.items() if not k.startswith('_')}} for s, t in plan]
(ROOT / 'data/blog-calendar.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))

DAYS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
MONTHS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
lines = ['# Calendrier éditorial du blog', '',
         f'{len(out)} articles du {start:%d/%m/%Y} au {plan[-1][0]:%d/%m/%Y} ({weeks} semaines, 1,5 article par semaine en moyenne).',
         'Jours et heures variés ; heures en UTC (13 h UTC = 9 h à New York, 14 h à Paris). Les articles saisonniers sont placés avant leur date limite.',
         'Généré par `scripts/blog_calendar.py` à partir de `data/blog-topics-*.json`.', '',
         '| # | Date (UTC) | Article | Mot-clé cible | Vol. US | KD | Page mère | Priorité |', '|---|---|---|---|---|---|---|---|']
for n, (s, t) in enumerate(plan, 1):
    lines.append(f"| {n} | {DAYS[s.weekday()]} {s.day} {MONTHS[s.month-1]} {s.year} · {s:%H:%M} | {t['title']} | {t['target_keyword']} | {t.get('volume_us') or '–'} | {t.get('kd') if t.get('kd') is not None else '–'} | `/{t['silo']}/` | {t.get('priority', '–')} |")
left = [t for t in topics if t not in [p[1] for p in plan]]
if left:
    lines += ['', '## Sujets en réserve (non planifiés)', '']
    lines += [f"- {t['title']} ({t['target_keyword']}, {t.get('volume_us') or '–'}/mois, KD {t.get('kd')}){' — ' + t['_unplaced'] if t.get('_unplaced') else ''}" for t in left]
(ROOT / 'docs/14-calendrier-editorial.md').write_text('\n'.join(lines) + '\n')
print(f'{len(out)} articles planned, {len(left)} in reserve')
