import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://printandplaygame.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr'],
    routing: { prefixDefaultLocale: false },
  },
  integrations: [
    sitemap({
      filter: (page) => !/\/page\/\d+\/$/.test(page) && !page.includes('/drafts/'),
      i18n: { defaultLocale: 'en', locales: { en: 'en', fr: 'fr' } },
    }),
  ],
});
