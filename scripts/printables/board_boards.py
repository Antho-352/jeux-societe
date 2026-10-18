#!/usr/bin/env python3
"""One-page printable boards and score sheets for the classic board, dice and
pen-and-paper rules pages (public-domain games only).

Run from the repository root:

    python3 -I scripts/printables/board_boards.py

Every file is a single US Letter page with 18 mm margins, so it also prints
unscaled on A4 with at least 15 mm of margin. Output goes to
public/pdf/rules/<slug>/<file>.pdf. Only vector drawing and the built-in
Helvetica font are used, which keeps every file well under 100 KB.
"""
from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib.colors import Color, black, white
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "public" / "pdf" / "rules"
MARGIN = 18 * mm  # 51 pt
SITE = "printandplaygame.com"

GREY = Color(0.80, 0.80, 0.80)
LIGHT = Color(0.90, 0.90, 0.90)
DARK = Color(0.22, 0.22, 0.22)
MID = Color(0.55, 0.55, 0.55)


# ---------------------------------------------------------------- helpers --
def new_canvas(slug: str, filename: str, title: str, pagesize=letter) -> tuple[canvas.Canvas, Path]:
    folder = OUT_DIR / slug
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    c = canvas.Canvas(str(path), pagesize=pagesize)
    c.setTitle(title)
    c.setAuthor("Print & Play Game")
    c.setSubject(f"{title} - free printable from {SITE}")
    c.setCreator("scripts/printables/board_boards.py (reportlab)")
    return c, path


def header(c: canvas.Canvas, title: str, subtitle: str = "", pagesize=letter) -> float:
    """Draw the page title and footer. Returns the y coordinate under the title."""
    w, h = pagesize
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN, h - MARGIN - 14, title)
    if subtitle:
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DARK)
        c.drawString(MARGIN, h - MARGIN - 28, subtitle)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID)
    c.drawString(MARGIN, MARGIN - 14, f"{SITE}  ·  free printable for personal use  ·  print at 100 % on Letter or A4")
    c.drawRightString(w - MARGIN, MARGIN - 14, "Rules: " + SITE + "/rules/")
    c.setFillColor(black)
    return h - MARGIN - (36 if subtitle else 24)


def cut_line(c: canvas.Canvas, y: float, x0: float, x1: float, label: str = "cut") -> None:
    c.saveState()
    c.setDash([4, 3])
    c.setLineWidth(0.6)
    c.setStrokeColor(MID)
    c.line(x0, y, x1, y)
    c.restoreState()
    if label:
        c.setFont("Helvetica", 7)
        c.setFillColor(MID)
        c.drawString(x0, y + 2, label)
        c.setFillColor(black)


def grid(c: canvas.Canvas, x0: float, y0: float, cols: int, rows: int, cell: float, lw: float = 0.8) -> None:
    c.setLineWidth(lw)
    c.setStrokeColor(black)
    for i in range(cols + 1):
        c.line(x0 + i * cell, y0, x0 + i * cell, y0 + rows * cell)
    for j in range(rows + 1):
        c.line(x0, y0 + j * cell, x0 + cols * cell, y0 + j * cell)


def checkered(c: canvas.Canvas, x0: float, y0: float, n: int, cell: float, fill: Color, dark_first: bool = True) -> None:
    """Fill the dark squares of an n x n board. The bottom-left square is dark
    when dark_first is True (chess: a1 is dark; checkers: play on dark squares)."""
    c.setFillColor(fill)
    for r in range(n):
        for col in range(n):
            is_dark = ((r + col) % 2 == 0) == dark_first
            if is_dark:
                c.rect(x0 + col * cell, y0 + r * cell, cell, cell, stroke=0, fill=1)
    c.setFillColor(black)
    c.setLineWidth(1.2)
    c.rect(x0, y0, n * cell, n * cell, stroke=1, fill=0)


def token_row(c: canvas.Canvas, x0: float, y: float, count: int, r: float, pitch: float, fill: Color, labels=None, label_color=black) -> None:
    for i in range(count):
        cx = x0 + r + i * pitch
        c.setFillColor(fill)
        c.setStrokeColor(black)
        c.setLineWidth(0.8)
        c.circle(cx, y, r, stroke=1, fill=1)
        if labels:
            c.setFillColor(label_color)
            c.setFont("Helvetica-Bold", r * 0.95)
            c.drawCentredString(cx, y - r * 0.34, labels[i])
    c.setFillColor(black)


