#!/usr/bin/env python3
"""Dot-to-dot (connect the dots) generator for printandplaygame.com.

Shapes are closed outlines (normalised 0..1). The outline is resampled into N evenly spaced dots,
numbered 1..N (or A..Z), drawn on a US Letter page with margins that also fit A4. Page 2 shows the
finished picture. Usage (from the repo root):
  python3 -I scripts/puzzles/dot_to_dot.py build   # writes PDFs, covers and content entries
"""
import math, json, pathlib, sys, datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / 'public/pdf/puzzles/dot-to-dot'
IMG_DIR = ROOT / 'public/img/puzzles'
CONTENT = ROOT / 'src/content/puzzles'
W, H = letter
MARGIN = 16 * mm
INK = (0.06, 0.24, 0.18)
RED = (1.0, 0.42, 0.34)

# ---------- shape outlines (lists of (x, y) in 0..1, y up) ----------
def polar(fn, n=400):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = fn(t)
        pts.append((0.5 + r * math.cos(t), 0.5 + r * math.sin(t)))
    return pts

def star(points=5, inner=0.42):
    pts = []
    for i in range(points * 2):
        a = math.pi / 2 + i * math.pi / points
        r = 0.48 if i % 2 == 0 else 0.48 * inner
        pts.append((0.5 + r * math.cos(a), 0.5 + r * math.sin(a)))
    return pts

def heart():
    pts = []
    for i in range(400):
        t = 2 * math.pi * i / 400
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((0.5 + x / 36, 0.5 + y / 36))
    return pts

