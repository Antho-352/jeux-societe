# Blog guide: how every article is built

Read CONTENT-GUIDE.md first (verification, tone, licences). This file adds the blog-specific rules.
The reference article is `src/content/blog/how-to-solve-a-maze.mdx`: copy its structure.

## 1. One article = one intent, one parent page
- Each article targets **one keyword** (`target_keyword`) plus 2–5 close variants (`secondary_keywords`), checked with DataForSEO (`scripts/dfs.py overview`). Record `keyword_volume` and `keyword_difficulty`.
- Each article belongs to **one silo**: `silo` is the path of the parent page it pushes (a hub, e.g. `puzzles/mazes`, `rules/card-games`, `escape-games`, `occasions/christmas`). The page automatically ends with a call-to-action box toward that parent.
- **Never compete with a product or category page.** If the keyword is "printable X" or "X rules", the page already exists (hub, puzzle or rules page): the article must target the informational question around it ("how to…", "why…", "best … for …", "… vs …", "ideas for …") and link to that page.
- `pushes`: the 2–4 child pages (games, puzzles, rules) the article sends readers and link equity to.

## 2. Structure (in this order)
1. **H1** (`title`): the keyword near the start, a promise, ≤ 70 characters. `seo_title` ≤ 60 characters when the H1 is longer.
2. **Short answer** (`tldr`, inverted pyramid): 2–3 sentences that answer the query completely. A reader who stops here must have the answer. `key_takeaways`: 3 bullets.
3. Intro paragraph (2–4 sentences): why the question matters and what the reader will get. No "In this article…".
4. **H2 sections** phrased as the sub-questions people ask (People Also Ask, related searches). 4–8 H2s, H3s only inside H2s. The table of contents is built from them.
5. At least **one visual element** every ~400 words: `StatGrid` (key numbers), `BarChart` (comparison), a markdown table, a `Figure` (our covers or our own photos only), a callout.
6. At least **one interactive tool** where it helps the reader do the thing (see §4).
7. **Internal links**: 5–10 contextual links in the text (descriptive anchors, never "click here"), plus 2–4 `ItemCallout` cards for the pages in `pushes`. Link to other blog posts once they exist.
8. A closing `Callout type="key"` that sums up in one sentence.
9. **FAQ** (`faq`): 3–5 real questions with direct, 1–3 sentence answers that start with the answer ("Yes.", "No.", "Usually…").
10. **Sources** (`sources`, `sources_checked`): every factual claim that does not come from our own catalogue is backed by a source we actually opened. **Resources** (`resources`): 3–5 internal pages.

## 3. Writing rules
- 1,000–2,000 words, depending on the query (look at what ranks: `scripts/dfs.py serp "<keyword>"`).
- Short paragraphs (2–4 sentences). One idea per paragraph. Bold the key phrase of a paragraph, not whole sentences.
- First person plural ("we printed…", "in our tests") only for things we really did.
- Numbers about our catalogue must match the catalogue (count with grep before writing).
- No fake statistics, no invented quotes, no "studies show" without the study in `sources`.
- Dates: `publish_at` is a full UTC timestamp. The article is built only once that moment has passed.

## 4. Components (import them at the top of the .mdx)
| Component | Use it for |
|---|---|
| `Callout type="tip/note/warning/key/example"` | Highlight one point. Max one every 300 words. |
| `StatGrid items=[{value,label,note}]` | 3–4 key numbers (infographic). |
| `BarChart items=[{label,value}] unit title caption` | Compare quantities (infographic). |
| `Figure src alt caption` | An image with a caption. Only images we made or have rights to. |
| `ItemCallout href="/rules/go-fish/" note` | Card linking to a game, puzzle or rules page (build fails if the page does not exist). |
| `HubCta path="puzzles/mazes"` | Extra CTA toward a hub mid-article (one is added at the end automatically). |
| `Quiz mode="score"` | Knowledge quiz with explanations (rules, trivia). |
| `Quiz mode="match" outcomes=[…]` | "Which game/puzzle is for you?" recommender; each outcome links to a page. |
| `DiceRoller dice sides` | Dice games, roll & write, "no dice at home". |
| `Picker items` | "Who goes first", "which game tonight", random prompts. |
| `Timer seconds` | Party games, speed challenges, maze races. |
| `ScoreKeeper players` | Card and dice games played over several rounds. |
| `Checklist id items` | Party prep, printing kit, classroom set-up (kept in the reader's browser). |
| `TicTacToeBoard boards=[{cells,caption,highlight}]` | Static 3×3 grid diagrams (cells: 9 chars of X, O or `.`), e.g. the steps of a trap. |
| `TicTacToeQuiz positions=[{cells,toPlay,correct,explain}]` | "Where should X play?" quiz: the reader taps a square. |
| `TicTacToeGame` | Tic-tac-toe against the computer (beginner or perfect). |

## 5. Files
- Article: `src/content/blog/<slug>.mdx` (slug = keyword in kebab case, no stop words, ≤ 5 words).
- Cover: `node scripts/covers/blog_covers.mjs <slug>` writes `public/img/blog/<slug>.png` (1200×630, also the social image). Set `cover`, `cover_alt`, `cover_emoji`.
- Check: `npm run build && npm run check:links`.
- **Preview a scheduled article without touching its date:** `BLOG_PREVIEW=1 npx astro build`, then look at `dist/blog/<slug>/`. **Never edit `publish_at` to test**: a commit made at that moment would publish the article early. Rebuild without the variable before committing.
- Scheduling: commit the article with a future `publish_at`. The hourly GitHub Action rebuilds the site when the time comes (needs the `CF_PAGES_DEPLOY_HOOK` secret, see `.github/workflows/scheduled-publish.yml`).
