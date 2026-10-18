import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';

export const GAME_TYPES = ['board', 'card', 'dice', 'roll-and-write', 'escape', 'party', 'scavenger-hunt'] as const;
export const PUZZLE_TYPES = ['maze', 'dot-to-dot', 'word-search', 'sudoku', 'crossword', 'rebus', 'bingo', 'logic'] as const;
export const DIFFICULTIES = ['easy', 'medium', 'hard'] as const;
export const AGE_BANDS = ['preschool', 'kids', 'tweens', 'teens', 'adults'] as const;
export const OCCASIONS = ['christmas', 'halloween', 'thanksgiving', 'easter', 'valentines', 'birthday', 'summer', 'winter', 'back-to-school', 'travel', 'baby-shower', 'bridal-shower', 'new-year'] as const;

const themes = z.array(z.string()).default([]);

const games = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/games' }),
  schema: z.object({
    title: z.string(),
    type: z.enum(GAME_TYPES),
    subtype: z.string().optional(),
    summary: z.string().max(220),
    players_min: z.number().int().min(1),
    players_max: z.number().int().min(1),
    age_min: z.number().int().min(2).optional(),
    time_min: z.number().int().optional(),
    time_max: z.number().int().optional(),
    complexity: z.number().min(1).max(5).optional(),
    themes,
    occasions: z.array(z.enum(OCCASIONS)).default([]),
    mechanics: z.array(z.string()).default([]),
    languages: z.array(z.string()).default(['en']),
    components_included: z.array(z.string()).default([]),
    components_needed: z.array(z.string()).default([]),
    pages: z.number().int().optional(),
    paper: z.enum(['a4', 'letter', 'both']).optional(),
    colour: z.enum(['colour', 'bw', 'both']).optional(),
    app_required: z.boolean().default(false),
    creator: reference('creators').optional(),
    designers: z.array(z.string()).default([]),
    artists: z.array(z.string()).default([]),
    publisher: z.string().optional(),
    year: z.number().int().optional(),
    award: z.string().optional(),
    licence: z.string(),
    licence_url: z.string().url().optional(),
    hosting_mode: z.enum(['mirror', 'link']),
    source_url: z.string().url(),
    download_url: z.string().optional(),
    download_size_mb: z.number().optional(),
    files: z.array(z.object({ label: z.string(), url: z.string() })).default([]),
    cover: z.string().optional(),
    cover_colour: z.string().optional(),
    status: z.enum(['published', 'draft']).default('published'),
    featured: z.boolean().default(false),
    date_added: z.coerce.date(),
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
  }),
});

const rules = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/rules' }),
  schema: z.object({
    title: z.string(),
    game_name: z.string(),
    aliases: z.array(z.string()).default([]),
    category: z.enum(['card', 'board', 'dice', 'party', 'pen-and-paper', 'tile']),
    summary: z.string().max(220),
    players_min: z.number().int().min(1),
    players_max: z.number().int().min(1),
    age_min: z.number().int().optional(),
    time_min: z.number().int().optional(),
    time_max: z.number().int().optional(),
    equipment: z.array(z.string()).default([]),
    public_domain: z.boolean().default(false),
    trademark_note: z.string().optional(),
    printable: z.string().optional(),
    printable_label: z.string().optional(),
    cover: z.string().optional(),
    related_game: reference('games').optional(),
    sources: z.array(z.object({ label: z.string(), url: z.string().url() })).default([]),
    status: z.enum(['published', 'draft']).default('published'),
    date_added: z.coerce.date(),
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
  }),
});

const puzzles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/puzzles' }),
  schema: z.object({
    title: z.string(),
    type: z.enum(PUZZLE_TYPES),
    summary: z.string().max(220),
    difficulty: z.enum(DIFFICULTIES).optional(),
    age_band: z.enum(AGE_BANDS).optional(),
    age_min: z.number().int().optional(),
    themes,
    occasions: z.array(z.enum(OCCASIONS)).default([]),
    pages: z.number().int(),
    paper: z.enum(['a4', 'letter', 'both']).default('both'),
    colour: z.enum(['colour', 'bw', 'both']).default('bw'),
    answers_included: z.boolean().default(true),
    grid: z.string().optional(),
    count: z.number().int().optional(),
    download_url: z.string(),
    download_size_mb: z.number().optional(),
    cover: z.string().optional(),
    licence: z.string().default('CC BY-NC 4.0'),
    status: z.enum(['published', 'draft']).default('published'),
    date_added: z.coerce.date(),
    seo_title: z.string().optional(),
    seo_description: z.string().optional(),
  }),
});

const creators = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/creators' }),
  schema: z.object({
    name: z.string(),
    url: z.string().url().optional(),
    country: z.string().optional(),
    bio: z.string(),
    support_url: z.string().url().optional(),
    support_label: z.string().optional(),
  }),
});

// A hub entry is the editorial whitelist: a listing URL exists only if a hub file exists for its path.
const hubs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/hubs' }),
  schema: z.object({
    path: z.string(),
    title: z.string(),
    h1: z.string(),
    lead: z.string(),
    seo_title: z.string(),
    seo_description: z.string().max(165),
    collection: z.enum(['games', 'puzzles', 'rules', 'mixed']),
    filter: z.record(z.string(), z.any()).default({}),
    related: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    min_items: z.number().int().default(1),
  }),
});


export const BLOG_CATEGORIES = ['guides', 'game-rules', 'printables', 'holidays', 'classroom', 'game-night', 'best-of'] as const;

const authors = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/authors' }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    bio: z.string(),
    avatar: z.string().optional(),
    url: z.string().url().optional(),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),                         // H1
    seo_title: z.string().max(60).optional(),  // <title>, falls back to title
    description: z.string().max(165),          // meta description
    excerpt: z.string().max(220),              // blog cards
    category: z.enum(BLOG_CATEGORIES),
    author: reference('authors'),
    publish_at: z.coerce.date(),               // date AND time; the post is built only once this moment has passed
    updated_at: z.coerce.date().optional(),
    // SEO plan
    target_keyword: z.string(),
    secondary_keywords: z.array(z.string()).default([]),
    keyword_volume: z.number().int().optional(),
    keyword_difficulty: z.number().optional(),
    silo: z.string(),                          // path of the parent (mother) page this post pushes, e.g. "puzzles/mazes"
    pushes: z.array(z.string()).default([]),   // other internal targets, site paths like "/rules/go-fish/"
    // Inverted pyramid
    tldr: z.string(),                          // short answer shown first
    key_takeaways: z.array(z.string()).default([]),
    // Media
    cover: z.string().optional(),              // /img/blog/<slug>.png (generated)
    cover_alt: z.string().optional(),
    cover_emoji: z.string().optional(),        // big glyph on the generated cover
    // End matter
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    sources: z.array(z.object({ label: z.string(), url: z.string().url() })).default([]),
    sources_checked: z.coerce.date().optional(),
    resources: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
    related: z.array(z.string()).default([]),  // blog slugs; filled automatically when empty
    status: z.enum(['published', 'draft']).default('published'),
  }),
});

export const collections = { games, rules, puzzles, creators, hubs, authors, blog };
