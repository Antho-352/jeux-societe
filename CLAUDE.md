# printandplaygame.com

Static Astro 7 site (English at `/`, French under `/fr/` later) that lists free printable games and puzzles.
Owner: Anthony (French speaker; talk to him in French, write site content in English unless the page is a French one).

## Commands
- `npm install` then `npm run build` (output in `dist/`), `npm run dev` for a local server, `npx astro preview --port 4321` to serve `dist/`.
- Python helpers run with `python3 -I` from the repo root: `scripts/import_games.py` (catalogue JSON → game drafts), `scripts/dfs.py` (DataForSEO, needs `DFS_LOGIN` / `DFS_PASS`), `scripts/puzzles/*.py` (puzzle generators), `scripts/printables/*.py` (boards and score sheets).

## Where things are
- `src/content.config.ts`: the five collections (games, rules, puzzles, creators, hubs) and their Zod schemas. A hub file is the whitelist for a listing URL (`src/content/hubs/<path with __ for />.md`).
- `src/lib/taxonomy.ts`: type → URL silo mapping, labels, age bands, filter matching. `src/lib/hubs.ts`: items for a hub (shared by the page and the sitemap). `src/lib/related.ts`: related-games scoring.
- `src/pages/[...path].astro` renders hubs and puzzle pages; `src/pages/[silo]/[slug].astro` game pages; `src/pages/rules/[slug].astro` rules; `src/pages/sitemap.xml.ts` the sitemap (noindex pages excluded).
- `src/styles/global.css`: design tokens (palette B3: ground #F7F5EE, ink #0F3D2E, primary #FF6B57, accent #CFFF5E, tint #B8D8FF; fonts Fraunces + Outfit). No Tailwind.
- `public/pdf/`: hosted PDFs (only when the licence allows); `public/img/`: covers; `downloads/`: raw catalogue downloads, git-ignored, untrusted.
- `docs/`: research and decisions (01 keywords … 12 Cloudflare deployment). `CONTENT-GUIDE.md`: the writing checklist every content page follows.

## Rules of the house
- Never host a PDF without a licence that allows it (CC, public domain) or written permission; otherwise `hosting_mode: link`.
- Never invent metadata, reviews or download counts. Verify on the source page or BoardGameGeek (api.geekdo.com JSON works; boardgamegeek.com HTML is behind Cloudflare).
- Facet pages are static URLs only when they are in the hub whitelist and have at least 4 items (docs/10); everything else is a client-side filter.
- Commit messages in French, no model names in commits.
