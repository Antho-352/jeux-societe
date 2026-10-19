import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { hubListing, THIN_THRESHOLD } from '../lib/hubs';
import { SITE_URL } from '../lib/seo';
import { creatorUrl, gameUrl, hubUrl, puzzleUrl, rulesUrl } from '../lib/taxonomy';
import { BLOG_CATEGORY_LABEL, blogCategoryUrl, livePosts, postUrl } from '../lib/blog';

const fmt = (d: Date) => d.toISOString().slice(0, 10);

export const GET: APIRoute = async () => {
  const urls: { loc: string; lastmod?: string; priority: string }[] = [];
  // lastmod must only move when the page really changes (Google ignores it otherwise): listings take the date of
  // their newest item, fixed pages have none.
  urls.push({ loc: '/', priority: '1.0' });
  for (const p of ['/how-to-print/', '/about/', '/find-a-game/', '/creators/', '/legal-notice/', '/privacy/']) urls.push({ loc: p, priority: '0.5' });

  const hubs = await getCollection('hubs');
  for (const hub of hubs) {
    const { items } = await hubListing(hub);
    if (items.length < Math.max(hub.data.min_items, THIN_THRESHOLD)) continue;
    const last = items.reduce((m, i) => Math.max(m, i.sortDate), 0);
    urls.push({ loc: hubUrl(hub.data.path), lastmod: last ? fmt(new Date(last)) : undefined, priority: hub.data.path.includes('/') ? '0.7' : '0.8' });
  }
  for (const g of await getCollection('games')) if (g.data.status === 'published') urls.push({ loc: gameUrl(g), lastmod: fmt(g.data.date_added), priority: '0.6' });
  for (const p of await getCollection('puzzles')) if (p.data.status === 'published') urls.push({ loc: puzzleUrl(p), lastmod: fmt(p.data.date_added), priority: '0.6' });
  for (const r of await getCollection('rules')) if (r.data.status === 'published') urls.push({ loc: rulesUrl(r), lastmod: fmt(r.data.date_added), priority: '0.6' });
  const posts = await livePosts();
  if (posts.length) urls.push({ loc: '/blog/', lastmod: fmt(posts[0].data.publish_at), priority: '0.7' });
  for (const p of posts) urls.push({ loc: postUrl(p), lastmod: fmt(p.data.updated_at ?? p.data.publish_at), priority: '0.6' });
  for (const c of Object.keys(BLOG_CATEGORY_LABEL)) {
    const inCat = posts.filter((p) => p.data.category === c);
    if (inCat.length >= 3) urls.push({ loc: blogCategoryUrl(c), lastmod: fmt(inCat[0].data.publish_at), priority: '0.4' });
  }
  urls.push({ loc: '/site-map/', priority: '0.3' });
  const games = await getCollection('games');
  for (const c of await getCollection('creators')) {
    const own = games.filter((g) => g.data.creator?.id === c.id && g.data.status === 'published');
    const last = own.reduce((m, g) => Math.max(m, g.data.date_added.getTime()), 0);
    if (own.length >= 2) urls.push({ loc: creatorUrl(c.id), lastmod: fmt(new Date(last)), priority: '0.4' });
  }
  // Home page: the newest dated URL above.
  urls[0].lastmod = urls.reduce((m, u) => (u.lastmod && u.lastmod > m ? u.lastmod : m), '') || undefined;

  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${SITE_URL}${u.loc}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}<priority>${u.priority}</priority></url>`)
    .join('\n')}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
