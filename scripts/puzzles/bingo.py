#!/usr/bin/env python3
"""Bingo card generator: 1-75 number bingo, themed word bingo and blank templates.

    python3 -I scripts/puzzles/bingo.py --mode numbers --cards 20 --seed 1 --out out.pdf
    python3 -I scripts/puzzles/bingo.py --mode words --theme christmas --cards 20 --out out.pdf
    python3 -I scripts/puzzles/bingo.py --mode blank --size 5 --out out.pdf

Number and word sets: 2 unique 5x5 cards per page (FREE centre) followed by a call
sheet (number tracker, or cut-out calling cards for word bingo).
Blank templates: 3x3, 4x4 or 5x5 grids, one large card then smaller cards.
Deterministic for a given seed; vector only.
"""
from __future__ import annotations

import argparse
import os
import random
import sys

from reportlab.pdfbase.pdfmetrics import stringWidth

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I drops the script dir
from common import GREY, INK, LIGHT, MARGIN, PAGE_W, free_area, new_canvas, page_header, render_cover  # noqa: E402

THEMES: dict[str, list[str]] = {
    "christmas": ["Santa", "Reindeer", "Sleigh", "Elf", "Stocking", "Snowman", "Tinsel", "Wreath", "Carols", "Gifts",
                  "Mistletoe", "Candy cane", "Ornament", "Chimney", "Gingerbread", "Holly", "Star", "Angel", "Cookies",
                  "Jingle bells", "Eggnog", "Fireplace", "Snowflake", "Nutcracker", "Presents", "Rudolph", "North Pole",
                  "Garland", "Hot cocoa", "Ribbon", "Lights", "Advent", "Scrooge", "Ice skates", "Turkey", "Pudding"],
    "halloween": ["Pumpkin", "Ghost", "Witch", "Vampire", "Zombie", "Skeleton", "Spider", "Bat", "Candy", "Costume",
                  "Haunted house", "Cauldron", "Broomstick", "Mummy", "Werewolf", "Lantern", "Spooky", "Trick or treat",
                  "Cobweb", "Black cat", "Full moon", "Graveyard", "Scarecrow", "Potion", "Monster", "Owl", "Candy corn",
                  "Tombstone", "Fangs", "Goblin", "Mask", "Crow", "Frankenstein", "Wizard", "Apple bobbing", "Skull"],
    "thanksgiving": ["Turkey", "Pilgrim", "Harvest", "Gravy", "Stuffing", "Cranberry sauce", "Pumpkin pie", "Feast",
                     "Family", "Thankful", "Corn", "Autumn", "Parade", "Mayflower", "Cornucopia", "Mashed potatoes",
                     "Leaves", "Gratitude", "Football", "November", "Wishbone", "Pecan pie", "Sweet potato",
                     "Green beans", "Acorn", "Scarecrow", "Apple cider", "Hayride", "Squash", "Rolls", "Nap",
                     "Leftovers", "Casserole", "Pumpkin", "Gobble", "Blessing"],
    "easter": ["Bunny", "Egg hunt", "Basket", "Chick", "Lily", "Spring", "Jellybeans", "Lamb", "Tulip", "Nest",
               "Bonnet", "Carrot", "Chocolate egg", "Daffodil", "Parade", "Marshmallow", "Hop", "Sunday",
               "Painted eggs", "Butterfly", "Duckling", "Rainbow", "Grass", "Candy", "Church", "Brunch", "Ham",
               "Cross", "Flowers", "Pastel", "Hot cross bun", "Rabbit", "Garden", "Bloom", "Picnic", "Ribbon"],
    "valentines": ["Heart", "Love", "Cupid", "Roses", "Chocolate", "Card", "Arrow", "Hug", "Kiss", "Friend",
                   "Sweetheart", "Flowers", "Pink", "Red", "Candy hearts", "Romance", "Valentine", "Secret admirer",
                   "February", "Teddy bear", "Balloon", "Poem", "Date night", "Ribbon", "Lace", "Lollipop", "Crush",
                   "Smile", "Doves", "Dinner", "Letter", "Bouquet", "Ring", "Cake", "Glitter", "Be mine"],
    "classroom": ["Pencil", "Book", "Desk", "Teacher", "Ruler", "Eraser", "Crayon", "Glue", "Paper", "Lunch box",
                  "School bus", "Recess", "Homework", "Backpack", "Scissors", "Notebook", "Whiteboard", "Marker",
                  "Calculator", "Globe", "Library", "Computer", "Clock", "Chair", "Map", "Folder", "Stapler", "Chalk",
                  "Flag", "Playground", "Science", "Math", "Reading", "Art", "Music", "Principal"],
    "baby-shower": ["Diaper", "Bottle", "Pacifier", "Crib", "Stroller", "Rattle", "Onesie", "Bib", "Blanket", "Booties",
                    "Teddy bear", "Lullaby", "Bath tub", "Wipes", "Car seat", "Mobile", "Rocking chair", "Burp cloth",
                    "High chair", "Night light", "Nursery", "Monitor", "Swaddle", "Socks", "Hat", "Toys", "Book",
                    "Bouncer", "Changing table", "Thermometer", "Nail clippers", "Play mat", "Sippy cup",
                    "Hooded towel", "Mittens", "Stork"],
    "bridal-shower": ["Bride", "Groom", "Veil", "Bouquet", "Ring", "Vows", "Cake", "Honeymoon", "Champagne", "Dress",
                      "Garter", "Bridesmaid", "Best man", "First dance", "Toast", "Invitation", "Flowers", "Tuxedo",
                      "Love", "Kiss", "Candles", "Reception", "Aisle", "Confetti", "Limo", "Photos", "Registry",
                      "Something blue", "Tiara", "Rehearsal", "Diamond", "Father of the bride", "Flower girl",
                      "Ring bearer", "Proposal", "Forever"],
    "road-trip": ["Stop sign", "Gas station", "Red car", "Motorcycle", "School bus", "Cow", "Horse", "Bridge", "Tunnel",
                  "Train", "Rest area", "Police car", "Billboard", "Water tower", "Tractor", "Ambulance", "Camper",
                  "Bicycle", "Church", "Airplane", "Flag", "Traffic light", "Fire truck", "Boat", "Barn", "Windmill",
                  "Mailbox", "Speed limit", "Yellow car", "Dog in a car", "Hotel", "Exit sign", "Truck", "Lake",
                  "Mountain", "Taxi"],
}
THEME_TITLE = {
    "christmas": "Christmas Bingo", "halloween": "Halloween Bingo", "thanksgiving": "Thanksgiving Bingo",
    "easter": "Easter Bingo", "valentines": "Valentine's Bingo", "classroom": "Classroom Bingo",
    "baby-shower": "Baby Shower Bingo", "bridal-shower": "Bridal Shower Bingo", "road-trip": "Road Trip Bingo",
}
BINGO = "BINGO"


