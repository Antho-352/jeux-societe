# Sujets de blog (lot A) : puzzles, bingo, fêtes, classe, chasses au trésor, escape games

Date : 19 octobre 2026. Données : DataForSEO (Google US 2840 et UK 2826, anglais), relevées le 19 octobre 2026.
Fichier de données : `data/blog-topics-a.json` (25 sujets, un objet par article, au format demandé par `BLOG-GUIDE.md`).
Données brutes : `data/kw/blog/ideas-*.json`, `overview-*.json`, `volume-kids-us.json`, `kd-kids-us.json`, `serp/*.json`.

Périmètre de ce lot : puzzles (labyrinthes, points à relier, mots mêlés, sudoku, bingo, logique), fêtes et occasions, activités enfants et famille, classe, chasses au trésor, escape games pour enfants. Les jeux de plateau, de cartes, d'ambiance, les règles, les soirées jeux et les guides print-and-play relèvent de l'autre lot (B).

## 1. Méthode

1. Lecture de `BLOG-GUIDE.md`, de `docs/08` (grappes puzzles, bingo, occasions, classe, chasses au trésor, escape) et de `docs/09` (silos), puis de l'article modèle `how-to-solve-a-maze.mdx`.
2. Fouille de `data/kw/keywords-master.csv` : il contient surtout des requêtes « printable », donc des pages produit. Peu de requêtes informationnelles exploitables, sauf la classe (`games to play in class`, `indoor recess`…).
3. Quatre appels `ideas` (80 graines : questions sur les puzzles, fêtes, classe, chasses, escape), puis `overview` (volume, KD, intention) sur 308 candidats, puis `volume` et `kd` sur les 142 requêtes sans données.
4. `serp` (top 10 US) sur 45 finalistes, plus 2 SERP UK (`bingo calls`, `easter egg hunt clues`). Rejet de tout sujet dont le top 5 est fait de pages produit que nos hubs visent déjà.
5. `overview` US et UK sur les 134 mots-clés retenus (cible + secondaires) pour des chiffres homogènes.

Dépense DataForSEO de ce lot : **0,70 $** (4 `ideas` à 0,09 $, 47 `serp` à 0,002 $, 5 `overview`, 1 `volume`, 1 `kd`). Budget : 3 $.

### Limite importante : « for kids » n'a pas de volume

Google Ads ne renvoie **aucun volume** pour les requêtes qui ciblent les enfants (« thanksgiving games for kids », « escape room for kids at home », « scavenger hunt ideas for kids »…) : 142 requêtes de ce type sont revenues vides, aussi bien en Google Ads qu'en DataForSEO Labs. Les formulations « preschoolers », « toddlers », « teens », « kindergarten », « students », « family » sont, elles, mesurées. Conséquence : chaque sujet vise une requête mesurable (« family », « preschoolers », « classroom ») et traite l'angle enfants dans le texte. Le trafic réel sur les variantes « for kids » s'ajoutera, mais on ne peut pas le chiffrer.

Les KD de DataForSEO Labs valent souvent 0 sur ces niches (peu de liens mesurés). La lecture des SERP a donc servi d'arbitre : sont jugés faibles les tops 5 occupés par Pinterest, Reddit, Facebook, Quora, YouTube, des PDF, des blogs de vendeurs ou des pages d'événements locaux.

## 2. Tableau des 25 sujets

Priorité : 1 = gain rapide, 2 = bon sujet avec un peu plus de concurrence ou un besoin de contenu, 3 = cible de croissance (gros volume, concurrence plus forte). Les sujets saisonniers sont classés par date limite. « Vol. » = recherches mensuelles du mot-clé cible.

