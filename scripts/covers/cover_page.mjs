// Shared 600×600 cover layout (illustration on a coloured ground, white name panel), rendered with Playwright.
import { createRequire } from 'node:module';
import { INK, CORAL } from './rules_art.mjs';
const require = createRequire(import.meta.url);

export const BG = ['#CFFF5E', '#B8D8FF', '#FFD9D2', '#FFE8A3', '#D9F2E6'];
export const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 0);
export const fm = (src, key) => (src.match(new RegExp(`^${key}:\\s*"?([^"\\n]*)"?`, 'm')) || [])[1];
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

export function coverHtml({ bg, art, tag, name }) {
  const size = name.length > 34 ? 34 : name.length > 22 ? 40 : name.length > 16 ? 46 : name.length > 11 ? 54 : 64;
  return `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,800,100,1&family=Outfit:wght@700&display=block" rel="stylesheet">
  <style>body{margin:0;width:600px;height:600px;background:${bg};position:relative;overflow:hidden;font-family:Outfit}
  .panel{position:absolute;left:20px;right:20px;bottom:20px;background:#fff;border:5px solid ${INK};border-radius:22px;padding:18px 26px 22px}
  .tag{font-weight:700;font-size:20px;letter-spacing:.06em;text-transform:uppercase;color:${CORAL}}
  .name{font-family:Fraunces;font-variation-settings:'SOFT' 100,'WONK' 1;font-weight:800;font-size:${size}px;line-height:1.02;color:${INK};letter-spacing:-.02em;margin-top:4px;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}</style></head>
  <body><svg width="600" height="420" viewBox="0 0 600 420" style="position:absolute;top:10px;left:0"><g transform="translate(300 215) scale(1.18) translate(-300 -205)">${art}</g></svg>
  <div class="panel"><div class="tag">${esc(tag)}</div><div class="name">${esc(name)}</div></div></body></html>`;
}

// Open a browser page sized for covers; returns { shoot(html, file), close() }.
export async function coverRenderer() {
  let chromium;
  try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(process.env.PW_PATH ?? 'playwright')); }
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 600, height: 600 } });
  return {
    async shoot(html, file) {
      await page.setContent(html, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: file });
    },
    close: () => browser.close(),
  };
}