# ---------------------------------------------------------------- boards --
def checkers() -> Path:
    c, path = new_canvas("checkers", "checkers-board.pdf", "Checkers (draughts) board")
    top = header(c, "Checkers board", "8 x 8 board for checkers / English draughts. Pieces move on the shaded squares.")
    cell = 60
    x0 = MARGIN
    y0 = top - 8 - 8 * cell
    checkered(c, x0, y0, 8, cell, GREY, dark_first=True)
    # pieces to cut out: 12 light, 12 dark
    y = y0 - 22
    cut_line(c, y + 4, MARGIN, letter[0] - MARGIN, "cut out the 24 pieces below (stack two to make a king)")
    r = 19
    pitch = (8 * cell) / 12
    token_row(c, x0, y - r - 6, 12, r, pitch, white)
    token_row(c, x0, y - 3 * r - 14, 12, r, pitch, DARK)
    c.showPage()
    c.save()
    return path


def chess() -> Path:
    c, path = new_canvas("chess", "chess-board.pdf", "Chess board with coordinates")
    top = header(c, "Chess board", "8 x 8 board with file letters and rank numbers. Set up with a light square in each player's right-hand corner.")
    cell = 58
    x0 = MARGIN + 14
    y0 = top - 10 - 8 * cell
    checkered(c, x0, y0, 8, cell, LIGHT, dark_first=True)
    c.setFont("Helvetica", 9)
    for i, f in enumerate("abcdefgh"):
        c.drawCentredString(x0 + i * cell + cell / 2, y0 - 11, f)
        c.drawCentredString(x0 + i * cell + cell / 2, y0 + 8 * cell + 4, f)
    for j in range(8):
        c.drawRightString(x0 - 4, y0 + j * cell + cell / 2 - 3, str(j + 1))
        c.drawString(x0 + 8 * cell + 4, y0 + j * cell + cell / 2 - 3, str(j + 1))
    y = y0 - 36
    cut_line(c, y + 4, MARGIN, letter[0] - MARGIN, "cut out the 32 piece tokens: K king, Q queen, R rook, B bishop, N knight, P pawn")
    labels = list("KQRRBBNN") + ["P"] * 8
    r = 13.5
    pitch = (8 * cell + 14) / 16
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, y - 8, "White")
    token_row(c, MARGIN + 30, y - r - 4, 16, r, pitch, white, labels)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, y - 2 * r - 20, "Black")
    token_row(c, MARGIN + 30, y - 3 * r - 14, 16, r, pitch, GREY, labels)
    c.showPage()
    c.save()
    return path


def tic_tac_toe() -> Path:
    c, path = new_canvas("tic-tac-toe", "tic-tac-toe-sheet.pdf", "Tic-tac-toe sheet (12 grids)")
    top = header(c, "Tic-tac-toe", "12 empty 3 x 3 grids. Take turns marking X and O; three in a row wins.")
    size = 140
    gap_x = (letter[0] - 2 * MARGIN - 3 * size) / 2
    gap_y = 22
    c.setLineWidth(2)
    for row in range(4):
        for col in range(3):
            x = MARGIN + col * (size + gap_x)
            y = top - 10 - size - row * (size + gap_y)
            for k in (1, 2):
                c.line(x + k * size / 3, y, x + k * size / 3, y + size)
                c.line(x, y + k * size / 3, x + size, y + k * size / 3)
    c.showPage()
    c.save()
    return path


def dots_and_boxes() -> Path:
    c, path = new_canvas("dots-and-boxes", "dots-and-boxes-sheet.pdf", "Dots and boxes sheet (4 grids)")
    top = header(c, "Dots and boxes", "Four 6 x 6 dot grids (25 boxes each). Join two dots with a line; close a box to score it and play again.")
    n = 6
    spacing = 40
    size = (n - 1) * spacing
    gap_x = letter[0] - 2 * MARGIN - 2 * size
    gap_y = 70
    c.setFillColor(black)
    for row in range(2):
        for col in range(2):
            x = MARGIN + col * (size + gap_x)
            y = top - 24 - size - row * (size + gap_y)
            for i in range(n):
                for j in range(n):
                    c.circle(x + i * spacing, y + j * spacing, 2.6, stroke=0, fill=1)
            c.setFont("Helvetica", 9)
            c.drawString(x, y - 22, "Player 1 boxes: ________      Player 2 boxes: ________")
    c.showPage()
    c.save()
    return path