def regular(n, r=0.46, rot=0.0):
    return [(0.5 + r * math.cos(rot + 2 * math.pi * i / n), 0.5 + r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]

def flower(petals=6):
    return polar(lambda t: 0.30 + 0.16 * abs(math.cos(petals * t / 2)))

def egg():
    return polar(lambda t: 0.40 / math.sqrt((math.cos(t) / 1.0) ** 2 + (math.sin(t) / 1.35) ** 2) * (1 + 0.12 * math.sin(t)))

def pumpkin():
    body = polar(lambda t: 0.40 / math.sqrt(math.cos(t) ** 2 + (math.sin(t) / 0.78) ** 2) * (1 + 0.03 * math.cos(6 * t)))
    # stem: splice a small bump at the top
    out = []
    for (x, y) in body:
        out.append((x, y))
    top_i = max(range(len(out)), key=lambda i: out[i][1])
    stem = [(0.47, out[top_i][1] + 0.02), (0.46, out[top_i][1] + 0.10), (0.54, out[top_i][1] + 0.11), (0.53, out[top_i][1] + 0.02)]
    return out[:top_i] + stem + out[top_i + 1:]

def crescent():
    pts = []
    for i in range(200):
        t = math.pi / 2 + math.pi * i / 199
        pts.append((0.5 + 0.44 * math.cos(t), 0.5 + 0.44 * math.sin(t)))
    for i in range(200):
        t = 3 * math.pi / 2 - math.pi * i / 199
        pts.append((0.62 + 0.36 * math.cos(t), 0.5 + 0.36 * math.sin(t)))
    return pts

HOUSE = [(0.15, 0.10), (0.15, 0.55), (0.50, 0.90), (0.85, 0.55), (0.85, 0.10), (0.60, 0.10), (0.60, 0.38), (0.40, 0.38), (0.40, 0.10)]
ROCKET = [(0.50, 0.95), (0.62, 0.78), (0.66, 0.45), (0.80, 0.28), (0.80, 0.14), (0.66, 0.22), (0.58, 0.10), (0.50, 0.18), (0.42, 0.10), (0.34, 0.22), (0.20, 0.14), (0.20, 0.28), (0.34, 0.45), (0.38, 0.78)]
FISH = [(0.10, 0.50), (0.22, 0.66), (0.40, 0.76), (0.60, 0.74), (0.74, 0.62), (0.90, 0.78), (0.86, 0.50), (0.90, 0.22), (0.74, 0.38), (0.60, 0.26), (0.40, 0.24), (0.22, 0.34)]
SAILBOAT = [(0.10, 0.32), (0.44, 0.32), (0.44, 0.92), (0.50, 0.92), (0.88, 0.38), (0.88, 0.32), (0.92, 0.32), (0.80, 0.14), (0.20, 0.14)]
TREE = [(0.50, 0.95), (0.66, 0.74), (0.58, 0.74), (0.74, 0.54), (0.64, 0.54), (0.82, 0.32), (0.56, 0.32), (0.56, 0.10), (0.44, 0.10), (0.44, 0.32), (0.18, 0.32), (0.36, 0.54), (0.26, 0.54), (0.42, 0.74), (0.34, 0.74)]
ARROW = [(0.10, 0.42), (0.60, 0.42), (0.60, 0.26), (0.92, 0.50), (0.60, 0.74), (0.60, 0.58), (0.10, 0.58)]
BOLT = [(0.58, 0.95), (0.28, 0.50), (0.48, 0.50), (0.36, 0.05), (0.72, 0.56), (0.52, 0.56)]
BUTTERFLY = [(0.50, 0.50), (0.38, 0.72), (0.18, 0.86), (0.08, 0.68), (0.16, 0.50), (0.08, 0.32), (0.18, 0.14), (0.38, 0.28), (0.50, 0.44), (0.62, 0.28), (0.82, 0.14), (0.92, 0.32), (0.84, 0.50), (0.92, 0.68), (0.82, 0.86), (0.62, 0.72)]
CAT = [(0.20, 0.10), (0.20, 0.52), (0.14, 0.86), (0.34, 0.70), (0.66, 0.70), (0.86, 0.86), (0.80, 0.52), (0.80, 0.10), (0.68, 0.10), (0.68, 0.30), (0.32, 0.30), (0.32, 0.10)]
UMBRELLA = [(0.08, 0.52), (0.20, 0.60), (0.32, 0.52), (0.44, 0.60), (0.50, 0.52), (0.56, 0.60), (0.68, 0.52), (0.80, 0.60), (0.92, 0.52), (0.80, 0.78), (0.50, 0.94), (0.20, 0.78), (0.08, 0.52), (0.50, 0.52), (0.50, 0.14), (0.44, 0.08), (0.36, 0.14), (0.44, 0.14), (0.50, 0.10), (0.56, 0.14), (0.56, 0.52)]
SNOWMAN = None  # built from circles below
DINO = [(0.08, 0.40), (0.20, 0.52), (0.32, 0.48), (0.40, 0.60), (0.48, 0.86), (0.66, 0.92), (0.82, 0.84), (0.90, 0.70), (0.76, 0.64), (0.70, 0.52), (0.64, 0.30), (0.70, 0.12), (0.58, 0.12), (0.54, 0.28), (0.44, 0.28), (0.40, 0.12), (0.28, 0.12), (0.30, 0.30), (0.18, 0.28)]

def circles(spec):
    """Union-ish outline for stacked circles (snowman): trace each circle's visible arc."""
    pts = []
    for (cx, cy, r, a0, a1) in spec:
        n = 120
        for i in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts

def snowman_outline():
    """Exact union outline of three stacked circles (base, body, head)."""
    A, B, C = (0.5, 0.22, 0.20), (0.5, 0.52, 0.15), (0.5, 0.76, 0.11)
    def inter(p, q):
        (x1, y1, r1), (x2, y2, r2) = p, q
        d = y2 - y1
        a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(max(r1 ** 2 - a ** 2, 0))
        return a, h
    aAB, hAB = inter(A, B); aBC, hBC = inter(B, C)
    angA = math.degrees(math.atan2(aAB, hAB)); angA2 = 180 - angA              # on A: right, left
    angB_low = math.degrees(math.atan2(aAB - (B[1] - A[1]), hAB))               # on B, lower right (negative)
    angB_hi = math.degrees(math.atan2(aBC, hBC)); angB_hi2 = 180 - angB_hi      # on B, upper right/left
    angC = math.degrees(math.atan2(aBC - (C[1] - B[1]), hBC))                   # on C, lower right (negative)
    spec = [
        (C[0], C[1], C[2], angC, 180 - angC),                 # head: from lower right, over the top, to lower left
        (B[0], B[1], B[2], angB_hi2, 180 - angB_low),         # body left side
        (A[0], A[1], A[2], angA2, 360 + angA),                # base: left, around the bottom, to right
        (B[0], B[1], B[2], 360 + angB_low, 360 + angB_hi),    # body right side
    ]
    return circles(spec)

SNOWMAN_PTS = snowman_outline()

SHAPES = {
    'star': ('Star', star()), 'heart': ('Heart', heart()), 'house': ('House', HOUSE), 'rocket': ('Rocket', ROCKET), 'fish': ('Fish', FISH),
    'sailboat': ('Sailboat', SAILBOAT), 'christmas-tree': ('Christmas tree', TREE), 'arrow': ('Arrow', ARROW), 'lightning': ('Lightning bolt', BOLT),
    'butterfly': ('Butterfly', BUTTERFLY), 'cat': ('Cat', CAT), 'umbrella': ('Umbrella', UMBRELLA), 'dinosaur': ('Dinosaur', DINO), 'snowman': ('Snowman', SNOWMAN_PTS),
    'flower': ('Flower', flower()), 'easter-egg': ('Easter egg', egg()), 'pumpkin': ('Pumpkin', pumpkin()), 'moon': ('Crescent moon', crescent()),
    'hexagon': ('Hexagon', regular(6)), 'diamond': ('Diamond', regular(4, rot=math.pi / 2)),
}

# ---------- geometry ----------
def resample(pts, n, closed=True):
    path = pts + ([pts[0]] if closed else [])
    seg = [math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)]
    total = sum(seg)
    out, acc, j = [], 0.0, 0
    targets = [total * k / n for k in range(n)]
    for tg in targets:
        while j < len(seg) - 1 and acc + seg[j] < tg:
            acc += seg[j]; j += 1
        f = (tg - acc) / seg[j] if seg[j] else 0
        (x0, y0), (x1, y1) = path[j], path[j + 1]
        out.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f))
    return out