# ---------------------------------------------------------------------------
# Card content
# ---------------------------------------------------------------------------

def number_cards(count: int, rng: random.Random):
    cards, seen = [], set()
    while len(cards) < count:
        cols = []
        for i in range(5):
            lo = i * 15 + 1
            nums = rng.sample(range(lo, lo + 15), 5)
            cols.append(nums)
        cols[2][2] = None  # free centre
        key = tuple(tuple(c) for c in cols)
        if key in seen:
            continue
        seen.add(key)
        # grid[row][col]
        cards.append([[cols[c][r] for c in range(5)] for r in range(5)])
    return cards


def word_cards(words: list[str], count: int, rng: random.Random):
    if len(words) < 24:
        raise ValueError("need at least 24 words")
    cards, seen = [], set()
    while len(cards) < count:
        pick = rng.sample(words, 24)
        key = tuple(sorted(pick))
        if key in seen:
            continue
        seen.add(key)
        pick.insert(12, None)
        cards.append([pick[r * 5:(r + 1) * 5] for r in range(5)])
    return cards


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def wrap_text(text, font, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(c, text, cx, cy, w, h, font="Helvetica-Bold", max_size=15, min_size=6.5, colour=INK):
    """Draw text centred in a w x h box, shrinking and wrapping to fit."""
    size = max_size
    while size >= min_size:
        lines = wrap_text(text, font, size, w - 8)
        if all(stringWidth(l, font, size) <= w - 8 for l in lines) and len(lines) * size * 1.15 <= h - 6:
            break
        size -= 0.5
    c.setFont(font, size)
    c.setFillColorRGB(*colour)
    lh = size * 1.15
    total = lh * len(lines)
    y = cy + total / 2 - size * 0.95
    for line in lines:
        c.drawCentredString(cx, y, line)
        y -= lh


def draw_card(c, x, y_top, w, grid, header: str | None, cell_h, free_label="FREE", header_letters=False,
              blank=False, title_line=False):
    """Draw one bingo card with its top-left corner at (x, y_top). Returns the card height."""
    n = len(grid)
    cell_w = w / n
    head_h = cell_h * 0.62 if (header or header_letters) else 0
    total_h = head_h + cell_h * n + (18 if title_line else 0)
    y = y_top
    if title_line:
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(*GREY)
        c.drawString(x, y - 10, "Bingo · theme: ______________________   name: ______________")
        y -= 18
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.4)
    if head_h:
        c.setFillColorRGB(*INK)
        c.rect(x, y - head_h, w, head_h, stroke=1, fill=1)
        c.setFillColorRGB(1, 1, 1)
        if header_letters:
            c.setFont("Helvetica-Bold", head_h * 0.62)
            for i, ch in enumerate(BINGO):
                c.drawCentredString(x + (i + 0.5) * cell_w, y - head_h * 0.72, ch)
        else:
            c.setFont("Helvetica-Bold", head_h * 0.5)
            c.drawCentredString(x + w / 2, y - head_h * 0.68, header)
        y -= head_h
    # cells
    c.setLineWidth(0.9)
    c.setStrokeColorRGB(*INK)
    for r in range(n):
        for col in range(n):
            cx0 = x + col * cell_w
            cy0 = y - (r + 1) * cell_h
            c.setFillColorRGB(1, 1, 1)
            c.rect(cx0, cy0, cell_w, cell_h, stroke=1, fill=0)
            val = grid[r][col]
            if val is None:
                c.setFillColorRGB(0.93, 0.93, 0.94)
                c.rect(cx0 + 0.45, cy0 + 0.45, cell_w - 0.9, cell_h - 0.9, stroke=0, fill=1)
                if not blank:
                    fit_text(c, free_label, cx0 + cell_w / 2, cy0 + cell_h / 2, cell_w, cell_h, max_size=cell_h * 0.34)
                else:
                    fit_text(c, free_label, cx0 + cell_w / 2, cy0 + cell_h / 2, cell_w, cell_h, max_size=cell_h * 0.3,
                             colour=GREY)
            elif val != "":
                if isinstance(val, int):
                    fit_text(c, str(val), cx0 + cell_w / 2, cy0 + cell_h / 2, cell_w, cell_h, max_size=cell_h * 0.5)
                else:
                    fit_text(c, val, cx0 + cell_w / 2, cy0 + cell_h / 2, cell_w, cell_h, max_size=min(13, cell_h * 0.3))
    c.setLineWidth(1.6)
    c.rect(x, y - n * cell_h, w, n * cell_h, stroke=1, fill=0)
    return total_h


