import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// TODO: 換成正式網域（sitemap / canonical 需要）
export default defineConfig({
  site: 'https://example.com',
  integrations: [react(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