def keep_corners(pts, n):
    """For polygon shapes with few vertices, keep every vertex and spread the rest evenly."""
    if len(pts) >= n: return resample(pts, n)
    extra = n - len(pts)
    path = pts + [pts[0]]
    seg = [math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)]
    total = sum(seg)
    out = []
    alloc = [int(round(extra * s / total)) for s in seg]
    while sum(alloc) > extra:
        alloc[alloc.index(max(alloc))] -= 1
    while sum(alloc) < extra:
        alloc[alloc.index(min(alloc))] += 1
    for i, (a, b) in enumerate(zip(path[:-1], path[1:])):
        out.append(a)
        for k in range(1, alloc[i] + 1):
            f = k / (alloc[i] + 1)
            out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out

def labels(n, letters=False):
    if letters:
        return [chr(65 + i) for i in range(n)]
    return [str(i + 1) for i in range(n)]

# ---------- drawing ----------
def page_frame(c, title, subtitle):
    c.setFillColorRGB(*INK)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(MARGIN, H - MARGIN - 6, title)
    c.setFont('Helvetica', 10.5)
    c.drawString(MARGIN, H - MARGIN - 22, subtitle)
    c.setFont('Helvetica', 8.5)
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawRightString(W - MARGIN, MARGIN - 4, 'printandplaygame.com  ·  CC BY-NC 4.0  ·  free for home and classroom use')

