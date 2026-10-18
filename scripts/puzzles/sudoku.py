#!/usr/bin/env python3
"""Sudoku book generator with a uniqueness-checking backtracking solver.

    python3 -I scripts/puzzles/sudoku.py --difficulty hard --pages 10 --seed 1 \
        --title "Hard sudoku" --out out.pdf --cover out.png

Difficulties: easy (4 per page), medium / hard / expert (2 per page), kids4 (4x4, 6 per page),
kids6 (6x6, 4 per page). Every puzzle has exactly one solution; difficulty is set by the
number of clues and by whether the puzzle can be solved with singles only.
Solutions are printed on the last pages. Deterministic for a given seed.
"""
from __future__ import annotations

import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I drops the script dir
from common import GREY, INK, LIGHT, free_area, new_canvas, page_header, render_cover  # noqa: E402

# name: (box rows, box cols, target clues, per page, needs-singles-solvable, must-not-be-singles-solvable)
DIFFICULTY = {
    "easy": (3, 3, 38, 4, True, False),
    "medium": (3, 3, 32, 2, True, False),
    "hard": (3, 3, 27, 2, False, True),
    "expert": (3, 3, 24, 2, False, True),
    "kids4": (2, 2, 7, 6, True, False),
    "kids6": (2, 3, 16, 4, True, False),
}
LABEL = {"easy": "Easy", "medium": "Medium", "hard": "Hard", "expert": "Expert", "kids4": "4 × 4", "kids6": "6 × 6"}


