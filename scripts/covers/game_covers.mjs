// Covers for game pages that have no picture we may use (link-only games: we never copy the publisher's box art).
// Usage from the repo root: node scripts/covers/game_covers.mjs [--all | slug slug …]
// Without --all, only game files with no `cover:` line get one (and the line is added); --all redraws every page
// whose cover is one of ours (cover_art: true), never a cover taken from a hosted PDF.
import fs from 'node:fs';
import path from 'node:path';
import { ART, GAME_ART, GAME_PICK } from './rules_art.mjs';
import { BG, hash, fm, coverHtml, coverRenderer } from './cover_page.mjs';

const ROOT = process.cwd();
const DIR = path.join(ROOT, 'src/content/games');
const OUT = path.join(ROOT, 'public/img/games');
const all = process.argv.includes('--all');
const only = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const TAG = { board: 'Board game', card: 'Card game', dice: 'Dice game', escape: 'Escape game', party: 'Party game', 'roll-and-write': 'Roll & write', 'scavenger-hunt': 'Scavenger hunt' };

const ours = (src) => !/^cover:/m.test(src) || /^cover_art: true/m.test(src);
const files = fs.readdirSync(DIR).filter((f) => f.endsWith('.md'));
const todo = files.filter((f) => {
  const src = fs.readFileSync(path.join(DIR, f), 'utf8');
  if (only.length) return only.includes(f.replace(/\.md$/, '')) && ours(src);
  return all ? ours(src) : !/^cover:/m.test(src);
});
if (!todo.length) { console.log('No game page to draw.'); process.exit(0); }
fs.mkdirSync(OUT, { recursive: true });
const r = await coverRenderer();
for (const f of todo) {
  const slug = f.replace(/\.md$/, '');
  let src = fs.readFileSync(path.join(DIR, f), 'utf8');
  const type = fm(src, 'type') ?? 'board';
  const [pick, acc] = GAME_PICK[slug] ?? [type];
  const draw = GAME_ART[pick] ?? ART[pick] ?? GAME_ART[type] ?? GAME_ART.board;
  await r.shoot(coverHtml({ bg: BG[hash(slug) % BG.length], art: draw(acc), tag: TAG[type] ?? 'Game', name: fm(src, 'title') ?? slug }), path.join(OUT, `${slug}.png`));
  if (!/^cover:/m.test(src)) {
    src = src.replace(/^---\n/, `---\ncover: "/img/games/${slug}.png"\ncover_art: true\n`);
    fs.writeFileSync(path.join(DIR, f), src);
  }
  console.log('cover', slug, pick, acc ?? '');
}
await r.close();