def cards_page(c, title, cards, page_no, total, header, header_letters, start_index):
    top = page_header(c, title, f"Cards {start_index + 1} and {start_index + 2} · each card is unique", page_no, total)
    x0, y0, w, h = free_area(top)
    card_w = 400
    gap = 20
    # two cards: each is a 12 pt label + header (0.62 cell) + 5 rows
    cell_h = min(54, (h - gap - 2 * 12) / (2 * 5.62))
    x = x0 + (w - card_w) / 2
    y = y0 + h
    for i, grid in enumerate(cards):
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(*GREY)
        c.drawRightString(x + card_w, y - 8, f"Card {start_index + i + 1}")
        used = draw_card(c, x, y - 12, card_w, grid, header, cell_h, header_letters=header_letters)
        y -= used + 12 + gap
    c.showPage()


def number_call_sheet(c, title, page_no, total):
    top = page_header(c, title + " – call sheet", "Cross off each number as you call it. Call the letter and the number, e.g. “B 7”.", page_no, total)
    x0, y0, w, h = free_area(top)
    cell = 30
    label_w = 40
    gx = x0 + (w - (label_w + 15 * cell)) / 2
    gy = y0 + h - 10
    c.setLineWidth(0.8)
    for r, letter in enumerate(BINGO):
        y = gy - r * cell
        c.setFillColorRGB(*INK)
        c.rect(gx, y - cell, label_w, cell, stroke=1, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(gx + label_w / 2, y - cell + 9, letter)
        c.setFillColorRGB(*INK)
        for i in range(15):
            x = gx + label_w + i * cell
            c.setStrokeColorRGB(*INK)
            c.rect(x, y - cell, cell, cell, stroke=1, fill=0)
            c.setFont("Helvetica", 11)
            c.drawCentredString(x + cell / 2, y - cell + 10, str(r * 15 + i + 1))
    y = gy - 5 * cell - 34
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x0, y, "How to play")
    c.setFont("Helvetica", 10)
    lines = [
        "1. Give each player one card and something to mark it with (pencil, counters, dry beans).",
        "2. The caller draws numbers at random from 1 to 75 (shuffled slips, an app, or a dice-free method of your choice)",
        "   and crosses each one off on this sheet so claims can be checked.",
        "3. Players mark matching numbers. The centre square is free.",
        "4. The first player to complete the agreed pattern shouts “Bingo!”. Check the card against the call sheet.",
    ]
    for i, line in enumerate(lines):
        c.drawString(x0, y - 16 - i * 14, line)
    y -= 16 + len(lines) * 14 + 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x0, y, "Winning patterns")
    patterns = [
        ("Any line", [(2, j) for j in range(5)]),
        ("Four corners", [(0, 0), (0, 4), (4, 0), (4, 4)]),
        ("Letter X", [(i, i) for i in range(5)] + [(i, 4 - i) for i in range(5)]),
        ("Full card", [(i, j) for i in range(5) for j in range(5)]),
    ]
    mini = 13
    px = x0
    for name, cells in patterns:
        py = y - 14
        for r in range(5):
            for col in range(5):
                c.setStrokeColorRGB(*GREY)
                c.setLineWidth(0.5)
                if (r, col) in cells:
                    c.setFillColorRGB(*INK)
                    c.rect(px + col * mini, py - (r + 1) * mini, mini, mini, stroke=1, fill=1)
                else:
                    c.rect(px + col * mini, py - (r + 1) * mini, mini, mini, stroke=1, fill=0)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 9)
        c.drawString(px, py - 5 * mini - 11, name)
        px += 5 * mini + 36
    c.showPage()


