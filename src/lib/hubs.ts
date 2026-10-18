import { getCollection } from 'astro:content';
import { gameFacets, gameItem, mixedFacets, puzzleFacets, puzzleItem, ruleFacets, ruleItem } from './listing';
import type { ListingItem } from '../components/Listing.astro';
import { gameMatches, puzzleMatches, ruleMatches } from './taxonomy';
import type { Hub } from './taxonomy';

export const THIN_THRESHOLD = 4;

/** Items and facets for a hub; shared by the hub page and the sitemap. */
export async function hubListing(hub: Hub): Promise<{ items: ListingItem[]; facets: ReturnType<typeof gameFacets>; noun: string }> {
  const d = hub.data;
  if (d.collection === 'games') {
    const creators = await getCollection('creators');
    const byId = new Map(creators.map((c) => [c.id, c.data.name]));
    const games = (await getCollection('games')).filter((g) => gameMatches(g, d.filter));
    const items = games.map((g) => gameItem(g, g.data.creator ? byId.get(g.data.creator.id) : undefined));
    return { items, facets: gameFacets(items), noun: 'games' };
  }
  if (d.collection === 'mixed') {
    const creators = await getCollection('creators');
    const byId = new Map(creators.map((c) => [c.id, c.data.name]));
    const games = (await getCollection('games')).filter((g) => gameMatches(g, d.filter)).map((g) => gameItem(g, g.data.creator ? byId.get(g.data.creator.id) : undefined));
    const puzzles = (await getCollection('puzzles')).filter((p) => puzzleMatches(p, d.filter)).map(puzzleItem);
    const items = [...games, ...puzzles];
    return { items, facets: mixedFacets(items), noun: 'games and puzzles' };
  }
  if (d.collection === 'puzzles') {
    const puzzles = (await getCollection('puzzles')).filter((p) => puzzleMatches(p, d.filter));
    const items = puzzles.map(puzzleItem);
    return { items, facets: puzzleFacets(items), noun: 'puzzles' };
  }
  const rules = (await getCollection('rules')).filter((r) => ruleMatches(r, d.filter));
  const items = rules.map(ruleItem);
  return { items, facets: ruleFacets(items), noun: 'games' };
}

export async function hubPathSet(): Promise<Set<string>> {
  const hubs = await getCollection('hubs');
  return new Set(hubs.map((h) => h.data.path));
}
