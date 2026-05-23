import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    tech: z.array(z.string()).default([]),
    links: z
      .array(z.object({ label: z.string(), href: z.string().url() }))
      .default([]),
    cover: z.string().optional(),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = { projects };