def word_call_sheet(c, title, words, page_no, total):
    top = page_header(c, title + " – calling cards", "Cut along the lines, fold the slips and draw them one at a time. Keep the drawn slips to check a winning card.", page_no, total)
    x0, y0, w, h = free_area(top)
    cols = 4
    rows = -(-len(words) // cols)
    cell_w = w / cols
    cell_h = min(52, (h - 10) / rows)
    gy = y0 + h - 6
    c.setLineWidth(0.6)
    c.setStrokeColorRGB(*GREY)
    c.setDash(3, 3)
    for i, word in enumerate(words):
        r, col = divmod(i, cols)
        x = x0 + col * cell_w
        y = gy - r * cell_h
        c.rect(x, y - cell_h, cell_w, cell_h, stroke=1, fill=0)
        fit_text(c, word, x + cell_w / 2, y - cell_h / 2, cell_w, cell_h, max_size=14)
    c.setDash()
    c.showPage()


def blank_pages(c, title, size, total_pages):
    free = size % 2 == 1 and size >= 5
    grid = [[None if (free and r == size // 2 and col == size // 2) else "" for col in range(size)] for r in range(size)]
    # page 1: one large card
    top = page_header(c, title, f"{size} × {size} blank card · write your own words, numbers or pictures in the squares", 1, total_pages)
    x0, y0, w, h = free_area(top)
    card_w = min(w, 430)
    cell_h = min(card_w / size, (h - 40) / (size + 0.62))
    card_w = cell_h * size
    draw_card(c, x0 + (w - card_w) / 2, y0 + h - 6, card_w, grid, "BINGO", cell_h, free_label="FREE", blank=True, title_line=True)
    c.showPage()
    # page 2: smaller cards
    per = 2 if size >= 4 else 4
    top = page_header(c, title, f"{per} cards per page · cut along the outer border", 2, total_pages)
    x0, y0, w, h = free_area(top)
    if per == 2:
        card_w = 330
        cell_h = min(card_w / size, (h - 2 * 30 - 20) / (2 * (size + 0.62)))
        card_w = cell_h * size
        y = y0 + h - 4
        for i in range(2):
            used = draw_card(c, x0 + (w - card_w) / 2, y, card_w, grid, "BINGO", cell_h, blank=True, title_line=True)
            y -= used + 22
    else:
        card_w = (w - 30) / 2
        cell_h = min(card_w / size, (h - 2 * 30 - 20) / (2 * (size + 0.62)))
        card_w = cell_h * size
        for i in range(4):
            col, row = i % 2, i // 2
            x = x0 + col * (card_w + 30) + (w - 2 * card_w - 30) / 2
            y = y0 + h - 4 - row * (cell_h * (size + 0.62) + 18 + 24)
            draw_card(c, x, y, card_w, grid, "BINGO", cell_h, blank=True, title_line=True)
    c.showPage()


# ---------------------------------------------------------------------------
# Books
# ---------------------------------------------------------------------------

def render_numbers(out_pdf, title, cards_n, seed):
    rng = random.Random(seed)
    cards = number_cards(cards_n, rng)
    pages = -(-cards_n // 2) + 1
    c = new_canvas(out_pdf, title, "Printable 1-75 bingo cards with call sheet")
    for p in range(0, cards_n, 2):
        cards_page(c, title, cards[p:p + 2], p // 2 + 1, pages, None, True, p)
    number_call_sheet(c, title, pages, pages)
    c.save()
    return pages


def render_words(out_pdf, title, theme, cards_n, seed, header=None):
    rng = random.Random(seed)
    words = THEMES[theme]
    cards = word_cards(words, cards_n, rng)
    pages = -(-cards_n // 2) + 1
    c = new_canvas(out_pdf, title, f"Printable {THEME_TITLE[theme].lower()} cards with calling cards")
    for p in range(0, cards_n, 2):
        cards_page(c, title, cards[p:p + 2], p // 2 + 1, pages, header or THEME_TITLE[theme], False, p)
    word_call_sheet(c, title, words, pages, pages)
    c.save()
    return pages


def render_blank(out_pdf, title, size):
    c = new_canvas(out_pdf, title, f"Blank {size}x{size} bingo card template")
    blank_pages(c, title, size, 2)
    c.save()
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["numbers", "words", "blank"], required=True)
    ap.add_argument("--theme", choices=THEMES)
    ap.add_argument("--cards", type=int, default=20)
    ap.add_argument("--size", type=int, default=5, choices=[3, 4, 5])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--title", default="Bingo")
    ap.add_argument("--header", help="text in the card header (word bingo)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cover")
    a = ap.parse_args(argv)
    if a.mode == "numbers":
        pages = render_numbers(a.out, a.title, a.cards, a.seed)
    elif a.mode == "words":
        pages = render_words(a.out, a.title, a.theme, a.cards, a.seed, a.header)
    else:
        pages = render_blank(a.out, a.title, a.size)
    if a.cover:
        render_cover(a.out, a.cover)
    print(f"{a.out}: {pages} pages")


if __name__ == "__main__":
    main()
