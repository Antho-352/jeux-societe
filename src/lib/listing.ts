import type { ListingItem } from '../components/Listing.astro';
import { ageBand, AGE_BAND_LABEL, ageLabel, coverColour, gameUrl, playersLabel, puzzleUrl, PUZZLE_LABEL, rulesUrl, RULES_CATEGORY_LABEL, timeLabel, TYPE_LABEL, titleCase, OCCASION_LABEL } from './taxonomy';
import type { Game, Puzzle, Rule } from './taxonomy';

export function gameItem(g: Game, byName?: string): ListingItem {
  const d = g.data;
  return {
    href: gameUrl(g), title: d.title, by: byName ?? d.designers[0] ?? d.publisher, typeLabel: TYPE_LABEL[d.type],
    cover: d.cover, colour: d.cover_colour ?? coverColour(g.id),
    pills: [playersLabel(d.players_min, d.players_max), timeLabel(d.time_min, d.time_max), ageLabel(d.age_min)].filter(Boolean) as string[],
    data: {
      kind: d.type, 'players-min': d.players_min, 'players-max': d.players_max, age: ageBand(d.age_min), colour: d.colour, lang: d.languages.join(','),
      theme: d.themes.join(','), occasion: d.occasions.join(','), mechanic: d.mechanics.join(','), hosting: d.hosting_mode, paper: d.paper,
      components: d.components_needed.length ? 'needed' : 'none',
    },
    sortTitle: d.title, sortDate: d.date_added.getTime(), sortTime: d.time_max ?? d.time_min,
  };
}
export function puzzleItem(p: Puzzle): ListingItem {
  const d = p.data;
  const band = d.age_band ?? ageBand(d.age_min);
  return {
    href: puzzleUrl(p), title: d.title, by: d.count && d.count > 1 ? `${d.count} ${PUZZLE_LABEL[d.type].toLowerCase()}s` : undefined, typeLabel: PUZZLE_LABEL[d.type],
    cover: d.cover, colour: coverColour(p.id),
    pills: [d.difficulty ? titleCase(d.difficulty) : undefined, band ? AGE_BAND_LABEL[band] : undefined, `${d.pages} page${d.pages > 1 ? 's' : ''}`].filter(Boolean) as string[],
    data: { kind: d.type, difficulty: d.difficulty, age: band, theme: d.themes.join(','), occasion: d.occasions.join(','), colour: d.colour, answers: d.answers_included ? 'yes' : 'no' },
    sortTitle: d.title, sortDate: d.date_added.getTime(),
  };
}
export function ruleItem(r: Rule): ListingItem {
  const d = r.data;
  return {
    href: rulesUrl(r), title: d.title, by: d.public_domain ? 'Public domain · printable included' : undefined, typeLabel: RULES_CATEGORY_LABEL[d.category],
    cover: d.cover, colour: coverColour(r.id),
    pills: [playersLabel(d.players_min, d.players_max), timeLabel(d.time_min, d.time_max), ageLabel(d.age_min)].filter(Boolean) as string[],
    data: { 'players-min': d.players_min, 'players-max': d.players_max, category: d.category, age: ageBand(d.age_min), equipment: d.equipment.map((e) => e.toLowerCase().replace(/[^a-z0-9]+/g, '-')).join(','), printable: d.printable ? 'yes' : 'no' },
    sortTitle: d.title, sortDate: d.date_added.getTime(), sortTime: d.time_max ?? d.time_min,
  };
}