def battleship() -> Path:
    c, path = new_canvas("battleship", "battleship-sheet.pdf", "Battleship grids (two players)")
    top = header(c, "Battleship grids", "Two players per page. Mark your ships on 'My fleet'; record your shots on 'My shots'. Cut along the dashed line.")
    cell = 18
    width = letter[0] - 2 * MARGIN
    block_h = (top - MARGIN - 30) / 2

    def one_grid(x, y, label):
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y + 10 * cell + 16, label)
        c.setFont("Helvetica", 7.5)
        for i in range(10):
            c.drawCentredString(x + i * cell + cell / 2, y + 10 * cell + 4, str(i + 1))
            c.drawRightString(x - 3, y + (9 - i) * cell + cell / 2 - 2.5, "ABCDEFGHIJ"[i])
        grid(c, x, y, 10, 10, cell, 0.6)

    for p in range(2):
        base = top - 8 - p * block_h
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, base - 12, f"Player {p + 1}")
        gy = base - 46 - 10 * cell
        one_grid(MARGIN + 12, gy, "My fleet (place your 5 ships here)")
        one_grid(MARGIN + 12 + 10 * cell + 62, gy, "My shots (X = hit, / = miss)")
        c.setFont("Helvetica", 8)
        c.drawString(MARGIN, gy - 14, "Fleet: Carrier 5 squares  ·  Battleship 4  ·  Cruiser 3  ·  Submarine 3  ·  Destroyer 2.  Ships lie in a straight line, no overlap, no diagonals.")
        if p == 0:
            cut_line(c, gy - 26, MARGIN, MARGIN + width, "cut")
    c.showPage()
    c.save()
    return path


def nine_mens_morris() -> Path:
    c, path = new_canvas("nine-mens-morris", "nine-mens-morris-board.pdf", "Nine men's morris board")
    top = header(c, "Nine men's morris", "Three squares joined at the midpoints: 24 points. Three in a line along a drawn line is a mill.")
    size = 440
    cx = letter[0] / 2
    cy = top - 12 - size / 2
    c.setLineWidth(2)
    pts = []
    for k, s in enumerate((size, size * 2 / 3, size / 3)):
        c.rect(cx - s / 2, cy - s / 2, s, s, stroke=1, fill=0)
        h = s / 2
        for (px, py) in ((-h, -h), (0, -h), (h, -h), (-h, 0), (h, 0), (-h, h), (0, h), (h, h)):
            pts.append((cx + px, cy + py))
    inner = size / 6
    outer = size / 2
    c.line(cx, cy + inner, cx, cy + outer)
    c.line(cx, cy - inner, cx, cy - outer)
    c.line(cx + inner, cy, cx + outer, cy)
    c.line(cx - inner, cy, cx - outer, cy)
    c.setFillColor(white)
    c.setLineWidth(1.4)
    for (px, py) in pts:
        c.circle(px, py, 7, stroke=1, fill=1)
    c.setFillColor(black)
    y = cy - size / 2 - 24
    cut_line(c, y + 6, MARGIN, letter[0] - MARGIN, "cut out the 18 men: 9 light, 9 dark")
    r = 17
    pitch = (letter[0] - 2 * MARGIN) / 9
    token_row(c, MARGIN, y - r - 4, 9, r, pitch, white)
    token_row(c, MARGIN, y - 3 * r - 12, 9, r, pitch, DARK)
    c.showPage()
    c.save()
    return path


