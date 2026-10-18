#!/usr/bin/env python3
"""Perfect-maze generator (recursive backtracker) with shaped masks.

    python3 -I scripts/puzzles/mazes.py --difficulty easy --shape heart --seed 7 \
        --title "Heart maze" --out out.pdf --cover out.png

Difficulty drives the grid size and the wall thickness:
  easy    8x8 .. 12x12, thick walls, shortest of several candidate solutions
  medium  18x18 .. 24x24
  hard    36x36 .. 48x48, thin walls, longest candidate solution
Shapes mask the grid (circle, star, heart, tree, pumpkin, egg, hexagon, triangle,
diamond, snowflake, sun, flower, rocket, fish, house, barn, square).
Styles: square (default), rounded (round joins) and diagonal (grid rotated 45 degrees).
Page 1 is the maze, page 2 the solution drawn in red. Deterministic for a given seed.
"""
from __future__ import annotations

import argparse
import math
import random
from collections import deque
from dataclasses import dataclass, field

from reportlab.pdfgen import canvas

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I drops the script dir
from common import (GREY, INK, LIGHT, RED, free_area, new_canvas, page_header, render_cover)

# ---------------------------------------------------------------------------
# Shapes: f(u, v) -> bool with u (right) and v (up) in [-1, 1]
# ---------------------------------------------------------------------------

def _poly(points):
    def inside(u, v):
        hit = False
        n = len(points)
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if (y1 > v) != (y2 > v):
                x = x1 + (v - y1) * (x2 - x1) / (y2 - y1)
                if u < x:
                    hit = not hit
        return hit
    return inside


