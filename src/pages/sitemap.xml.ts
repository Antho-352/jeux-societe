import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { hubListing, THIN_THRESHOLD } from '../lib/hubs';
import { SITE_URL } from '../lib/seo';
import { creatorUrl, gameUrl, hubUrl, puzzleUrl, rulesUrl } from '../lib/taxonomy';

const fmt = (d: Date) => d.toISOString().slice(0, 10);

export const GET: APIRoute = async () => {
  const urls: { loc: string; lastmod?: string; priority: string }[] = [];
  const today = fmt(new Date());
  urls.push({ loc: '/', lastmod: today, priority: '1.0' });
  for (const p of ['/how-to-print/', '/about/', '/find-a-game/', '/creators/']) urls.push({ loc: p, lastmod: today, priority: '0.5' });

  const hubs = await getCollection('hubs');
  for (const hub of hubs) {
    const { items } = await hubListing(hub);
    if (items.length < Math.max(hub.data.min_items, THIN_THRESHOLD)) continue;
    const last = items.reduce((m, i) => Math.max(m, i.sortDate), 0);
    urls.push({ loc: hubUrl(hub.data.path), lastmod: last ? fmt(new Date(last)) : today, priority: hub.data.path.includes('/') ? '0.7' : '0.8' });
  }
  for (const g of await getCollection('games')) if (g.data.status === 'published') urls.push({ loc: gameUrl(g), lastmod: fmt(g.data.date_added), priority: '0.6' });
  for (const p of await getCollection('puzzles')) if (p.data.status === 'published') urls.push({ loc: puzzleUrl(p), lastmod: fmt(p.data.date_added), priority: '0.6' });
  for (const r of await getCollection('rules')) if (r.data.status === 'published') urls.push({ loc: rulesUrl(r), lastmod: fmt(r.data.date_added), priority: '0.6' });
  const games = await getCollection('games');
  for (const c of await getCollection('creators')) {
    const n = games.filter((g) => g.data.creator?.id === c.id && g.data.status === 'published').length;
    if (n >= 2) urls.push({ loc: creatorUrl(c.id), lastmod: today, priority: '0.4' });
  }

  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${SITE_URL}${u.loc}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}<priority>${u.priority}</priority></url>`)
    .join('\n')}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