| Prio | Article (slug) | Mot-clé cible | Vol. US | Vol. UK | KD | Silo poussé | En ligne avant | Besoins |
|---|---|---|---|---|---|---|---|---|
| 1 | thanksgiving-games-for-family | thanksgiving games for family | 8 100 | 10 | 10 | occasions | **en retard** (15/10/2026) | hub Thanksgiving (4e fiche) |
| 1 | christmas-activities-for-preschoolers | christmas activities for preschoolers | 1 300 | 720 | 0 | occasions/christmas | 06/11/2026 | — |
| 1 | classroom-christmas-party-ideas | classroom christmas party ideas | 390 (+880 « christmas game classroom ») | 10 | 0 | occasions/christmas | 06/11/2026 | — |
| 1 | christmas-scavenger-hunt-ideas | christmas scavenger hunt ideas | 1 300 | 140 | 0 | scavenger-hunts | 13/11/2026 | — |
| 1 | valentines-day-classroom-games | valentines day classroom games | 390 | — | 0 | occasions/valentines | 03/01/2027 | cartes d'indices Saint-Valentin |
| 1 | leprechaun-hunt | leprechaun hunt | 390 | 10 | 0 | scavenger-hunts | 03/02/2027 | cartes d'indices + labyrinthe Saint-Patrick |
| 1 | easter-scavenger-hunt-clues | easter scavenger hunt clues | 1 600 | 260 (5 400 sur « easter egg hunt clues ») | 2 | scavenger-hunts | 14/02/2027 | — |
| 1 | bingo-patterns | bingo patterns | 5 400 | 170 | 0 | bingo | — | — |
| 1 | scavenger-hunt-clues | scavenger hunt clues | 3 600 | 390 | 2 | scavenger-hunts | — | (option) cartes d'indices maison |
| 1 | human-bingo | human bingo | 3 600 | 1 000 | 6 | bingo | — | carte « find someone who » |
| 1 | activities-for-4-year-olds | activities for 4 year olds | 2 400 | 590 | 6 | puzzles/mazes/easy | — | — |
| 1 | is-sudoku-good-for-your-brain | is sudoku good for your brain | 1 900 | 260 | 5 | puzzles/sudoku | — | — |
| 1 | how-to-draw-a-maze | how to draw a maze | 1 000 | 140 | 6 | puzzles/mazes | — | — |
| 1 | are-word-searches-good-for-your-brain | are word searches good for your brain | 880 | 170 | 13 | puzzles/word-search | — | mots mêlés gros caractères |
| 1 | early-finisher-activities | early finisher activities | 880 | 20 | 0 | puzzles | — | hub /classroom/ (plus tard) |
| 1 | bingo-prize-ideas | bingo prizes for adults | 480 | 110 | 0 | bingo | — | — |
| 2 | new-years-eve-games-for-family | new years eve games for family | 880 | 170 | 0 | occasions/winter | 19/11/2026 | bingo + mots mêlés Nouvel An |
| 2 | easter-egg-hunt-ideas | easter egg hunt ideas | 1 600 | 1 600 | 0 | occasions/easter | 14/02/2027 | — |
| 2 | birthday-scavenger-hunt | scavenger hunt birthday party | 1 600 | 40 | 0 | scavenger-hunts | — | hub /occasions/birthday/ (plus tard) |
| 2 | indoor-recess-games | indoor recess games | 1 600 | 10 | 0 | rules/pen-and-paper | — | hub /classroom/ (plus tard) |
| 2 | diy-escape-room | diy escape room | 1 000 | 140 | 0 | escape-games | — | kit escape enfants maison |
| 3 | sudoku-strategies | sudoku strategies | 12 100 | 720 | 5 | puzzles/sudoku | — | — |
| 3 | bingo-calls | bingo calls | 9 900 | 9 900 | 4 | bingo | — | tickets bingo 90 boules + feuille d'annonce |
| 3 | how-to-play-bingo | how to play bingo | 8 100 | 2 400 | 8 | bingo | — | tickets bingo 90 boules |
| 3 | brain-games-for-seniors | brain games for seniors | 2 400 | 70 | 17 | puzzles | — | mots mêlés et bingo gros caractères |

Volume mensuel US des 25 mots-clés cibles : **72 790**. Avec les mots-clés secondaires (dédoublonnés) : **154 300**. Volume UK des cibles : 19 050 (porté par `bingo calls` et `how to play bingo`).

## 3. Les 5 meilleurs gains rapides