def mancala() -> Path:
    size = landscape(letter)
    c, path = new_canvas("mancala", "mancala-board.pdf", "Mancala (Kalah) board", pagesize=size)
    top = header(c, "Mancala board (Kalah)", "Two rows of six pits and a store at each end. Your store is on your right. Start with 4 seeds (beans, buttons, pebbles) in every pit.", pagesize=size)
    w = size[0] - 2 * MARGIN
    pit = 64
    gap = 12
    store_w = 76
    row_gap = 18
    board_h = 2 * pit + row_gap + 2 * 26
    board_w = 2 * store_w + 6 * pit + 5 * gap + 2 * 26 + 2 * 16
    x0 = MARGIN + (w - board_w) / 2
    y0 = top - 40 - board_h
    c.setLineWidth(1.6)
    c.roundRect(x0, y0, board_w, board_h, 18, stroke=1, fill=0)
    # stores
    for sx, label in ((x0 + 26, "Store of the player on the right"), (x0 + board_w - 26 - store_w, "Store of the player on the left")):
        c.setFillColor(LIGHT)
        c.roundRect(sx, y0 + 26, store_w, board_h - 52, store_w / 2, stroke=1, fill=1)
        c.setFillColor(black)
    # pits
    px0 = x0 + 26 + store_w + 16
    for r_i, cy in enumerate((y0 + 26 + pit / 2, y0 + 26 + pit + row_gap + pit / 2)):
        for i in range(6):
            cx = px0 + i * (pit + gap) + pit / 2
            c.setFillColor(LIGHT)
            c.circle(cx, cy, pit / 2, stroke=1, fill=1)
            c.setFillColor(MID)
            c.setFont("Helvetica", 8)
            num = (6 - i) if r_i == 1 else (i + 1)
            c.drawCentredString(cx, cy - 3, str(num))
    c.setFillColor(black)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(size[0] / 2, y0 - 22, "Sit on the long sides. Sow counter-clockwise, one seed per pit, into your own store but never your opponent's.")
    c.drawCentredString(size[0] / 2, y0 - 36, "Last seed in your store: play again. Last seed in an empty pit on your side: capture it together with the seeds in the pit opposite.")
    c.drawCentredString(size[0] / 2, y0 - 50, "The game ends when one side is empty; the other player keeps the seeds left on their side. Most seeds in the store wins.")
    c.showPage()
    c.save()
    return path


