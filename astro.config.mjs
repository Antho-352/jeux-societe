import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// House rule: every outbound link is rel="nofollow" (we never pass link equity). Applied to the built HTML, so it
// covers components, Markdown and MDX alike.
const nofollowOutbound = {
  name: 'nofollow-outbound',
  hooks: {
    'astro:build:done': ({ dir }) => {
      const tag = /<a\b[^>]*>/g;
      const external = /\bhref="https?:\/\/(?!(www\.)?printandplaygame\.com)/;
      const fix = (a) => {
        if (!external.test(a)) return a;
        const rel = a.match(/\brel="([^"]*)"/);
        if (!rel) return a.replace(/^<a\b/, '<a rel="nofollow noopener"');
        const words = new Set(rel[1].split(/\s+/).filter(Boolean));
        words.add('nofollow'); words.add('noopener');
        return a.replace(rel[0], `rel="${[...words].join(' ')}"`);
      };
      const walk = (d) => {
        for (const e of fs.readdirSync(d, { withFileTypes: true })) {
          const f = path.join(d, e.name);
          if (e.isDirectory()) walk(f);
          else if (e.name.endsWith('.html')) {
            const html = fs.readFileSync(f, 'utf8');
            const out = html.replace(tag, fix);
            if (out !== html) fs.writeFileSync(f, out);
          }
        }
      };
      walk(fileURLToPath(dir));
    },
  },
};

export default defineConfig({
  site: 'https://printandplaygame.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [mdx(), nofollowOutbound],
  markdown: { shikiConfig: { theme: 'github-light' } },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr'],
    routing: { prefixDefaultLocale: false },
  },
});
