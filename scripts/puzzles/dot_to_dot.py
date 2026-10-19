#!/usr/bin/env python3
"""Dot-to-dot (connect the dots) generator for printandplaygame.com.

Each picture starts from a filled silhouette (game-icons.net, CC BY 3.0, or Phosphor Icons, MIT; path
data in dot_to_dot_icons.json) or a hand-made polygon. The silhouette is rasterised, its outer contour
traced, then simplified so dots sit on the corners and turns of the picture only, never evenly spread
along a curve: the shape stays hidden until the dots are joined. Small inner details (eyes, windows)
are printed as thin lines. Difficulty comes from the picture: easy = 10-26 dots, medium = 29-40,
hard = 53-90 on a detailed animal, expert = 110-180 split into several lines (each starts at a red circle).

Needs: pip install svgelements opencv-python-headless reportlab pypdfium2 pillow
  python3 -I scripts/puzzles/dot_to_dot.py build            # PDFs, covers and content entries
  python3 -I scripts/puzzles/dot_to_dot.py preview OUT.png  # contact sheet of every page 1
"""
import math, json, pathlib, sys, datetime, tempfile
import numpy as np
import cv2
from PIL import Image, ImageDraw
from svgelements import Path, Move, Close
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / 'public/pdf/puzzles/dot-to-dot'
IMG_DIR = ROOT / 'public/img/puzzles'
CONTENT = ROOT / 'src/content/puzzles'
ICONS = json.loads((pathlib.Path(__file__).parent / 'dot_to_dot_icons.json').read_text())
W, H = letter
MARGIN = 16 * mm
INK = (0.06, 0.24, 0.18)
RED = (1.0, 0.42, 0.34)
GREY = (0.45, 0.45, 0.45)
RES = 1000  # raster size used to trace silhouettes

# ---------- hand-made polygons (x, y in 0..1, y up) ----------
def area(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) / 2

def star(points=5, inner=0.42):
    pts = []
    for i in range(points * 2):
        a = math.pi / 2 + i * math.pi / points
        r = 0.48 if i % 2 == 0 else 0.48 * inner
        pts.append((0.5 + r * math.cos(a), 0.5 + r * math.sin(a)))
    return pts