1. **bingo-patterns** : 5 400 US (+ « blackout bingo » 5 400), KD 0 à 4. Top 5 : catalogues de fournisseurs de bingo et une appli. Aucune page n'est écrite pour un hôte à la maison, en classe ou en maison de retraite. On peut mesurer la durée moyenne de chaque motif en simulant nos propres cartes 1-75 : une vraie donnée maison.
2. **scavenger-hunt-clues** : 3 600 US, KD 2, plus 4 variantes de 590 à 880. Top 5 : un blog de maman, un vieux site mono-sujet, Parade, YouTube, un générateur. Pousse trois chasses du catalogue, dont deux à indices rimés.
3. **human-bingo** : 3 600 US, 1 000 UK, KD 6, plus « get to know you bingo » 1 900 et « find someone who bingo » 1 000 (KD 0). Pousse nos grilles vierges et le bingo de classe. Seul besoin : une carte « find someone who » à imprimer.
4. **is-sudoku-good-for-your-brain** : 1 900 US, KD 5, plus « sudoku for seniors » 1 000 et « benefits of sudoku » 880. Top 5 : Quora (deux fois), le blog d'une agence d'intérim, Facebook, une association australienne. Personne ne cite les études.
5. **activities-for-4-year-olds** : 2 400 US, 590 UK, KD 6. Top 5 : Instagram, Facebook, YouTube, une liste maigre, un blog. Pousse les labyrinthes faciles, les points à relier 10 points et le sudoku 4×4.

Urgences de calendrier (les gains rapides saisonniers) : **thanksgiving-games-for-family** est déjà en retard sur la règle des 6 semaines (Thanksgiving le 26 novembre). À publier cette semaine, il peut encore se positionner sur la fin de la saison. Ensuite viennent les trois articles de Noël : `christmas-activities-for-preschoolers` et `classroom-christmas-party-ideas` avant le 6 novembre, `christmas-scavenger-hunt-ideas` avant le 13 novembre.

## 4. Cibles de croissance (mois suivants)

| Sujet | Pourquoi plus dur | Ce qui le rend jouable |
|---|---|---|
| sudoku-strategies (12 100 US) | Domaines établis (sudoku.com, nytimes sur « sudoku for beginners »), vidéos | Le top 5 sur « sudoku strategies » : YouTube, un PDF, Reddit, Wikipédia, un site ancien. Schémas tirés de nos propres grilles. |
| bingo-calls (9 900 US, 9 900 UK) | Affiliés casino à forte autorité (William Hill, Gala, Wink, LiveScore) | Seule page non liée aux jeux d'argent, avec feuille d'annonce imprimable et outil d'annonce 1-90. Marché UK prioritaire. |
| how-to-play-bingo (8 100 US, 2 400 UK) | Wikipédia et une université dans le top 3 | 75 boules (US) et 90 boules (UK) côte à côte, avec des schémas. |
| brain-games-for-seniors (2 400 US) | Forums Mayo Clinic, A Place for Mom, SERP « puzzles for seniors » pleine de produits | Guide gratuit, sans écran, par capacité (vue, mains, mémoire). Les affirmations sur la santé sont sourcées. |

## 5. Calendrier de publication saisonnier

Règle : en ligne 6 semaines avant l'événement.

| Événement | Date | En ligne avant | Articles |
|---|---|---|---|
| Thanksgiving | 26/11/2026 | 15/10/2026 (dépassé) | thanksgiving-games-for-family |
| Fêtes de classe de Noël / décembre en maternelle | mi-décembre | 06/11/2026 | classroom-christmas-party-ideas, christmas-activities-for-preschoolers |
| Noël | 25/12/2026 | 13/11/2026 | christmas-scavenger-hunt-ideas |
| Nouvel An | 31/12/2026 | 19/11/2026 | new-years-eve-games-for-family |
| Saint-Valentin | 14/02/2027 | 03/01/2027 | valentines-day-classroom-games |
| Saint-Patrick | 17/03/2027 | 03/02/2027 | leprechaun-hunt |
| Pâques | 28/03/2027 | 14/02/2027 | easter-scavenger-hunt-clues, easter-egg-hunt-ideas |

## 6. Contenus à créer pour ces articles (« needs »)

Par ordre d'urgence :

1. **Fiche Thanksgiving n° 4** (points à relier ou set de table à jeux), pour ouvrir `/occasions/thanksgiving/`, qui exige au moins 4 fiches (docs/10).
2. **Bingo et mots mêlés du Nouvel An** (avant le 19/11), puis un hub `/occasions/new-year/` à 4 fiches (le libellé existe déjà dans `taxonomy.ts`).
3. **Carte de human bingo** « find someone who » (versions enfants et adultes) sous `/bingo/`.
4. **Tickets de bingo 90 boules** (format UK 3×9) et **feuille d'annonce des 90 nicknames**, pour `bingo-calls` et `how-to-play-bingo`.
5. **Mots mêlés et bingo gros caractères** pour les seniors (`are-word-searches-good-for-your-brain`, `brain-games-for-seniors`).
6. **Cartes d'indices Saint-Valentin** (avant le 03/01) et **chasse au lutin de la Saint-Patrick** avec un labyrinthe arc-en-ciel ou trèfle (avant le 03/02). Ce sont des créations maison sous CC BY-NC, donc hébergeables.
7. **Kit d'escape game enfants maison** (5 énigmes, 7-10 ans) : il permettrait d'offrir un PDF hébergé et d'ouvrir `/escape-games/kids/`.
8. Plus tard : hubs `/classroom/` et `/occasions/birthday/` prévus dans docs/09 (3 articles de ce lot visent la classe).

