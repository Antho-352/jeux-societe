// Rules-page covers in the site style (600×600 PNG), rendered with Playwright.
// Usage from the repo root: node scripts/covers/rules_covers.mjs [--all | slug slug …]
// Without --all, only rules files that have no `cover:` line get one (and the line is added).
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(process.env.PW_PATH ?? 'playwright')); }

const ROOT = process.cwd();
const DIR = path.join(ROOT, 'src/content/rules');
const OUT = path.join(ROOT, 'public/img/rules');
const all = process.argv.includes('--all');
const only = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const BG = ['#CFFF5E', '#B8D8FF', '#FFD9D2', '#FFE8A3', '#D9F2E6'];
const INK = '#0F3D2E', CORAL = '#FF6B57';

const fm = (src, key) => (src.match(new RegExp(`^${key}:\\s*"?([^"\\n]*)"?`, 'm')) || [])[1];
const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 0);

// Simple inline-SVG illustrations per family.
const art = {
  card: () => `<g>${[-18, 0, 18].map((r, i) => `<g transform="rotate(${r} 300 330)"><rect x="${245}" y="120" width="110" height="160" rx="12" fill="#fff" stroke="${INK}" stroke-width="5"/><text x="262" y="160" font-size="30" font-family="Fraunces" font-weight="800" fill="${i === 1 ? CORAL : INK}">${['A', 'K', '7'][i]}</text></g>`).join('')}</g>`,
  board: () => { let s = ''; for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) s += `<rect x="${190 + c * 37}" y="${90 + r * 37}" width="37" height="37" fill="${(r + c) % 2 ? INK : '#fff'}"/>`; return `<g><rect x="186" y="86" width="230" height="230" rx="8" fill="none" stroke="${INK}" stroke-width="6"/>${s}<circle cx="245" cy="182" r="14" fill="${CORAL}" stroke="#fff" stroke-width="3"/><circle cx="356" cy="219" r="14" fill="#fff" stroke="${INK}" stroke-width="4"/></g>`; },
  dice: () => { const die = (x, y, rot, pips) => `<g transform="rotate(${rot} ${x + 55} ${y + 55})"><rect x="${x}" y="${y}" width="110" height="110" rx="20" fill="#fff" stroke="${INK}" stroke-width="5"/>${pips.map(([a, b]) => `<circle cx="${x + a}" cy="${y + b}" r="10" fill="${INK}"/>`).join('')}</g>`; return die(170, 120, -12, [[30, 30], [55, 55], [80, 80]]) + die(320, 140, 10, [[30, 30], [80, 30], [30, 80], [80, 80], [55, 55]]); },
  'pen-and-paper': () => `<g stroke="${INK}" stroke-width="7" stroke-linecap="round"><line x1="255" y1="100" x2="255" y2="300"/><line x1="345" y1="100" x2="345" y2="300"/><line x1="190" y1="165" x2="410" y2="165"/><line x1="190" y1="235" x2="410" y2="235"/></g><g stroke="${CORAL}" stroke-width="9" stroke-linecap="round" fill="none"><line x1="205" y1="115" x2="240" y2="150"/><line x1="240" y1="115" x2="205" y2="150"/><circle cx="300" cy="200" r="22"/><line x1="360" y1="250" x2="395" y2="285"/><line x1="395" y1="250" x2="360" y2="285"/></g>`,
  tile: () => [0, 1, 2].map((i) => `<g transform="rotate(${-14 + i * 14} 300 230)"><rect x="${250}" y="${110}" width="100" height="190" rx="14" fill="#fff" stroke="${INK}" stroke-width="5"/><line x1="258" y1="205" x2="342" y2="205" stroke="${INK}" stroke-width="4"/><circle cx="300" cy="160" r="9" fill="${i === 1 ? CORAL : INK}"/><circle cx="280" cy="250" r="9" fill="${INK}"/><circle cx="320" cy="250" r="9" fill="${INK}"/></g>`).join(''),
  party: () => `<g>${[0, 1, 2].map((i) => `<circle cx="${220 + i * 80}" cy="${190 - (i % 2) * 30}" r="44" fill="${i === 1 ? CORAL : '#fff'}" stroke="${INK}" stroke-width="5"/><circle cx="${207 + i * 80}" cy="${180 - (i % 2) * 30}" r="6" fill="${INK}"/><circle cx="${233 + i * 80}" cy="${180 - (i % 2) * 30}" r="6" fill="${INK}"/><path d="M ${205 + i * 80} ${203 - (i % 2) * 30} q 15 14 30 0" stroke="${INK}" stroke-width="5" fill="none"/>`).join('')}</g>`,
};

const files = fs.readdirSync(DIR).filter((f) => f.endsWith('.md'));
const todo = only.length ? files.filter((f) => only.includes(f.replace(/\.md$/, ''))) : files.filter((f) => all || !/^cover:/m.test(fs.readFileSync(path.join(DIR, f), 'utf8')));
if (!todo.length) { console.log('No rules page without cover.'); process.exit(0); }
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 600, height: 600 } });
for (const f of todo) {
  const slug = f.replace(/\.md$/, '');
  const src = fs.readFileSync(path.join(DIR, f), 'utf8');
  const name = fm(src, 'game_name') ?? slug;
  const cat = fm(src, 'category') ?? 'board';
  const tag = { card: 'Card game rules', board: 'Board game rules', dice: 'Dice game rules', 'pen-and-paper': 'Pen & paper game', tile: 'Tile game rules', party: 'Party game rules' }[cat] ?? 'Game rules';
  const bg = BG[hash(slug) % BG.length];
  const size = name.length > 16 ? 44 : name.length > 11 ? 54 : 64;
  const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,800,100,1&family=Outfit:wght@700&display=block" rel="stylesheet">
  <style>body{margin:0;width:600px;height:600px;background:${bg};position:relative;overflow:hidden;font-family:Outfit}
  .panel{position:absolute;left:20px;right:20px;bottom:20px;background:#fff;border:5px solid ${INK};border-radius:22px;padding:18px 26px 22px}
  .tag{font-weight:700;font-size:20px;letter-spacing:.06em;text-transform:uppercase;color:${CORAL}}
  .name{font-family:Fraunces;font-variation-settings:'SOFT' 100,'WONK' 1;font-weight:800;font-size:${size}px;line-height:1.02;color:${INK};letter-spacing:-.02em;margin-top:4px}</style></head>
  <body><svg width="600" height="420" viewBox="0 0 600 420" style="position:absolute;top:10px;left:0"><g transform="translate(300 205) scale(1.4) translate(-300 -205)">${(art[cat] ?? art.board)()}</g></svg>
  <div class="panel"><div class="tag">${tag}</div><div class="name">${name.replace(/&/g, '&amp;')}</div></div></body></html>`;
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, `${slug}.png`) });
  if (!/^cover:/m.test(src)) fs.writeFileSync(path.join(DIR, f), src.replace(/^---\n/, `---\ncover: "/img/rules/${slug}.png"\n`));
  console.log('cover', slug, cat);
}
await browser.close();
