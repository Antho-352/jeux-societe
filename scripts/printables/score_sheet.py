#!/usr/bin/env python3
"""Generate a clean one-page score sheet PDF for a classic card game.

Usage (run with ``python -I``):

    python -I scripts/printables/score_sheet.py --slug rummy
    python -I scripts/printables/score_sheet.py --slug hearts --preset hearts
    python -I scripts/printables/score_sheet.py --slug my-game --game "My game" \
        --columns "Player 1,Player 2,Player 3" --rows 20 --row-label "Hand"

Writes public/pdf/rules/<slug>/<slug>-score-sheet.pdf. US Letter page with
18 mm margins: the printed area also fits on A4 with margins of 15 mm or more.
Uses only the built-in Helvetica fonts so the file stays a few kilobytes.
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

SITE = "printandplaygame.com"
MARGIN = 18 * mm
PAGE_W, PAGE_H = letter
INK = colors.HexColor("#1f2a37")
RULE = colors.HexColor("#8a94a6")
LIGHT = colors.HexColor("#eef1f5")
ACCENT = colors.HexColor("#0f6e56")

# column spec: (label, relative width). The first column is the row label.
PRESETS: dict[str, dict] = {
    "rummy": dict(
        game="Rummy", row_label="Deal", rows=20,
        columns=[("Player 1", 1), ("Player 2", 1), ("Player 3", 1), ("Player 4", 1), ("Player 5", 1), ("Player 6", 1)],
        footer_rows=["Total"],
        note="Winner scores the cards left in every other hand: face cards 10, aces 1, number cards face value. Going rummy doubles the hand. Agree the target (100 or 200) before the first deal.",
    ),
    "gin-rummy": dict(
        game="Gin Rummy", row_label="Hand", rows=20,
        columns=[("Player A: points", 1), ("Player A: boxes", 0.6), ("Player B: points", 1), ("Player B: boxes", 0.6)],
        footer_rows=["Total points", "Game bonus (100, or 200 for a shutout)", "Box bonus (20 per hand won)", "Final score"],
        note="Knock: difference in deadwood. Undercut: difference + 10 to the opponent. Gin: 20 + opponent's deadwood. First to 100 points ends the game, then add the bonuses.",
    ),
    "canasta": dict(
        game="Canasta", row_label="Hand", rows=14,
        columns=[("We: bonuses", 1), ("We: cards", 1), ("We: in hand (−)", 1), ("We: running total", 1.1), ("They: bonuses", 1), ("They: cards", 1), ("They: in hand (−)", 1), ("They: running total", 1.1)],
        footer_rows=["Final"],
        note="Bonuses: natural canasta 500, mixed 300, red three 100 (all four 800), going out 100, concealed 200. Initial meld: 50 (0–1,495), 90 (1,500–2,995), 120 (3,000+). Game to 5,000.",
        landscape_hint=True,
    ),
    "hearts": dict(
        game="Hearts", row_label="Deal", rows=18,
        columns=[("Player 1", 1), ("Player 2", 1), ("Player 3", 1), ("Player 4", 1), ("Player 5", 1), ("Player 6", 1)],
        footer_rows=["Total"],
        note="Each heart 1 point, queen of spades 13. Shooting the moon: 0 for the shooter, 26 for everyone else. Lowest score wins when someone reaches 100. Pass: left, right, across, hold.",
    ),
    "spades": dict(
        game="Spades", row_label="Deal", rows=16,
        columns=[("Team 1: bid", 0.7), ("Team 1: tricks", 0.7), ("Team 1: score", 0.9), ("Team 1: bags", 0.7), ("Team 2: bid", 0.7), ("Team 2: tricks", 0.7), ("Team 2: score", 0.9), ("Team 2: bags", 0.7)],
        footer_rows=["Total"],
        note="Made contract: 10 per trick bid + 1 per bag. Failed: −10 per trick bid. Ten bags: −100. Nil ±100, blind nil ±200. Game to 500.",
    ),
    "euchre": dict(
        game="Euchre", row_label="Hand", rows=20,
        columns=[("Makers", 0.8), ("Us: points", 1), ("Us: total", 1), ("Them: points", 1), ("Them: total", 1)],
        footer_rows=["Game"],
        note="Makers take 3 or 4 tricks: 1 point. All 5 (march): 2. Alone and all 5: 4. Euchred: defenders score 2. First team to 10 wins.",
    ),
    "golf": dict(
        game="Golf", row_label="Hole", rows=18,
        columns=[("Player 1", 1), ("Player 2", 1), ("Player 3", 1), ("Player 4", 1), ("Player 5", 1), ("Player 6", 1)],
        footer_rows=["Total after 9", "Total after 18"],
        note="Ace 1, two −2, 3 to 10 face value, jack and queen 10, king 0. A pair in the same column scores 0. Lowest total after 9 (or 18) holes wins.",
    ),
    "thirty-one": dict(
        game="Thirty-One (Scat)", row_label="Round", rows=20,
        columns=[("Player 1", 1), ("Player 2", 1), ("Player 3", 1), ("Player 4", 1), ("Player 5", 1), ("Player 6", 1)],
        footer_rows=["Lives lost (3 = on the county)"],
        note="Mark one life lost (X) per round for the lowest hand; two for a knocker who is lowest. A declared 31 costs everyone else a life. Out after losing a life with none left.",
    ),
    "cribbage": dict(
        game="Cribbage", row_label="Hand", rows=14,
        columns=[("Player A: pegging", 0.9), ("Player A: hand", 0.8), ("Player A: crib", 0.8), ("Player A: total", 0.9), ("Player B: pegging", 0.9), ("Player B: hand", 0.8), ("Player B: crib", 0.8), ("Player B: total", 0.9)],
        footer_rows=["Game (121)"],
        note="No board needed: write each hand's pegging, hand and crib points and keep the running total. First to 121 wins; a loser below 91 is skunked.",
    ),
}


def draw_sheet(path: Path, game: str, row_label: str, columns: list[tuple[str, float]], rows: int,
               footer_rows: list[str], note: str = "") -> None:
    c = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle(f"{game} score sheet")
    c.setAuthor(SITE)
    c.setSubject(f"Printable {game} score sheet")

    x0, x1 = MARGIN, PAGE_W - MARGIN
    width = x1 - x0
    y = PAGE_H - MARGIN

    # Header
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(x0, y - 18, f"{game} score sheet")
    c.setFont("Helvetica", 9.5)
    c.setFillColor(RULE)
    c.drawRightString(x1, y - 18, SITE)
    y -= 30
    c.setFont("Helvetica", 10)
    c.setFillColor(INK)
    c.drawString(x0, y, "Date: ____________________")
    c.drawString(x0 + width * 0.45, y, "Players: " + "_" * 34)
    y -= 10
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.2)
    c.line(x0, y, x1, y)
    y -= 12

    # Table geometry
    # first column wide enough for the longest row label (footer labels can be long)
    longest = max([c.stringWidth(f"{row_label} {rows}", "Helvetica", 8.5)]
                  + [c.stringWidth(t, "Helvetica-Bold", 8.5) for t in footer_rows]) + 10
    label_abs = max(longest, width * 0.08)
    rel_sum = sum(w for _, w in columns)
    col_ws = [label_abs] + [(width - label_abs) * w / rel_sum for _, w in columns]
    header_h = 24
    n_rows = rows + len(footer_rows)
    note_h = 44 if note else 14
    avail = y - MARGIN - header_h - note_h
    row_h = max(13.5, min(20, avail / n_rows))

    # Header row
    c.setFillColor(LIGHT)
    c.rect(x0, y - header_h, width, header_h, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8.5)
    cx = x0
    for i, text in enumerate([row_label] + [t for t, _ in columns]):
        w = col_ws[i]
        # split "Team 1: bid" into two lines if a colon is present
        if ":" in text:
            a, b = text.split(":", 1)
            c.drawCentredString(cx + w / 2, y - 10, a.strip())
            c.setFont("Helvetica", 8)
            c.drawCentredString(cx + w / 2, y - 19.5, b.strip())
            c.setFont("Helvetica-Bold", 8.5)
        else:
            c.drawCentredString(cx + w / 2, y - 15, text)
        cx += w
    y -= header_h

    # Body rows
    c.setLineWidth(0.5)
    c.setStrokeColor(RULE)
    c.setFont("Helvetica", 8.5)
    for r in range(n_rows):
        top = y - r * row_h
        is_footer = r >= rows
        if is_footer:
            c.setFillColor(LIGHT)
            c.rect(x0, top - row_h, width, row_h, stroke=0, fill=1)
            label = footer_rows[r - rows]
            c.setFont("Helvetica-Bold", 8.5)
        else:
            label = f"{row_label} {r + 1}"
            c.setFont("Helvetica", 8.5)
        c.setFillColor(INK)
        c.drawString(x0 + 4, top - row_h + (row_h - 8.5) / 2 + 1, label)
        c.line(x0, top - row_h, x1, top - row_h)
    # Vertical lines
    bottom = y - n_rows * row_h
    cx = x0
    c.line(x0, y, x1, y)
    for w in col_ws:
        c.line(cx, y + header_h, cx, bottom)
        cx += w
    c.line(x1, y + header_h, x1, bottom)
    c.setLineWidth(1)
    c.rect(x0, bottom, width, n_rows * row_h + header_h, stroke=1, fill=0)

    # Note and footer
    yy = bottom - 12
    if note:
        c.setFont("Helvetica", 8.5)
        c.setFillColor(INK)
        for line in _wrap(c, note, "Helvetica", 8.5, width):
            c.drawString(x0, yy, line)
            yy -= 10.5
    c.setFont("Helvetica", 7.5)
    c.setFillColor(RULE)
    c.drawString(x0, MARGIN - 8, f"Free printable from {SITE} · rules at {SITE}/rules/ · for personal use")
    c.drawRightString(x1, MARGIN - 8, dt.date.today().isoformat())
    c.showPage()
    c.save()


def _wrap(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="rules page slug, also the output folder and file name")
    ap.add_argument("--preset", help="preset name (defaults to --slug when it matches a preset)")
    ap.add_argument("--game", help="game name printed in the title")
    ap.add_argument("--columns", help="comma-separated column labels (use 'Group: label' for two-line headers)")
    ap.add_argument("--rows", type=int, help="number of scoring rows")
    ap.add_argument("--row-label", default=None, help="label for the first column, e.g. Hand, Deal, Hole")
    ap.add_argument("--footer", help="comma-separated footer row labels (default: Total)")
    ap.add_argument("--note", default=None, help="one or two sentences printed under the table")
    ap.add_argument("--out-root", default="public/pdf/rules", help="output root (default public/pdf/rules)")
    args = ap.parse_args()

    preset = PRESETS.get(args.preset or args.slug, {})
    game = args.game or preset.get("game")
    if not game:
        ap.error("--game is required when no preset matches the slug")
    if args.columns:
        columns = [(t.strip(), 1.0) for t in args.columns.split(",") if t.strip()]
    else:
        columns = preset.get("columns") or [(f"Player {i}", 1.0) for i in range(1, 5)]
    rows = args.rows or preset.get("rows", 20)
    row_label = args.row_label or preset.get("row_label", "Hand")
    footer_rows = [t.strip() for t in args.footer.split(",")] if args.footer else preset.get("footer_rows", ["Total"])
    note = args.note if args.note is not None else preset.get("note", "")

    out_dir = Path(args.out_root) / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{args.slug}-score-sheet.pdf"
    draw_sheet(out, game, row_label, columns, rows, footer_rows, note)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