def draw_dots(c, dots, labs, box, reveal=False):
    x0, y0, bw, bh = box
    def P(p): return (x0 + p[0] * bw, y0 + p[1] * bh)
    n = len(dots)
    if reveal:
        c.setStrokeColorRGB(*RED); c.setLineWidth(2.2)
        path = c.beginPath()
        path.moveTo(*P(dots[0]))
        for d in dots[1:]: path.lineTo(*P(d))
        path.close(); c.drawPath(path, stroke=1, fill=0)
    c.setFillColorRGB(*INK); c.setStrokeColorRGB(*INK)
    cx = sum(d[0] for d in dots) / n; cy = sum(d[1] for d in dots) / n
    for i, d in enumerate(dots):
        px, py = P(d)
        r = 3.4 if n <= 30 else 2.6 if n <= 80 else 2.0
        c.circle(px, py, r, stroke=0, fill=1)
        # label pushed away from the shape centre
        vx, vy = d[0] - cx, d[1] - cy
        L = math.hypot(vx, vy) or 1
        off = 11 if n <= 30 else 9 if n <= 80 else 8
        lx, ly = px + vx / L * off, py + vy / L * off
        c.setFont('Helvetica-Bold' if i == 0 else 'Helvetica', 11 if n <= 30 else 8.5 if n <= 80 else 7)
        c.drawCentredString(lx, ly - 3, labs[i])
    # start marker
    sx, sy = P(dots[0])
    c.setStrokeColorRGB(*RED); c.setLineWidth(1.5); c.circle(sx, sy, 7, stroke=1, fill=0)

def build_pdf(slug, shape_key, n, letters, title, out_pdf):
    name, pts = SHAPES[shape_key]
    dots = keep_corners(pts, n) if len(pts) <= 24 else resample(pts, n)
    labs = labels(n, letters)
    c = canvas.Canvas(str(out_pdf), pagesize=letter)
    c.setTitle(title); c.setAuthor('Print & Play Game')
    sub = f'Connect the dots from {labs[0]} to {labs[-1]}, then colour the picture.' if not letters else 'Join the letters in alphabetical order, A to Z, then colour the picture.'
    box = (MARGIN + 10 * mm, MARGIN + 14 * mm, W - 2 * MARGIN - 20 * mm, H - 2 * MARGIN - 36 * mm)
    side = min(box[2], box[3]); box = (MARGIN + (W - 2 * MARGIN - side) / 2, box[1], side, side)
    page_frame(c, title, sub)
    draw_dots(c, dots, labs, box)
    c.showPage()
    page_frame(c, f'{title} – finished picture', 'The picture you get once every dot is joined.')
    draw_dots(c, dots, labs, box, reveal=True)
    c.showPage(); c.save()

