#!/usr/bin/env python3
"""Exit 0 and print the slugs of blog posts that became due in the last WINDOW minutes (default 65).
Exit 1 when nothing is due. Used by .github/workflows/scheduled-publish.yml to decide whether to
trigger a Cloudflare Pages rebuild. Usage: python3 -I scripts/due_posts.py [window_minutes]"""
import datetime as dt, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
window = int(sys.argv[1]) if len(sys.argv) > 1 else 65
now = dt.datetime.now(dt.timezone.utc)
due = []
for f in sorted((ROOT / 'src/content/blog').glob('*.md*')):
    head = f.read_text(encoding='utf-8').split('---', 2)[1]
    m = re.search(r'^publish_at:\s*"?([^"\n]+)"?', head, re.M)
    st = re.search(r'^status:\s*"?(\w+)', head, re.M)
    if not m or (st and st.group(1) != 'published'):
        continue
    t = dt.datetime.fromisoformat(m.group(1).strip().replace('Z', '+00:00'))
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    if now - dt.timedelta(minutes=window) < t <= now:
        due.append((t.isoformat(), f.stem))
for t, slug in due:
    print(f'{t} {slug}')
sys.exit(0 if due else 1)
