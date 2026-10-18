import type { CollectionEntry } from 'astro:content';

export type Game = CollectionEntry<'games'>;
export type Puzzle = CollectionEntry<'puzzles'>;
export type Rule = CollectionEntry<'rules'>;
export type Hub = CollectionEntry<'hubs'>;

export const SILO_BY_TYPE: Record<Game['data']['type'], string> = {
  board: 'board-games',
  card: 'card-games',
  dice: 'dice-games',
  'roll-and-write': 'roll-and-write',
  escape: 'escape-games',
  party: 'party-games',
  'scavenger-hunt': 'scavenger-hunts',
};
export const TYPE_LABEL: Record<Game['data']['type'], string> = {
  board: 'Board game',
  card: 'Card game',
  dice: 'Dice game',
  'roll-and-write': 'Roll & write',
  escape: 'Escape game',
  party: 'Party game',
  'scavenger-hunt': 'Scavenger hunt',
};
export const PUZZLE_SILO: Record<Puzzle['data']['type'], string> = {
  maze: 'puzzles/mazes',
  'dot-to-dot': 'puzzles/dot-to-dot',
  'word-search': 'puzzles/word-search',
  sudoku: 'puzzles/sudoku',
  crossword: 'puzzles/crosswords',
  rebus: 'puzzles/rebus',
  bingo: 'bingo',
  logic: 'puzzles/logic',
};
export const PUZZLE_LABEL: Record<Puzzle['data']['type'], string> = {
  maze: 'Maze',
  'dot-to-dot': 'Dot to dot',
  'word-search': 'Word search',
  sudoku: 'Sudoku',
  crossword: 'Crossword',
  rebus: 'Rebus puzzle',
  bingo: 'Bingo',
  logic: 'Logic puzzle',
};
export const RULES_CATEGORY_LABEL: Record<Rule['data']['category'], string> = {
  card: 'Card game',
  board: 'Board game',
  dice: 'Dice game',
  party: 'Party game',
  'pen-and-paper': 'Pen & paper game',
  tile: 'Tile game',
};
export const AGE_BAND_LABEL: Record<string, string> = {
  preschool: 'Ages 3–5',
  kids: 'Ages 6–8',
  tweens: 'Ages 9–12',
  teens: 'Teens',
  adults: 'Adults',
};
export const OCCASION_LABEL: Record<string, string> = {
  christmas: 'Christmas', halloween: 'Halloween', thanksgiving: 'Thanksgiving', easter: 'Easter', valentines: "Valentine's Day",
  birthday: 'Birthday', summer: 'Summer', winter: 'Winter', 'back-to-school': 'Back to school', travel: 'Travel',
  'baby-shower': 'Baby shower', 'bridal-shower': 'Bridal shower', 'new-year': 'New Year',
};

export function ageBand(ageMin?: number): string | undefined {
  if (ageMin === undefined) return undefined;
  if (ageMin < 6) return 'preschool';
  if (ageMin < 9) return 'kids';
  if (ageMin < 13) return 'tweens';
  if (ageMin < 18) return 'teens';
  return 'adults';
}
export function playersLabel(min: number, max: number): string {
  if (min === max) return min === 1 ? '1 player' : `${min} players`;
  return `${min}–${max} players`;
}
export function timeLabel(min?: number, max?: number): string | undefined {
  if (min === undefined && max === undefined) return undefined;
  if (min !== undefined && max !== undefined && min !== max) return `${min}–${max} min`;
  return `${max ?? min} min`;
}
export function ageLabel(ageMin?: number): string | undefined {
  return ageMin === undefined ? undefined : `Age ${ageMin}+`;
}
export function titleCase(s: string): string {
  return s.replace(/[-_]/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export const gameUrl = (g: Game) => `/${SILO_BY_TYPE[g.data.type]}/${g.id}/`;
export const puzzleUrl = (p: Puzzle) => `/${PUZZLE_SILO[p.data.type]}/${p.id}/`;
export const rulesUrl = (r: Rule) => `/rules/${r.id}/`;
export const creatorUrl = (id: string) => `/creators/${id}/`;
export const hubUrl = (path: string) => `/${path}/`;

export const COVER_COLOURS = ['#CFFF5E', '#B8D8FF', '#FFD9D2', '#FFE8A3', '#D9F2E6'];
export function coverColour(seed: string): string {
  let h = 0;
  for (const c of seed) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return COVER_COLOURS[h % COVER_COLOURS.length];
}

/** Evaluate a hub filter against a games item. Keys are optional; all given keys must match. */
export function gameMatches(g: Game, f: Record<string, any>): boolean {
  const d = g.data;
  if (d.status !== 'published') return false;
  if (f.type && d.type !== f.type) return false;
  if (f.subtype && d.subtype !== f.subtype) return false;
  if (f.age_band && ageBand(d.age_min) !== f.age_band) return false;
  if (f.age_max !== undefined && (d.age_min === undefined || d.age_min > f.age_max)) return false;
  if (f.players === 'solo' && d.players_min !== 1) return false;
  if (f.players === '2' && !(d.players_min <= 2 && d.players_max >= 2)) return false;
  if (f.players === 'party' && d.players_max < 6) return false;
  if (f.time_max !== undefined && (d.time_max ?? d.time_min ?? 999) > f.time_max) return false;
  if (f.occasion && !d.occasions.includes(f.occasion)) return false;
  if (f.theme && !d.themes.includes(f.theme)) return false;
  if (f.mechanic && !d.mechanics.includes(f.mechanic)) return false;
  if (f.hosting_mode && d.hosting_mode !== f.hosting_mode) return false;
  if (f.featured && !d.featured) return false;
  return true;
}
export function puzzleMatches(p: Puzzle, f: Record<string, any>): boolean {
  const d = p.data;
  if (d.status !== 'published') return false;
  if (f.type && d.type !== f.type) return false;
  if (f.difficulty && d.difficulty !== f.difficulty) return false;
  if (f.age_band && (d.age_band ?? ageBand(d.age_min)) !== f.age_band) return false;
  if (f.occasion && !d.occasions.includes(f.occasion)) return false;
  if (f.theme && !d.themes.includes(f.theme)) return false;
  return true;
}
export function ruleMatches(r: Rule, f: Record<string, any>): boolean {
  const d = r.data;
  if (d.status !== 'published') return false;
  if (f.category && d.category !== f.category) return false;
  if (f.players === 'solo' && d.players_min !== 1) return false;
  if (f.players === '2' && !(d.players_min <= 2 && d.players_max >= 2)) return false;
  if (f.public_domain !== undefined && d.public_domain !== f.public_domain) return false;
  return true;
}

export function sizeLabel(mb?: number): string | undefined {
  if (mb === undefined) return undefined;
  return mb < 1 ? `${Math.max(1, Math.round(mb * 1024))} KB` : `${mb} MB`;
}