def ludo() -> Path:
    c, path = new_canvas("ludo", "ludo-board.pdf", "Ludo board (simplified)")
    top = header(c, "Ludo board", "Simplified 15 x 15 cross. Numbers mark each player's yard, start square and home column. Stars are safe squares.")
    cell = 31
    n = 15
    x0 = MARGIN + (letter[0] - 2 * MARGIN - n * cell) / 2
    y0 = top - 8 - n * cell

    def cxy(col, row):
        return x0 + col * cell + cell / 2, y0 + row * cell + cell / 2

    # loop squares (52) drawn as a grid of cells on the cross arms
    arms = []
    for col in range(n):
        for row in range(n):
            if 6 <= col <= 8 or 6 <= row <= 8:
                arms.append((col, row))
    homes = {
        1: [(7, r) for r in range(1, 6)],
        2: [(cc, 7) for cc in range(1, 6)],
        3: [(7, r) for r in range(9, 14)],
        4: [(cc, 7) for cc in range(9, 14)],
    }
    starts = {1: (6, 1), 2: (1, 8), 3: (8, 13), 4: (13, 6)}
    safe = [(2, 6), (6, 12), (12, 8), (8, 2)]
    yards = {1: (0, 0), 2: (0, 9), 3: (9, 9), 4: (9, 0)}

    c.setLineWidth(0.7)
    for (col, row) in arms:
        if 6 <= col <= 8 and 6 <= row <= 8:
            continue
        shade = None
        label = ""
        for p, cells in homes.items():
            if (col, row) in cells:
                shade, label = LIGHT, str(p)
        for p, s in starts.items():
            if (col, row) == s:
                shade, label = GREY, str(p)
        if shade:
            c.setFillColor(shade)
            c.rect(x0 + col * cell, y0 + row * cell, cell, cell, stroke=1, fill=1)
        else:
            c.rect(x0 + col * cell, y0 + row * cell, cell, cell, stroke=1, fill=0)
        if label:
            c.setFillColor(black)
            c.setFont("Helvetica-Bold", 10)
            cx, cy = cxy(col, row)
            c.drawCentredString(cx, cy - 3.5, label)
    # safe squares: star
    c.setFont("Helvetica-Bold", 13)
    for (col, row) in safe + list(starts.values()):
        cx, cy = cxy(col, row)
        if (col, row) in starts.values():
            c.drawCentredString(cx + 10, cy + 6, "*")
        else:
            c.drawCentredString(cx, cy - 4.5, "*")
    # centre home
    cx, cy = x0 + 7.5 * cell, y0 + 7.5 * cell
    h = 1.5 * cell
    c.setLineWidth(1.2)
    c.rect(cx - h, cy - h, 2 * h, 2 * h, stroke=1, fill=0)
    c.line(cx - h, cy - h, cx + h, cy + h)
    c.line(cx - h, cy + h, cx + h, cy - h)
    c.setFillColor(LIGHT)
    for tri in (((cx - h, cy - h), (cx + h, cy - h), (cx, cy)), ((cx - h, cy + h), (cx + h, cy + h), (cx, cy))):
        p = c.beginPath()
        p.moveTo(*tri[0]); p.lineTo(*tri[1]); p.lineTo(*tri[2]); p.close()
        c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(white)
    c.rect(cx - 17, cy - 6, 34, 12, stroke=0, fill=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(cx, cy - 3, "HOME")
    # yards
    for p, (col, row) in yards.items():
        yx, yy = x0 + col * cell, y0 + row * cell
        c.setFillColor(LIGHT)
        c.setLineWidth(1.2)
        c.rect(yx, yy, 6 * cell, 6 * cell, stroke=1, fill=1)
        c.setFillColor(white)
        c.roundRect(yx + cell, yy + cell, 4 * cell, 4 * cell, 10, stroke=1, fill=1)
        for (dx, dy) in ((2, 2), (4, 2), (2, 4), (4, 4)):
            c.circle(yx + dx * cell, yy + dy * cell, cell * 0.42, stroke=1, fill=1)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(yx + 3 * cell, yy + 3 * cell - 9, str(p))
    c.setLineWidth(1.4)
    c.rect(x0, y0, n * cell, n * cell, stroke=1, fill=0)
    # tokens
    y = y0 - 22
    cut_line(c, y + 6, MARGIN, letter[0] - MARGIN, "cut out the 16 tokens (4 per player) or use buttons")
    labels = [str(p) for p in (1, 2, 3, 4) for _ in range(4)]
    token_row(c, MARGIN, y - 12, 16, 11, (letter[0] - 2 * MARGIN) / 16, white, labels)
    c.showPage()
    c.save()
    return path


def snakes_and_ladders() -> Path:
    c, path = new_canvas("snakes-and-ladders", "snakes-and-ladders-board.pdf", "Snakes and ladders board")
    top = header(c, "Snakes and ladders", "100 squares, 8 ladders and 8 snakes. Roll one die; ladders take you up, snakes take you down. First to 100 wins.")
    cell = 48
    x0 = MARGIN + (letter[0] - 2 * MARGIN - 10 * cell) / 2
    y0 = top - 10 - 10 * cell

    def centre(num):
        r = (num - 1) // 10
        k = (num - 1) % 10
        col = k if r % 2 == 0 else 9 - k
        return x0 + col * cell + cell / 2, y0 + r * cell + cell / 2

    ladders = [(4, 14), (9, 31), (20, 38), (28, 84), (40, 59), (51, 67), (63, 81), (71, 91)]
    snakes = [(17, 7), (54, 34), (62, 19), (64, 60), (87, 24), (93, 73), (95, 75), (99, 78)]

    # shade ladder feet and snake heads lightly
    c.setFillColor(LIGHT)
    for a, b in ladders + snakes:
        cx, cy = centre(a)
        c.rect(cx - cell / 2, cy - cell / 2, cell, cell, stroke=0, fill=1)
    c.setFillColor(black)
    grid(c, x0, y0, 10, 10, cell, 0.7)
    c.setFont("Helvetica", 8)
    for num in range(1, 101):
        cx, cy = centre(num)
        c.drawString(cx - cell / 2 + 3, cy + cell / 2 - 10, str(num))

    import math
    # ladders: two rails and rungs
    c.setLineWidth(2)
    for a, b in ladders:
        (ax, ay), (bx, by) = centre(a), centre(b)
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * 5.5, dx / L * 5.5
        c.line(ax + nx, ay + ny, bx + nx, by + ny)
        c.line(ax - nx, ay - ny, bx - nx, by - ny)
        c.setLineWidth(1.2)
        steps = max(2, int(L / 13))
        for s in range(1, steps):
            t = s / steps
            px, py = ax + dx * t, ay + dy * t
            c.line(px + nx, py + ny, px - nx, py - ny)
        c.setLineWidth(2)
    # snakes: wavy bezier path from head (high number) to tail
    for a, b in snakes:
        (ax, ay), (bx, by) = centre(a), centre(b)
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        waves = max(2, int(L / 70))
        p = c.beginPath()
        p.moveTo(ax, ay)
        amp = 11
        for wv in range(waves):
            t0, t1 = wv / waves, (wv + 1) / waves
            sgn = 1 if wv % 2 == 0 else -1
            c1x = ax + dx * (t0 + (t1 - t0) / 3) + nx * amp * sgn
            c1y = ay + dy * (t0 + (t1 - t0) / 3) + ny * amp * sgn
            c2x = ax + dx * (t0 + 2 * (t1 - t0) / 3) + nx * amp * sgn
            c2y = ay + dy * (t0 + 2 * (t1 - t0) / 3) + ny * amp * sgn
            p.curveTo(c1x, c1y, c2x, c2y, ax + dx * t1, ay + dy * t1)
        c.setLineWidth(3.2)
        c.setStrokeColor(DARK)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(DARK)
        c.circle(ax, ay, 5.5, stroke=0, fill=1)  # head
        c.setFillColor(white)
        c.circle(ax - 1.6, ay + 1.6, 1.3, stroke=0, fill=1)  # eye
        c.setFillColor(black)
        c.setStrokeColor(black)
    c.setFont("Helvetica", 8.5)
    c.drawString(x0, y0 - 14, "Ladders: 4-14, 9-31, 20-38, 28-84, 40-59, 51-67, 63-81, 71-91.   Snakes: 17-7, 54-34, 62-19, 64-60, 87-24, 93-73, 95-75, 99-78.")
    c.showPage()
    c.save()
    return path


def yacht_score() -> Path:
    c, path = new_canvas("yacht", "yacht-score-sheet.pdf", "Yacht score sheet")
    top = header(c, "Yacht score sheet", "Five dice, up to three rolls a turn, twelve categories, each used once. Two sheets per page; cut along the dashed line.")
    cats = [
        ("Ones", "sum of the 1s"), ("Twos", "sum of the 2s"), ("Threes", "sum of the 3s"),
        ("Fours", "sum of the 4s"), ("Fives", "sum of the 5s"), ("Sixes", "sum of the 6s"),
        ("Full house", "3 + 2 of a kind: sum of all dice"), ("Four of a kind", "sum of the four dice"),
        ("Little straight", "1-2-3-4-5: 30 points"), ("Big straight", "2-3-4-5-6: 30 points"),
        ("Choice", "any dice: sum of all five"), ("Yacht", "five of a kind: 50 points"),
    ]
    width = letter[0] - 2 * MARGIN
    cat_w = 176
    players = 6
    col_w = (width - cat_w) / players
    row_h = 21.5
    rows = len(cats) + 2
    table_h = rows * row_h
    for t in range(2):
        y_top = top - 8 - t * (table_h + 34)
        y_bot = y_top - table_h
        c.setLineWidth(0.7)
        c.rect(MARGIN, y_bot, width, table_h, stroke=1, fill=0)
        c.setFillColor(LIGHT)
        c.rect(MARGIN, y_top - row_h, width, row_h, stroke=1, fill=1)
        c.rect(MARGIN, y_bot, width, row_h, stroke=1, fill=1)
        c.setFillColor(black)
        for i in range(1, rows):
            c.line(MARGIN, y_top - i * row_h, MARGIN + width, y_top - i * row_h)
        for p in range(players + 1):
            x = MARGIN + cat_w + p * col_w
            c.line(x, y_bot, x, y_top)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(MARGIN + 4, y_top - row_h + 7, "Category")
        for p in range(players):
            c.drawString(MARGIN + cat_w + p * col_w + 4, y_top - row_h + 7, f"Player {p + 1}")
        for i, (name, desc) in enumerate(cats):
            y = y_top - (i + 2) * row_h + 7
            c.setFont("Helvetica-Bold", 9)
            c.drawString(MARGIN + 4, y, name)
            c.setFont("Helvetica", 7.5)
            c.setFillColor(DARK)
            c.drawRightString(MARGIN + cat_w - 4, y, desc)
            c.setFillColor(black)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(MARGIN + 4, y_bot + 7, "TOTAL (maximum 297)")
        if t == 0:
            cut_line(c, y_bot - 17, MARGIN, MARGIN + width, "cut")
    c.showPage()
    c.save()
    return path


def farkle_score() -> Path:
    c, path = new_canvas("farkle", "farkle-score-sheet.pdf", "Farkle score sheet")
    top = header(c, "Farkle score sheet", "Six dice. Set aside scoring dice after every roll, then bank or roll on; nothing scoring is a farkle. Write each player's running total. First to 10,000 wins.")
    width = letter[0] - 2 * MARGIN
    # scoring box
    box_h = 112
    c.setLineWidth(0.8)
    c.setFillColor(LIGHT)
    c.rect(MARGIN, top - 8 - box_h, width, box_h, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(MARGIN + 8, top - 22, "Scoring (dice from one roll only)")
    left = [
        "Single 1 ............ 100", "Single 5 ............. 50",
        "Three 1s .......... 1,000", "Three 2s ............ 200",
        "Three 3s ............ 300", "Three 4s ............ 400",
        "Three 5s ............ 500", "Three 6s ............ 600",
    ]
    right = [
        "Four of a kind ........... 1,000", "Five of a kind ........... 2,000",
        "Six of a kind ............ 3,000", "Three pairs .............. 1,500",
        "Straight 1-2-3-4-5-6 ..... 2,500", "Boxed-game rules: three 1s 300,",
        "  straight 1,500, two triplets 2,500", "Agree house rules before you start",
    ]
    c.setFont("Courier", 8.2)
    for i, line in enumerate(left):
        c.drawString(MARGIN + 8, top - 36 - i * 10.5, line)
    for i, line in enumerate(right):
        c.drawString(MARGIN + width / 2 + 4, top - 36 - i * 10.5, line)
    # turn table
    players = 6
    turn_w = 34
    col_w = (width - turn_w) / players
    row_h = 17.5
    turns = 24
    y_top = top - 8 - box_h - 16
    y_bot = y_top - (turns + 1) * row_h
    c.setFillColor(LIGHT)
    c.rect(MARGIN, y_top - row_h, width, row_h, stroke=1, fill=1)
    c.setFillColor(black)
    c.rect(MARGIN, y_bot, width, (turns + 1) * row_h, stroke=1, fill=0)
    for i in range(1, turns + 1):
        c.setLineWidth(0.4 if i % 5 else 0.9)
        c.line(MARGIN, y_top - i * row_h, MARGIN + width, y_top - i * row_h)
    c.setLineWidth(0.7)
    for p in range(players + 1):
        x = MARGIN + turn_w + p * col_w
        c.line(x, y_bot, x, y_top)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN + 4, y_top - row_h + 5.5, "Turn")
    for p in range(players):
        c.drawString(MARGIN + turn_w + p * col_w + 4, y_top - row_h + 5.5, f"Player {p + 1}")
    c.setFont("Helvetica", 7.5)
    for i in range(turns):
        c.drawString(MARGIN + 4, y_top - (i + 2) * row_h + 5.5, str(i + 1))
    c.showPage()
    c.save()
    return path


def go_board() -> Path:
    c, path = new_canvas("go", "go-board-9x9.pdf", "Go board 9 x 9")
    top = header(c, "Go board, 9 x 9", "Beginner board. Stones go on the intersections, not in the squares. Black plays first.")
    spacing = 55
    n = 9
    size = (n - 1) * spacing
    x0 = MARGIN + (letter[0] - 2 * MARGIN - size) / 2
    y0 = top - 20 - size
    c.setLineWidth(1)
    for i in range(n):
        c.line(x0 + i * spacing, y0, x0 + i * spacing, y0 + size)
        c.line(x0, y0 + i * spacing, x0 + size, y0 + i * spacing)
    c.setLineWidth(2)
    c.rect(x0, y0, size, size, stroke=1, fill=0)
    c.setFillColor(black)
    for (i, j) in ((2, 2), (2, 6), (6, 2), (6, 6), (4, 4)):
        c.circle(x0 + i * spacing, y0 + j * spacing, 3.2, stroke=0, fill=1)
    c.setFont("Helvetica", 8)
    for i, f in enumerate("ABCDEFGHJ"):
        c.drawCentredString(x0 + i * spacing, y0 - 14, f)
    for j in range(n):
        c.drawRightString(x0 - 10, y0 + j * spacing - 3, str(j + 1))
    y = y0 - 34
    cut_line(c, y + 6, MARGIN, letter[0] - MARGIN, "cut out 40 black and 40 white stones, or use two kinds of buttons or coins")
    r = 10
    pitch = (letter[0] - 2 * MARGIN) / 20
    token_row(c, MARGIN, y - r - 2, 20, r, pitch, black)
    token_row(c, MARGIN, y - 3 * r - 6, 20, r, pitch, black)
    token_row(c, MARGIN, y - 5 * r - 10, 20, r, pitch, white)
    token_row(c, MARGIN, y - 7 * r - 14, 20, r, pitch, white)
    c.showPage()
    c.save()
    return path


def hangman() -> Path:
    c, path = new_canvas("hangman", "hangman-sheet.pdf", "Hangman sheet (6 games)")
    top = header(c, "Hangman", "Six games per page. Write one dash per letter, cross out letters as they are guessed, add one body part per wrong guess.")
    pw = (letter[0] - 2 * MARGIN - 24) / 2
    ph = 202
    for row in range(3):
        for col in range(2):
            x = MARGIN + col * (pw + 24)
            y = top - 6 - ph - row * (ph + 16)
            c.setLineWidth(0.6)
            c.setStrokeColor(MID)
            c.roundRect(x, y, pw, ph, 6, stroke=1, fill=0)
            c.setStrokeColor(black)
            # gallows
            gx, gy = x + 14, y + 40
            c.setLineWidth(2)
            c.line(gx, gy, gx + 54, gy)             # base
            c.line(gx + 12, gy, gx + 12, gy + 118)  # post
            c.line(gx + 12, gy + 118, gx + 58, gy + 118)  # beam
            c.line(gx + 58, gy + 118, gx + 58, gy + 104)  # rope
            c.setLineWidth(0.6)
            # word dashes
            c.setFont("Helvetica", 8)
            c.drawString(x + 90, y + ph - 18, "Word")
            for k in range(10):
                dx = x + 90 + k * 14
                c.line(dx, y + ph - 40, dx + 10, y + ph - 40)
            # alphabet
            c.setFont("Helvetica", 9.5)
            for k, letter_ in enumerate("ABCDEFGHIJKLM"):
                c.drawCentredString(x + 94 + k * 11.5, y + ph - 70, letter_)
            for k, letter_ in enumerate("NOPQRSTUVWXYZ"):
                c.drawCentredString(x + 94 + k * 11.5, y + ph - 88, letter_)
            c.setFont("Helvetica", 8)
            c.drawString(x + 90, y + ph - 112, "Wrong guesses (6 = out):")
            for k in range(6):
                c.rect(x + 90 + k * 16, y + ph - 130, 11, 11, stroke=1, fill=0)
            c.drawString(x + 90, y + 18, "Guesser: ________   Setter: ________")
    c.showPage()
    c.save()
    return path


def reversi() -> Path:
    c, path = new_canvas("reversi", "reversi-board.pdf", "Reversi board")
    top = header(c, "Reversi board", "8 x 8 board. Start with four discs in the centre, same colours on a diagonal. Dark plays first.")
    cell = 54
    x0 = MARGIN + (letter[0] - 2 * MARGIN - 8 * cell) / 2
    y0 = top - 8 - 8 * cell
    grid(c, x0, y0, 8, 8, cell, 0.8)
    c.setLineWidth(1.6)
    c.rect(x0, y0, 8 * cell, 8 * cell, stroke=1, fill=0)
    c.setFillColor(black)
    for (i, j) in ((2, 2), (2, 6), (6, 2), (6, 6)):
        c.circle(x0 + i * cell, y0 + j * cell, 2.8, stroke=0, fill=1)
    c.setFont("Helvetica", 8)
    for i, f in enumerate("abcdefgh"):
        c.drawCentredString(x0 + i * cell + cell / 2, y0 - 11, f)
    for j in range(8):
        c.drawRightString(x0 - 5, y0 + (7 - j) * cell + cell / 2 - 3, str(j + 1))
    y = y0 - 30
    cut_line(c, y + 6, MARGIN, letter[0] - MARGIN, "cut out 64 discs and colour one side black (or use 64 coins: heads and tails)")
    r = 12.5
    pitch = (letter[0] - 2 * MARGIN) / 16
    for k in range(4):
        token_row(c, MARGIN, y - r - 2 - k * (2 * r + 4), 16, r, pitch, white)
    c.showPage()
    c.save()
    return path


ALL = [checkers, chess, tic_tac_toe, dots_and_boxes, battleship, nine_mens_morris, mancala,
       ludo, snakes_and_ladders, yacht_score, farkle_score, go_board, hangman, reversi]


def main(argv: list[str]) -> int:
    wanted = set(argv[1:])
    for fn in ALL:
        if wanted and fn.__name__ not in wanted:
            continue
        path = fn()
        size_kb = path.stat().st_size / 1024
        flag = "" if size_kb < 100 else "   <-- OVER 100 KB"
        print(f"{path.relative_to(ROOT)}  {size_kb:.1f} KB{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
