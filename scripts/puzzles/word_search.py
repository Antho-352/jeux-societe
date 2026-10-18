#!/usr/bin/env python3
"""Themed word-search generator.

    python3 -I scripts/puzzles/word_search.py --theme christmas --difficulty medium \
        --seed 3 --title "Christmas word search" --out out.pdf --cover out.png

Difficulty sets the grid and the directions:
  easy    10x10, words read forwards only (left to right, top to bottom)
  medium  15x15, four directions (across, down and both diagonals, never backwards)
  hard    20x20, all eight directions including backwards
Page 1: grid + word bank. Page 2: answer key with every word highlighted.
Every listed word appears exactly once in the grid. Deterministic for a given seed.
"""
from __future__ import annotations

import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I drops the script dir
from common import GREY, INK, LIGHT, free_area, new_canvas, page_header, render_cover  # noqa: E402

THEMES: dict[str, list[str]] = {
    "animals": ["Elephant", "Giraffe", "Tiger", "Lion", "Zebra", "Monkey", "Kangaroo", "Panda", "Rabbit", "Fox",
                "Wolf", "Bear", "Hippo", "Crocodile", "Penguin", "Dolphin", "Owl", "Squirrel"],
    "farm": ["Cow", "Pig", "Hen", "Duck", "Goat", "Sheep", "Horse", "Barn", "Hay", "Tractor", "Egg", "Corn",
             "Farmer", "Lamb", "Calf"],
    "ocean": ["Shark", "Whale", "Dolphin", "Octopus", "Coral", "Seahorse", "Jellyfish", "Crab", "Lobster",
              "Starfish", "Turtle", "Seaweed", "Clam", "Eel", "Stingray", "Wave", "Tide", "Reef"],
    "space": ["Planet", "Rocket", "Astronaut", "Moon", "Stars", "Galaxy", "Comet", "Orbit", "Saturn", "Jupiter",
              "Mars", "Earth", "Venus", "Meteor", "Telescope", "Gravity", "Nebula", "Shuttle"],
    "dinosaurs": ["T. rex", "Triceratops", "Stegosaurus", "Raptor", "Fossil", "Extinct", "Jurassic", "Pterodactyl",
                  "Herbivore", "Carnivore", "Skeleton", "Claws", "Teeth", "Eggs", "Volcano", "Brachiosaurus",
                  "Diplodocus", "Ankylosaurus"],
    "sports": ["Soccer", "Basketball", "Tennis", "Baseball", "Hockey", "Swimming", "Golf", "Rugby", "Cycling",
               "Skiing", "Boxing", "Volleyball", "Gymnastics", "Surfing", "Archery", "Cricket", "Running", "Football"],
    "food": ["Pizza", "Burger", "Salad", "Pasta", "Taco", "Sushi", "Sandwich", "Pancake", "Cheese", "Bread",
             "Apple", "Banana", "Carrot", "Soup", "Rice", "Noodles", "Yogurt", "Cookie", "Chicken", "Muffin"],
    "school": ["Pencil", "Book", "Desk", "Teacher", "Ruler", "Eraser", "Crayon", "Glue", "Paper", "Lunch", "Bus",
               "Class", "Math", "Read", "Bell"],
    "christmas": ["Santa", "Reindeer", "Sleigh", "Elf", "Stocking", "Snowman", "Tinsel", "Wreath", "Carols", "Gifts",
                  "Mistletoe", "Candy cane", "Ornament", "Chimney", "Gingerbread", "Holly", "Star", "Angel",
                  "Cookies", "Jingle"],
    "halloween": ["Pumpkin", "Ghost", "Witch", "Vampire", "Zombie", "Skeleton", "Spider", "Bat", "Candy", "Costume",
                  "Haunted", "Cauldron", "Broom", "Mummy", "Werewolf", "Lantern", "Spooky", "Trick", "Treat", "Cobweb"],
    "thanksgiving": ["Turkey", "Pilgrim", "Harvest", "Gravy", "Stuffing", "Cranberry", "Pumpkin pie", "Feast",
                     "Family", "Thankful", "Corn", "Autumn", "Parade", "Mayflower", "Cornucopia", "Potatoes",
                     "Leaves", "Gratitude", "Football", "November"],
    "easter": ["Bunny", "Egg", "Basket", "Chick", "Lily", "Hunt", "Spring", "Candy", "Lamb", "Tulip", "Hop", "Nest",
               "Bonnet", "Jellybean", "Carrot"],
    "valentines": ["Heart", "Love", "Cupid", "Roses", "Chocolate", "Card", "Arrow", "Hug", "Kiss", "Friend",
                   "Sweetheart", "Flowers", "Pink", "Red", "Candy", "Romance", "Valentine", "Secret", "Admirer",
                   "February"],
    "summer": ["Beach", "Sunshine", "Swimming", "Popsicle", "Sandcastle", "Vacation", "Lemonade", "Sunglasses",
               "Picnic", "Camping", "Watermelon", "Flip flops", "Surfing", "Barbecue", "Pool", "Seashell", "Hammock",
               "July", "Fireflies", "Ice cream"],
    "winter": ["Snowflake", "Mittens", "Scarf", "Icicle", "Sledding", "Frost", "Blizzard", "Hot cocoa", "Snowman",
               "Skating", "Fireplace", "January", "Snowball", "Boots", "Chilly", "Igloo", "Penguin", "Skiing",
               "Sweater", "Freeze"],
    "weather": ["Rain", "Snow", "Sunny", "Cloud", "Wind", "Storm", "Fog", "Hail", "Thunder", "Rainbow", "Sleet",
                "Hot", "Cold", "Breeze", "Ice"],
    "colours": ["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Brown", "Black", "White", "Gray",
                "Gold", "Silver", "Teal", "Violet"],
    "body": ["Head", "Shoulder", "Knee", "Toes", "Elbow", "Finger", "Stomach", "Heart", "Lungs", "Brain", "Skeleton",
             "Muscle", "Ankle", "Wrist", "Tongue", "Eyebrow", "Ear", "Nose", "Neck", "Thumb"],
    "transport": ["Car", "Bus", "Train", "Boat", "Plane", "Bike", "Truck", "Taxi", "Ship", "Subway", "Scooter",
                  "Tram", "Ferry", "Rocket", "Van"],
    "music": ["Guitar", "Piano", "Drums", "Violin", "Trumpet", "Flute", "Melody", "Rhythm", "Chorus", "Singer",
              "Orchestra", "Concert", "Tempo", "Harmony", "Banjo", "Cello", "Lyrics", "Notes", "Saxophone", "Clarinet"],
    "countries": ["Australia", "Brazil", "Canada", "China", "Egypt", "France", "Germany", "India", "Italy", "Japan",
                  "Kenya", "Mexico", "Norway", "Portugal", "Spain", "Sweden", "Thailand", "Turkey", "Argentina",
                  "Switzerland"],
    "science": ["Molecule", "Gravity", "Experiment", "Hypothesis", "Microscope", "Chemistry", "Biology", "Physics",
                "Electron", "Photosynthesis", "Evolution", "Atom", "Energy", "Magnet", "Ecosystem", "Laboratory",
                "Volcano", "Telescope", "Genetics", "Velocity"],
    "math": ["Addition", "Subtract", "Multiply", "Divide", "Fraction", "Decimal", "Angle", "Triangle", "Equation",
             "Number", "Graph", "Perimeter", "Area", "Sum", "Product", "Digit", "Even", "Odd", "Measure", "Geometry"],
    "sight-words": ["The", "And", "You", "Said", "Like", "Look", "Can", "See", "Play", "Come", "Here", "Little", "Big",
                    "Run", "Jump"],
    "big-words": ["Serendipity", "Ephemeral", "Ubiquitous", "Melancholy", "Quintessential", "Labyrinth", "Cacophony",
                  "Euphoria", "Nostalgia", "Resilience", "Eloquent", "Paradox", "Juxtapose", "Benevolent", "Zephyr",
                  "Luminous", "Perseverance", "Enigmatic", "Solitude", "Metamorphosis"],
}

