# Sujets de blog C : sélections « best of », « games like X » et alternatives

Troisième famille d'articles du blog : les sélections (« board games for couples », « games like Catan », « games like Monopoly », « games to play without anything »…). Périmètre voulu par Anthony : les jeux de société et les escape games ; chaque article recommande de vrais jeux, du commerce (liens affiliés possibles plus tard) et gratuits à imprimer, et pousse au moins 3 pages existantes du site. Données DataForSEO du **19 octobre 2026**, marché US (2840), volumes UK (2826) pour la liste retenue.

Fichier source : `data/blog-topics-c.json` (24 sujets, même format que `data/blog-topics-b.json`, décrit dans `BLOG-GUIDE.md`). Données brutes : `data/kw/blog-c/` (`ideas_us_*`, `overview_us_1/2/3`, `overview_uk_1/2`, `serp_us_<requête>.json/.tsv`).

## 1. Méthode

1. Trois appels `ideas` US (60 graines : « games like » + 20 jeux connus, « best … » / couples / coopératif / adultes / famille / voyage / sans matériel / papier-crayon, escape games et jeux d'enquête) → ~11 000 idées, filtrées sur les formes « best X », « games like X », « X alternatives », « X without Y » et les jeux de société (pas d'applis, pas de jeux vidéo, pas de lieux d'escape game).
2. `overview` US sur 222 candidats (volume, KD, intention, saisonnalité), complété par deux petits appels ; `overview` UK sur les 94 mots-clés retenus.
3. 45 SERP US (top 10) : chaque cible retenue a sa SERP vérifiée, ainsi que les variantes dont il fallait savoir si elles partagent la SERP (date night games, board games for 6 year olds, filler games, travel board games, best 2 player board games, fun games to play on paper…).
4. Règles appliquées : KD ≤ 10 pour les cibles (maximum 9, « abstract strategy board games ») ; SERP battable (forums, Reddit, Facebook, BGG en fil de discussion, blogs de boutiques ou de lieux, petites listes) ; au moins 3 pages existantes et publiées à pousser (vérifié par script sur `src/content/games` et `src/content/rules`, brouillons exclus) ; une part réelle de jeux gratuits imprimables dans la réponse ; aucune cible déjà visée par un hub ou par les plans A et B.

**Attention au KD.** Presque toutes les requêtes « best / games like » ont un KD DataForSEO de 0 : le KD ne discrimine pas ici, c'est la lecture des SERP qui a fait le tri (priorité 3 quand des médias forts sont présents : Wargamer, IGN, Shut Up & Sit Down, Wirecutter, BGG en force).

**Anti-cannibalisation.**
- Hubs : `/board-games/2-player/` garde « print and play games for 2 players » et **best 2 player board games** (6 600 US, KD 0 ; SERP boardgamequest, BGG, zatu) ; l'article couples ne vise que l'intention couple / date night. `/rules/pen-and-paper/` garde **pen and paper games** (2 900, KD 31) et **fun games to play on paper** (9 900, KD 5 ; SERP papermate, Quora, Wikipedia « paper-and-pencil game ») : à ajouter comme secondaire du hub, pas d'article. `/escape-games/` garde **escape room at home** / **escape room games at home** (1 300 chacun ; SERP mixte : escape rooms virtuels, kits imprimables, DIY) : à ajouter au hub. `/board-games/kids/` garde « print and play games for kids » (l'article vise l'âge : « board games for 5 year olds »).
- Plans A et B : chaque article renvoie vers ses voisins sans viser leur mot-clé (games-like-uno ↔ can-you-stack-in-uno / how-to-win-at-uno ; games-like-tic-tac-toe ↔ how-to-win-tic-tac-toe ; games-like-yahtzee ↔ yahtzee-strategy ; board-games-for-3-players ↔ card-games-for-3-people ; board-games-for-seniors ↔ card-games-for-seniors et brain-games-for-seniors ; board-games-for-large-groups et games-like-clue ↔ social-deduction-games ; escape-room-board-games ↔ diy-escape-room).
- Entre articles de ce plan : games-like-clue (déduction compétitive, familiale) et mystery-board-games (enquêtes coopératives, silo escape) poussent des pages différentes ; games-like-chess (famille des échecs) et abstract-strategy-board-games (autres familles abstraites) aussi.

## 2. Synthèse

- **24 sujets** : 19 quick wins (priorité 1), 2 à moyen terme (priorité 2), 3 cibles de croissance (priorité 3).
- **Volume US des cibles : 93 190 recherches / mois** ; 136 860 avec les secondaires (les variantes que Google Ads regroupe au même volume, marquées `note` dans le JSON, ne sont pas additionnées). Quick wins seuls : 31 450 sur les cibles, 60 740 avec les secondaires. UK : 11 360 / mois sur les cibles.
- KD médian des cibles : 0 ; 21 cibles ont un KD de 0 à 3.
- Silos : 15 articles poussent le silo jeux de société (`board-games`, `printable-boards`, `2-player`, `kids`, `solo`), 2 le silo escape games (escape-room-board-games, mystery-board-games) ; mystery, couples, coopératif et adultes poussent aussi des pages escape.
- Saisonnalité : presque tout culmine en novembre-décembre (cadeaux, fêtes). 19 articles ont une échéance entre le 15 novembre et le 1er décembre 2026 ; les plus urgents : escape-room-board-games (9 900 en décembre 2025), board-games-for-couples (8 100 de novembre à janvier, Saint-Valentin ensuite), games-like-catan, games-like-monopoly, cooperative-board-games.
- Deux volumes à prendre avec prudence : **cooperative board games** (moyenne 40 500 tirée par un pic à 74 000 fin 2025, 5 400 en septembre 2026) et **abstract strategy board games** (moyenne 14 800, moins de 300/mois avant 2025, pic à 40 500 en décembre 2025). Ce sont des cibles de croissance, pas des quick wins.

## 3. Tableau des 24 sujets (ordre conseillé de publication)

| # | Slug | Mot-clé cible | Vol. US | Vol. UK | KD | Grappe US | Type | Silo (parent) | Pages poussées | Échéance | Priorité |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `board-games-for-couples` | board games for couples | 4 400 | 720 | 0 | 10 480 | liste | `board-games/2-player` | `/party-games/choose-two/`, `/card-games/love-letter-print-and-play/`, `/board-games/pandemic-hot-zone-north-america-print-and-play/`, `/escape-games/unlock-demo-the-temple-of-ra/`, `/board-games/printable-backgammon-board/` | 2026-11-15 | 1 · quick win |
| 2 | `games-like-catan` | games like catan | 1 900 | 320 | 0 | 2 780 | liste | `board-games` | `/board-games/carcassonne-print-and-play-demo/`, `/card-games/citadels-print-and-play-demo/`, `/board-games/pandemic-hot-zone-north-america-print-and-play/`, `/board-games/kingdomino-the-court/` | 2026-11-15 | 1 · quick win |
| 3 | `games-like-monopoly` | games like monopoly | 590 | 170 | 0 | 1 700 | liste | `board-games` | `/card-games/unfair-base-game/`, `/board-games/printable-pachisi-board/`, `/rules/ludo/`, `/dice-games/goblin-teeth/` | 2026-11-15 | 1 · quick win |
| 4 | `games-like-uno` | games like uno | 1 300 | 590 | 0 | 2 600 | liste | `rules/card-games` | `/rules/crazy-eights/`, `/rules/phase-10/`, `/rules/skip-bo/`, `/card-games/scuttle/`, `/card-games/ninjitsu/` | 2026-11-30 | 1 · quick win |
| 5 | `games-like-clue` | games like clue | 590 | 140 | 0 | 4 450 | liste | `board-games` | `/card-games/dracula-s-feast/`, `/card-games/night-of-the-mummy/`, `/card-games/love-letter-print-and-play/`, `/board-games/printable-battleship-board/` | 2026-11-30 | 1 · quick win |
| 6 | `mystery-board-games` | mystery board games | 1 900 | 170 | 2 | 4 480 | comparatif | `escape-games` | `/escape-games/the-secret-of-langton-manor-episode-1-legacy/`, `/escape-games/unlock-demo-the-elite/`, `/escape-games/unlock-demo-the-ghost-stone/`, `/escape-games/escape-team-training-mission-and-central-station/` | 2026-11-30 | 1 · quick win |
| 7 | `games-like-chess` | games like chess | 1 300 | 390 | 0 | 2 020 | liste | `board-games/printable-boards` | `/board-games/printable-chinese-chess/`, `/board-games/printable-shogi/`, `/board-games/printable-the-jungle-game/`, `/board-games/printable-fox-and-geese/`, `/board-games/printable-checkerboard/` | – | 1 · quick win |
| 8 | `games-like-tic-tac-toe` | games like tic tac toe | 720 | 50 | 3 | 990 | liste | `rules/pen-and-paper` | `/board-games/printable-three-mens-morris/`, `/rules/connect-four/`, `/rules/sim/`, `/board-games/printable-go-board-9x9/`, `/rules/dots-and-boxes/` | – | 1 · quick win |
| 9 | `games-like-yahtzee` | games like yahtzee | 320 | 40 | 0 | 410 | liste | `rules/dice-games` | `/rules/yacht/`, `/rules/farkle/`, `/dice-games/printable-shut-the-box-game/`, `/roll-and-write/hall-of-the-dwarven-king/`, `/roll-and-write/hide-nor-hare/` | 2026-11-30 | 1 · quick win |
| 10 | `games-like-sorry` | games like sorry | 390 | 10 | 0 | 880 | liste | `board-games/printable-boards` | `/board-games/printable-pachisi-board/`, `/rules/ludo/`, `/board-games/printable-chinese-checkers/`, `/board-games/printable-snakes-and-ladders/`, `/board-games/printable-backgammon-board/` | 2026-11-30 | 1 · quick win |
| 11 | `games-like-exploding-kittens` | games like exploding kittens | 480 | 210 | 0 | 480 | liste | `card-games` | `/card-games/brains/`, `/card-games/ninjitsu/`, `/card-games/scuttle/`, `/card-games/village-pillage/`, `/dice-games/goblin-teeth/` | 2026-11-30 | 1 · quick win |
| 12 | `games-like-codenames` | games like codenames | 480 | 90 | 3 | 480 | liste | `party-games` | `/party-games/concept-print-and-play-demo/`, `/party-games/dixit-print-and-play/`, `/party-games/show-tile/`, `/party-games/printable-quick-on-the-draw/` | 2026-11-30 | 1 · quick win |
| 13 | `games-like-risk` | games like risk | 1 000 | 170 | 0 | 2 320 | liste | `board-games` | `/board-games/bloc-by-bloc-uprising/`, `/board-games/printable-siege-of-paris/`, `/board-games/the-fantasy-trip-melee/`, `/board-games/small-world-lost-tribes-crusade/` | 2026-11-30 | 1 · quick win |
| 14 | `games-to-play-without-anything` | games to play with friends without anything | 5 400 | 1 300 | 0 | 9 390 | liste | `rules/pen-and-paper` | `/rules/dots-and-boxes/`, `/rules/sprouts/`, `/rules/hangman/`, `/rules/sim/`, `/party-games/printable-heads-bodies-and-legs-game/` | 2026-11-20 | 1 · quick win |
| 15 | `escape-room-board-games` | escape room board games | 3 600 | 1 000 | 0 | 5 860 | comparatif | `escape-games` | `/escape-games/unlock-demo-the-temple-of-ra/`, `/escape-games/unlock-demo-5th-avenue/`, `/escape-games/the-secret-of-langton-manor-episode-1-legacy/`, `/escape-games/escape-team-training-mission-and-central-station/` | 2026-11-15 | 1 · quick win |
| 16 | `board-games-for-seniors` | board games for seniors | 1 600 | 140 | 0 | 1 600 | liste | `board-games/printable-boards` | `/board-games/printable-crossword-game-with-friends/`, `/board-games/printable-checkerboard/`, `/board-games/printable-cribbage-board/`, `/board-games/printable-backgammon-board/`, `/rules/dominoes/` | – | 1 · quick win |
| 17 | `board-games-for-5-year-olds` | board games for 5 year olds | 3 600 | 1 900 | 0 | 5 500 | liste | `board-games/kids` | `/board-games/printable-snakes-and-ladders/`, `/board-games/printable-pachisi-board/`, `/board-games/printable-mancala-board/`, `/card-games/spot-it-dobble-print-and-play-demo/`, `/card-games/bandido-covid-19-edition/` | 2026-11-30 | 1 · quick win |
| 18 | `board-games-for-3-players` | board games for 3 players | 1 000 | 260 | 0 | 1 720 | liste | `board-games` | `/board-games/carcassonne-print-and-play-demo/`, `/card-games/citadels-print-and-play-demo/`, `/dice-games/goblin-teeth/`, `/card-games/village-pillage/`, `/board-games/printable-chinese-checkers/` | 2026-12-01 | 1 · quick win |
| 19 | `games-to-play-on-a-plane` | games to play on a plane | 880 | 320 | 5 | 2 600 | liste | `board-games/solo` | `/card-games/orchard-9-card-solitaire/`, `/card-games/mini-rogue-print-and-play/`, `/dice-games/under-falling-skies-9-card-solo-game/`, `/card-games/zombie-in-my-pocket/`, `/rules/dots-and-boxes/` | 2026-11-20 | 1 · quick win |
| 20 | `board-games-for-large-groups` | board games for large groups | 720 | 110 | 0 | 1 440 | liste | `party-games` | `/party-games/two-rooms-and-a-boom/`, `/party-games/concept-print-and-play-demo/`, `/card-games/meow/`, `/party-games/secret-hitler/`, `/party-games/dixit-print-and-play/` | 2026-11-30 | 2 · moyen terme |
| 21 | `quick-board-games` | quick board games | 320 | 90 | 0 | 910 | liste | `board-games` | `/card-games/love-letter-print-and-play/`, `/card-games/spot-it-dobble-print-and-play-demo/`, `/card-games/ninjitsu/`, `/board-games/the-closest-ghost/`, `/board-games/printable-three-mens-morris/` | – | 2 · moyen terme |
| 22 | `cooperative-board-games` | cooperative board games | 40 500 | 720 | 4 | 45 430 | liste | `board-games` | `/board-games/pandemic-hot-zone-north-america-print-and-play/`, `/card-games/bandido-covid-19-edition/`, `/board-games/bloc-by-bloc-uprising/`, `/escape-games/the-secret-of-langton-manor-episode-1-legacy/`, `/escape-games/unlock-demo-the-temple-of-ra/` | 2026-11-15 | 3 · croissance |
| 23 | `best-board-games-for-adults` | best board games for adults | 5 400 | 2 400 | 0 | 13 500 | liste | `board-games` | `/party-games/secret-hitler/`, `/card-games/citadels-print-and-play-demo/`, `/card-games/unfair-base-game/`, `/party-games/dixit-print-and-play/`, `/board-games/pandemic-hot-zone-north-america-print-and-play/` | 2026-11-30 | 3 · croissance |
| 24 | `abstract-strategy-board-games` | abstract strategy board games | 14 800 | 50 | 9 | 14 840 | liste | `board-games/printable-boards` | `/board-games/printable-go-board-9x9/`, `/board-games/printable-reversi-board/`, `/board-games/printable-nine-mens-morris/`, `/board-games/printable-mancala-board/`, `/board-games/icetoids/` | – | 3 · croissance |

Ordre : priorité, puis urgence saisonnière et volume. « Grappe US » = cible + secondaires (hors variantes regroupées par Google Ads). « Type » : liste ou comparatif (`article_type` = `list` / `comparison` dans le JSON).

## 4. Les 10 meilleurs sujets

| Slug | Mot-clé | Vol. US | KD | Angle en une phrase |
|---|---|---|---|---|
| `board-games-for-couples` | board games for couples | 4 400 (grappe 10 480) | 0 | Classés par type de couple (compétitif, coopératif, enquête) et par durée, chacun avec une option gratuite à imprimer ce soir (Choose Two, Love Letter, Pandemic Hot Zone, démo Unlock). |
| `games-to-play-without-anything` | games to play with friends without anything | 5 400 (grappe 9 390) | 0 | La demande « sans matériel » d'Anthony : 20 jeux sans rien (devinettes, mots, Mafia sans cartes), puis « avec un crayon » vers nos pages de règles papier. SERP 100 % forums. |
| `escape-room-board-games` | escape room board games | 3 600 (grappe 5 860) | 0 | Comparatif des séries (Exit, Unlock, Deckscape, Escape Tales…) avec les démos gratuites pour tester le système avant d'acheter ; pic de 9 900 en décembre. |
| `board-games-for-5-year-olds` | board games for 5 year olds | 3 600 (grappe 5 500) | 0 | Ce qu'un enfant de 5 ans sait faire, premiers jeux coopératifs, classiques imprimables (Serpents et échelles, Pachisi, Mancala) ; fusionné avec « 6 year olds ». |
| `mystery-board-games` | mystery board games | 1 900 (grappe 4 480) | 2 | Typologie (livres d'enquête, enquêtes avec appli, boîtes d'escape, kits de murder party) avec tableau comparatif et une enquête gratuite par type ; pousse le silo escape. |
| `games-like-clue` | games like clue | 590 (grappe 4 450) | 0 | La déduction expliquée, puis des jeux qui la font mieux ou plus vite, dont Dracula's Feast et Night of the Mummy gratuits ; « deduction board games » (3 600) en secondaire. |
| `games-like-catan` | games like catan | 1 900 (grappe 2 780) | 0 | Partir de ce qu'on aime dans Catan (échanges, moteur de ressources, carte) et recommander par goût, avec les démos Carcassonne, Citadels et Pandemic à imprimer. |
| `games-like-uno` | games like uno | 1 300 (grappe 2 600) | 0 | UNO descend du Crazy Eights : alternatives avec un jeu de 52 cartes, cousins Mattel (Phase 10, Skip-Bo), puis jeux de cartes gratuits (Scuttle, Ninjitsu). |
| `games-like-risk` | games like risk | 1 000 (grappe 2 000) | 0 | Classés selon le défaut de Risk qu'ils corrigent (durée, élimination, hasard), avec des wargames gratuits (Bloc by Bloc sous CC, Siege of Paris, Melee). |
| `games-like-monopoly` | games like monopoly | 590 (grappe 1 700) | 0 | La demande « alternatives au Monopoly » : classées par défaut corrigé, Unfair gratuit pour le thème, plateaux Pachisi et Ludo pour la nostalgie, et l'histoire du Landlord's Game. SERP polluée par l'appli Monopoly GO. |

## 5. Cibles de croissance (priorité 2 et 3)

- **`board-games-for-large-groups`** (720 US, KD 0) et **`quick-board-games`** (320 US + « filler games » 480, KD 0) : SERP faibles mais volumes modestes ; à publier après les quick wins.
- **`cooperative-board-games`** (40 500 US en moyenne, KD 4) : Shut Up & Sit Down et Wirecutter dans le top 10, volume gonflé par un pic fin 2025. Les sous-intentions (« for 2 players » 720, « for families » 590, « cooperative card games » 1 600) sont faibles et peuvent porter l'article.
- **`best-board-games-for-adults`** (5 400 US, KD 0 ; « board games for adults » 8 100, KD 14) : Wargamer et IGN présents. À construire comme page de tête de ce plan, avec des liens internes depuis les articles plus précis.
- **`abstract-strategy-board-games`** (14 800 US en moyenne, KD 9) : BGG occupe 4 places sur 10 et la série de volumes est très irrégulière. Notre force : tous les classiques sont imprimables gratuitement sur le site.

## 6. Pages nouvelles à créer (« needs »)

- Page jeu, optionnelle : The Landlord's Game (Lizzie Magie, brevet US de 1904), l'ancêtre du Monopoly ; vérifier qu'une version imprimable gratuite et légalement hébergeable existe (article `games-like-monopoly`).
- Règles : Mau Mau / Switch, cousins européens du UNO avec un jeu standard ; mesurer le volume (article `games-like-uno`).
- Plateau imprimable : Makruk ou Janggi (échecs thaï ou coréens) ; mesurer le volume (article `games-like-chess`).
- Règles : Ultimate tic-tac-toe ; Gomoku / cinq en ligne sur un goban (« gomoku » 12 100 US, KD 29, surtout intention de jeu en ligne) (article `games-like-tic-tac-toe`).
- Plateau imprimable : course de billes générique type Aggravation (nom générique, Aggravation et Trouble sont des marques) ; « game like sorry with marbles » 140 US (article `games-like-sorry`).
- Règles des classiques sans matériel (Twenty Questions, Contact, Ghost, Botticelli, Mafia sans cartes) : mesurer les volumes (article `games-to-play-without-anything`).

## 7. Réserve (sujets mesurés, non retenus dans les 24)

| Mot-clé | Vol. US | Vol. UK | KD | Pourquoi en réserve |
|---|---|---|---|---|
| games like cards against humanity | 1 900 | 480 | 0 | SERP faible (whodaresrolls, Reddit, davincisroom), mais nos pages ne collent qu'en partie (Dixit, Meow) ; il faudrait d'abord une fiche Cards Against Humanity (PDF gratuit officiel sous CC BY-NC-SA 2.0, à vérifier, en `link`). |
| board games for 6 players | 1 300 | 320 | 0 | SERP faible (donteatthemeeples, Reddit, Dice Tower) ; recoupe large groups et 3 players. |
| board games for 8 year olds | 1 300 | 880 | 1 | SERP non vérifiée ; suite logique de l'article 5 ans. |
| board games for 10 year olds | 1 000 | 720 | 1 | SERP non vérifiée ; idem. |
| board games for teens | 1 000 | 320 | 0 | SERP faible (bigpotato, boutiques, Reddit) ; pages poussées possibles : Secret Hitler, Two Rooms, Unfair. |
| escape room for teens | 1 300 | – | 0 | SERP mixte (lieux locaux, kits imprimables, escaperoomgeeks en 1) : proche du hub `/escape-games/`. |
| games like pictionary | 590 | 90 | 0 | SERP faible ; mêmes pages poussées que games-like-codenames, à fusionner ou à programmer plus tard. |
| games like secret hitler | 480 | 70 | 0 | Couvert par social-deduction-games (plan B). |
| board games for beginners | 320 | 30 | 0 | NYT Wirecutter dans le top 3 ; bonne idée de démos « essayer avant d'acheter », volume faible. |
| games like scattergories / games like taboo | 720 / 720 | – | 0 | SERP non vérifiées ; peu de pages à pousser. |

## 8. Écartés

- **best 2 player board games** (6 600, KD 0), **2 player board games** (9 900) : intention du hub `/board-games/2-player/`.
- **fun games to play on paper** (9 900, KD 5), **pen and paper games** (2 900, KD 31) : intention du hub `/rules/pen-and-paper/`.
- **escape room at home**, **escape room games at home** (1 300 chacun) : intention du hub `/escape-games/` (et `diy-escape-room` des plans A et B).
- **escape room for 2 players** (320), **2 people escape room** (3 600) : SERP de lieux physiques (worldofescapes, Yelp, salles locales).
- **free board games** (2 900, KD 35) : hub `/board-games/` et jeux en ligne.
- **travel games** (9 900) : requête produit (sets de voyage) ; on garde « games to play on a plane » et « travel board games » en secondaire.
- **games to play with a deck of cards** (12 100, KD 6) : périmètre jeux de cartes et règles du plan B.
- **diy board games** / **homemade board games** : couverts par how-to-make-a-board-game (plan B). **solo board games** : hub `/board-games/solo/` et réserve du plan B. **roll and write games** : hub `/roll-and-write/`.
- **games like ticket to ride** (480), **legacy board games** (1 600) : aucune page du site à pousser.
- **murder mystery games for adults** (1 000, KD 18) : SERP de vendeurs de kits, gardé en secondaire de mystery-board-games.

## 9. Coût DataForSEO

Environ **0,45 $** pour 53 appels : 3 `ideas`, 5 `overview` (3 US, 2 UK, dont deux petits compléments) et 45 SERP. Les fichiers de ce plan sont tous dans `data/kw/blog-c/` (aucun partage avec les dossiers des plans A et B).

## 10. Rappels pour la rédaction

- Tout fait marqué « to be checked » / « to be sourced » dans `angle` (nombre de joueurs, âge, durée, poids BGG, dates d'invention, filiation Pachisi → Sorry!, Crazy Eights → UNO, Landlord's Game → Monopoly) se vérifie sur la source (éditeur, api.geekdo.com, source historique) et se cite dans `sources`.
- Monopoly, UNO, Clue, Sorry!, Trouble, Yahtzee, Catan, Risk, Codenames, Exploding Kittens sont des marques : usage descriptif dans les titres et le texte, aucun matériel imprimable à leur nom.
- Les démos et extensions gratuites ne sont pas des jeux complets : Kingdomino The Court et Small World Lost Tribes exigent la boîte de base, à présenter comme « si vous avez déjà le jeu ».
- Jeux du commerce : liens neutres pour l'instant (affiliation éventuelle plus tard), jamais d'avis ou de note inventés ; les notes BGG se lisent sur api.geekdo.com.
- `scripts/blog_calendar.py` lit tous les `data/blog-topics-*.json` : ce fichier entrera dans le calendrier au prochain lancement du script.