type Opt = { value: string; label: string; count: number };
function countBy(items: ListingItem[], key: string, labelOf: (v: string) => string, order?: string[]): Opt[] {
  const m = new Map<string, number>();
  for (const it of items) for (const v of String(it.data[key] ?? '').split(',').filter(Boolean)) m.set(v, (m.get(v) ?? 0) + 1);
  let opts = Array.from(m, ([value, count]) => ({ value, label: labelOf(value), count }));
  if (order) opts = opts.sort((a, b) => order.indexOf(a.value) - order.indexOf(b.value));
  else opts = opts.sort((a, b) => b.count - a.count).slice(0, 12);
  return opts;
}
const AGE_ORDER = ['preschool', 'kids', 'tweens', 'teens', 'adults'];
// Player and time options; the same tests run in the browser (Listing.astro), keep them in sync.
const PLAYERS: [string, string, (min: number, max: number) => boolean][] = [
  ['solo', 'Solo', (min) => min === 1],
  ['2', '2 players', (min, max) => min <= 2 && max >= 2],
  ['2plus', '2+ players', (_min, max) => max >= 2],
  ['party', 'Party (6+)', (_min, max) => max >= 6],
];
const TIMES: [string, string, (t: number) => boolean][] = [
  ['15', 'Under 15 min', (t) => t <= 15],
  ['30', 'Under 30 min', (t) => t <= 30],
  ['60', 'Under an hour', (t) => t < 60],
  ['60plus', '1 hour+', (t) => t >= 60],
];
function playerOptions(items: ListingItem[]) {
  return PLAYERS.map(([value, label, test]) => ({ value, label, count: items.filter((i) => test(Number(i.data['players-min']), Number(i.data['players-max']))).length })).filter((o) => o.count > 0);
}
function timeOptions(items: ListingItem[]) {
  return TIMES.map(([value, label, test]) => ({ value, label, count: items.filter((i) => i.sortTime !== undefined && test(i.sortTime)).length })).filter((o) => o.count > 0);
}
export function gameFacets(items: ListingItem[]) {
  const players = playerOptions(items);
  const time = timeOptions(items);
  return [
    { key: 'players', label: 'Players', options: players },
    { key: 'age', label: 'Age', options: countBy(items, 'age', (v) => AGE_BAND_LABEL[v] ?? v, AGE_ORDER) },
    { key: 'time', label: 'Play time', options: time },
    { key: 'theme', label: 'Theme', options: countBy(items, 'theme', titleCase) },
    { key: 'mechanic', label: 'Mechanics', options: countBy(items, 'mechanic', titleCase) },
    { key: 'occasion', label: 'Occasion', options: countBy(items, 'occasion', (v) => OCCASION_LABEL[v] ?? titleCase(v)) },
    { key: 'colour', label: 'Printing', options: countBy(items, 'colour', (v) => ({ colour: 'Colour', bw: 'Black & white', both: 'Colour or B&W' })[v] ?? v) },
    { key: 'lang', label: 'Language', options: countBy(items, 'lang', (v) => ({ en: 'English', fr: 'French', de: 'German', es: 'Spanish', it: 'Italian', none: 'No text' })[v] ?? v.toUpperCase()) },
  ];
}
const PUZZLE_ORDER = ['dot-to-dot', 'sudoku', 'bingo', 'maze', 'word-search', 'crossword', 'rebus', 'logic'];
export function puzzleFacets(items: ListingItem[]) {
  return [
    { key: 'kind', label: 'Type', options: countBy(items, 'kind', (v) => (PUZZLE_LABEL as Record<string, string>)[v] ?? titleCase(v), PUZZLE_ORDER) },
    { key: 'difficulty', label: 'Difficulty', options: countBy(items, 'difficulty', titleCase, ['easy', 'medium', 'hard']) },
    { key: 'age', label: 'Age', options: countBy(items, 'age', (v) => AGE_BAND_LABEL[v] ?? v, AGE_ORDER) },
    { key: 'theme', label: 'Theme', options: countBy(items, 'theme', titleCase) },
    { key: 'occasion', label: 'Occasion', options: countBy(items, 'occasion', (v) => OCCASION_LABEL[v] ?? titleCase(v)) },
  ];
}
export function ruleFacets(items: ListingItem[]) {
  return [
    { key: 'category', label: 'Type', options: countBy(items, 'category', (v) => RULES_CATEGORY_LABEL[v as keyof typeof RULES_CATEGORY_LABEL] ?? titleCase(v)) },
    { key: 'players', label: 'Players', options: playerOptions(items) },
    { key: 'age', label: 'Age', options: countBy(items, 'age', (v) => AGE_BAND_LABEL[v] ?? v, AGE_ORDER) },
    { key: 'time', label: 'Play time', options: timeOptions(items) },
    { key: 'equipment', label: 'What you need', options: countBy(items, 'equipment', titleCase) },
    { key: 'printable', label: 'Printable', options: countBy(items, 'printable', (v) => (v === 'yes' ? 'PDF included' : 'Rules only')) },
  ];
}

export function mixedFacets(items: ListingItem[]) {
  const label = (v: string) => (TYPE_LABEL as Record<string, string>)[v] ?? (PUZZLE_LABEL as Record<string, string>)[v] ?? titleCase(v);
  return [
    { key: 'kind', label: 'Type', options: countBy(items, 'kind', label) },
    { key: 'age', label: 'Age', options: countBy(items, 'age', (v) => AGE_BAND_LABEL[v] ?? v, AGE_ORDER) },
    { key: 'difficulty', label: 'Difficulty', options: countBy(items, 'difficulty', titleCase, ['easy', 'medium', 'hard']) },
    { key: 'theme', label: 'Theme', options: countBy(items, 'theme', titleCase) },
  ];
}
