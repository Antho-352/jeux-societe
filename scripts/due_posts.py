#!/usr/bin/env python3
"""Exit 0 and print the slugs of blog posts that are due but not online yet. Exit 1 when nothing is due.
A post is due when its publish_at passed within the last WINDOW minutes (default 14 days); with --live SITE,
only due posts whose page on SITE does not answer 200 are kept, so a run that comes late (GitHub delays
scheduled runs by hours) still publishes everything it missed, and a run with nothing new does nothing.
Used by .github/workflows/scheduled-publish.yml. Usage: python3 -I scripts/due_posts.py [window_minutes] [--live https://site]"""
import datetime as dt, pathlib, re, sys, urllib.error, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:]]
live = None
if '--live' in args:
    i = args.index('--live'); live = args[i + 1].rstrip('/'); del args[i:i + 2]
window = int(args[0]) if args else 14 * 24 * 60
now = dt.datetime.now(dt.timezone.utc)

def online(slug):
    req = urllib.request.Request(f'{live}/blog/{slug}/', method='HEAD', headers={'User-Agent': 'scheduled-publish-check'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        return e.code != 404  # only a real 404 means "not published"; a 403 from bot protection must not rebuild every hour
    except Exception:
        return True  # network trouble: don't rebuild blindly, the next run checks again

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
    if now - dt.timedelta(minutes=window) < t <= now and not (live and online(f.stem)):
        due.append((t.isoformat(), f.stem))
for t, slug in due:
    print(f'{t} {slug}')
sys.exit(0 if due else 1)