HOUSE = [(0.50, 0.92), (0.66, 0.78), (0.66, 0.88), (0.76, 0.88), (0.76, 0.69), (0.90, 0.56), (0.80, 0.56), (0.80, 0.10), (0.56, 0.10), (0.56, 0.36), (0.40, 0.36), (0.40, 0.10), (0.20, 0.10), (0.20, 0.56), (0.10, 0.56)]
HOUSE_WINDOW = [(0.62, 0.30), (0.74, 0.30), (0.74, 0.44), (0.62, 0.44)]
TREE = [(0.50, 0.90), (0.66, 0.70), (0.58, 0.70), (0.74, 0.50), (0.64, 0.50), (0.82, 0.28), (0.56, 0.28), (0.56, 0.12), (0.44, 0.12), (0.44, 0.28), (0.18, 0.28), (0.36, 0.50), (0.26, 0.50), (0.42, 0.70), (0.34, 0.70)]
TREE_STAR = [(0.5 + 0.05 * math.cos(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45), 0.95 + 0.05 * math.sin(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)]

def circle(cx, cy, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]

def snowman():
    """Three stacked snowballs and a top hat; the face, buttons and stick arms are printed details."""
    balls = [(0.5, 0.22, 0.20), (0.5, 0.52, 0.15), (0.5, 0.76, 0.11)]
    m = Image.new('L', (RES, RES), 0); d = ImageDraw.Draw(m)
    for x, y, r in balls:
        d.ellipse(((x - r) * RES, (1 - y - r) * RES, (x + r) * RES, (1 - y + r) * RES), fill=255)
    c = max(cv2.findContours(np.array(m), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)
    ring = [(float(q[0][0]) / RES, 1 - float(q[0][1]) / RES) for q in c]
    if area(ring) < 0: ring.reverse()  # counter-clockwise, so the walk over the head goes right to left
    hat_y = 0.85
    start = max(range(len(ring)), key=lambda i: ring[i][1])
    ring = ring[start:] + ring[:start]  # begin at the top of the head
    outline = [q for q in ring if q[1] < hat_y]
    top = len(outline) - 1  # last point before the hat on the right side, walking counter-clockwise from the top
    hat = [(0.65, hat_y), (0.65, 0.89), (0.58, 0.89), (0.58, 1.0), (0.42, 1.0), (0.42, 0.89), (0.35, 0.89), (0.35, hat_y)]
    outline = outline[:top + 1] + hat + outline[top + 1:]
    details = [(True, circle(0.465, 0.785, 0.011, 10)), (True, circle(0.535, 0.785, 0.011, 10)),
               (True, [(0.5, 0.76), (0.58, 0.748), (0.5, 0.736)]),
               (True, circle(0.5, 0.58, 0.013, 10)), (True, circle(0.5, 0.52, 0.013, 10)), (True, circle(0.5, 0.46, 0.013, 10)),
               (False, [(0.37, 0.58), (0.28, 0.66), (0.24, 0.71)]), (False, [(0.28, 0.66), (0.23, 0.65)]),
               (False, [(0.63, 0.58), (0.72, 0.66), (0.76, 0.71)]), (False, [(0.72, 0.66), (0.77, 0.65)])]
    return outline, details
SAILBOAT = [(0.45, 0.96), (0.64, 0.92), (0.55, 0.87), (0.55, 0.82), (0.68, 0.66), (0.80, 0.52), (0.90, 0.38), (0.55, 0.38), (0.55, 0.29), (0.94, 0.29), (0.80, 0.08), (0.20, 0.08), (0.06, 0.29), (0.45, 0.29), (0.45, 0.38), (0.12, 0.38), (0.28, 0.58), (0.45, 0.78)]
ROCKET = [(0.50, 0.95), (0.60, 0.82), (0.65, 0.62), (0.65, 0.42), (0.80, 0.26), (0.80, 0.12), (0.64, 0.20), (0.58, 0.10), (0.42, 0.10), (0.36, 0.20), (0.20, 0.12), (0.20, 0.26), (0.35, 0.42), (0.35, 0.62), (0.40, 0.82)]
def ellipse(cx, cy, rx, ry, n=24):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]

def union(polys):
    """Outline of several filled polygons merged together (0..1, y up, counter-clockwise)."""
    m = Image.new('L', (RES, RES), 0); d = ImageDraw.Draw(m)
    for poly in polys: d.polygon([(x * RES, (1 - y) * RES) for x, y in poly], fill=255)
    c = max(cv2.findContours(np.array(m), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)
    ring = [(float(q[0][0]) / RES, 1 - float(q[0][1]) / RES) for q in c]
    return ring[::-1] if area(ring) < 0 else ring

def pig_head():
    """A pig's face seen from the front: round head and two pointed ears; snout and eyes are printed details."""
    outline = union([ellipse(0.5, 0.45, 0.38, 0.30, 72), [(0.22, 0.62), (0.08, 0.84), (0.40, 0.73)], [(0.78, 0.62), (0.92, 0.84), (0.60, 0.73)]])
    details = [(True, ellipse(0.5, 0.36, 0.15, 0.095, 28)), (True, ellipse(0.45, 0.36, 0.022, 0.035, 10)), (True, ellipse(0.55, 0.36, 0.022, 0.035, 10)),
               (True, ellipse(0.37, 0.55, 0.028, 0.028, 12)), (True, ellipse(0.63, 0.55, 0.028, 0.028, 12)),
               (False, [(0.40, 0.21), (0.50, 0.18), (0.60, 0.21)]),
               (False, [(0.25, 0.66), (0.15, 0.80), (0.35, 0.71)]), (False, [(0.75, 0.66), (0.85, 0.80), (0.65, 0.71)])]
    return outline, details

POLYGONS = {'star': (star(), []), 'rocket': (ROCKET, []), 'house': (HOUSE, [(True, HOUSE_WINDOW)]), 'sailboat': (SAILBOAT, []),
            'christmas-tree': (TREE, [(True, TREE_STAR)]), 'snowman': snowman(), 'pig': pig_head()}

# ---------- silhouettes ----------
def raster(key):
    """Fill the icon path (even-odd) into a RES x RES mask, 8% padding."""
    ic = ICONS[key]
    s = RES * 0.84 / ic['size']; pad = RES * 0.08
    img = Image.new('L', (RES, RES), 0)
    path = Path(ic['d'])
    polys, cur = [], []
    for seg in path:
        if isinstance(seg, Move):
            if len(cur) > 2: polys.append(cur)
            cur = [seg.end]
        elif isinstance(seg, Close):
            if len(cur) > 2: polys.append(cur)
            cur = []
        else:
            L = seg.length(error=1e-2) if hasattr(seg, 'length') else 1
            k = max(2, int(L * s / 3))
            cur += [seg.point(i / k) for i in range(1, k + 1)]
    if len(cur) > 2: polys.append(cur)
    for poly in polys:
        layer = Image.new('L', (RES, RES), 0)
        ImageDraw.Draw(layer).polygon([(pad + p.x * s, pad + p.y * s) for p in poly], fill=255)
        img = Image.fromarray(np.bitwise_xor(np.array(img), np.array(layer)))
    return np.array(img)

def rdp_n(contours, n):
    """Largest RDP tolerance that keeps about n corners in total over all contours."""
    lo, hi = 0.2, 200.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if sum(len(cv2.approxPolyDP(c, mid, True)) for c in contours) > n: lo = mid
        else: hi = mid
    return [[tuple(map(float, q[0])) for q in cv2.approxPolyDP(c, hi, True)] for c in contours]

def trace(key, n, close=0, details=True, mirror=False, pieces=False):
    """Outer contour(s) simplified to about n corner dots, plus inner details as polylines (pixel coords, y down).
    pieces=True keeps every separate part of the picture (for hard puzzles drawn in several lines)."""
    m = raster(key)
    if mirror: m = m[:, ::-1].copy()
    if close:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close))
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cs = sorted(cs, key=cv2.contourArea, reverse=True)
    parts = [c for c in cs if cv2.contourArea(c) > RES * RES * 0.002] if pieces else cs[:1]
    outlines = rdp_n(parts, n)
    extra = []
    if details:  # small shapes inside the silhouette (eyes, buttons, windows), taken from the unmerged picture
        A = cv2.contourArea(parts[0])
        raw = raster(key)
        if mirror: raw = raw[:, ::-1].copy()
        for c in cv2.findContours(raw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)[0]:
            a = cv2.contourArea(c)
            if not (RES * RES * 0.0005 < a < A * 0.04) or 4 * math.pi * a / cv2.arcLength(c, True) ** 2 < 0.4: continue
            if any(min(cv2.pointPolygonTest(part, (float(q[0][0]), float(q[0][1])), True) for q in c[::4]) > 4 for part in parts):
                extra.append((True, [tuple(map(float, q[0])) for q in cv2.approxPolyDP(c, 1.5, True)]))
    return outlines, extra

