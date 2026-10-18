// Blog covers (1200×630 PNG, also used as og:image), rendered with Playwright in the site style.
// Usage from the repo root: node scripts/covers/blog_covers.mjs [slug …]   (default: posts whose cover file is missing)
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(process.env.PW_PATH ?? 'playwright')); }

const ROOT = process.cwd();
const DIR = path.join(ROOT, 'src/content/blog');
const OUT = path.join(ROOT, 'public/img/blog');
const BG = ['#CFFF5E', '#B8D8FF', '#FFD9D2', '#FFE8A3', '#D9F2E6'];
const LABEL = { guides: 'Guide', 'game-rules': 'Rules & tips', printables: 'Printables', holidays: 'Holidays', classroom: 'Classroom', 'game-night': 'Game night', 'best-of': 'Best of' };
const fm = (src, key) => (src.match(new RegExp(`^${key}:\\s*"?([^"\\n]*)"?`, 'm')) || [])[1];
const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 0);
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const only = process.argv.slice(2);
const files = fs.readdirSync(DIR).filter((f) => /\.mdx?$/.test(f));
const todo = files.filter((f) => { const slug = f.replace(/\.mdx?$/, ''); return only.length ? only.includes(slug) : !fs.existsSync(path.join(OUT, `${slug}.png`)); });
if (!todo.length) { console.log('No cover to make.'); process.exit(0); }
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
for (const f of todo) {
  const slug = f.replace(/\.mdx?$/, '');
  const src = fs.readFileSync(path.join(DIR, f), 'utf8');
  const title = (fm(src, 'title') ?? slug).split(':')[0];
  const sub = (fm(src, 'title') ?? '').split(':').slice(1).join(':').trim();
  const emoji = fm(src, 'cover_emoji') ?? '🎲';
  const cat = LABEL[fm(src, 'category')] ?? 'Blog';
  const bg = BG[hash(slug) % BG.length];
  const size = title.length > 34 ? 66 : title.length > 22 ? 78 : 92;
  const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,800,100,1&family=Outfit:wght@600;700&display=block" rel="stylesheet">
  <style>body{margin:0;width:1200px;height:630px;background:${bg};font-family:Outfit;color:#0F3D2E;position:relative;overflow:hidden}
  .card{position:absolute;left:56px;top:56px;bottom:56px;width:760px;background:#fff;border:6px solid #0F3D2E;border-radius:36px;box-shadow:14px 14px 0 #0F3D2E;padding:44px 48px;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box}
  .cat{font-weight:700;font-size:24px;letter-spacing:.08em;text-transform:uppercase;color:#FF6B57}
  h1{font-family:Fraunces;font-variation-settings:'SOFT' 100,'WONK' 1;font-weight:800;font-size:${size}px;line-height:1;margin:0;letter-spacing:-.02em}
  .sub{font-size:28px;font-weight:600;line-height:1.25;color:#4B5A54}
  .brand{font-family:Fraunces;font-weight:800;font-size:26px}
  .emoji{position:absolute;right:70px;top:50%;transform:translateY(-50%) rotate(8deg);font-size:230px;line-height:1}
  .dot{position:absolute;border-radius:50%;background:#0F3D2E;opacity:.9}</style></head>
  <body><div class="card"><div><div class="cat">${esc(cat)}</div><h1 style="margin-top:18px">${esc(title)}</h1>${sub ? `<p class="sub" style="margin:18px 0 0">${esc(sub)}</p>` : ''}</div><div class="brand">printandplaygame.com</div></div>
  <div class="emoji">${emoji}</div><span class="dot" style="width:26px;height:26px;right:120px;top:70px"></span><span class="dot" style="width:16px;height:16px;right:330px;bottom:80px"></span></body></html>`;
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, `${slug}.png`) });
  console.log('cover', slug);
}
await browser.close();