## 7. Sujets écartés et pourquoi

| Requête | Volume US / KD | Raison |
|---|---|---|
| dot to dot for adults | 1 600 / 0 | SERP de pages produit (Amazon, imprimables) : c'est le rôle d'une facette `/puzzles/dot-to-dot/`, pas d'un article. |
| road trip bingo, car bingo, 4x4 sudoku | 2 400, 1 600, 1 000 | Intention produit, déjà couverte par nos fiches. |
| sight word games | 5 400 / 1 | Intention « jeu en ligne » (Starfall, applis), hors de notre offre imprimable. |
| fall scavenger hunt, halloween scavenger hunt ideas | 1 300, 480 | Saison passée ou trop tard (Halloween le 31/10). À reprendre en août 2027. |
| riddles for kids | 110 000 / 0 | Pas de lien avec le catalogue. |
| how to make a word search | 1 000 / 43 | KD trop élevé. |
| what is a rebus puzzle, what is a nonogram, how to solve logic grid puzzles | 1 000 / 7, 590 / 17, 390 / 14 | SERP très faibles, mais aucun rébus, nonogramme ni puzzle de logique au catalogue. **Lot suivant**, dès que `/puzzles/rebus/` ou `/puzzles/logic/` existent. |
| license plate game | 3 600 / 0 | Bon sujet (SERP faible), mais demande une fiche à créer et la saison des road trips est en mai. À ajouter au lot de printemps. |
| christmas games for family | 27 100 (volume de grappe) / 0 | SERP de grands médias (Delish, Today) ; recoupe « christmas party games », qui relève du lot B (party games). Laissé au lot B ou à plus tard. |
| bridal shower game ideas, baby shower games | 3 600 / 11, 90 500 | Médias mariage et Pinterest ; ce sont des « party games » (lot B). Nos fiches bingo de shower restent poussées par `bingo-prize-ideas`. |
| games to play in class | 2 900 / 0 | Proche d'`indoor-recess-games` et d'`early-finisher-activities` ; à faire quand le hub `/classroom/` existera. |

## 8. Recoupements avec le lot B

- L'autre agent a aussi relevé la SERP de `diy escape room` et de `escape room puzzles ideas`. Ce lot garde `diy-escape-room` sous l'angle enfants et famille (silo `escape-games`). Il faut choisir un seul propriétaire avant la rédaction pour éviter la cannibalisation.
- `indoor-recess-games` pousse le hub `rules/pen-and-paper` et des pages de règles (dots and boxes, hangman, sprouts) : le sujet relève de la classe, mais les pages poussées appartiennent au silo règles.
- `how-to-play-bingo` est une page de règles. Le bingo est dans ce lot, mais il faut vérifier que le lot B ne prévoit pas de page `/rules/bingo/`.

## 9. Notes pour la rédaction

- Chaque URL de `pushes` existe et est publiée (vérifié par script contre `src/content`). Les kits d'escape et de chasse en français, encore en brouillon, ne sont jamais poussés.
- Les articles santé (sudoku, mots mêlés, seniors) doivent citer des études ouvertes et lues. Le JSON nomme des pistes (par ex. l'étude PROTECT sur les puzzles de chiffres, Brooker et al. 2019) à vérifier avant d'écrire.
- Les formats d'indices sont les mêmes d'un article à l'autre (`scavenger-hunt-clues`, `easter-scavenger-hunt-clues`, `christmas-scavenger-hunt-ideas`, `leprechaun-hunt`, `birthday-scavenger-hunt`). Il faut les relier entre eux et garder des cibles distinctes : indices génériques, Pâques, Noël, Saint-Patrick, anniversaire.
- `easter-scavenger-hunt-clues` doit employer le vocabulaire UK (« easter egg hunt clues » : 5 400 recherches par mois au UK, KD 0).
