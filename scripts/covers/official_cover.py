#!/usr/bin/env python3
"""Install an official game image as a cover: python3 -I scripts/covers/official_cover.py [--rules] <slug> <image file> "<credit>" <source page url>
With --rules the cover goes to a rules page (box of a branded game) instead of a game page.

The image is fitted into a 600×600 JPEG: centre-cropped when it is nearly square, otherwise shown whole on a
blurred copy of itself so nothing important is cut. The game's frontmatter gets cover, cover_credit and
cover_source, and loses cover_art (our drawings are only for games with no official image)."""
import sys, pathlib, re
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if a != '--rules']
KIND = 'rules' if '--rules' in sys.argv else 'games'
slug, src, credit, page = args[:4]
im = Image.open(src).convert('RGB')
w, h = im.size
S = 600
if max(w, h) / min(w, h) <= 1.35:
    s = min(w, h); im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((S, S), Image.LANCZOS)
else:
    bg = im.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(24))
    fg = im.copy(); fg.thumbnail((S - 40, S - 40), Image.LANCZOS)
    bg.paste(fg, ((S - fg.width) // 2, (S - fg.height) // 2)); im = bg
out = ROOT / f'public/img/{KIND}' / f'{slug}.jpg'
im.save(out, quality=86, optimize=True, progressive=True)
md = ROOT / f'src/content/{KIND}' / f'{slug}.md'
t = md.read_text()
t = re.sub(r'^cover_art: true\n', '', t, flags=re.M)
t = re.sub(r'^cover_credit: .*\n', '', t, flags=re.M)
t = re.sub(r'^cover_source: .*\n', '', t, flags=re.M)
line = f'cover: "/img/{KIND}/{slug}.jpg"\ncover_credit: "{credit}"\ncover_source: "{page}"\n'
t = re.sub(r'^cover: .*\n', line, t, count=1, flags=re.M) if re.search(r'^cover: ', t, re.M) else t.replace('---\n', '---\n' + line, 1)
md.write_text(t)
old = ROOT / f'public/img/{KIND}' / f'{slug}.png'
if old.exists(): old.unlink()
print('cover', slug, im.size)
