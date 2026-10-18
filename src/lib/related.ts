import type { Game } from './taxonomy';
import { ageBand } from './taxonomy';

/** Score other games against a reference game (doc 09 § maillage). */
export function relatedGames(ref: Game, all: Game[], n = 4): Game[] {
  const band = ageBand(ref.data.age_min);
  return all
    .filter((g) => g.id !== ref.id && g.data.status === 'published')
    .map((g) => {
      let s = 0;
      if (g.data.subtype && g.data.subtype === ref.data.subtype) s += 50;
      if (g.data.type === ref.data.type) s += 30;
      if (band && ageBand(g.data.age_min) === band) s += 20;
      const themes = g.data.themes.filter((t) => ref.data.themes.includes(t)).length;
      s += Math.min(30, themes * 15);
      if (g.data.occasions.some((o) => ref.data.occasions.includes(o))) s += 10;
      const mech = g.data.mechanics.filter((m) => ref.data.mechanics.includes(m)).length;
      s += Math.min(20, mech * 10);
      return { g, s };
    })
    .sort((a, b) => b.s - a.s || a.g.data.title.localeCompare(b.g.data.title))
    .slice(0, n)
    .map((x) => x.g);
}
