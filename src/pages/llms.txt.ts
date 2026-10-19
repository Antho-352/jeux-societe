import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { hubListing, THIN_THRESHOLD } from '../lib/hubs';
import { SITE_URL } from '../lib/seo';
import { hubUrl, rulesUrl } from '../lib/taxonomy';
import { livePosts, postUrl } from '../lib/blog';

// llms.txt (https://llmstxt.org): a plain-text map of the site for AI assistants. Built from the same hub
// whitelist as the sitemap, so it never lists a thin or noindex page.
export const GET: APIRoute = async () => {
  const hubs = (await getCollection('hubs')).sort((a, b) => a.data.path.localeCompare(b.data.path));
  const sections: string[] = [];
  for (const hub of hubs) {
    const { items } = await hubListing(hub);
    if (items.length < Math.max(hub.data.min_items, THIN_THRESHOLD)) continue;
    const indent = hub.data.path.includes('/') ? '  ' : '';
    sections.push(`${indent}- [${hub.data.h1}](${SITE_URL}${hubUrl(hub.data.path)}): ${hub.data.seo_description} (${items.length} items)`);
  }
  const rules = (await getCollection('rules')).filter((r) => r.data.status === 'published').sort((a, b) => a.data.title.localeCompare(b.data.title));
  const posts = await livePosts();
  const body = [
    '# Print & Play Game',
    '',
    '> Free print and play board games, card games, escape games and printable puzzles (mazes, word searches, bingo cards, sudoku, dot to dots) as PDFs, plus plain-English rules for classic games. Every game is credited to its designer, with its licence; PDFs are hosted only when the licence allows it, otherwise the page links to the creator\'s own download.',
    '',
    'The mazes, word searches, bingo cards and other puzzles marked "Made by Print & Play Game" are our own work, licensed CC BY-NC 4.0. Player counts, play times and ages come from the creator\'s page or BoardGameGeek.',
    '',
    '## Sections',
    '',
    ...sections,
    '',
    '## Game rules',
    '',
    ...rules.map((r) => `- [${r.data.title}](${SITE_URL}${rulesUrl(r)})`),
    ...(posts.length ? ['', '## Guides', '', ...posts.map((p) => `- [${p.data.title}](${SITE_URL}${postUrl(p)}): ${p.data.description}`)] : []),
    '',
    '## About',
    '',
    `- [How to print board games at home](${SITE_URL}/how-to-print/)`,
    `- [About the site](${SITE_URL}/about/)`,
    `- [Full site map](${SITE_URL}/site-map/)`,
    '',
  ].join('\n');
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