DIFFICULTY = {
    "easy": (10, [(1, 0), (0, 1)], "Words read left to right or top to bottom."),
    "medium": (15, [(1, 0), (0, 1), (1, 1), (1, -1)], "Words run across, down and diagonally, never backwards."),
    "hard": (20, [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)],
             "Words run in all eight directions, including backwards."),
}
ALL_DIRS = DIFFICULTY["hard"][1]
HIGHLIGHT = (0.70, 0.84, 1.0)


def letters(word: str) -> str:
    return "".join(ch for ch in word.upper() if ch.isalpha())


def count_occurrences(grid, word):
    n = len(grid)
    L = len(word)
    total = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] != word[0]:
                continue
            for dc, dr in ALL_DIRS:
                er, ec = r + dr * (L - 1), c + dc * (L - 1)
                if not (0 <= er < n and 0 <= ec < n):
                    continue
                if all(grid[r + dr * i][c + dc * i] == word[i] for i in range(L)):
                    total += 1
    return total


def place_words(words, n, dirs, rng: random.Random):
    """Return (grid, placements) or None. placements: word -> (c, r, dc, dr)."""
    grid = [[None] * n for _ in range(n)]
    placements = {}
    order = sorted(words, key=len, reverse=True)
    for w in order:
        L = len(w)
        options = []
        for dc, dr in dirs:
            for r in range(n):
                for c in range(n):
                    er, ec = r + dr * (L - 1), c + dc * (L - 1)
                    if not (0 <= er < n and 0 <= ec < n):
                        continue
                    overlap, ok = 0, True
                    for i in range(L):
                        cell = grid[r + dr * i][c + dc * i]
                        if cell is None:
                            continue
                        if cell != w[i]:
                            ok = False
                            break
                        overlap += 1
                    if ok and overlap < L:
                        options.append((c, r, dc, dr, overlap))
        if not options:
            return None
        # mild preference for crossings, which makes the grid denser and harder to scan
        weights = [1 + 2 * o[4] for o in options]
        c, r, dc, dr, _ = rng.choices(options, weights=weights, k=1)[0]
        for i in range(L):
            grid[r + dr * i][c + dc * i] = w[i]
        placements[w] = (c, r, dc, dr)
    return grid, placements


