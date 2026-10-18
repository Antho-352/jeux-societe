import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'blog'>;

export const BLOG_CATEGORY_LABEL: Record<string, string> = {
  guides: 'Guides',
  'game-rules': 'Game rules & tips',
  printables: 'Printables',
  holidays: 'Holidays & parties',
  classroom: 'Classroom',
  'game-night': 'Game night',
  'best-of': 'Best of',
};
export const BLOG_CATEGORY_LEAD: Record<string, string> = {
  guides: 'How to print, cut, play and make your own games.',
  'game-rules': 'Strategy, variants and answers to the rule questions that start arguments.',
  printables: 'Ideas and tips for mazes, word searches, bingo and other printables.',
  holidays: 'Games and activities for Christmas, Halloween, Easter, birthdays and every party in between.',
  classroom: 'Printable games and activities for teachers, by age and subject.',
  'game-night': 'What to play, with whom, and how to make the evening work.',
  'best-of': 'Hand-picked lists of the best free games and printables.',
};

/** A post is live when it is published and its publish_at moment has passed at build time. */
export function isLive(p: Post, now = new Date()): boolean {
  return p.data.status === 'published' && p.data.publish_at.getTime() <= now.getTime();
}
export async function livePosts(): Promise<Post[]> {
  const now = new Date();
  return (await getCollection('blog')).filter((p) => isLive(p, now)).sort((a, b) => b.data.publish_at.getTime() - a.data.publish_at.getTime());
}
export const postUrl = (p: Post) => `/blog/${p.id}/`;
export const blogCategoryUrl = (c: string) => `/blog/category/${c}/`;

export function readingMinutes(body = ''): number {
  const words = body.replace(/<[^>]+>|import .*|export .*|[#*_>`|-]/g, ' ').split(/\s+/).filter(Boolean).length;
  return Math.max(2, Math.round(words / 230));
}

/** Related posts: explicit list first, then same silo, same category, newest. */
export function relatedPosts(p: Post, all: Post[], n = 3): Post[] {
  const explicit = p.data.related.map((id) => all.find((x) => x.id === id)).filter(Boolean) as Post[];
  const rest = all
    .filter((x) => x.id !== p.id && !explicit.includes(x))
    .map((x) => ({ x, s: (x.data.silo === p.data.silo ? 3 : 0) + (x.data.category === p.data.category ? 2 : 0) + (x.data.silo.split('/')[0] === p.data.silo.split('/')[0] ? 1 : 0) }))
    .sort((a, b) => b.s - a.s || b.x.data.publish_at.getTime() - a.x.data.publish_at.getTime())
    .map((o) => o.x);
  return [...explicit, ...rest].slice(0, n);
}

export const fmtDate = (d: Date) => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