class Board:
    def __init__(self, br, bc):
        self.br, self.bc = br, bc
        self.n = br * bc
        n = self.n
        self.full = (1 << n) - 1
        self.peers = []
        for i in range(n * n):
            r, c = divmod(i, n)
            b = (r // br) * bc + (c // bc)
            ps = set()
            for j in range(n * n):
                rj, cj = divmod(j, n)
                bj = (rj // br) * bc + (cj // bc)
                if j != i and (rj == r or cj == c or bj == b):
                    ps.add(j)
            self.peers.append(sorted(ps))

    # --- generic backtracking solver (MRV) -------------------------------
    def count_solutions(self, grid, limit=2, rng=None):
        n = self.n
        cand = [0] * (n * n)
        for i in range(n * n):
            if grid[i]:
                continue
            m = self.full
            for p in self.peers[i]:
                if grid[p]:
                    m &= ~(1 << (grid[p] - 1))
            cand[i] = m
        count = 0
        found = None

        def search():
            nonlocal count, found
            best, best_m = -1, None
            best_bits = n + 1
            for i in range(n * n):
                if grid[i]:
                    continue
                m = self.full
                for p in self.peers[i]:
                    if grid[p]:
                        m &= ~(1 << (grid[p] - 1))
                bits = bin(m).count("1")
                if bits == 0:
                    return
                if bits < best_bits:
                    best, best_m, best_bits = i, m, bits
                    if bits == 1:
                        break
            if best == -1:
                count += 1
                if found is None:
                    found = grid[:]
                return
            vals = [v for v in range(1, n + 1) if best_m >> (v - 1) & 1]
            if rng is not None:
                rng.shuffle(vals)
            for v in vals:
                grid[best] = v
                search()
                if count >= limit:
                    grid[best] = 0
                    return
            grid[best] = 0

        search()
        return count, found

    def random_full(self, rng):
        grid = [0] * (self.n * self.n)
        _, sol = self.count_solutions(grid, limit=1, rng=rng)
        return sol

    # --- singles-only solver (naked + hidden singles) --------------------
    def singles_solvable(self, grid):
        n = self.n
        g = grid[:]
        units = self._units()
        progress = True
        while progress:
            progress = False
            cands = {}
            for i in range(n * n):
                if g[i]:
                    continue
                m = self.full
                for p in self.peers[i]:
                    if g[p]:
                        m &= ~(1 << (g[p] - 1))
                if m == 0:
                    return False
                cands[i] = m
                if m & (m - 1) == 0:          # naked single
                    g[i] = m.bit_length()
                    progress = True
            if progress:
                continue
            for unit in units:                # hidden single
                for v in range(1, n + 1):
                    bit = 1 << (v - 1)
                    spots = [i for i in unit if not g[i] and cands.get(i, 0) & bit]
                    if len(spots) == 1 and not any(g[i] == v for i in unit):
                        g[spots[0]] = v
                        progress = True
        return all(g)

    def _units(self):
        n, br, bc = self.n, self.br, self.bc
        units = []
        for r in range(n):
            units.append([r * n + c for c in range(n)])
        for c in range(n):
            units.append([r * n + c for r in range(n)])
        for b in range(n):
            r0, c0 = (b // bc) * br, (b % bc) * bc
            units.append([(r0 + dr) * n + c0 + dc for dr in range(br) for dc in range(bc)])
        return units


def make_puzzle(board: Board, difficulty: str, rng: random.Random):
    _, _, target, _, need_singles, forbid_singles = DIFFICULTY[difficulty]
    n = board.n
    for attempt in range(60):
        sol = board.random_full(rng)
        puzzle = sol[:]
        cells = list(range(n * n))
        rng.shuffle(cells)
        clues = n * n
        for i in cells:
            if clues <= target:
                break
            saved = puzzle[i]
            puzzle[i] = 0
            cnt, _ = board.count_solutions(puzzle, limit=2)
            if cnt != 1:
                puzzle[i] = saved
            else:
                clues -= 1
        if clues > target + (2 if n == 9 else 1):
            continue
        singles = board.singles_solvable(puzzle)
        if need_singles and not singles:
            continue
        if forbid_singles and singles:
            continue
        return puzzle, sol, clues
    raise RuntimeError(f"could not reach the {difficulty} target")


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_grid(c, board: Board, grid, x, y_top, size, label=None, clues=None, bold_clues=True):
    n = board.n
    cell = size / n
    if label:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColorRGB(*GREY)
        c.drawString(x, y_top + 4, label)
    c.setStrokeColorRGB(*INK)
    for i in range(n + 1):
        c.setLineWidth(1.8 if i % board.br == 0 else 0.5)
        c.line(x, y_top - i * cell, x + size, y_top - i * cell)
        c.setLineWidth(1.8 if i % board.bc == 0 else 0.5)
        c.line(x + i * cell, y_top, x + i * cell, y_top - size)
    fs = cell * 0.55
    for i, v in enumerate(grid):
        if not v:
            continue
        r, col = divmod(i, n)
        is_clue = clues is None or clues[i]
        c.setFont("Helvetica-Bold" if (is_clue and bold_clues) else "Helvetica", fs)
        c.setFillColorRGB(*(INK if is_clue else (0.35, 0.35, 0.4)))
        c.drawCentredString(x + (col + 0.5) * cell, y_top - (r + 0.5) * cell - fs * 0.35, str(v))


def layout(count_per_page, box, n):
    """Return list of (x, y_top, size) slots for the puzzles on a page."""
    x0, y0, w, h = box
    if count_per_page == 1:
        cols, rows = 1, 1
    elif count_per_page == 2:
        cols, rows = 1, 2
    elif count_per_page == 4:
        cols, rows = 2, 2
    elif count_per_page == 6:
        cols, rows = (2, 3) if n == 4 else (3, 2)
    elif count_per_page == 9:
        cols, rows = 3, 3
    else:
        cols, rows = 4, -(-count_per_page // 4)
    label_h = 16
    gap_x, gap_y = 24, 22
    size = min((w - (cols - 1) * gap_x) / cols, (h - rows * label_h - (rows - 1) * gap_y) / rows)
    total_w = cols * size + (cols - 1) * gap_x
    total_h = rows * (size + label_h) + (rows - 1) * gap_y
    ox = x0 + (w - total_w) / 2
    oy = y0 + h - (h - total_h) / 2
    slots = []
    for i in range(count_per_page):
        col, row = i % cols, i // cols
        x = ox + col * (size + gap_x)
        y = oy - row * (size + label_h + gap_y) - label_h
        slots.append((x, y, size))
    return slots


def render_book(out_pdf, title, difficulty, pages, seed, per_page=None):
    br, bc, _, default_pp, _, _ = DIFFICULTY[difficulty]
    per_page = per_page or default_pp
    board = Board(br, bc)
    rng = random.Random(seed)
    total = pages * per_page
    puzzles = [make_puzzle(board, difficulty, rng) for _ in range(total)]
    n = board.n
    sol_pp = {4: 12, 6: 9, 9: 6}[n]
    sol_pages = -(-total // sol_pp)
    total_pages = pages + sol_pages
    rule = f"Fill every row, column and {br} × {bc} box with the numbers 1 to {n}."
    c = new_canvas(out_pdf, title, f"{LABEL[difficulty]} printable sudoku book")
    for p in range(pages):
        first = p * per_page
        top = page_header(c, title, f"Puzzles {first + 1}–{first + per_page} · {rule} Solutions from page {pages + 1}.", p + 1, total_pages)
        slots = layout(per_page, free_area(top), n)
        for k, (x, y, size) in enumerate(slots):
            idx = first + k
            if idx >= total:
                break
            puzzle, sol, clues = puzzles[idx]
            draw_grid(c, board, puzzle, x, y, size, label=f"Puzzle {idx + 1} · {clues} clues")
        c.showPage()
    for sp in range(sol_pages):
        first = sp * sol_pp
        top = page_header(c, f"{title} – solutions", f"Solutions {first + 1}–{min(total, first + sol_pp)}", pages + sp + 1, total_pages)
        slots = layout(sol_pp, free_area(top), n)
        for k, (x, y, size) in enumerate(slots):
            idx = first + k
            if idx >= total:
                break
            puzzle, sol, clues = puzzles[idx]
            draw_grid(c, board, sol, x, y, size, label=f"Puzzle {idx + 1}", clues=[bool(v) for v in puzzle])
        c.showPage()
    c.save()
    return total, total_pages


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--difficulty", choices=DIFFICULTY, default="easy")
    ap.add_argument("--pages", type=int, default=10)
    ap.add_argument("--per-page", type=int)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--title", default="Sudoku")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cover")
    a = ap.parse_args(argv)
    total, pages = render_book(a.out, a.title, a.difficulty, a.pages, a.seed, a.per_page)
    if a.cover:
        render_cover(a.out, a.cover)
    print(f"{a.out}: {total} puzzles, {pages} pages")


if __name__ == "__main__":
    main()
