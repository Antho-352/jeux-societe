// Rules-page covers in the site style (600×600 PNG), rendered with Playwright.
// Usage from the repo root: node scripts/covers/rules_covers.mjs [--all | slug slug …]
// Without --all, only rules files that have no `cover:` line get one (and the line is added).
// Each game has its own drawing in rules_art.mjs; FAMILY gives a fallback for a new page without one.
import fs from 'node:fs';
import path from 'node:path';
import { ART } from './rules_art.mjs';
import { BG, hash, fm, coverHtml, coverRenderer } from './cover_page.mjs';

const ROOT = process.cwd();
const DIR = path.join(ROOT, 'src/content/rules');
const OUT = path.join(ROOT, 'public/img/rules');
const all = process.argv.includes('--all');
const only = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const FAMILY = { card: 'war', board: 'checkers', dice: 'yacht', 'pen-and-paper': 'tic-tac-toe', tile: 'dominoes', party: 'cheat', drinking: 'kings-cup' };
const TAG = { card: 'Card game rules', board: 'Board game rules', dice: 'Dice game rules', 'pen-and-paper': 'Pen & paper game', tile: 'Tile game rules', party: 'Party game rules', drinking: 'Drinking game · 21+' };

const files = fs.readdirSync(DIR).filter((f) => f.endsWith('.md'));
const todo = only.length ? files.filter((f) => only.includes(f.replace(/\.md$/, ''))) : files.filter((f) => all || !/^cover:/m.test(fs.readFileSync(path.join(DIR, f), 'utf8')));
if (!todo.length) { console.log('No rules page without cover.'); process.exit(0); }
fs.mkdirSync(OUT, { recursive: true });
const r = await coverRenderer();
for (const f of todo) {
  const slug = f.replace(/\.md$/, '');
  const src = fs.readFileSync(path.join(DIR, f), 'utf8');
  const cat = fm(src, 'category') ?? 'board';
  if (!ART[slug]) console.warn(`no drawing for ${slug}, using the ${cat} fallback`);
  const art = (ART[slug] ?? ART[FAMILY[cat] ?? 'checkers'])();
  await r.shoot(coverHtml({ bg: BG[hash(slug) % BG.length], art, tag: TAG[cat] ?? 'Game rules', name: fm(src, 'game_name') ?? slug }), path.join(OUT, `${slug}.png`));
  if (!/^cover:/m.test(src)) fs.writeFileSync(path.join(DIR, f), src.replace(/^---\n/, `---\ncover: "/img/rules/${slug}.png"\n`));
  console.log('cover', slug, cat);
}
await r.close();