def _star(points_n, r_out, r_in, rot=math.pi / 2):
    pts = []
    for i in range(points_n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / points_n
        pts.append((r * math.cos(a), r * math.sin(a)))
    return _poly(pts)


def _ellipse(cx, cy, rx, ry):
    return lambda u, v: ((u - cx) / rx) ** 2 + ((v - cy) / ry) ** 2 <= 1


def _rect(x0, y0, x1, y1):
    return lambda u, v: x0 <= u <= x1 and y0 <= v <= y1


def _union(*fs):
    return lambda u, v: any(f(u, v) for f in fs)


def _rot_rect(length, width, angle):
    ca, sa = math.cos(angle), math.sin(angle)
    def inside(u, v):
        x = u * ca + v * sa
        y = -u * sa + v * ca
        return abs(x) <= length / 2 and abs(y) <= width / 2
    return inside


def _heart(u, v):
    x, y = u * 1.15, v * 1.1 + 0.12
    return (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0


def _egg(u, v):
    w = 0.82 * (1 - 0.22 * max(v, 0.0))
    return (u / w) ** 2 + (v / 1.0) ** 2 <= 1


def _snowflake():
    arms = [_rot_rect(2.0, 0.2, k * math.pi / 3) for k in range(3)]
    branches = []
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 2
        for s in (-1, 1):
            # short bar starting at 0.5 along the arm, leaning +-60 degrees
            bx, by = 0.52 * math.cos(a), 0.52 * math.sin(a)
            ang = a + s * math.pi / 3
            ex, ey = bx + 0.42 * math.cos(ang), by + 0.42 * math.sin(ang)
            cx, cy = (bx + ex) / 2, (by + ey) / 2
            ca, sa = math.cos(ang), math.sin(ang)
            def bar(u, v, cx=cx, cy=cy, ca=ca, sa=sa):
                x = (u - cx) * ca + (v - cy) * sa
                y = -(u - cx) * sa + (v - cy) * ca
                return abs(x) <= 0.23 and abs(y) <= 0.09
            branches.append(bar)
    return _union(_ellipse(0, 0, 0.3, 0.3), *arms, *branches)


SHAPES = {
    "square": lambda u, v: True,
    "circle": _ellipse(0, 0, 1, 1),
    "heart": _heart,
    "star": _star(5, 1.0, 0.47),
    "tree": _union(_rect(-0.11, -1.0, 0.11, -0.72), _poly([(0, 0.15), (-1.0, -0.74), (1.0, -0.74)]),
                   _poly([(0, 0.62), (-0.76, -0.24), (0.76, -0.24)]), _poly([(0, 1.0), (-0.52, 0.26), (0.52, 0.26)])),
    "pumpkin": _union(_ellipse(0, -0.08, 1.0, 0.82), _rect(-0.12, 0.6, 0.12, 1.0)),
    "egg": _egg,
    "hexagon": _poly([(math.cos(a) * 1.0, math.sin(a) * 1.0) for a in [math.pi / 2 + i * math.pi / 3 for i in range(6)]]),
    "triangle": _poly([(0, 1.0), (-1.0, -0.76), (1.0, -0.76)]),
    "diamond": lambda u, v: abs(u) + abs(v) <= 1,
    "snowflake": _snowflake(),
    "sun": _star(16, 1.0, 0.66),
    "flower": _union(_ellipse(0, 0, 0.36, 0.36), *[_ellipse(0.62 * math.cos(k * math.pi / 3 + math.pi / 2),
                                                           0.62 * math.sin(k * math.pi / 3 + math.pi / 2), 0.37, 0.37) for k in range(6)]),
    "rocket": _union(_rect(-0.36, -0.62, 0.36, 0.45), _poly([(0, 1.0), (-0.36, 0.45), (0.36, 0.45)]),
                     _poly([(-0.36, -0.1), (-0.85, -0.95), (-0.36, -0.95)]), _poly([(0.36, -0.1), (0.85, -0.95), (0.36, -0.95)]),
                     _rect(-0.2, -0.86, 0.2, -0.6)),
    "fish": _union(_ellipse(0.2, 0, 0.72, 0.46), _poly([(-0.35, 0), (-1.0, 0.55), (-1.0, -0.55)]),
                   _poly([(-0.05, 0.35), (0.25, 0.8), (0.5, 0.38)])),
    "house": _union(_rect(-0.72, -1.0, 0.72, 0.22), _poly([(0, 0.95), (-0.92, 0.2), (0.92, 0.2)]), _rect(0.38, 0.3, 0.58, 0.82)),
    "barn": _union(_rect(-0.82, -1.0, 0.82, 0.2), _poly([(-0.96, 0.2), (-0.82, 0.64), (-0.42, 0.95), (0.42, 0.95), (0.82, 0.64), (0.96, 0.2)])),
}

DIFFICULTY = {
    #           size range, wall width, solution width, candidates, pick
    "easy": ((8, 12), 4.6, 6.0, 8, "min"),
    "medium": ((18, 24), 2.2, 3.2, 5, "median"),
    "hard": ((36, 48), 1.05, 1.5, 5, "max"),
}

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}


@dataclass
class Maze:
    cols: int
    rows: int
    cells: set = field(default_factory=set)        # (c, r) inside the mask
    passages: set = field(default_factory=set)     # frozenset({cell_a, cell_b})
    start: tuple = (0, 0)
    end: tuple = (0, 0)
    start_side: str = "N"
    end_side: str = "S"
    solution: list = field(default_factory=list)

    def linked(self, a, b):
        return frozenset((a, b)) in self.passages


def build_mask(cols, rows, shape):
    f = SHAPES[shape]
    cells = set()
    for r in range(rows):
        for c in range(cols):
            u = (c + 0.5) / cols * 2 - 1
            v = 1 - (r + 0.5) / rows * 2
            if f(u, v):
                cells.add((c, r))
    # keep the largest connected component so the maze is always solvable
    best, seen = set(), set()
    for cell in cells:
        if cell in seen:
            continue
        comp, dq = {cell}, deque([cell])
        seen.add(cell)
        while dq:
            c, r = dq.popleft()
            for dc, dr in DIRS.values():
                nb = (c + dc, r + dr)
                if nb in cells and nb not in seen:
                    seen.add(nb)
                    comp.add(nb)
                    dq.append(nb)
        if len(comp) > len(best):
            best = comp
    return best


def carve(maze: Maze, rng: random.Random):
    cells = maze.cells
    start = rng.choice(sorted(cells))
    visited = {start}
    stack = [start]
    while stack:
        c, r = stack[-1]
        nbs = [(c + dc, r + dr) for dc, dr in DIRS.values()]
        nbs = [n for n in nbs if n in cells and n not in visited]
        if not nbs:
            stack.pop()
            continue
        nxt = rng.choice(nbs)
        maze.passages.add(frozenset(((c, r), nxt)))
        visited.add(nxt)
        stack.append(nxt)


def pick_openings(maze: Maze, entry: str):
    cells = maze.cells
    if entry == "left-right":
        minc = min(c for c, _ in cells)
        maxc = max(c for c, _ in cells)
        midr = maze.rows / 2
        maze.start = min((x for x in cells if x[0] == minc), key=lambda x: abs(x[1] + 0.5 - midr))
        maze.end = min((x for x in cells if x[0] == maxc), key=lambda x: abs(x[1] + 0.5 - midr))
        maze.start_side, maze.end_side = "W", "E"
    else:
        minr = min(r for _, r in cells)
        maxr = max(r for _, r in cells)
        midc = maze.cols / 2
        maze.start = min((x for x in cells if x[1] == minr), key=lambda x: abs(x[0] + 0.5 - midc))
        maze.end = min((x for x in cells if x[1] == maxr), key=lambda x: abs(x[0] + 0.5 - midc))
        maze.start_side, maze.end_side = "N", "S"


def solve(maze: Maze):
    prev = {maze.start: None}
    dq = deque([maze.start])
    while dq:
        cur = dq.popleft()
        if cur == maze.end:
            break
        c, r = cur
        for dc, dr in DIRS.values():
            nb = (c + dc, r + dr)
            if nb in maze.cells and nb not in prev and maze.linked(cur, nb):
                prev[nb] = cur
                dq.append(nb)
    path, cur = [], maze.end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    maze.solution = path[::-1]


def generate(seed: int, difficulty: str, shape: str = "square", size: int | None = None,
             aspect: float = 1.0, entry: str = "top-bottom") -> Maze:
    (lo, hi), _, _, n_cand, pick = DIFFICULTY[difficulty]
    rng = random.Random(seed)
    cols = size or rng.randint(lo, hi)
    rows = max(2, round(cols * aspect))
    cands = []
    for i in range(n_cand):
        m = Maze(cols, rows)
        m.cells = build_mask(cols, rows, shape)
        carve(m, random.Random(seed * 1000 + i))
        pick_openings(m, entry)
        solve(m)
        cands.append(m)
    cands.sort(key=lambda m: len(m.solution))
    if pick == "min":
        return cands[0]
    if pick == "max":
        return cands[-1]
    return cands[len(cands) // 2]


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def _wall_segments(maze: Maze):
    """Yield wall segments in grid units ((x1, y1), (x2, y2)); y grows downwards."""
    segs = []
    for (c, r) in maze.cells:
        for side, (dc, dr) in DIRS.items():
            nb = (c + dc, r + dr)
            if (c, r) == maze.start and side == maze.start_side:
                continue
            if (c, r) == maze.end and side == maze.end_side:
                continue
            if nb in maze.cells:
                if maze.linked((c, r), nb):
                    continue
                # interior wall: draw once (from the N/W side only)
                if side in ("S", "E"):
                    continue
            if side == "N":
                segs.append(((c, r), (c + 1, r)))
            elif side == "S":
                segs.append(((c, r + 1), (c + 1, r + 1)))
            elif side == "W":
                segs.append(((c, r), (c, r + 1)))
            else:
                segs.append(((c + 1, r), (c + 1, r + 1)))
    return segs


def _join_segments(segs):
    """Merge collinear touching segments to keep the PDF small."""
    horiz, vert = {}, {}
    for (x1, y1), (x2, y2) in segs:
        if y1 == y2:
            horiz.setdefault(y1, set()).add((min(x1, x2), max(x1, x2)))
        else:
            vert.setdefault(x1, set()).add((min(y1, y2), max(y1, y2)))
    out = []
    for y, runs in horiz.items():
        for a, b in _merge(runs):
            out.append(((a, y), (b, y)))
    for x, runs in vert.items():
        for a, b in _merge(runs):
            out.append(((x, a), (x, b)))
    return out


def _merge(runs):
    runs = sorted(runs)
    merged = []
    for a, b in runs:
        if merged and merged[-1][1] >= a:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


class Transform:
    """Grid units -> page points, with optional 45-degree rotation, fitted to a box."""

    def __init__(self, maze: Maze, box, style: str, pad: float, label_reach: float = 1.9):
        x0, y0, w, h = box
        self.rot = math.radians(45) if style == "diagonal" else 0.0
        self.cos, self.sin = math.cos(self.rot), math.sin(self.rot)
        corners = []
        for (c, r) in maze.cells:
            for dx in (0, 1):
                for dy in (0, 1):
                    corners.append(self._rot(c + dx, r + dy))
        # room for the arrows and the Start / Finish labels outside the openings
        for cellxy, side in ((maze.start, maze.start_side), (maze.end, maze.end_side)):
            dx, dy = DIRS[side]
            cx, cy = cellxy[0] + 0.5, cellxy[1] + 0.5
            reach = label_reach + 0.8
            corners.append(self._rot(cx + dx * reach, cy + dy * reach))
            if dx == 0:
                corners.append(self._rot(cx - 1.6, cy + dy * reach))
                corners.append(self._rot(cx + 1.6, cy + dy * reach))
        xs = [p[0] for p in corners]
        ys = [p[1] for p in corners]
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
        gw, gh = maxx - minx, maxy - miny
        self.scale = min((w - 2 * pad) / gw, (h - 2 * pad) / gh)
        self.ox = x0 + (w - gw * self.scale) / 2 - minx * self.scale
        self.oy = y0 + h - (h - gh * self.scale) / 2 + miny * self.scale   # flip y (page y grows up)

    def _rot(self, x, y):
        return (x * self.cos - y * self.sin, x * self.sin + y * self.cos)

    def __call__(self, x, y):
        rx, ry = self._rot(x, y)
        return (self.ox + rx * self.scale, self.oy - ry * self.scale)

    @property
    def cell(self):
        return self.scale


def draw_maze(c: canvas.Canvas, maze: Maze, box, difficulty: str, style: str,
              start_label="Start", end_label="Finish", solution=False):
    _, wall_w, sol_w, _, _ = DIFFICULTY[difficulty]
    pad = 6
    label_reach = 2.7 if style == "diagonal" else 1.9
    T = Transform(maze, box, style, pad, label_reach)
    cell = T.cell
    c.saveState()
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(wall_w)
    rounded = style in ("rounded", "diagonal")
    c.setLineCap(1 if rounded else 2)
    c.setLineJoin(1 if rounded else 0)
    p = c.beginPath()
    for (a, b) in _join_segments(_wall_segments(maze)):
        p.moveTo(*T(*a))
        p.lineTo(*T(*b))
    c.drawPath(p, stroke=1, fill=0)

    # openings: arrows and labels
    def opening(cellxy, side, label, into: bool):
        cx, cy = cellxy[0] + 0.5, cellxy[1] + 0.5
        dx, dy = DIRS[side]
        edge = (cx + dx * 0.5, cy + dy * 0.5)
        far = (cx + dx * 1.35, cy + dy * 1.35)
        p_edge, p_far = T(*edge), T(*far)
        if into:
            tail, head = p_far, T(cx + dx * 0.45, cy + dy * 0.45)
        else:
            tail, head = p_edge, T(cx + dx * 1.3, cy + dy * 1.3)
        _arrow(c, tail, head, max(1.3, wall_w * 0.6))
        # label beyond the arrow
        lx, ly = T(cx + dx * label_reach, cy + dy * label_reach)
        c.setFont("Helvetica-Bold", 9 if difficulty != "easy" else 10.5)
        c.setFillColorRGB(*INK)
        ang = math.degrees(math.atan2(head[1] - tail[1], head[0] - tail[0]))
        # keep labels horizontal; nudge so they sit outside the maze
        if abs(dx) > abs(dy) and T.rot == 0:
            if dx > 0:
                c.drawString(lx - 2, ly - 3.5, label)
            else:
                c.drawRightString(lx + 2, ly - 3.5, label)
        else:
            c.drawCentredString(lx, ly - 3.5 if dy > 0 and T.rot == 0 else ly - 3.5, label)
        _ = ang

    opening(maze.start, maze.start_side, start_label, True)
    opening(maze.end, maze.end_side, end_label, False)

    if solution and maze.solution:
        c.setStrokeColorRGB(*RED)
        c.setLineWidth(sol_w)
        c.setLineCap(1)
        c.setLineJoin(1)
        p = c.beginPath()
        sx, sy = maze.start
        dx, dy = DIRS[maze.start_side]
        p.moveTo(*T(sx + 0.5 + dx * 0.9, sy + 0.5 + dy * 0.9))
        for (x, y) in maze.solution:
            p.lineTo(*T(x + 0.5, y + 0.5))
        ex, ey = maze.end
        dx, dy = DIRS[maze.end_side]
        p.lineTo(*T(ex + 0.5 + dx * 0.9, ey + 0.5 + dy * 0.9))
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()
    return cell


def _arrow(c, tail, head, w):
    c.saveState()
    c.setStrokeColorRGB(*INK)
    c.setFillColorRGB(*INK)
    c.setLineWidth(w)
    c.setLineCap(1)
    c.line(tail[0], tail[1], head[0], head[1])
    ang = math.atan2(head[1] - tail[1], head[0] - tail[0])
    size = 3.2 * w + 2
    p = c.beginPath()
    p.moveTo(*head)
    p.lineTo(head[0] - size * math.cos(ang - 0.45), head[1] - size * math.sin(ang - 0.45))
    p.lineTo(head[0] - size * math.cos(ang + 0.45), head[1] - size * math.sin(ang + 0.45))
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


# ---------------------------------------------------------------------------
# PDF assembly
# ---------------------------------------------------------------------------

def render_pdf(maze: Maze, out_pdf, title: str, difficulty: str, style: str = "square",
               start_label="Start", end_label="Finish", intro: str | None = None):
    label = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}[difficulty]
    intro = intro or f"{label} maze · {maze.cols} × {maze.rows} grid · find the one path from {start_label} to {end_label}."
    c = new_canvas(out_pdf, title, f"{label} printable maze")
    top = page_header(c, title, intro, 1, 2)
    draw_maze(c, maze, free_area(top), difficulty, style, start_label, end_label)
    c.showPage()
    top = page_header(c, f"{title} – solution", f"The path is drawn in red ({len(maze.solution)} cells long).", 2, 2)
    draw_maze(c, maze, free_area(top), difficulty, style, start_label, end_label, solution=True)
    c.showPage()
    c.save()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--difficulty", choices=DIFFICULTY, default="medium")
    ap.add_argument("--shape", choices=SHAPES, default="square")
    ap.add_argument("--style", choices=["square", "rounded", "diagonal"], default="square")
    ap.add_argument("--size", type=int, help="grid columns (default: random in the difficulty range)")
    ap.add_argument("--aspect", type=float, default=1.0, help="rows / cols")
    ap.add_argument("--entry", choices=["top-bottom", "left-right"], default="top-bottom")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--title", default="Maze")
    ap.add_argument("--start-label", default="Start")
    ap.add_argument("--end-label", default="Finish")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cover", help="PNG path for a 600x600 render of page 1")
    a = ap.parse_args(argv)
    m = generate(a.seed, a.difficulty, a.shape, a.size, a.aspect, a.entry)
    render_pdf(m, a.out, a.title, a.difficulty, a.style, a.start_label, a.end_label)
    if a.cover:
        render_cover(a.out, a.cover)
    print(f"{a.out}: {m.cols}x{m.rows}, {len(m.cells)} cells, solution {len(m.solution)}")


if __name__ == "__main__":
    main()
