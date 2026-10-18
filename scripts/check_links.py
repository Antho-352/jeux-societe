#!/usr/bin/env python3
"""Check every internal link and asset in dist/ resolves. Exit 1 on broken links.
Usage: npm run build && python3 -I scripts/check_links.py"""
import pathlib, re, sys, collections
DIST = pathlib.Path(__file__).resolve().parent.parent / 'dist'
broken = collections.defaultdict(set)
for html in DIST.rglob('*.html'):
    page = '/' + str(html.relative_to(DIST)).replace('index.html', '')
    for url in re.findall(r'(?:href|src)="(/[^"#?]*)', html.read_text(errors='ignore')):
        if url.startswith('//'): continue
        target = DIST / url.lstrip('/')
        if url.endswith('/'): target = target / 'index.html'
        if not target.exists(): broken[url].add(page)
for url, pages in sorted(broken.items()):
    print(f'BROKEN {url}  ← {len(pages)} page(s), e.g. {sorted(pages)[0]}')
print(f'{len(broken)} broken internal link target(s)')
sys.exit(1 if broken else 0)
