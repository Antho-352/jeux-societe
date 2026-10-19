# Sujets de blog B : jeux de société, jeux de cartes, règles et soirées jeux

Plan éditorial du blog pour le périmètre « jeux » (cartes, plateau, dés, roll & write, jeux d'ambiance et de déduction, soirées jeux, fabrication de cartes et de plateaux, escape games ado/adulte). Les puzzles, fêtes, activités enfants et la classe sont traités dans un autre plan. Données DataForSEO du 19 octobre 2026, marché US (2840) sauf mention UK (2826).

Fichier source : `data/blog-topics-b.json` (25 sujets, un objet par article, format décrit dans `BLOG-GUIDE.md`). Données brutes : `data/kw/blog/` (fichiers `ideas_us_*`, `overview_us_1/2`, `b_overview_uk`, `serp_*`, `serp_batch2.txt`, `serp_batch3.txt`).

## 1. Méthode

1. Fouille de `data/kw/keywords-master.csv` : il ne contient presque que des requêtes « printable … » (intention produit, déjà couvertes par les hubs et les fiches), donc peu de sujets de blog dans ce périmètre.
2. Quatre appels `ideas` (80 graines : stratégie, variantes, comparatifs, questions de règles, histoire, fabrication, soirées jeux) → ~15 000 idées, filtrées sur l'intention informationnelle, sans « how to play » ni « rules » (rôle des pages de règles).
3. Deux appels `overview` US sur ~320 candidats (volume, KD, intention, saisonnalité), puis un `overview` UK sur la même liste.
4. 60 SERP US (top 10) : chaque sujet retenu a sa SERP vérifiée ; les 5 premiers domaines et leur type sont notés dans `serp_notes`.
5. Règles appliquées : KD ≤ 25 (un seul sujet au-dessus de 20 : rummy vs gin rummy, KD 21 ; les secondaires « chess origin » KD 41 et « board game design » KD 22 restent secondaires), SERP faible (forums, Reddit, Quora, vidéos, blogs de boutiques), lien réel avec au moins deux pages enfants existantes, aucune cible « X rules » / « how to play X ».

**Anti-cannibalisation.** Chaque article vise une intention que la page de règles ne vise pas : stratégie (« how to win at checkers »), question de règle disputée (« can you stack in uno »), variante (« 2 player spades »), comparatif (« chess vs checkers »), liste (« card games for 3 people »), histoire, fabrication. Chaque article renvoie vers la page de règles par un `ItemCallout`. Deux pages de règles traitent déjà brièvement un sujet de blog (spades à deux joueurs, empilement au UNO en FAQ) : l'article approfondit et la page de règles garde la requête « rules ».

## 2. Synthèse

- **25 sujets** : 19 quick wins (priorité 1), 2 sujets à moyen terme (priorité 2), 4 cibles de croissance (priorité 3).
- **Volume US des mots-clés cibles : 171 160 recherches / mois** ; 328 410 en ajoutant les mots-clés secondaires (attention, certains secondaires sont des variantes proches que Google Ads regroupe, ce total est un plafond). UK : 31 130 / mois sur les cibles.
- KD médian des cibles : 2 ; 18 cibles ont un KD de 0 à 3, 22 un KD ≤ 10.
- Saisonnalité : presque toutes les requêtes de jeux de cartes et de plateau culminent en novembre-janvier (fêtes, visites en famille). 13 articles ont une échéance entre le 1er novembre et le 15 décembre 2026 ; « social deduction games » (49 500 en novembre 2025) et « family game night ideas » sont les plus urgents.

## 3. Tableau des 25 sujets (ordre conseillé de publication)

| # | Slug | Mot-clé cible | Vol. US | Vol. UK | KD | Grappe US | Type | Silo (parent) | Pages poussées | Échéance | Priorité |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `card-games-for-3-people` | card games for 3 people | 9 900 | 1 000 | 0 | 21 560 | liste | `rules/card-games` | `/rules/hearts/`, `/rules/cribbage/`, `/rules/president/`, `/rules/golf/` | 2026-12-01 | 1 · quick win |
| 2 | `how-many-cards-in-a-deck` | how many cards in a deck | 49 500 | 8 100 | 10 | 64 390 | explication | `card-games` | `/card-games/printable-playing-card-deck/`, `/rules/uno/`, `/rules/canasta/`, `/rules/euchre/` | – | 1 · quick win |
| 3 | `how-to-win-tic-tac-toe` | how to win tic tac toe | 8 100 | 1 300 | 0 | 11 230 | stratégie | `rules/pen-and-paper` | `/rules/tic-tac-toe/`, `/rules/sim/`, `/rules/dots-and-boxes/` | – | 1 · quick win |
| 4 | `types-of-solitaire` | types of solitaire | 1 300 | 110 | 0 | 7 270 | liste | `board-games/solo` | `/rules/klondike-solitaire/`, `/card-games/orchard-9-card-solitaire/`, `/card-games/mini-rogue-print-and-play/`, `/card-games/bismarck-s-dance/` | – | 1 · quick win |
| 5 | `how-to-win-at-checkers` | how to win at checkers | 3 600 | 260 | 0 | 6 170 | stratégie | `rules/board-games` | `/rules/checkers/`, `/board-games/printable-checkerboard/` | 2026-12-01 | 1 · quick win |
| 6 | `can-you-stack-in-uno` | can you stack in uno | 1 600 | 140 | 3 | 8 360 | explication | `rules/card-games` | `/rules/uno/`, `/rules/crazy-eights/` | 2026-11-30 | 1 · quick win |
| 7 | `how-to-make-a-paper-dice` | how to make a paper dice | 1 300 | 210 | 1 | 5 200 | tutoriel | `dice-games` | `/dice-games/printable-shut-the-box-game/`, `/dice-games/goblin-teeth/`, `/rules/pig/` | 2027-04-15 | 1 · quick win |
| 8 | `mancala-strategy` | mancala strategy | 1 600 | 90 | 0 | 3 820 | stratégie | `rules/board-games` | `/rules/mancala/`, `/board-games/printable-mancala-board/` | 2026-12-01 | 1 · quick win |
| 9 | `card-games-for-seniors` | card games for seniors | 1 000 | 30 | 0 | 3 330 | liste | `rules/card-games` | `/rules/rummy/`, `/rules/canasta/`, `/rules/cribbage/`, `/card-games/printable-playing-card-deck/` | – | 1 · quick win |
| 10 | `diy-escape-room` | diy escape room | 1 000 | 140 | 0 | 3 320 | tutoriel | `escape-games` | `/escape-games/escape-team-instant-escape-room-kit/`, `/escape-games/the-secret-of-langton-manor-episode-1-legacy/`, `/escape-games/unlock-demo-the-temple-of-ra/` | 2026-12-10 | 1 · quick win |
| 11 | `chess-vs-checkers` | chess vs checkers | 1 900 | 140 | 0 | 3 200 | comparatif | `board-games/2-player` | `/board-games/printable-chess-board/`, `/board-games/printable-checkerboard/`, `/rules/chess/`, `/rules/checkers/` | – | 1 · quick win |
| 12 | `family-game-night-ideas` | family game night ideas | 1 300 | 140 | 3 | 4 670 | liste | `party-games` | `/party-games/dixit-print-and-play/`, `/card-games/spot-it-dobble-print-and-play-demo/`, `/card-games/timeline-classic-print-and-play-demo/`, `/party-games/printable-heads-bodies-and-legs-game/` | 2026-11-10 | 1 · quick win |
| 13 | `2-player-spades` | 2 player spades | 1 900 | 20 | 1 | 2 760 | guide | `rules/card-games` | `/rules/spades/`, `/rules/hearts/` | 2026-12-15 | 1 · quick win |
| 14 | `how-to-win-connect-4` | how to win connect 4 | 3 600 | 720 | 14 | 12 580 | stratégie | `rules/board-games` | `/rules/connect-four/`, `/rules/tic-tac-toe/`, `/rules/reversi/` | 2026-12-01 | 1 · quick win |
| 15 | `yahtzee-strategy` | yahtzee strategy | 480 | 140 | 0 | 1 840 | stratégie | `rules/dice-games` | `/rules/yacht/`, `/rules/farkle/` | 2026-12-10 | 1 · quick win |
| 16 | `how-to-win-at-uno` | how to win at uno | 1 900 | 320 | 2 | 2 610 | stratégie | `rules/card-games` | `/rules/uno/`, `/rules/crazy-eights/` | 2026-11-30 | 1 · quick win |
| 17 | `who-goes-first-in-chess` | who goes first in chess | 2 400 | 390 | 3 | 2 890 | explication | `rules/board-games` | `/rules/chess/`, `/rules/checkers/`, `/board-games/printable-chess-board/` | 2026-12-01 | 1 · quick win |
| 18 | `backgammon-strategy` | backgammon strategy | 1 300 | 210 | 4 | 1 800 | stratégie | `rules/board-games` | `/rules/backgammon/`, `/board-games/printable-backgammon-board/` | – | 1 · quick win |
| 19 | `how-to-make-a-card-game` | how to make a card game | 880 | 110 | 9 | 1 840 | tutoriel | `card-games` | `/card-games/printable-playing-card-deck/`, `/card-games/love-letter-print-and-play/`, `/card-games/scuttle/` | – | 1 · quick win |
| 20 | `how-to-make-a-board-game` | how to make a board game | 2 400 | 320 | 10 | 14 560 | tutoriel | `board-games` | `/board-games/piecepack/`, `/board-games/printable-snakes-and-ladders/`, `/board-games/printable-pachisi-board/`, `/board-games/garden-builder/` | 2027-03-31 | 2 · moyen terme |
| 21 | `rummy-vs-gin-rummy` | rummy vs gin rummy | 2 400 | 170 | 21 | 4 430 | comparatif | `rules/card-games` | `/rules/rummy/`, `/rules/gin-rummy/`, `/rules/canasta/`, `/rules/phase-10/` | – | 2 · moyen terme |
| 22 | `2-player-card-games` | 2 player card games | 40 500 | 14 800 | 0 | 89 000 | liste | `rules/card-games` | `/rules/gin-rummy/`, `/rules/cribbage/`, `/rules/speed/`, `/card-games/love-letter-print-and-play/` | 2026-12-01 | 3 · croissance |
| 23 | `social-deduction-games` | social deduction games | 14 800 | 390 | 2 | 17 140 | liste | `party-games` | `/party-games/secret-hitler/`, `/party-games/two-rooms-and-a-boom/`, `/party-games/hidden-panda/`, `/card-games/dracula-s-feast/` | 2026-11-01 | 3 · croissance |
| 24 | `trick-taking-card-games` | trick taking card games | 12 100 | 880 | 3 | 13 370 | explication | `rules/card-games` | `/rules/spades/`, `/rules/hearts/`, `/rules/euchre/`, `/rules/whist/` | – | 3 · croissance |
| 25 | `history-of-chess` | history of chess | 4 400 | 1 000 | 16 | 21 070 | histoire | `rules/board-games` | `/rules/chess/`, `/board-games/printable-chess-board/`, `/board-games/printable-chinese-chess/`, `/board-games/printable-shogi/` | – | 3 · croissance |

Ordre : priorité, puis volume de la grappe pondéré par la difficulté (volume / (KD + 10)²). « Grappe US » = cible + secondaires.

## 4. Les 5 meilleurs quick wins

- **`card-games-for-3-people`** (card games for 3 people, 9 900 US, KD 0). Top 5: boardgamegeek.com (2 forum threads), gamerules.com (list), betus.com.pa (casino site), reddit.com; Pinterest next. Mostly forum threads and a gambling site; only one real list, with no per-game adjustments for three players.
- **`how-to-win-tic-tac-toe`** (how to win tic tac toe, 8 100 US, KD 0). Top 5: reddit.com (r/howto thread), instructables.com, facebook.com (video), quora.com, a Monash University PDF; then a Medium post. Only forums, a video and a lecture PDF: no clear written guide with diagrams. AI overview and videos above, but the organic block is weak.
- **`how-many-cards-in-a-deck`** (how many cards in a deck, 49 500 US, KD 10). Top 5: facebook.com (post), reddit.com, geeksforgeeks.org, facebook.com, boardgamegeek.com wiki; playiro.com next. No AI overview and no featured snippet at the time of the check (People Also Ask only). Very weak for a 49,500/month query.
- **`can-you-stack-in-uno`** (can you stack in uno, 1 600 US, KD 3). Top 5: letsplayuno.com (mobile game), reddit.com, unorules.com, youtube.com, instagram.com; facebook.com next. Social posts and one fan rules site; a single clear page with the official text and the house-rule options does not exist.
- **`how-to-win-at-checkers`** (how to win at checkers, 3 600 US, KD 0). Top 5: reddit.com, thesprucecrafts.com, fitandfunplayscapes.com (playground maker, rules page), youtube.com, bobnewell.net (old personal site); 247checkers.com next. Weak: one craft magazine, the rest forums, videos and old pages.

## 5. Cibles de croissance (priorité 2 et 3)

- **`how-to-make-a-board-game`** (2 400 US, KD 10) : Top 5: bransonboardgamecafe.com (cafe blog), youtube.com, gamestructor.com (software), reddit.com, youtube.com; creativity.org next. Weak on paper, but the topic is broad and 'board game design' (KD 22) is contested by design schools.
- **`rummy-vs-gin-rummy`** (2 400 US, KD 21) : Top 5: ginrummy-palace.com (online game), en.wikipedia.org, reddit.com, euchre.com (game site), bicyclecards.com; youtube.com next. Wikipedia and two game sites with short pages; KD 21 is the highest in this list.
- **`2-player-card-games`** (40 500 US, KD 0) : Top 5: vanishingincmagic.com (magic shop blog), boardgamegeek.com (list), reddit.com, youtube.com, donteatthemeeples.com; youtube.com next. Weak today, but 40,500 a month will attract stronger players (Bicycle, The Spruce); treat as a growth target.
- **`social-deduction-games`** (14 800 US, KD 2) : Top 5: boardgamegeek.com (ranking thread), en.wikipedia.org, reddit.com, screenhype.co.uk (listicle), jackboxgames.com; amazon.com next. A mix of Wikipedia, hobby lists and a shop: harder, but KD stays at 2.
- **`trick-taking-card-games`** (12 100 US, KD 3) : Top 5: whatsericplaying.com (hobby blog), whatboardgame.com, en.wikipedia.org, opinionatedgamers.com, reddit.com; boardgamegeek.com next. Hobby blogs ranking modern boxed trick-takers; our classic-deck angle is a partial intent match, hence growth.
- **`history-of-chess`** (4 400 US, KD 16) : Top 5: artsandculture.google.com (×2), quora.com, youtube.com, officialstaunton.com (shop blog); reddit.com next. Google Arts & Culture and Wikipedia-type authority sit on the query; 'chess origin' has KD 41. Growth target.

## 6. Pages nouvelles à créer (« needs »)

- Rules page: Oh Hell / Up and Down the River (3 to 7 players, a classic 3-player trick-taker): measure volume first (article `card-games-for-3-people`)
- Rules pages: Spider Solitaire, FreeCell, Pyramid Solitaire, Golf Solitaire (volumes to measure; the article can launch with Klondike only) (article `types-of-solitaire`)
- Printable page: paper dice templates (d6 with pips, d6 with numbers, blank d6, d4, d8, d12, d20 nets), our own drawings (article `how-to-make-a-paper-dice`)
- Game page: large-print playing card deck (own design, free to print); 'large print playing cards' 480 US and 'large print poker cards' 480 in keywords-master.csv (article `card-games-for-seniors`)
- Printable page: blank 7×6 'four in a row' grid (generic name, Connect Four is a trademark) to play with two colours of pens or counters (article `how-to-win-connect-4`)
- Printable page: blank board game template (track board + blank cards), 'blank board game template' 880 US in docs/08 (article `how-to-make-a-board-game`)
- Rules page: Spit / Russian Bank ('2 player solitaire' 480 US, KD 0) (article `2-player-card-games`)
- Rules page: Oh Hell (shared with card-games-for-3-people) (article `trick-taking-card-games`)
- Hors liste, relevé pendant l'étude : fiches **Royal Game of Ur** (5 400 US, KD 15, UK 1 300) et **Senet** (6 600 US, KD 23) avec plateau imprimable et règles : deux jeux du domaine public, SERP faible pour Ur (mastersofgames, Reddit, YouTube). Elles serviraient aussi l'article de réserve « oldest board games in the world ».

## 7. Réserve (sujets validés, non retenus dans les 25)

Tous vérifiés en `overview` et en SERP. À programmer après les 25 sujets ou à fusionner.

| Mot-clé | Vol. US | Vol. UK | KD | Secondaires (vol. US, KD) | Silo | Pages poussées |
|---|---|---|---|---|---|---|
| mancala history | 2 400 | 110 | 2 | history of mancala (2 400, 4); how to make a mancala board (260, 0) | `board-games/printable-boards` | /board-games/printable-mancala-board/, /rules/mancala/ |
| escape room puzzles ideas | 2 400 | 480 | 0 | escape room puzzles for adults (90, 0) | `escape-games` | kits escape-games |
| 2 player euchre | 1 000 | 10 | 0 | euchre for two players (880, 1) | `rules/card-games` | /rules/euchre/ |
| euchre strategy | 880 | 10 | 0 | – | `rules/card-games` | /rules/euchre/ |
| shooting the moon hearts | 720 | 70 | 0 | hearts strategy (390, 0); how to win at hearts (140, 0) | `rules/card-games` | /rules/hearts/ |
| cribbage strategy | 590 | 40 | 0 | cribbage strategy tips (170, 0) | `rules/card-games` | /rules/cribbage/, /board-games/printable-cribbage-board/ |
| spades strategy | 390 | 10 | 0 | how to win at spades (320, 4) | `rules/card-games` | /rules/spades/ |
| othello strategy | 390 | 50 | 2 | reversi strategy (390, 0); how to win at othello (390, 0) | `rules/board-games` | /rules/reversi/, /board-games/printable-reversi-board/ |
| chinese checkers strategy | 480 | 40 | 5 | how to win at chinese checkers (260, 0) | `rules/board-games` | /rules/chinese-checkers/, /board-games/printable-chinese-checkers/ |
| go vs chess | 590 | 70 | 0 | shogi vs chess (720, 3); go vs shogi (210, 0) | `board-games/printable-boards` | /rules/go/, /board-games/printable-shogi/ |
| 2 player dice games | 1 000 | 70 | 0 | two player dice games (1 000, 0); dice games for adults (1 900, 6); dice games with 5 dice (1 300, 12) | `rules/dice-games` | /rules/pig/, /rules/liars-dice/, /dice-games/goblin-teeth/ |
| card games for large groups | 720 | 70 | 0 | games for large groups of adults (880, 11) | `rules/card-games` | /rules/spoons/, /rules/cheat/, /rules/president/ |
| oldest board games in the world | 390 | 90 | 7 | oldest board game (1 000, 16); ancient board games (720, 14); history of backgammon (1 600, 16) | `board-games/printable-boards` | plateaux imprimables + besoin Ur et Senet |
| is solitaire always winnable | 390 | 50 | 4 | solitaire odds of winning (320, 10) | `rules/card-games` | /rules/klondike-solitaire/ |
| best solo board games | 1 900 | 720 | 0 | solo board games (2 400, 0); single player board games for adults (210, 0) | `board-games/solo` | jeux solo PnP |
| mahjong history | 1 900 | 140 | 15 | mahjong origin (1 900, 15); history of mahjong (1 300, 19) | `rules` | /rules/mahjong/ |
| game night for adults | 1 900 | 210 | 8 | game night games (6 600, 18); game night ideas (1 300, 11) | `party-games` | jeux d'ambiance |
| how to win at dominoes | 880 | 210 | 0 | dominoes strategy (480, 0) | `rules` | /rules/dominoes/ |
| best roll and write games | 170 | 50 | 0 | what is a roll and write game (40, 0) | `roll-and-write` | roll & write PnP |

Les 19 sujets de réserve ont tous une SERP vérifiée (fichiers `serp_*.json`) : forums, vidéos, blogs de boutiques ou de sites de jeu en ligne, comme pour les 25 retenus.

## 8. Écartés

- **card games for couples** (12 100 US, KD 1) : la SERP montre des jeux de questions pour couples (dssgames, nemlys, Amazon), pas des jeux de cartes à deux : intention différente.
- **how to shuffle cards** (9 900, KD 2) : SERP vidéo, aucun lien avec le catalogue.
- **chess openings for beginners** (5 400, KD 6) : dominé par chess.com et les sites d'échecs, aucun avantage pour nous.
- **card sleeves**, **dragon shield sleeves**, **cardstock for playing cards** : intention transactionnelle (produits).
- **werewolf game** (74 000, KD 35), **mafia party game** (8 100, KD 27) : trop génériques ; couverts en secondaire par l'article social deduction.
- **how many cards in a uno deck** (9 900) n'a pas d'article propre : il est secondaire de l'article sur le paquet de cartes, pour ne pas concurrencer la page de règles UNO.
- Tout ce qui est « how to play X » / « X rules » : rôle des 51 pages de règles.

## 9. Coût DataForSEO

Environ **0,63 $** : 4 appels `ideas` (≈ 0,09 $ chacun), 4 appels `overview` (≈ 0,04 $ chacun : 2 US, 2 UK dont un refait, voir ci-dessous), 60 SERP à 0,002 $.

Incident : le répertoire scratchpad est partagé avec l'agent « puzzles » ; mon fichier de candidats a été écrasé par le sien et un premier `overview` UK a porté sur ses mots-clés. Il a été supprimé et refait sur ma liste (`b_overview_uk.json`, préfixe `b_` pour éviter la collision). Les fichiers `ideas-*-us.json`, `overview-cands-us.json`, `kd-kids-us.json`, `volume-kids-us.json` et `serp/` de `data/kw/blog/` appartiennent à l'autre agent.

## 10. Rappels pour la rédaction

- Chaque chiffre de l'angle marqué « to be sourced » / « to be checked » doit être vérifié sur une source ouverte et citée dans `sources` (règle de la maison : ne rien inventer).
- UNO, Yahtzee, Connect Four et Monopoly sont des marques : on les nomme (usage descriptif), on ne propose pas de matériel imprimable à leur nom ; les tirages imprimables passent par les équivalents génériques (Yacht, grille « four in a row »).
- Les articles « how-to-make-a-paper-dice » et « family-game-night-ideas » touchent le public familial : l'angle reste la soirée jeux, pour ne pas empiéter sur le plan « activités enfants ».