def space_out(pts, dmin):
    """Drop dots closer than dmin to the previous kept dot (keeps corners, which come first in RDP order)."""
    out = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, out[-1]) >= dmin: out.append(p)
    while len(out) > 3 and math.dist(out[-1], out[0]) < dmin: out.pop()
    return out

def shape(item):
    """Return (lines, details) in 0..1 coordinates, y up. Each line is a closed run of dots, clockwise, starting at its
    top-most dot; lines are ordered top to bottom and numbered in that order."""
    src = item['src']
    if src in POLYGONS:
        dots, extra = list(POLYGONS[src][0]), POLYGONS[src][1]
        if item.get('n') and len(dots) > item['n']:  # dense hand-made outline: keep the n most telling corners
            c = np.array([[[x * RES, y * RES]] for x, y in dots], dtype=np.float32)
            dots = [(x / RES, y / RES) for x, y in rdp_n([c], item['n'])[0]]
        lines = [dots]
    else:
        px, extra_px = trace(src, item['n'], item.get('close', 0), item.get('details', True), item.get('mirror', False), item.get('pieces', False))
        conv = lambda p: (p[0] / RES, 1 - p[1] / RES)
        lines = [[conv(p) for p in line] for line in px]; extra = [(closed, [conv(p) for p in e]) for closed, e in extra_px]
    out = []
    for dots in lines:
        dots = space_out(dots, item.get('dmin', 0.03))
        if len(dots) < 3: continue
        if area(dots) > 0: dots.reverse()  # clockwise on paper
        top = max(range(len(dots)), key=lambda i: (round(dots[i][1], 2), -dots[i][0]))
        out.append(dots[top:] + dots[:top])
    out.sort(key=lambda d: -d[0][1])
    return out, extra

# ---------- drawing ----------
def page_frame(c, title, subtitle, credit):
    c.setFillColorRGB(*INK)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(MARGIN, H - MARGIN - 6, title)
    c.setFont('Helvetica', 10.5)
    c.drawString(MARGIN, H - MARGIN - 22, subtitle)
    c.setFont('Helvetica', 7.5)
    c.setFillColorRGB(*GREY)
    if credit: c.drawString(MARGIN, MARGIN - 13, credit)
    c.drawRightString(W - MARGIN, MARGIN - 4, 'printandplaygame.com  ·  CC BY-NC 4.0  ·  free for home and classroom use')

