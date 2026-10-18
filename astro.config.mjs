import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://printandplaygame.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr'],
    routing: { prefixDefaultLocale: false },
  },
});