def fill_grid(grid, words, rng: random.Random, max_tries=60):
    n = len(grid)
    blanks = [(r, c) for r in range(n) for c in range(n) if grid[r][c] is None]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(max_tries):
        for r, c in blanks:
            grid[r][c] = rng.choice(alphabet)
        if all(count_occurrences(grid, w) == 1 for w in words):
            return True
    return False


def generate(theme_words, difficulty, seed):
    n, dirs, _ = DIFFICULTY[difficulty]
    words = [letters(w) for w in theme_words]
    for w in words:
        if len(w) > n:
            raise ValueError(f"'{w}' is longer than the {n}x{n} grid")
    for attempt in range(400):
        rng = random.Random(seed * 10007 + attempt)
        res = place_words(words, n, dirs, rng)
        if res is None:
            continue
        grid, placements = res
        if fill_grid(grid, words, rng):
            return grid, placements
    raise RuntimeError("could not build the grid; shorten the word list")


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def _bank_layout(display_words, width):
    cols = 4 if len(display_words) > 12 else 3
    rows = -(-len(display_words) // cols)
    line_h = 14.5
    return cols, rows, line_h, rows * line_h + 26


def draw_puzzle(c, grid, display_words, box, placements=None, show_bank=True):
    x0, y0, w, h = box
    n = len(grid)
    cols, rows, line_h, bank_h = _bank_layout(display_words, w) if show_bank else (0, 0, 0, 0)
    gap = 18 if show_bank else 0
    cell = min(w / n, (h - bank_h - gap) / n)
    gw = cell * n
    gx = x0 + (w - gw) / 2
    gy_top = y0 + h
    # highlights (answer key)
    if placements:
        c.saveState()
        c.setStrokeColorRGB(*HIGHLIGHT)
        c.setLineWidth(cell * 0.72)
        c.setLineCap(1)
        c.setStrokeAlpha(0.75)
        for word, (sc, sr, dc, dr) in placements.items():
            L = len(word)
            ax = gx + (sc + 0.5) * cell
            ay = gy_top - (sr + 0.5) * cell
            bx = gx + (sc + dc * (L - 1) + 0.5) * cell
            by = gy_top - (sr + dr * (L - 1) + 0.5) * cell
            c.line(ax, ay, bx, by)
        c.restoreState()
    # grid lines
    c.saveState()
    c.setStrokeColorRGB(*LIGHT)
    c.setLineWidth(0.4)
    for i in range(n + 1):
        c.line(gx, gy_top - i * cell, gx + gw, gy_top - i * cell)
        c.line(gx + i * cell, gy_top, gx + i * cell, gy_top - gw)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.2)
    c.rect(gx, gy_top - gw, gw, gw, stroke=1, fill=0)
    c.restoreState()
    # letters
    fs = cell * 0.52
    c.setFont("Helvetica", fs)
    c.setFillColorRGB(*INK)
    for r in range(n):
        for col in range(n):
            c.drawCentredString(gx + (col + 0.5) * cell, gy_top - (r + 0.5) * cell - fs * 0.35, grid[r][col])
    if not show_bank:
        return
    # word bank
    by = gy_top - gw - gap
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x0, by - 10, f"Word list ({len(display_words)} words)")
    c.setStrokeColorRGB(*LIGHT)
    c.setLineWidth(0.6)
    c.line(x0, by - 15, x0 + w, by - 15)
    c.setFont("Helvetica", 10.5)
    colw = w / cols
    for i, word in enumerate(display_words):
        col, row = i % cols, i // cols
        c.drawString(x0 + col * colw + 2, by - 30 - row * line_h, word)


def render_pdf(grid, placements, display_words, out_pdf, title, difficulty, intro=None):
    n, _, rule = DIFFICULTY[difficulty]
    label = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}[difficulty]
    intro = intro or f"{label} · {n} × {n} grid · {len(display_words)} words. {rule}"
    c = new_canvas(out_pdf, title, f"{label} printable word search")
    top = page_header(c, title, intro, 1, 2)
    draw_puzzle(c, grid, display_words, free_area(top))
    c.showPage()
    top = page_header(c, f"{title} – answer key", "Each word is highlighted in the grid.", 2, 2)
    draw_puzzle(c, grid, display_words, free_area(top), placements=placements)
    c.showPage()
    c.save()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--theme", choices=THEMES)
    ap.add_argument("--words", help="comma-separated custom list instead of a theme")
    ap.add_argument("--difficulty", choices=DIFFICULTY, default="medium")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--title", default="Word search")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cover")
    a = ap.parse_args(argv)
    words = [w.strip() for w in a.words.split(",")] if a.words else THEMES[a.theme]
    grid, placements = generate(words, a.difficulty, a.seed)
    render_pdf(grid, placements, words, a.out, a.title, a.difficulty)
    if a.cover:
        render_cover(a.out, a.cover)
    print(f"{a.out}: {len(grid)}x{len(grid)}, {len(words)} words")


if __name__ == "__main__":
    main()
