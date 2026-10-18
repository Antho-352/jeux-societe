# Content guide (for every page writer, human or agent)

Site: printandplaygame.com, Astro static site. English first; French under /fr/ comes later.
Design and SEO decisions live in docs/06, 08, 09, 10, 11. This file is the practical checklist.

## Golden rules
1. **Verify, never invent.** Players, age, time, designer, publisher, year, licence: check the source page (creator site, BoardGameGeek via api.geekdo.com, publisher rulebook, pagat.com for traditional card games, Wikipedia as a secondary source). If you cannot verify a value, leave the field out. Never write fake reviews, fake download counts or fake quotes.
2. **One page = one keyword intent.** Before writing, grep `data/kw/keywords-master.csv` for the game or puzzle name (`grep -i "go fish" data/kw/keywords-master.csv`). Use the highest-volume natural phrasing in `seo_title` (≤ 60 characters) and the H1, and the 2 or 3 variants in the first paragraph and headings. Do not stuff.
3. **Write for a person.** Short paragraphs (2–4 sentences), plain words, no filler ("In today's fast-paced world…"), no hype adjectives. Explain jargon once in brackets the first time (e.g. "trick-taking (each round, the highest card wins the cards played)").
4. **Credit and licence.** Designer, artist, publisher and the exact licence wording. `hosting_mode: mirror` only if the licence is Creative Commons / public domain or the catalogue says "rehosting_allowed: yes". Otherwise `link` and `download_url` is omitted (the button goes to `source_url`). If the publisher offers separate files (rules PDF and print-and-play PDF, or tiles plus a rulebook), list every file in `files`. One `download_url` is not enough.
5. **Mark your work.** Put `<!-- hand-edited -->` as the first line of the body once a human-quality text is in place; the import script then never overwrites the file.
6. **Publish only complete pages.** `status: published` needs: verified metadata, a summary (≤ 220 chars, one sentence, no trailing clause), a body of at least 150 words with the sections below, and for mirror games a working `download_url` under /pdf/.

## Game page body (src/content/games/<slug>.md)
```
<!-- hand-edited -->
## About <title>
2 paragraphs: what the game is, what makes it worth printing, who it is for. Mention the designer by name.

## How to play in one minute
A 3–6 step numbered list: setup, a turn, how it ends, how you win.

## What's in the PDF
Bullet list of the components in the file (cards, boards, rules, score sheets) and the printing notes (pages, colour or B&W, duplex, paper).
```
Frontmatter fields: see src/content.config.ts. `summary` is shown on cards and in meta descriptions. `themes`, `mechanics` are lowercase slugs (`social-deduction`, `pirates`). `occasions` only from the allowed list. `cover`: path to a PNG/JPG under /img/games/ (render page 1 of a mirrored PDF with pypdfium2 at 600 px square, crop to square; never copy a publisher's cover image for link-only games).

## Rules page body (src/content/rules/<slug>.md)
```
<!-- hand-edited -->
## What you need
## Setup
## How to play
(turn structure, with sub-headings if the game has phases)
## Scoring and winning
## Common variants
## Tips for first games
## Frequently asked questions (3–5 `**Q?**` lines followed by the answer)
```
400–900 words. `sources` must list at least two of the pages you actually read. `public_domain: true` only for traditional games with no trademark owner (checkers, rummy, dots and boxes…). Trademarked games (UNO, Yahtzee, Phase 10, Monopoly) get `trademark_note: "<Name> is a trademark of <owner>. This page describes the rules; the game itself is not for download."` and no printable.
Printables for public-domain games go in /public/pdf/rules/<slug>/ and are generated with reportlab (scripts/printables/); `printable` is the site path, `printable_label` the button text.

## Puzzle page body (src/content/puzzles/<slug>.md)
Generated puzzles (mazes, word search, bingo, sudoku) come from scripts/puzzles/. The body is 80–150 words: who the puzzle suits, what is on each page, one tip. `summary` one sentence. `cover` is a PNG render of page 1.

## Hubs (src/content/hubs/<path with __ for />.md)
A hub file is the whitelist: a listing URL exists only if its hub file exists. `lead` is 2–3 hand-written sentences that mention the facet (age, difficulty, occasion). `faq` 2–4 questions. Create a facet hub only when at least 8 items will match (docs/10).

## Checks before you finish
- `npx astro build` passes (run from the repo root).
- No duplicate slugs, titles or seo_titles across the collection you touched.
- Every external link opens; every `download_url` file exists.