def fit(lines, extra, box):
    xs = [p[0] for d in lines for p in d] + [p[0] for _, e in extra for p in e]
    ys = [p[1] for d in lines for p in d] + [p[1] for _, e in extra for p in e]
    x0, y0, bw, bh = box
    s = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
    ox = x0 + (bw - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    oy = y0 + (bh - (max(ys) - min(ys)) * s) / 2 - min(ys) * s
    return lambda p: (ox + p[0] * s, oy + p[1] * s)

def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0 if not L2 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

def place_labels(lines, labs, size, r):
    """Pick, for each dot, the label position (around the outward normal) with the most free space."""
    P = [p for line in lines for p in line]
    segs = [(line[i], line[(i + 1) % len(line)]) for line in lines for i in range(len(line))]
    placed = []
    for line in lines:
        for i in range(len(line)):
            idx = len(placed)
            prev, nxt = line[i - 1], line[(i + 1) % len(line)]
            tx, ty = nxt[0] - prev[0], nxt[1] - prev[1]
            L = math.hypot(tx, ty) or 1
            nx, ny = -ty / L, tx / L  # outward for a clockwise path
            w = 0.56 * size * len(labs[idx]); h = 0.72 * size
            rad = math.hypot(w, h) / 2
            best = None
            for k, ang in enumerate([0, 35, -35, 70, -70, 110, -110, 150, -150, 180]):
                a = math.radians(ang)
                dx, dy = nx * math.cos(a) - ny * math.sin(a), nx * math.sin(a) + ny * math.cos(a)
                for off in (r + rad + 1.5, r + rad + 4):
                    cx, cy = line[i][0] + dx * off, line[i][1] + dy * off
                    clear = min(min(math.dist((cx, cy), q) - r for j, q in enumerate(P) if j != idx),
                                min(seg_dist((cx, cy), a_, b_) for a_, b_ in segs),
                                min((math.dist((cx, cy), q) - qr for q, qr in placed), default=99)) - rad
                    score = clear - k * 0.15 - (off > r + rad + 2) * 0.6
                    if best is None or score > best[0]: best = (score, cx, cy)
                if best[0] > 2: break
            placed.append(((best[1], best[2]), rad))
    return [p for p, _ in placed]

def draw(c, lines, extra, labs, box, level, reveal=False):
    P0 = fit(lines, extra, box)
    L = [[P0(d) for d in line] for line in lines]
    r, size = {'easy': (3.6, 13), 'medium': (2.9, 10), 'hard': (2.3, 8), 'expert': (1.9, 6.5)}[level]
    c.setLineJoin(1); c.setLineCap(1)
    if extra:
        c.setStrokeColorRGB(*INK); c.setLineWidth(1.6 if level != 'expert' else 1.1)
        for closed, e in extra:
            path = c.beginPath(); path.moveTo(*P0(e[0]))
            for p in e[1:]: path.lineTo(*P0(p))
            if closed: path.close()
            c.drawPath(path, stroke=1, fill=0)
    if reveal:
        c.setStrokeColorRGB(*RED); c.setLineWidth(2.4 if level != 'expert' else 1.6)
        for line in L:
            path = c.beginPath(); path.moveTo(*line[0])
            for p in line[1:]: path.lineTo(*p)
            path.close(); c.drawPath(path, stroke=1, fill=0)
    c.setFillColorRGB(*INK)
    for line in L:
        for p in line: c.circle(p[0], p[1], r, stroke=0, fill=1)
    starts, i = set(), 0
    for line in L: starts.add(i); i += len(line)
    for i, (lx, ly) in enumerate(place_labels(L, labs, size, r)):
        c.setFont('Helvetica-Bold' if i in starts else 'Helvetica', size)
        c.drawCentredString(lx, ly - size * 0.36, labs[i])
    c.setStrokeColorRGB(*RED); c.setLineWidth(1.5 if level != 'expert' else 1.1)
    for line in L: c.circle(line[0][0], line[0][1], r + (4.5 if level != 'expert' else 3), stroke=1, fill=0)

def credit_line(item):
    if item['src'] in POLYGONS: return ''
    ic = ICONS[item['src']]
    name = item['src'].split(':')[1].replace('-fill', '').replace('-', ' ')
    if ic['licence'] == 'MIT':
        return f'Picture adapted from the "{name}" icon, Phosphor Icons (MIT licence).'
    return f'Picture adapted from "{name}" by {ic["author"]}, game-icons.net, CC BY 3.0.'

def build_pdf(item, lines, extra, out_pdf):
    n = sum(map(len, lines)); letters = item.get('letters', False)
    labs = [chr(65 + i) for i in range(n)] if letters else [str(i + 1) for i in range(n)]
    c = canvas.Canvas(str(out_pdf), pagesize=letter, invariant=1)
    c.setTitle(item['title']); c.setAuthor('Print & Play Game')
    if letters: sub = 'Join the letters in alphabetical order, A to Z, then colour the picture.'
    elif len(lines) > 1: sub = (f'Connect the dots from 1 to {n}. A red circle starts a new line: join its dots, close it back to that circle, '
                                'then lift your pencil.')
    else: sub = f'Connect the dots from 1 to {n}, then colour the picture.'
    box = (MARGIN + 6 * mm, MARGIN + 8 * mm, W - 2 * MARGIN - 12 * mm, H - 2 * MARGIN - 30 * mm)
    level = item.get('level', item['diff'])
    page_frame(c, item['title'], sub, credit_line(item))
    draw(c, lines, extra, labs, box, level)
    c.showPage()
    page_frame(c, f"{item['title']} – finished picture", 'The picture you get once every dot is joined.', credit_line(item))
    draw(c, lines, extra, labs, box, level, reveal=True)
    c.showPage(); c.save()

def cover(pdf, png):
    """Square crop of page 2 around the drawing area, on white."""
    import pypdfium2 as pdfium
    k = 1.6
    page = pdfium.PdfDocument(str(pdf))[1].render(scale=k).to_pil().convert('RGB')
    top, bottom = MARGIN + 12 * mm, H - MARGIN - 1 * mm  # drawing box plus room for labels, measured from the top
    side = int((bottom - top) * k)
    sq = Image.new('RGB', (side, side), 'white')
    sq.paste(page, ((side - page.width) // 2, -int(top * k)))
    sq.resize((600, 600), Image.LANCZOS).save(png, optimize=True)

# ---------- catalogue ----------
# n = target dots (the final count can be lower: dots never sit closer than dmin), close = pixels used to
# merge the separate pieces of a silhouette, details = print inner holes (eyes, windows) as lines.
E, M, Hd = 'easy', 'medium', 'hard'
ITEMS = [
    # easy: 10-20 dots, big numbers
    dict(slug='star-dot-to-dot-easy', src='star', diff=E, band='preschool', name='Star', themes=['shapes', 'space'], occ=['christmas'], dmin=0.05,
         body='Ten dots and a star: the simplest connect-the-dots for a first pencil. Big numbers, wide spacing, and a picture that is easy to colour afterwards.'),
    dict(slug='heart-dot-to-dot-easy', src='ph:heart-fill', n=12, diff=E, band='preschool', name='Heart', themes=['shapes', 'love'], occ=['valentines'], dmin=0.08,
         body="A heart in a dozen dots for Valentine's Day cards or a quiet morning. Small numbers to count and two round bumps to discover."),
    dict(slug='house-dot-to-dot-easy', src='house', diff=E, band='preschool', name='House', themes=['home', 'shapes'], occ=[], dmin=0.05,
         body='A little house with a chimney and a door. The window is already drawn: join the dots to build the walls, the roof and the chimney around it.'),
    dict(slug='fish-dot-to-dot-easy', src='ph:fish-fill', n=16, diff=E, band='preschool', name='Fish', themes=['animals', 'ocean'], occ=['summer'], dmin=0.06,
         body='A round fish with a pointed tail. Only the eye is printed: count to 14, join the dots and the fish swims out of the page. Add scales and bubbles after.'),
    dict(slug='rocket-dot-to-dot-easy', src='rocket', diff=E, band='preschool', name='Rocket', themes=['space', 'vehicles'], occ=[], dmin=0.05,
         body='Blast off: a rocket with fins and a nose cone in fifteen dots, all on corners, so every line is a straight one. Made for the space fans in kindergarten.'),
    dict(slug='ghost-dot-to-dot-easy', src='ph:ghost-fill', n=14, diff=E, band='preschool', name='Ghost', themes=['halloween'], occ=['halloween'], dmin=0.06,
         body='A friendly ghost with a wavy hem, eyes already printed. A gentle Halloween activity for children who count to 14.'),
    dict(slug='bat-dot-to-dot-easy', src='game-icons:bat', n=18, diff=E, band='preschool', name='Bat', themes=['halloween', 'animals'], occ=['halloween'], dmin=0.045, close=5,
         body='A bat with pointed wings and little ears. The zigzag of the wings is the fun part: every dot is a corner, and the picture only shows up at the end.'),
    dict(slug='christmas-tree-dot-to-dot', src='christmas-tree', diff=E, band='preschool', name='Christmas tree', themes=['christmas', 'nature'], occ=['christmas'], dmin=0.05,
         body='A three-tier Christmas tree with its trunk. The star on top is already drawn; join the dots underneath it, then decorate the branches with baubles.'),
    dict(slug='pig-dot-to-dot', src='pig', n=20, diff=E, band='preschool', name='Pig', themes=['animals', 'farm'], occ=[], dmin=0.05,
         body="A pig's face seen from the front, with two pointed ears. The snout, the eyes and the smile are printed; join the dots to draw the head and the ears around them."),
    dict(slug='sailboat-dot-to-dot', src='sailboat', diff=E, band='kids', name='Sailboat', themes=['vehicles', 'ocean'], occ=['summer'], dmin=0.035,
         body='A sailboat with a flag, a mast, two sails and a hull. Long straight lines and sharp corners: a good one for practising with a ruler.'),
    dict(slug='abc-butterfly-dot-to-dot', src='ph:butterfly-fill', n=26, diff=E, band='kids', name='Butterfly', letters=True, themes=['alphabet', 'animals', 'insects'], occ=['summer'], dmin=0.04, close=25,
         body='A butterfly whose wings follow the alphabet from A to Z. Good for letter recognition in kindergarten and first grade.'),
    dict(slug='abc-rabbit-dot-to-dot', src='ph:rabbit-fill', n=26, diff=E, band='kids', name='Rabbit', letters=True, themes=['alphabet', 'animals'], occ=['easter'], dmin=0.04,
         body='A bunny face with two long ears, drawn by joining the letters A to Z. An alphabet warm-up that turns into an Easter bunny.'),
    dict(slug='abc-gingerbread-man-dot-to-dot', src='game-icons:gingerbread-man', n=26, diff=E, band='kids', name='Gingerbread man', letters=True, themes=['alphabet', 'christmas', 'food'], occ=['christmas'], dmin=0.04, close=25,
         body='A gingerbread man drawn by joining the letters A to Z. His smile and icing buttons are already printed; the alphabet does the rest.'),
    # medium: 25-45 dots, a real animal or object to discover
    dict(slug='pumpkin-dot-to-dot', src='game-icons:pumpkin', n=30, diff=M, band='kids', name='Pumpkin', themes=['halloween', 'autumn'], occ=['halloween', 'thanksgiving'], dmin=0.04, close=41,
         body="A plump pumpkin with a curled stem. Join the dots, then draw the jack-o'-lantern face of your choice."),
    dict(slug='duck-dot-to-dot', src='game-icons:duck', n=32, diff=M, band='kids', name='Duck', themes=['animals', 'farm'], occ=['easter'], dmin=0.035, close=31,
         body='A duck with a flat bill and webbed feet. The curves of the back and tail make it a nice medium puzzle for 6 to 8 year-olds.'),
    dict(slug='penguin-dot-to-dot', src='game-icons:penguin', n=30, diff=M, band='kids', name='Penguin', themes=['animals', 'winter'], occ=['winter'], dmin=0.035, close=9,
         body='A standing penguin with its beak in the air. Thirty dots on the curves of the body and the flat feet, then colour the black back and white belly.'),
    dict(slug='cat-dot-to-dot', src='game-icons:cat', n=40, diff=M, band='kids', name='Cat', themes=['animals', 'pets'], occ=[], dmin=0.03, close=31,
         body='A cat lying down with two pointed ears. Its eyes are printed; the rest appears as you join the dots. Add whiskers, stripes and a tail when the outline is done.'),
    dict(slug='squirrel-dot-to-dot', src='game-icons:squirrel', n=35, diff=M, band='kids', name='Squirrel', themes=['animals', 'autumn'], occ=['thanksgiving'], dmin=0.03, close=31,
         body='A squirrel sitting up, with a big bushy tail curled over its back. The tail and the paws hide in the numbers until the last dots.'),
    dict(slug='turtle-dot-to-dot', src='game-icons:turtle', n=40, diff=M, band='kids', name='Turtle', themes=['animals', 'ocean'], occ=['summer'], dmin=0.03, close=5, details=False,
         body='A turtle seen from above: head, four flippers and a little tail around a round shell. Draw the shell pattern once the dots are joined.'),
    dict(slug='dolphin-dot-to-dot', src='game-icons:dolphin', n=40, diff=M, band='kids', name='Dolphin', themes=['animals', 'ocean'], occ=['summer'], dmin=0.03, close=5,
         body='A dolphin leaping out of the water, fins and tail included, in about forty dots. A summer favourite for 6 to 8 year-olds.'),
    dict(slug='dinosaur-dot-to-dot', src='game-icons:parasaurolophus', n=42, diff=M, band='kids', name='Dinosaur', themes=['dinosaurs', 'animals'], occ=[], dmin=0.03, close=25,
         body='A parasaurolophus, the duck-billed dinosaur with a long crest, standing on its hind legs. A favourite for 6 to 8 year-olds who count past 40.'),
    dict(slug='snowman-dot-to-dot', src='snowman', n=40, diff=M, band='kids', name='Snowman', themes=['winter', 'christmas'], occ=['winter', 'christmas'], dmin=0.03,
         body='A snowman in a top hat. The face, the buttons and the stick arms are printed; the dots trace the three snowballs and the hat. Add a scarf at the end.'),
    dict(slug='gingerbread-man-dot-to-dot', src='game-icons:gingerbread-man', n=40, diff=M, band='kids', name='Gingerbread man', themes=['christmas', 'food'], occ=['christmas'], dmin=0.03, close=25,
         body='A gingerbread man with a smile and icing buttons, ready to decorate. A December favourite that pairs well with real baking.'),
    # hard: 55-90 dots on detailed animals, small numbers
    dict(slug='elephant-dot-to-dot-hard', src='game-icons:elephant', n=70, diff=Hd, band='tweens', name='Elephant', themes=['animals', 'wildlife'], occ=[], dmin=0.022, close=35,
         body='An elephant walking, trunk curled and tusks out. Small numbers and many legs to tell apart: a patient puzzle for 9 to 12 year-olds.'),
    dict(slug='seahorse-dot-to-dot-hard', src='game-icons:seahorse', n=60, diff=Hd, band='tweens', name='Seahorse', themes=['animals', 'ocean'], occ=['summer'], dmin=0.026, close=21,
         body='A seahorse with a spiny back and a curled tail. The dots follow every small spike and the spiral of the tail, so it rewards careful counting.'),
    dict(slug='kangaroo-dot-to-dot-hard', src='game-icons:kangaroo', n=66, diff=Hd, band='tweens', name='Kangaroo', themes=['animals', 'wildlife'], occ=[], dmin=0.022, close=17,
         body='A kangaroo mid-hop, with its long tail, big feet and small front paws. Plenty of dots for confident counters aged 9 to 12.'),
    dict(slug='camel-dot-to-dot-hard', src='game-icons:camel', n=90, diff=Hd, band='teens', name='Camel', themes=['animals', 'wildlife'], occ=[], dmin=0.018, close=15,
         body='A two-humped camel standing on long, knobbly legs. Around eighty dots and small numbers, for teens and adults who like a slow drawing.'),
    dict(slug='octopus-dot-to-dot-hard', src='game-icons:octopus', n=90, diff=Hd, band='teens', name='Octopus', themes=['animals', 'ocean'], occ=['summer'], dmin=0.018, close=5,
         body='An octopus with eight curling arms. The curls pack the dots close together, which makes it the hardest picture of the set: take your time with the numbers.'),
    # expert: 110-180 dots over several lines (a red circle starts each line), tiny numbers, very detailed pictures
    dict(slug='frog-dot-to-dot-expert', src='game-icons:frog', n=140, diff=Hd, level='expert', band='teens', name='Frog', themes=['animals', 'pond'], occ=[], dmin=0.012, pieces=True,
         body='A frog sitting face on, with bulging eyes, a wide mouth and webbed feet. The picture is drawn in several lines: each red circle starts a new one. A detailed puzzle for teens.'),
    dict(slug='toucan-dot-to-dot-expert', src='game-icons:toucan', n=130, diff=Hd, level='expert', band='teens', name='Toucan', themes=['animals', 'birds'], occ=[], dmin=0.012, pieces=True,
         body='A toucan in profile, its huge beak drawn in two parts. Several separate lines, each starting at a red circle, and small numbers: take your time.'),
    dict(slug='barn-owl-dot-to-dot-expert', src='game-icons:barn-owl', n=140, diff=Hd, level='expert', band='teens', name='Barn owl', themes=['animals', 'birds'], occ=['halloween'], dmin=0.012, pieces=True,
         body='A barn owl perched on a branch, with its heart-shaped face and folded wing. Drawn in several lines that start at the red circles, it suits teens and adults.'),
    dict(slug='reindeer-dot-to-dot-expert', src='game-icons:deer', n=150, diff=Hd, level='expert', band='teens', name='Reindeer', themes=['christmas', 'animals'], occ=['christmas', 'winter'], dmin=0.012, pieces=True,
         body='A reindeer with tall branching antlers, one front leg raised. Most of the dots are in the antlers, drawn as separate lines from each red circle: a December challenge for teens and adults.'),
    dict(slug='lion-dot-to-dot-expert', src='game-icons:lion', n=160, diff=Hd, level='expert', band='teens', name='Lion', themes=['animals', 'wildlife'], occ=[], dmin=0.012, pieces=True,
         body="A lion's head in profile, its mane drawn as a ring of sharp tufts. Several lines, each starting at a red circle, and well over a hundred dots."),
    dict(slug='fox-dot-to-dot-expert', src='game-icons:fox', n=150, diff=Hd, level='expert', band='teens', name='Fox', themes=['animals', 'autumn'], occ=['thanksgiving'], dmin=0.012, pieces=True,
         body='A fox sitting with its big tail wrapped around its paws. The face, the ears and the tail are separate lines, each starting at a red circle.'),
    dict(slug='mammoth-dot-to-dot-expert', src='game-icons:mammoth', n=160, diff=Hd, level='expert', band='adults', name='Mammoth', themes=['dinosaurs', 'animals'], occ=[], dmin=0.012, pieces=True,
         body='A woolly mammoth with curled tusks and a shaggy coat. More than 150 dots spread over several lines: a long, slow puzzle for adults and older teens.'),
    dict(slug='rooster-dot-to-dot-expert', src='game-icons:rooster', n=160, diff=Hd, level='expert', band='adults', name='Rooster', themes=['animals', 'farm'], occ=[], dmin=0.012, pieces=True,
         body='A crowing rooster with its comb, wattles and a sweeping tail of feathers. The feathers are separate lines, each starting at a red circle: one of the most detailed pictures of the set.'),
    dict(slug='caravel-dot-to-dot-expert', src='game-icons:caravel', n=200, diff=Hd, level='expert', band='adults', name='Caravel', themes=['vehicles', 'ocean', 'pirates'], occ=[], dmin=0.012, pieces=True,
         body='An old sailing ship with three masts, square sails and a high stern, drawn in several lines. Long straight runs and tight corners, for adults who like a slow drawing.'),
    dict(slug='steam-locomotive-dot-to-dot-expert', src='game-icons:steam-locomotive', n=180, diff=Hd, level='expert', band='adults', name='Steam locomotive', themes=['vehicles', 'trains'], occ=[], dmin=0.012, pieces=True,
         body='A steam locomotive with its smoke cloud, cab, boiler and six wheels. The most lines of the set: every wheel and window is its own shape, starting at a red circle.'),
]

def prepare(item):
    lines, extra = shape(item)
    item['dots'] = n = sum(map(len, lines))
    item['title'] = f"Alphabet dot to dot: {item['name'].lower()} (A to Z)" if item.get('letters') else f"{item['name']} dot to dot ({n} dots)"
    return lines, extra

def preview(out, only=None):
    tiles = []
    for item in ITEMS:
        if only and item['slug'] not in only: continue
        dots, extra = prepare(item)
        tmp = pathlib.Path(tempfile.gettempdir()) / f"d2d-{item['slug']}.pdf"
        build_pdf(item, dots, extra, tmp)
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(tmp))
        tiles.append(doc[0].render(scale=0.9).to_pil().convert('RGB'))
    w, h = tiles[0].size; cols = 4
    sheet = Image.new('RGB', (w * cols, h * math.ceil(len(tiles) / cols)), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * w, (i // cols) * h))
    sheet.save(out)

def build():
    PDF_DIR.mkdir(parents=True, exist_ok=True); IMG_DIR.mkdir(parents=True, exist_ok=True); CONTENT.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    for item in ITEMS:
        dots, extra = prepare(item)
        slug, n, letters = item['slug'], item['dots'], item.get('letters', False)
        pdf = PDF_DIR / f'{slug}.pdf'; png = IMG_DIR / f'{slug}.png'
        build_pdf(item, dots, extra, pdf)
        cover(pdf, png)
        size = round(pdf.stat().st_size / 1048576, 2)
        summary = f"{item['name']} connect-the-dots with {n} {'letters' if letters else 'dots'}, {item['diff']} level, finished picture on page 2."
        old = CONTENT / f'{slug}.md'
        added = today
        if old.exists():
            for line in old.read_text().splitlines():
                if line.startswith('date_added:'): added = line.split('"')[1]
        cred = credit_line(item)
        fm = f'''---
title: {json.dumps(item['title'])}
type: "dot-to-dot"
summary: {json.dumps(summary)}
difficulty: "{item['diff']}"
age_band: "{item['band']}"
themes: {json.dumps(item['themes'])}
occasions: {json.dumps(item['occ'])}
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
date_added: "{added}"
seo_title: {json.dumps((item['title'] + ' – free printable')[:60])}
---
<!-- hand-edited -->
## About this dot to dot

{item['body']}

## What's in the PDF

- Page 1: the puzzle, {n} {'lettered' if letters else 'numbered'} dots with the starting point circled.
- Page 2: the finished picture, to check the drawing or to use as a colouring page.
- Black and white, prints on A4 or US Letter at 100% scale.

The dots sit on the corners and turns of the picture only, so the shape stays a surprise until the last line.

**Tip:** print page 1 only to keep the answer a surprise, and use a coloured pencil so the line stands out from the dots.
'''
        if cred:
            ic = ICONS[item['src']]
            fm += f"\n*{cred.replace(ic['site'], '[' + ic['site'] + '](' + ic['source'] + ')')}*\n"
        (CONTENT / f'{slug}.md').write_text(fm)
    print(f'{len(ITEMS)} dot-to-dot puzzles written to {PDF_DIR} / {CONTENT}')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build': build()
    elif len(sys.argv) > 2 and sys.argv[1] == 'preview': preview(sys.argv[2], sys.argv[3:])
    else: print(__doc__)