def cover(pdf, png):
    import pypdfium2 as pdfium
    from PIL import Image
    doc = pdfium.PdfDocument(str(pdf))
    img = doc[0].render(scale=1.6).to_pil().convert('RGB')
    w, h = img.size; s = min(w, h)
    img = img.crop(((w - s) // 2, int(h * 0.12), (w - s) // 2 + s, int(h * 0.12) + s)).resize((600, 600), Image.LANCZOS)
    img.save(png, optimize=True)

# ---------- catalogue of puzzles to produce ----------
# (slug, shape, dots, letters?, title, difficulty, age_band, themes, occasions, body)
ITEMS = [
    ('star-dot-to-dot-easy', 'star', 10, False, 'Star dot to dot (10 dots)', 'easy', 'preschool', ['shapes', 'space'], [], 'Ten dots and a star: the simplest connect-the-dots for a first pencil. Big numbers, wide spacing, and a picture that is easy to colour afterwards.'),
    ('heart-dot-to-dot-easy', 'heart', 14, False, 'Heart dot to dot (14 dots)', 'easy', 'preschool', ['shapes', 'love'], ['valentines'], 'A heart in fourteen dots for Valentine\'s Day cards or a quiet morning. Counting to 14 and a smooth curve to follow.'),
    ('house-dot-to-dot-easy', 'house', 12, False, 'House dot to dot (12 dots)', 'easy', 'preschool', ['home', 'shapes'], [], 'A little house with a door, twelve dots. Straight lines, so young children can keep the ruler out and just draw.'),
    ('fish-dot-to-dot-easy', 'fish', 16, False, 'Fish dot to dot (16 dots)', 'easy', 'preschool', ['animals', 'ocean'], ['summer'], 'A friendly fish in sixteen dots. Count to 16, join the dots, then add scales and bubbles.'),
    ('rocket-dot-to-dot-easy', 'rocket', 18, False, 'Rocket dot to dot (18 dots)', 'easy', 'preschool', ['space', 'vehicles'], [], 'Blast off: a rocket with fins and a nose cone in eighteen dots, for the space fans in kindergarten.'),
    ('christmas-tree-dot-to-dot', 'christmas-tree', 20, False, 'Christmas tree dot to dot (20 dots)', 'easy', 'kids', ['christmas', 'nature'], ['christmas'], 'A Christmas tree in twenty dots, ready to decorate with baubles once the outline is joined. A quick December activity for 5 to 7 year-olds.'),
    ('abc-star-dot-to-dot', 'star', 26, True, 'Alphabet dot to dot: star (A to Z)', 'easy', 'preschool', ['alphabet', 'shapes'], [], 'Twenty-six dots labelled A to Z instead of numbers. Children practise the alphabet order while drawing a star.'),
    ('abc-butterfly-dot-to-dot', 'butterfly', 26, True, 'Alphabet dot to dot: butterfly (A to Z)', 'easy', 'kids', ['alphabet', 'animals', 'insects'], ['summer'], 'A butterfly whose outline follows the alphabet from A to Z. Good for letter recognition in kindergarten and first grade.'),
    ('pumpkin-dot-to-dot', 'pumpkin', 30, False, 'Pumpkin dot to dot (30 dots)', 'medium', 'kids', ['halloween', 'autumn'], ['halloween'], 'A plump pumpkin with a stem in thirty dots. Join them, then draw the jack-o\'-lantern face of your choice.'),
    ('sailboat-dot-to-dot', 'sailboat', 32, False, 'Sailboat dot to dot (32 dots)', 'medium', 'kids', ['vehicles', 'ocean'], ['summer'], 'A sailboat with two sails and a hull in thirty-two dots. The lines cross back over the mast, so it rewards careful counting.'),
    ('cat-dot-to-dot', 'cat', 36, False, 'Cat dot to dot (36 dots)', 'medium', 'kids', ['animals', 'pets'], [], 'A sitting cat with pointed ears in thirty-six dots. Add whiskers and stripes when the outline is done.'),
    ('dinosaur-dot-to-dot', 'dinosaur', 40, False, 'Dinosaur dot to dot (40 dots)', 'medium', 'kids', ['dinosaurs', 'animals'], [], 'A long-necked dinosaur in forty dots, legs and tail included. A favourite for 6 to 8 year-olds who count well past 20.'),
    ('snowman-dot-to-dot', 'snowman', 45, False, 'Snowman dot to dot (45 dots)', 'medium', 'kids', ['winter', 'christmas'], ['winter', 'christmas'], 'Three snowballs stacked into a snowman, forty-five dots around the curves. Add a hat, a carrot nose and buttons.'),
    ('easter-egg-dot-to-dot', 'easter-egg', 40, False, 'Easter egg dot to dot (40 dots)', 'medium', 'kids', ['easter', 'spring'], ['easter'], 'An egg-shaped outline in forty dots that becomes a blank Easter egg to decorate with stripes and zigzags.'),
    ('umbrella-dot-to-dot', 'umbrella', 48, False, 'Umbrella dot to dot (48 dots)', 'medium', 'tweens', ['weather', 'objects'], [], 'A scalloped umbrella with a curved handle in forty-eight dots. The scallops make it a little trickier than it looks.'),
    ('flower-dot-to-dot-hard', 'flower', 80, False, 'Flower dot to dot (80 dots)', 'hard', 'tweens', ['nature', 'flowers'], ['spring'], 'Six petals traced by eighty closely spaced dots. The numbers get small, so this one suits patient 9 to 12 year-olds.') if False else
    ('flower-dot-to-dot-hard', 'flower', 80, False, 'Flower dot to dot (80 dots)', 'hard', 'tweens', ['nature', 'flowers'], [], 'Six petals traced by eighty closely spaced dots. The numbers get small, so this one suits patient 9 to 12 year-olds.'),
    ('heart-dot-to-dot-hard', 'heart', 100, False, 'Heart dot to dot (100 dots)', 'hard', 'teens', ['shapes', 'love'], ['valentines'], 'One hundred dots around a heart. A calm ten-minute puzzle for teens and adults, and a card once it is coloured.'),
    ('moon-dot-to-dot-hard', 'moon', 90, False, 'Crescent moon dot to dot (90 dots)', 'hard', 'teens', ['space', 'night'], [], 'A crescent moon in ninety dots. Two long arcs that meet at sharp points: easy to see, harder to count.'),
    ('butterfly-dot-to-dot-hard', 'butterfly', 120, False, 'Butterfly dot to dot (120 dots)', 'hard', 'adults', ['animals', 'insects'], [], 'A symmetrical butterfly traced by one hundred and twenty dots, the densest puzzle in this set. For adults and older teens who like a slow, precise drawing.'),
    ('hexagon-dot-to-dot-hard', 'hexagon', 60, False, 'Hexagon dot to dot (60 dots)', 'hard', 'tweens', ['shapes', 'geometry'], [], 'A regular hexagon drawn through sixty dots: a geometry warm-up that doubles as a ruler-free straight-line exercise.'),
]

def build():
    PDF_DIR.mkdir(parents=True, exist_ok=True); IMG_DIR.mkdir(parents=True, exist_ok=True); CONTENT.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    for slug, shape, n, letters, title, diff, band, themes, occ, body in ITEMS:
        pdf = PDF_DIR / f'{slug}.pdf'; png = IMG_DIR / f'{slug}.png'
        build_pdf(slug, shape, n, letters, title, pdf)
        cover(pdf, png)
        size = round(pdf.stat().st_size / 1048576, 2)
        summary = f"{SHAPES[shape][0]} connect-the-dots with {n} {'letters' if letters else 'dots'}, {diff} level, finished picture on page 2."
        fm = f'''---
title: {json.dumps(title)}
type: "dot-to-dot"
summary: {json.dumps(summary)}
difficulty: "{diff}"
age_band: "{band}"
themes: {json.dumps(themes)}
occasions: {json.dumps(occ)}
pages: 2
paper: "both"
colour: "bw"
answers_included: true
count: 1
grid: "{n} {'letters' if letters else 'dots'}"
download_url: "/pdf/puzzles/dot-to-dot/{slug}.pdf"
download_size_mb: {size}
cover: "/img/puzzles/{slug}.png"
licence: "CC BY-NC 4.0"
status: "published"
date_added: "{today}"
seo_title: {json.dumps((title.split(' (')[0] + ' printable (free PDF)')[:60])}
---
<!-- hand-edited -->
## About this dot to dot

{body}

## What's in the PDF

- Page 1: the puzzle, {n} {'lettered' if letters else 'numbered'} dots with the starting point circled.
- Page 2: the finished outline, to check the drawing or to use as a colouring page.
- Black and white, prints on A4 or US Letter at 100% scale.

**Tip:** print page 1 only to keep the answer a surprise, and use a coloured pencil so the line stands out from the dots.
'''
        (CONTENT / f'{slug}.md').write_text(fm)
    print(f'{len(ITEMS)} dot-to-dot puzzles written to {PDF_DIR} / {CONTENT}')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build': build()
    else: print(__doc__)
