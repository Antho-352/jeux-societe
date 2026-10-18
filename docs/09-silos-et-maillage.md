# Silos et maillage interne (cocon sémantique) : architecture définitive

Domaine : printandplaygame.com, Astro statique, anglais à la racine, français sous `/fr/`.
Date : 18 octobre 2026. Ce document remplace la section « silos » du brouillon `06-architecture-seo.md` et sert de spécification pour le modèle de données, les gabarits Astro et les contrôles de build.

Sources vérifiées pour ce document (pages lues le 18 octobre 2026) :

- Google, URL structure best practices : https://developers.google.com/search/docs/crawling-indexing/url-structure
- Google, Managing crawling of faceted navigation URLs (mis à jour 2025-12-18) : https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation et le billet « Crawling December: Faceted navigation » : https://developers.google.com/search/blog/2024/12/crawling-december-faceted-nav
- Google, Tell Google about localized versions of your page (hreflang) : https://developers.google.com/search/docs/specialty/international/localized-versions
- Google, How to specify a canonical : https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google, Pagination and incremental page loading : https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
- Google, Help Google understand your ecommerce site structure : https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure
- Google, SEO Starter Guide : https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google, Spam policies (doorway abuse, scaled content abuse) : https://developers.google.com/search/docs/essentials/spam-policies
- Google, Breadcrumb structured data : https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Google, Make your links crawlable : https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google, Large site owner's guide to managing crawl budget : https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget
- Ahrefs, Internal links for SEO : https://ahrefs.com/blog/internal-links-for-seo/ ; SEO silo structure : https://ahrefs.com/blog/seo-silo-structure/ ; Programmatic SEO : https://ahrefs.com/blog/programmatic-seo/ ; Faceted navigation : https://ahrefs.com/blog/faceted-navigation/ ; Hreflang : https://ahrefs.com/blog/hreflang-tags/ ; Orphan pages : https://ahrefs.com/blog/orphan-pages/
- Backlinko, Website architecture : https://backlinko.com/hub/seo/architecture ; Internal links : https://backlinko.com/hub/seo/internal-links
- Semrush, Topic clusters : https://www.semrush.com/blog/topic-clusters/ ; Programmatic SEO : https://www.semrush.com/blog/programmatic-seo/
- Moz, Internal links : https://moz.com/learn/seo/internal-link
- HubSpot, Silo SEO (2026) : https://blog.hubspot.com/website/silo-seo ; HubSpot FR, Cocon sémantique : https://blog.hubspot.fr/marketing/cocon-semantique

Les volumes cités viennent de `01-mots-cles-volumes.md`, `05-mots-cles-decouverte.md` et `05b-mots-cles-complementaires.md` (DataForSEO, Google Ads, moyenne mensuelle).

---

## 0. Les dix principes retenus (et pourquoi)

| # | Principe | Justification (source) |
|---|---|---|
| 1 | **Pyramide, pas silo étanche.** Chaque fiche vit sous un seul silo (une seule URL), mais les liens contextuels entre silos sont autorisés et même obligatoires (âge, occasion, thème). | Ahrefs : « Forbidding internal links between silos is silly and doesn't help SEO or users » ; John Mueller cité : « The top down approach or pyramid structure helps us a lot more to understand the context of individual pages within the site. » HubSpot 2026 : les silos rigides « sans liens entre sujets » sont dépassés. |
| 2 | **Une requête = une page.** Chaque hub, sous-hub et page facette vise un groupe de mots-clés distinct ; jamais deux URL pour la même combinaison. | Semrush : « a clean one-cluster-to-one-page mapping removes that guesswork » (cannibalisation). Google : « doorway abuse » = pages créées pour des requêtes similaires. |
| 3 | **Les facettes indexables sont des URL statiques décidées à l'avance (liste blanche) ; les autres filtres ne touchent pas l'URL.** | Google (facettes) : « If you don't need the faceted navigation URLs potentially indexed, prevent crawling… use URL fragments to specify filters » ; canonical et nofollow sont « generally less effective in the long term ». |
| 4 | **Profondeur de clic ≤ 3 depuis l'accueil, zéro page orpheline.** | Ahrefs : « keep every page within three clicks of the homepage » ; Google (ecommerce) : « the number of links it needs to follow to reach a page and the number of links to a page » servent à inférer l'importance ; Backlinko : « flat… 4 clicks or less ». |
| 5 | **Le maillage se fait par de vrais liens `<a href>`, dans le texte autant que dans les menus.** | Google : « Googlebot generally doesn't try to submit searches… link to all products that you wish indexed » ; Ahrefs : liens dans le corps = valeur maximale, navigation = valeur moyenne. |
| 6 | **Ancre descriptive, variée, jamais générique.** | Google : « Good anchor text is descriptive, reasonably concise » ; Backlinko : « Don't use the same anchor text for two different pages » ; Moz : « Use variations of anchor text ». |
| 7 | **Chaque page indexable apporte quelque chose d'unique** (intro rédigée, FAQ, données, sélection). Sinon elle n'existe pas ou elle est en `noindex`. | Google (spam) : « Scaled content abuse is when many pages are generated for the primary purpose of manipulating search rankings and not helping users » ; Ahrefs : « publishing at scale is only a risk if you don't have anything worth publishing at scale ». |
| 8 | **Une seule URL canonique par contenu, auto-référencée, dans la même langue.** | Google : « Do include a rel="canonical" link on the canonical page itself » ; « If you're using hreflang… specify a canonical page in the same language ». |
| 9 | **hreflang en paires EN ↔ FR + x-default, uniquement entre pages canoniques indexables.** | Google : « Each language version must list itself as well as all other language versions » ; « If two pages don't both point to each other, the tags will be ignored ». |
| 10 | **Pas de traduction automatique publiée telle quelle.** Une page FR n'existe que si son texte a été rédigé ou relu. | Google (spam) : les « automated transformations like synonymizing, translating » sans valeur ajoutée sont un exemple d'abus de contenu à grande échelle. |

---

## 1. L'arbre des silos

### 1.1 Vue d'ensemble : silos primaires et hubs transversaux

Deux familles de pages de navigation :

- **Silo primaire** : il possède les fiches. Une fiche (jeu, puzzle, kit) a exactement un silo primaire, déterminé par son champ `type`, et son URL vit sous ce silo. Le fil d'Ariane suit ce chemin.
- **Hub transversal** : il ne possède rien. Il liste des fiches venues de tous les silos (par âge, occasion, thème, joueurs, durée) et renvoie vers les pages facettes des silos. Il ne crée jamais de seconde URL pour une fiche.

Trois silos « éditoriaux » possèdent des pages qui ne sont pas des fiches : `/rules/` (une page de règles par jeu classique), `/creators/` (une page par créateur), `/collections/` (listes éditoriales) et `/guides/` (articles). Ces pages ont aussi un seul emplacement.

```
/                                   Accueil
├── /board-games/                   SILO  Jeux de plateau
├── /card-games/                    SILO  Jeux de cartes
├── /roll-and-write/                SILO  Roll & write (et flip & write)
├── /dice-games/                    SILO  Jeux de dés
├── /escape-games/                  SILO  Escape games (+ murder mystery)
├── /treasure-hunts/                SILO  Chasses au trésor et jeux de piste
├── /puzzles/                       FAMILLE de silos : mazes, word-search, dot-to-dot…
├── /bingo/                         SILO  Cartes de bingo / loto
├── /rules/                         SILO  Bibliothèque de règles
├── /classroom/                     SILO  Classe (activités) + hub transversal (fiches par niveau)
├── /occasions/                     TRANSVERSAL  Fêtes et événements
├── /themes/                        TRANSVERSAL  Univers
├── /ages/                          TRANSVERSAL  Tranches d'âge
├── /players/                       TRANSVERSAL  Nombre de joueurs
├── /time/                          TRANSVERSAL  Durée
├── /creators/                      SILO  Créateurs et éditeurs
├── /collections/                   SILO  Sélections éditoriales
└── /guides/                        SILO  Guides pratiques (blog)
```

Tout existe en miroir sous `/fr/` avec des slugs traduits (section 2.4).

### 1.2 Règle d'attribution d'une fiche à son silo primaire

| `type` de la fiche | Silo primaire | URL de la fiche |
|---|---|---|
| `board_game` | Board games | `/board-games/<slug>/` |
| `card_game` | Card games | `/card-games/<slug>/` |
| `roll_and_write` (dont flip & write) | Roll & write | `/roll-and-write/<slug>/` |
| `dice_game` | Dice games | `/dice-games/<slug>/` |
| `escape_game`, `murder_mystery` | Escape games | `/escape-games/<slug>/` |
| `treasure_hunt` | Treasure hunts | `/treasure-hunts/<slug>/` |
| `puzzle` + `subtype` (`maze`, `word_search`, `dot_to_dot`, `rebus`, `dot_marker`, `sudoku`, `crossword`, `spot_the_difference`, `logic`, `crack_the_code`) | Puzzles › sous-type | `/puzzles/<subtype>/<slug>/` |
| `bingo` | Bingo | `/bingo/<slug>/` |
| `rules` | Rules | `/rules/<slug>/` |
| `activity` (jeu de classe sans PDF : whiteboard games, jeux à jouer en classe) | Classroom | `/classroom/activities/<slug>/` |

Cas limites tranchés : un « memory » est un `card_game` (sous-type `memory`). Un « jeu des 7 familles » est un `card_game` (sous-type `happy_families`). Un « loto des animaux » est un `bingo`. Une « enquête policière » est un `murder_mystery` donc sous Escape games. Une « bataille navale » est un `board_game` (sous-type `classics`). Une feuille de score Yahtzee est un `dice_game`. Un « jeu de multiplication à imprimer » est un `board_game` avec `subjects: [math]` et `contexts: [classroom]` : il apparaît dans Classroom par lien, pas par URL.

### 1.3 Détail silo par silo

Légende : « H1 » = gabarit du titre ; « Liste » = ce que la page affiche ; « Cluster » = mots-clés visés (volume US sauf mention UK/FR).

#### Board games — `/board-games/` · FR `/fr/jeux-de-plateau/`

| Page | URL EN | URL FR | H1 EN / FR | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/board-games/` | `/fr/jeux-de-plateau/` | Free Printable Board Games (PDF) / Jeux de plateau à imprimer gratuits (PDF) | tous les `board_game`, onglets vers sous-hubs | printable board games 1 000, free printable board games 210, print and play board games 170, board game printable template 480 ; FR jeu de plateau à imprimer 260, plateau de jeux à imprimer 260 |
| Sous-hub | `/board-games/classics/` | `/fr/jeux-de-plateau/classiques/` | Classic Board Games to Print / Jeux de plateau classiques à imprimer | subtype `classics` (dames, petits chevaux, oie, morpion, serpents et échelles, bataille navale, puissance 4) | checkers printable 1 900, tic tac toe printable 1 600, snakes and ladders printable 260 (UK 480), connect four printable 140 ; FR bataille navale à imprimer 390, petits chevaux 50, jeu de l'oie 50 |
| Sous-hub | `/board-games/cooperative/` | `/fr/jeux-de-plateau/cooperatifs/` | Cooperative Board Games to Print / Jeux de plateau coopératifs | mechanics contient `cooperative` | longue traîne (Pandemic Hot Zone, Bandido) |
| Sous-hub | `/board-games/family/` | `/fr/jeux-de-plateau/famille/` | Family Board Games to Print / Jeux de plateau en famille | age_min ≤ 8 et players_max ≥ 4 | free printable family board games ; FR jeu de société famille à imprimer |
| Sous-hub | `/board-games/strategy/` | `/fr/jeux-de-plateau/strategie/` | Strategy Board Games to Print / Jeux de stratégie à imprimer | complexity ≥ 3 | longue traîne |
| Sous-hub | `/board-games/templates/` | `/fr/jeux-de-plateau/modeles-vierges/` | Blank Board Game Templates / Plateaux de jeu vierges à imprimer | subtype `template` (plateau vierge, piste vierge, cartes vierges) | blank board game template 880, board game printable template 480, blank board game printable 260 ; FR carte de jeu vierge 170 |
| Facettes autorisées | `/board-games/<age-band>/`, `/board-games/<occasion>/`, `/board-games/<theme>/` | idem traduit | ex. Board Games for Kids / Printable Christmas Board Games | règle de liste blanche, section 4.4 | printable board games for adults 20, free printable board games for kids |

Note licences : « monopoly printable » (480), « candyland » (320), « clue/cluedo cards » (480), « uno cards printable » (320), « guess who » (170) sont des marques. On ne crée **pas** de page `/board-games/monopoly/`. On couvre l'intention par des jeux « dans l'esprit de » (ex. fiche « Property Trading Game, inspired by Monopoly ») et par la page de règles `/rules/monopoly/` (les règles sont du savoir, pas du contenu protégé ; pas de PDF du plateau). Voir note dans `06-architecture-seo.md`.

#### Card games — `/card-games/` · FR `/fr/jeux-de-cartes/`

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/card-games/` | `/fr/jeux-de-cartes/` | Free Print and Play Card Games / Jeux de cartes à imprimer gratuits | tous les `card_game` | print and play card games 50, card game printable 480, printable playing cards 1 000 ; FR jeu de carte à imprimer 210, imprimer jeu de carte 590 |
| Sous-hub | `/card-games/micro/` | `/fr/jeux-de-cartes/micro-jeux/` | Micro Card Games (9 to 18 Cards) / Micro-jeux de 9 à 18 cartes | cards_count ≤ 18 | one card dungeon 70, 9-card nanogame (longue traîne BGG) |
| Sous-hub | `/card-games/party/` | `/fr/jeux-de-cartes/ambiance/` | Printable Party Card Games / Jeux d'ambiance à imprimer | players_max ≥ 6 | free printable party games 40, two rooms and a boom 110 ; FR cartes loup garou à imprimer 720, carte time's up 210, jeu de mime 50 |
| Sous-hub | `/card-games/solo/` | `/fr/jeux-de-cartes/solo/` | Solo Card Games to Print / Jeux de cartes solo | players_min = 1 | solo print and play games 50 |
| Sous-hub | `/card-games/memory/` | `/fr/jeux-de-cartes/memory/` | Printable Memory Games / Memory à imprimer | subtype `memory` | FR memory à imprimer gratuit 90, carte memory 30 |
| Sous-hub | `/card-games/happy-families/` | `/fr/jeux-de-cartes/7-familles/` | Happy Families Card Games / Jeux de 7 familles à imprimer | subtype `happy_families` | FR jeu de 7 familles à imprimer 170 + variantes (≈ 600 cumulés) |
| Sous-hub | `/card-games/playing-cards/` | `/fr/jeux-de-cartes/cartes-a-jouer/` | Printable Playing Card Decks / Jeux de 32 et 54 cartes à imprimer | subtype `deck` (jeux de 52/32 cartes, dos, cartes vierges) | printable playing cards 1 000, free printable playing cards 110 ; FR imprimer cartes à jouer 210, jeu de 54 cartes pdf 110 |
| Sous-hub | `/card-games/matching/` | `/fr/jeux-de-cartes/jeux-de-rapidite/` | Spot-the-Match Card Games / Jeux de rapidité et d'observation | subtype `matching` (jeux « dans l'esprit de Dobble ») | FR jeu dobble à imprimer 140 + variantes (marque : pas de slug « dobble ») |

#### Roll & write — `/roll-and-write/` · FR `/fr/roll-and-write/`

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/roll-and-write/` | `/fr/roll-and-write/` | Free Roll & Write Games to Print / Roll and write gratuits à imprimer | type `roll_and_write` | roll and write 590, roll and write games 480, best roll and write games 170, roll and write print and play 20 ; FR roll and write à imprimer gratuit |
| Sous-hub | `/roll-and-write/solo/` | `/fr/roll-and-write/solo/` | Solo Roll & Write Games / Roll and write solo | players_min = 1 | longue traîne |
| Sous-hub | `/roll-and-write/flip-and-write/` | `/fr/roll-and-write/flip-and-write/` | Flip & Write Games / Flip and write à imprimer | subtype `flip_and_write` | flip and write game 50 |

Le mot « roll and write » est conservé tel quel en français (c'est le terme utilisé par la communauté FR ; « print and play » 170 FR confirme l'usage des anglicismes).

#### Dice games — `/dice-games/` · FR `/fr/jeux-de-des/`

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/dice-games/` | `/fr/jeux-de-des/` | Printable Dice Games and Score Sheets / Jeux de dés à imprimer | type `dice_game` | printable dice games 170 ; FR jeu de dés à imprimer |
| Sous-hub | `/dice-games/score-sheets/` | `/fr/jeux-de-des/feuilles-de-score/` | Printable Dice Score Sheets / Feuilles de score à imprimer | subtype `score_sheet` | longue traîne (yahtzee score sheet est une marque : fiche « Five Dice score sheet ») |

Roll & write et Dice games sont deux silos voisins ; ils se citent mutuellement dans le bloc « Silos voisins » de chaque hub.

#### Escape games — `/escape-games/` · FR `/fr/escape-games/`

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/escape-games/` | `/fr/escape-games/` | Free Printable Escape Room Kits / Escape games à imprimer gratuits | types `escape_game` + `murder_mystery` | printable escape room 390, printable escape room kit 320, escape room printable free 210, free printable escape room kit 10 ; FR escape game à imprimer 260, kit escape game gratuit pdf 260, escape game à imprimer gratuit 170, escape game maison gratuit 90 |
| Sous-hub | `/escape-games/kids/` | `/fr/escape-games/enfants/` | Printable Escape Rooms for Kids / Escape games enfants à imprimer | age bands 6-8 et 9-12 | free printable escape room for kids ; FR escape game enfant à imprimer gratuit |
| Sous-hub | `/escape-games/teens/` | `/fr/escape-games/ados/` | Escape Rooms for Teens / Escape games ados | age band 13-17 | longue traîne |
| Sous-hub | `/escape-games/adults/` | `/fr/escape-games/adultes/` | Printable Escape Rooms for Adults / Escape games adultes à imprimer | age band 18+ | printable escape room for adults 40 ; FR escape game adulte gratuit à imprimer 70 |
| Sous-hub | `/escape-games/murder-mystery/` | `/fr/escape-games/murder-party/` | Free Printable Murder Mystery Games / Murder party à imprimer gratuit | type `murder_mystery` | printable murder mystery game free 20 ; FR murder party à imprimer gratuit 20, enquête policière (Escape Kit) |
| Sous-hub | `/escape-games/puzzles/` | `/fr/escape-games/enigmes/` | Printable Escape Room Puzzles / Énigmes d'escape game à imprimer | subtype `puzzle_pack` (énigmes seules, pas de scénario) | printable escape room puzzles 140 ; FR enigme escape game à imprimer 170 |
| Facettes autorisées | `/escape-games/<occasion>/` (christmas, halloween, easter, birthday), `/escape-games/<theme>/` (space, pirates, egypt, detective) | idem traduit | Christmas Escape Room Printable / Escape game de Noël à imprimer | liste blanche | free christmas escape room printable 50, easter escape room 50 ; FR escape game noël adulte 50, escape game pâques 30, escape game anniversaire 10, thème espace (Escape Kit) |

#### Treasure hunts — `/treasure-hunts/` · FR `/fr/chasse-au-tresor/`

Silo prioritaire côté FR (plus gros cluster français du corpus).

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/treasure-hunts/` | `/fr/chasse-au-tresor/` | Free Printable Treasure Hunts / Chasse au trésor gratuite à imprimer (PDF) | type `treasure_hunt` | printable treasure hunt for kids free ; FR chasse au trésor gratuite à imprimer pdf 1 900, chasse au trésor à imprimer 390 + variantes ≈ 1 500, kit chasse au trésor 170 |
| Sous-hub | `/treasure-hunts/clues/` | `/fr/chasse-au-tresor/enigmes/` | Treasure Hunt Clues and Riddles / Énigmes de chasse au trésor à imprimer | subtype `clues` | FR enigme chasse au trésor à imprimer gratuit 1 000, énigme jeu de piste 260 |
| Sous-hub | `/treasure-hunts/maps/` | `/fr/chasse-au-tresor/carte-au-tresor/` | Printable Treasure Maps / Carte au trésor à imprimer | subtype `map` (cartes, cartes vierges) | FR carte au trésor à imprimer 720 + variantes ≈ 1 200, carte au trésor vierge 170 |
| Sous-hub | `/treasure-hunts/scavenger-hunts/` | `/fr/chasse-au-tresor/jeu-de-piste/` | Printable Scavenger Hunts / Jeu de piste gratuit à imprimer | subtype `scavenger` | FR jeu de piste gratuit à imprimer 390, jeu de piste adulte 140, jeu de piste ado 110 |
| Facettes autorisées | `/treasure-hunts/<age-band>/`, `/treasure-hunts/<occasion>/` (easter, christmas, birthday, halloween), `/treasure-hunts/<theme>/` (pirates, nature, animals, dinosaurs) | idem traduit | Pirate Treasure Hunt Printable / Chasse au trésor pirate à imprimer | liste blanche | FR chasse au trésor pâques 320 + 90, chasse au trésor maternelle 170, pirate 110, nature 110, forêt 90, pokemon 70 (marque : univers « monstres de poche », mention dans le texte seulement), animaux 40, jardin 50, automne 30 |

#### Puzzles — `/puzzles/` · FR `/fr/jeux-de-reflexion/`

`/puzzles/` est un hub de famille : chaque sous-type est un silo à part entière, parce que « word search » (60 500), « dot to dot » (9 900 × 3) et « printable mazes » (6 600) sont des clusters indépendants plus gros que la plupart des silos de jeux. Les fiches vivent sous `/puzzles/<subtype>/<slug>/`.

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub famille | `/puzzles/` | `/fr/jeux-de-reflexion/` | Free Printable Puzzles (PDF) / Jeux de réflexion et de logique à imprimer | tous les `puzzle`, grille des sous-types | printable puzzles for kids ; FR jeu de logique à imprimer 170, jeux de concentration 210, puzzle à imprimer gratuit 110 |
| Silo | `/puzzles/word-search/` | `/fr/jeux-de-reflexion/mots-meles/` | Free Printable Word Search Puzzles / Mots mêlés à imprimer | subtype `word_search` | word search printable 60 500 ; FR mots mêlés maternelle 30 |
| Silo | `/puzzles/mazes/` | `/fr/jeux-de-reflexion/labyrinthes/` | Printable Mazes for Kids and Adults / Labyrinthes à imprimer | subtype `maze` | printable mazes 6 600, children's mazes to print 4 400 ; FR labyrinthe à imprimer gratuit 90 |
| Facette difficulté | `/puzzles/mazes/easy/`, `/medium/`, `/hard/` | `/fr/jeux-de-reflexion/labyrinthes/facile/`, `/moyen/`, `/difficile/` | Easy Mazes to Print / Hard Mazes to Print | difficulty 1-2 / 3 / 4-5 | easy maze 2 400, hard mazes 2 900, difficult maze 2 900 |
| Silo | `/puzzles/dot-to-dot/` | `/fr/jeux-de-reflexion/points-a-relier/` | Free Dot to Dot Printables (Connect the Dots) / Points à relier à imprimer | subtype `dot_to_dot` | dot to dot printable 9 900, dot to dot sheets 9 900, connect the dots printable 9 900 (une seule page pour les trois) |
| Facette difficulté | `/puzzles/dot-to-dot/1-20/`, `/1-50/`, `/1-100/`, `/hard/` | `/fr/.../points-a-relier/1-a-20/`… | Dot to Dot 1-20 for Preschool | dots_count | longue traîne |
| Silo | `/puzzles/rebus/` | `/fr/jeux-de-reflexion/rebus/` | Printable Rebus Puzzles with Answers / Rébus à imprimer avec réponses | subtype `rebus` | printable rebus puzzles 1 600, difficult rebus puzzles 2 400, rebus puzzles with answers printable 480 |
| Facette difficulté | `/puzzles/rebus/hard/` | `/fr/.../rebus/difficile/` | Difficult Rebus Puzzles | difficulty ≥ 4 | difficult rebus puzzles 2 400 |
| Silo | `/puzzles/dot-marker/` | `/fr/jeux-de-reflexion/tampons-encreurs/` | Free Dot Marker Printables / Fiches tampons encreurs (dot painting) | subtype `dot_marker` | dot marker printables 2 900 |
| Silo | `/puzzles/spot-the-difference/` | `/fr/jeux-de-reflexion/jeu-des-7-erreurs/` | Spot the Difference Printables / Jeu des 7 erreurs à imprimer | subtype `spot_the_difference` | FR jeu des 10 différences 210, jeux des 12 erreurs adulte 210, jeu des 7 erreurs adultes 170 |
| Silo | `/puzzles/sudoku/` | `/fr/jeux-de-reflexion/sudoku/` | Printable Sudoku (Easy to Hard) / Sudoku à imprimer | subtype `sudoku` | à mesurer avant lancement (hors corpus actuel) |
| Silo | `/puzzles/crosswords/` | `/fr/jeux-de-reflexion/mots-croises/` | Printable Crossword Puzzles / Mots croisés à imprimer | subtype `crossword` | FR mots croisés maternelle 30 ; EN à mesurer |
| Silo | `/puzzles/logic/` | `/fr/jeux-de-reflexion/logique/` | Printable Logic Puzzles / Jeux de logique à imprimer | subtype `logic` (suites logiques, grilles) | FR jeu de logique à imprimer 170, suites logiques 30 |
| Silo | `/puzzles/crack-the-code/` | `/fr/jeux-de-reflexion/messages-codes/` | Crack the Code Puzzles / Messages codés à imprimer | subtype `crack_the_code` | longue traîne, pont vers escape games |
| Facettes autorisées sur chaque silo puzzle | `<occasion>` (christmas, halloween, easter, valentines), `<theme>` (animals, dinosaurs, space), `<age-band>` | idem traduit | Christmas Word Search Printable | liste blanche | ex. halloween word search, christmas maze (à mesurer) |

#### Bingo — `/bingo/` · FR `/fr/bingo/`

Silo dédié parce que le cluster bingo cumule plus de 30 000 recherches US (bingo cards printable 6 600, free bingo cards 4 400 × 5 variantes, blank bingo 2 900 × 3, 1 600, 1 000 × 6…) et 1 600 × 5 au UK.

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/bingo/` | `/fr/bingo/` | Free Printable Bingo Cards (PDF) / Cartes de bingo et loto à imprimer | type `bingo` | bingo cards printable 6 600, free printable bingo cards 4 400, bingo printable 880 ; FR jeu de loto à imprimer gratuit 40 |
| Sous-hub | `/bingo/blank-templates/` | `/fr/bingo/grilles-vierges/` | Blank Bingo Card Templates / Grilles de bingo vierges | subtype `blank` | blank bingo card printable 2 900, empty bingo template 1 600, blank bingo card template 880 |
| Sous-hub | `/bingo/number-cards/` | `/fr/bingo/cartes-numeros/` | Printable Number Bingo Cards (1-75, 1-90) / Cartons de loto chiffrés | subtype `numbers` | bingo cards free printable numbers 260, print bingo cards 1 75 90, bingo tickets printable (UK 320) |
| Sous-hub | `/bingo/picture-bingo/` | `/fr/bingo/loto-images/` | Picture Bingo for Kids / Loto d'images pour enfants | subtype `picture` | longue traîne |
| Sous-hub | `/bingo/baby-shower/` | `/fr/bingo/baby-shower/` | Baby Shower Bingo | occasion `baby_shower` | à mesurer |
| Facettes autorisées | `/bingo/<occasion>/` (christmas, halloween, easter, thanksgiving, valentines, wedding), `/bingo/<theme>/` (animals, dinosaurs…), `/bingo/<age-band>/` | idem traduit | Christmas Bingo Cards Printable / Bingo de Noël à imprimer | liste blanche | FR bingo de noël gratuit à imprimer 40 + 30 |

#### Rules — `/rules/` · FR `/fr/regles/`

| Page | URL EN | URL FR | H1 | Liste / contenu | Cluster |
|---|---|---|---|---|---|
| Hub | `/rules/` | `/fr/regles/` | Board Game Rules Library / Règles des jeux de société | index alphabétique + par famille (classiques, cartes, dés) | board game rules 4 400, board games and rules 4 400 |
| Page règles | `/rules/<game>/` ex. `/rules/checkers/` | `/fr/regles/<jeu>/` ex. `/fr/regles/dames/` | Checkers Rules: How to Play / Règles des dames | texte ≥ 400 mots, balisage `HowTo`, encart « Print this game » vers la fiche PDF correspondante | « <jeu> rules », « how to play <jeu> » (à mesurer jeu par jeu) |
| Sous-hub | `/rules/classic-board-games/`, `/rules/card-games/`, `/rules/dice-games/` | `/fr/regles/jeux-de-plateau/`… | Classic Board Game Rules | filtre `family` | longue traîne |

Les pages de règles sur des jeux de marque (Monopoly, Uno, Cluedo) sont autorisées (expliquer des règles est licite) à condition de ne pas héberger le matériel de marque et de pointer vers une fiche « inspirée de » ou vers aucune fiche.

#### Classroom — `/classroom/` · FR `/fr/classe/`

Hybride : silo primaire pour les `activity` (sans PDF) et hub transversal pour les fiches ayant `contexts: [classroom]`.

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/classroom/` | `/fr/classe/` | Free Printable Games for the Classroom / Jeux à imprimer pour la classe | activités + fiches `contexts: classroom` | free printable games for the classroom, printable classroom games 10, educational board games printable 10 ; FR jeu de société éducatif à imprimer |
| Sous-hub (activités) | `/classroom/whiteboard-games/` | `/fr/classe/jeux-au-tableau/` | Whiteboard Games for the Classroom / Jeux au tableau pour la classe | `activity` subtype `whiteboard` | whiteboard games 2 900 |
| Sous-hub (activités) | `/classroom/games-to-play-in-class/` | `/fr/classe/jeux-a-faire-en-classe/` | Games to Play in Class (No Prep) / Jeux à faire en classe sans matériel | `activity` subtype `no_prep` | games to play in class 2 900, fun games to play at school |
| Fiche activité | `/classroom/activities/<slug>/` | `/fr/classe/activites/<slug>/` | Nom de l'activité | texte ≥ 300 mots, règles, variantes | longue traîne |
| Sous-hub par niveau | `/classroom/preschool/`, `/classroom/kindergarten-to-grade-2/`, `/classroom/grades-3-5/`, `/classroom/middle-school/` | `/fr/classe/maternelle/`, `/fr/classe/cp-ce2/`, `/fr/classe/cm1-6e/`, `/fr/classe/college/` | Printable Games for Preschool / Jeux à imprimer maternelle | grade_levels | FR jeu à imprimer maternelle 210, jeux de société maternelle 40, chasse au trésor maternelle 170 |
| Sous-hub par matière | `/classroom/math/`, `/classroom/reading/`, `/classroom/languages/` | `/fr/classe/maths/`, `/fr/classe/lecture/`, `/fr/classe/langues/` | Printable Math Games / Jeux de maths à imprimer | subjects | multiplication board game printable 140, math board game printable 50 |

Les niveaux EN et FR sont des bandes d'âge équivalentes (preschool = maternelle = 3-5 ans ; K-2 = CP-CE2 = 6-8 ; grades 3-5 = CM1-6e = 9-11 ; middle school = collège = 11-14), ce qui permet l'appariement hreflang.

#### Occasions (transversal) — `/occasions/` · FR `/fr/occasions/`

| Page | URL EN | URL FR | H1 | Liste | Cluster |
|---|---|---|---|---|---|
| Hub | `/occasions/` | `/fr/occasions/` | Printable Games for Every Occasion / Jeux à imprimer par occasion | grille des occasions, calendrier | navigation |
| Occasion | `/occasions/christmas/` | `/fr/occasions/noel/` | Free Christmas Printable Games / Jeux de Noël à imprimer gratuits | toutes fiches `occasions: christmas`, sections par silo renvoyant vers `/bingo/christmas/`, `/escape-games/christmas/`, `/puzzles/word-search/christmas/`… | christmas printable games free 1 600 ; FR jeux de noël à imprimer gratuit 170 + 140 |
| Occasion | `/occasions/halloween/` | `/fr/occasions/halloween/` | Halloween Printable Games | idem | halloween printable games 390, halloween printable games free 170 |
| Occasion | `/occasions/easter/` | `/fr/occasions/paques/` | Easter Printable Games | idem | easter printable games 170 ; FR chasse au trésor pâques 320 |
| Occasion | `/occasions/birthday/` | `/fr/occasions/anniversaire/` | Printable Birthday Party Games | idem | free printable birthday party games 10 ; FR escape game anniversaire 10 |
| Occasion | `/occasions/travel/` | `/fr/occasions/voyage/` | Printable Travel Games for Kids | idem | printable travel games for kids ; FR jeux de voyage à imprimer 50 + 90 |
| Occasion | `/occasions/baby-shower/`, `/occasions/wedding/`, `/occasions/valentines-day/`, `/occasions/thanksgiving/`, `/occasions/new-year/`, `/occasions/back-to-school/`, `/occasions/summer/`, `/occasions/mothers-day/`, `/occasions/fathers-day/` | `/fr/occasions/baby-shower/`, `/mariage/`, `/saint-valentin/`, `/thanksgiving/` (EN seulement au lancement), `/nouvel-an/`, `/rentree/`, `/ete/`, `/fete-des-meres/`, `/fete-des-peres/` | | | ouverts quand ≥ 5 fiches |

Une page occasion existe uniquement au niveau hub transversal (`/occasions/christmas/`). La combinaison occasion × silo vit **sous le silo** (`/bingo/christmas/`) et jamais sous `/occasions/christmas/bingo/`. C'est la règle qui évite deux pages pour la même intention.

#### Themes (transversal) — `/themes/` · FR `/fr/themes/`

| Page | URL EN | URL FR | H1 | Liste |
|---|---|---|---|---|
| Hub | `/themes/` | `/fr/themes/` | Printable Games by Theme / Jeux à imprimer par univers | grille des thèmes |
| Thème | `/themes/pirates/` | `/fr/themes/pirates/` | Pirate Printable Games and Puzzles / Jeux de pirates à imprimer | toutes fiches `themes: pirates`, sections par silo vers `/treasure-hunts/pirates/`… |
| Thèmes ouverts au lancement | pirates, space, dinosaurs, animals, ocean, jungle, farm, princesses-and-castles, knights-and-medieval, superheroes, zombies, detective, ancient-egypt, fantasy-dungeon, robots-and-sci-fi, unicorns, monsters, vehicles, sports, nature | pirates, espace, dinosaures, animaux, ocean, jungle, ferme, princesses-et-chateaux, chevaliers-et-moyen-age, super-heros, zombies, detective, egypte-antique, donjon-et-fantasy, robots-et-science-fiction, licornes, monstres, vehicules, sport, nature | | |
| Univers « inspirés de » (licences) | `/themes/wizard-school/` (inspiré de Harry Potter), `/themes/pocket-monsters/` (Pokémon), `/themes/galactic-saga/` (Star Wars), `/themes/brick-building/` (Lego) | `/fr/themes/ecole-de-sorciers/`, `/fr/themes/monstres-de-poche/`, `/fr/themes/saga-galactique/`, `/fr/themes/briques-de-construction/` | Wizard School Printable Games (Harry Potter-Inspired) | la marque figure dans le H1 entre parenthèses et dans le texte, jamais dans le slug ; champ `licensed_universe: true` ; fiches en `hosting_mode: link-only` par défaut |

Mots-clés : harry potter printable board game, harry potter printable games 20 ; FR jeu de société harry potter pdf gratuit, chasse au trésor pokemon 70. Volume faible et risque de retrait : phase 3.

#### Ages (transversal) — `/ages/` · FR `/fr/age/`

Cinq tranches fixes, utilisées partout (facettes de silo, classroom, related).

| Tranche | URL EN | URL FR | H1 | Règle d'appartenance |
|---|---|---|---|---|
| Hub | `/ages/` | `/fr/age/` | Printable Games by Age / Jeux à imprimer par âge | |
| 3-5 | `/ages/3-5/` | `/fr/age/3-5-ans/` | Printable Games for Toddlers and Preschoolers (3-5) / Jeux à imprimer 3-5 ans (maternelle) | `age_min ≤ 5` et `age_max ≥ 3` |
| 6-8 | `/ages/6-8/` | `/fr/age/6-8-ans/` | Printable Games for Kids 6-8 / Jeux à imprimer 6-8 ans | `age_min ≤ 8` et `age_max ≥ 6` |
| 9-12 | `/ages/9-12/` | `/fr/age/9-12-ans/` | Printable Games for Kids 9-12 / Jeux à imprimer 9-12 ans | `age_min ≤ 12` et `age_max ≥ 9` |
| 13-17 | `/ages/teens/` | `/fr/age/ados/` | Printable Games for Teens / Jeux à imprimer pour ados | `age_min ≤ 17` et `age_max ≥ 13` |
| 18+ | `/ages/adults/` | `/fr/age/adultes/` | Printable Games for Adults / Jeux de société adultes à imprimer | `age_max ≥ 18` et (`age_min ≥ 12` ou `adult_friendly: true`) |

Clusters : free printable games for toddlers, free printable board games for kids, printable board games for adults 20 ; FR jeu à imprimer 3 ans, jeu à imprimer 6 ans, jeu de société adulte à imprimer 10, jeux de société à imprimer pour adultes 30. Une fiche « 6-99 ans » appartient aux tranches 6-8, 9-12, ados et adultes : c'est voulu, mais la page « adultes » applique une règle plus stricte (ci-dessus) pour ne pas devenir une copie de tout le catalogue.

#### Players (transversal) — `/players/` · FR `/fr/joueurs/`

| Tranche | URL EN | URL FR | H1 | Règle |
|---|---|---|---|---|
| Hub | `/players/` | `/fr/joueurs/` | Printable Games by Number of Players | |
| Solo | `/players/solo/` | `/fr/joueurs/solo/` | Solo Print and Play Games / Jeux à imprimer solo | `players_min = 1` |
| 2 joueurs | `/players/2-players/` | `/fr/joueurs/2-joueurs/` | 2-Player Print and Play Games / Jeux de société 2 joueurs à imprimer | `players_min ≤ 2 ≤ players_max` |
| Petit groupe | `/players/3-5-players/` | `/fr/joueurs/3-a-5-joueurs/` | Games for 3 to 5 Players | chevauchement avec [3,5] |
| Ambiance | `/players/party/` | `/fr/joueurs/grand-groupe/` | Party Games for 6+ Players / Jeux pour grands groupes | `players_max ≥ 6` |

Clusters : solo print and play games 50, print and play solo games 50, 2 player print and play games 10 ; FR jeu de société 2 joueurs à imprimer.

#### Time (transversal) — `/time/` · FR `/fr/duree/`

| Tranche | URL EN | URL FR | H1 | Règle |
|---|---|---|---|---|
| Hub | `/time/` | `/fr/duree/` | Printable Games by Play Time | |
| < 15 min | `/time/under-15-minutes/` | `/fr/duree/moins-de-15-minutes/` | Quick Printable Games (Under 15 Minutes) / Jeux rapides de moins de 15 minutes | `time_max ≤ 15` |
| 15-30 | `/time/15-30-minutes/` | `/fr/duree/15-30-minutes/` | | durée typique dans [15,30] |
| 30-60 | `/time/30-60-minutes/` | `/fr/duree/30-60-minutes/` | | durée typique dans [30,60] |
| > 60 | `/time/over-60-minutes/` | `/fr/duree/plus-de-60-minutes/` | | `time_min ≥ 60` |

Volume de recherche faible : ces pages servent d'abord la navigation et le maillage. Seule `/time/under-15-minutes/` est en `index` au lancement ; les autres restent `noindex,follow` tant qu'aucune demande n'est mesurée (section 4.5).

#### Creators — `/creators/` · FR `/fr/createurs/`

| Page | URL EN | URL FR | H1 | Contenu |
|---|---|---|---|---|
| Hub | `/creators/` | `/fr/createurs/` | Print and Play Designers and Publishers / Créateurs et éditeurs de print and play | index alphabétique, créateurs à l'honneur |
| Créateur | `/creators/<slug>/` (slug identique EN/FR, nom propre) | `/fr/createurs/<slug>/` | Nom (Designer / Publisher) | bio, liens externes (site, itch, BGG), prix de concours, liste de toutes ses fiches, « soutenez ce créateur » |

Une page créateur est indexable à partir de 2 fiches publiées, ou 1 fiche plus une bio d'au moins 150 mots ; sinon elle existe (pour le crédit et le lien depuis la fiche) en `noindex,follow`.

#### Collections — `/collections/` · FR `/fr/collections/`

| Page | URL EN | URL FR | H1 | Contenu |
|---|---|---|---|---|
| Hub | `/collections/` | `/fr/collections/` | Curated Collections / Sélections | toutes les collections |
| Collection | `/collections/<slug>/` | `/fr/collections/<slug-fr>/` | ex. The Best Free Print and Play Games (2026) / Les meilleurs print and play gratuits | texte éditorial ≥ 300 mots, 5 à 20 fiches commentées une par une |

Collections de lancement : best-free-print-and-play-games (best free print and play games 10, best print and play games 70 ; FR meilleurs print and play gratuits), best-roll-and-write-games (170), one-sheet-games, black-and-white-printable-games, 9-card-games, rainy-day-games, classroom-starter-pack, christmas-game-night.

#### Guides — `/guides/` · FR `/fr/guides/`

| Page | URL EN | URL FR | H1 | Cluster |
|---|---|---|---|---|
| Hub | `/guides/` | `/fr/guides/` | How to Print and Play / Guides pratiques | |
| Article | `/guides/how-to-print-and-play-board-games/` | `/fr/guides/comment-imprimer-un-jeu-de-societe/` | How to Print and Play Board Games (Paper, Sleeves, Cutting) | how to print and play board games 10 ; FR comment imprimer un jeu de société |
| Article | `/guides/how-to-make-your-own-board-game/` | `/fr/guides/fabriquer-son-jeu-de-societe/` | | FR jeu de société à fabriquer soi-même 10 |
| Article | `/guides/print-and-play-games-2026/` | `/fr/guides/print-and-play-2026/` | New Print and Play Games in 2026 | print and play games 2026 |

Les guides sont le seul endroit où l'on publie du contenu daté (actualités, « nouveautés du mois »).

### 1.4 Tableau récapitulatif : primaire ou transversal

| Hub | Nature | Possède des URL de fiches ? | Peut avoir des facettes (âge / occasion / thème) ? |
|---|---|---|---|
| board-games, card-games, roll-and-write, dice-games, escape-games, treasure-hunts, puzzles/*, bingo | Silo primaire | Oui | Oui (liste blanche) |
| rules, creators, collections, guides | Silo éditorial | Oui (pages règles, créateurs, collections, articles) | Non |
| classroom | Hybride | Oui pour `activity` seulement | Niveau et matière (ce sont ses propres sous-hubs) |
| occasions, themes, ages, players, time | Transversal | Non, jamais | Non : la combinaison vit sous le silo |

---

## 2. Règles d'URL, canonical, pagination, slugs, hreflang

### 2.1 Forme des URL

| Règle | Valeur | Source |
|---|---|---|
| Schéma et hôte | `https://printandplaygame.com` sans `www` ; 301 de `http://`, de `www.` et de toute variante de casse vers la forme canonique | Google (canonical) : « link consistently to the URL that you consider to be canonical » |
| Slash final | **Toujours** (`/puzzles/mazes/`). Astro : `trailingSlash: 'always'`, `build.format: 'directory'`. 301 de la version sans slash. | Pas de consigne Google sur le slash lui-même ; la consigne est la cohérence (éviter deux URL pour une page) |
| Casse | minuscules uniquement | Google : URL « simple, descriptive » |
| Séparateur | tiret `-`, jamais `_` ni mots collés | Google : « use hyphens (-) instead of underscores (_) » |
| Caractères | ASCII uniquement ; accents FR translittérés (`é` → `e`, `ç` → `c`, `œ` → `oe`) ; pas d'apostrophe | Google accepte l'UTF-8, mais l'ASCII évite les doubles encodages dans les liens externes |
| Paramètres `?` | Aucun sur les pages indexables. Les seuls paramètres tolérés sont les UTM entrants, qui portent un canonical vers l'URL propre. `robots.txt` : `Disallow: /*?` | Google (facettes) : bloquer le crawl des filtres paramétrés |
| Fragments `#` | Réservés aux filtres secondaires côté client (tri, format A4/Letter, couleur, langue du PDF). Ils ne changent pas le contenu indexé. | Google : « Google Search generally doesn't support URL fragments in crawling and indexing », donc « no impact on crawling (positive or negative) » |
| Profondeur d'URL | Maximum 3 segments hors préfixe de langue (`/puzzles/mazes/hard/`, `/puzzles/mazes/<slug>/`, `/fr/jeux-de-reflexion/labyrinthes/<slug>/`) ; la pagination ajoute `page/<n>/` | Lisibilité des breadcrumbs : « Google learns breadcrumbs automatically based on the words in the URL » |
| Identifiants | Jamais d'ID numérique dans l'URL ; l'`id` interne reste dans les données | Google : « use readable words rather than long ID numbers » |
| Mots interdits dans les slugs | `printable`, `free`, `pdf`, `download`, `online`, année (sauf guides datés) | Évite `/puzzles/mazes/hard-mazes-printable/` qui dupliquerait le mot-clé déjà porté par le chemin |

Motifs complets :

```
Hub silo            /<silo>/
Sous-hub (subtype)  /<silo>/<subtype>/
Facette difficulté  /puzzles/<subtype>/<easy|medium|hard>/
Facette âge         /<silo>/<3-5|6-8|9-12|teens|adults>/          (ou kids/teens/adults pour escape-games)
Facette occasion    /<silo>/<occasion>/
Facette thème       /<silo>/<theme>/
Fiche               /<silo>/<slug>/            ou  /puzzles/<subtype>/<slug>/
Règles              /rules/<game>/
Créateur            /creators/<slug>/
Collection          /collections/<slug>/
Guide               /guides/<slug>/
Transversal         /<occasions|themes|ages|players|time>/<value>/
Pagination          <listing>/page/<n>/        (n ≥ 2)
Français            /fr/ + même motif avec slugs traduits
```

Ordre des facettes : une URL ne porte **qu'une seule dimension de facette** après le silo ou le sous-type (plus la difficulté pour les puzzles). `/escape-games/kids/christmas/` n'existe pas. Si une combinaison à deux dimensions a une vraie demande (ex. « christmas escape room for kids »), elle devient une **collection** éditoriale, pas une facette. Cela respecte la consigne Google « ensure that the logical order of the filters always stays the same and that no duplicate filters can exist » en la rendant triviale, et garantit qu'une combinaison non prévue renvoie un vrai 404 (site statique : la page n'est pas générée).

Collision de slugs : un slug de facette (`christmas`, `kids`, `hard`) et un slug de fiche partagent le même niveau sous `/<silo>/`. Le générateur réserve la liste des slugs de facettes et de sous-types ; une fiche ne peut pas prendre un slug réservé (contrôle de build, section 4.6).

### 2.2 Canonical

- Chaque page indexable porte un `<link rel="canonical">` **absolu et auto-référencé** (Google : « Do include a rel="canonical" link on the canonical page itself »).
- Le canonical pointe toujours vers une page **de la même langue** : la page FR est canonique d'elle-même, jamais de la page EN (Google : « If you're using hreflang elements, make sure to specify a canonical page in the same language »).
- Une fiche n'a qu'une URL ; il n'y a donc jamais de canonical « vers le silo » depuis une page transversale, parce que la page transversale ne reproduit pas la fiche.
- Les URL avec paramètres (UTM, partages) portent un canonical vers l'URL propre ; elles ne sont liées nulle part en interne.
- Pas de canonical vers une page `noindex`, pas de canonical depuis une page vers une autre page qui a elle-même un canonical ailleurs (chaîne).
- Le sitemap ne contient que des URL canoniques et indexables (Google : ne pas déclarer des canoniques différents par des moyens différents).

### 2.3 Pagination

- URL : `/<listing>/page/2/`, `/page/3/`… ; la page 1 est l'URL du listing lui-même ; `/page/1/` n'existe pas (404).
- Chaque page paginée est **auto-canonique** (Google : « Don't use the first page of a paginated sequence as the canonical page. Instead, give each page its own canonical URL »).
- Liens `<a href>` « page suivante », « page précédente » et barre de numéros complète (toutes les pages, pas seulement ±2) pour que toute page paginée soit à un clic du listing (Google : « include links from each page to the following page using `<a href>` tags »). Lien « retour à la page 1 » explicite (Google : « consider linking from all individual pages in a collection back to the first page »).
- `index,follow` : on n'applique pas de `noindex` aux pages paginées (Google ne le recommande pas et compte sur elles pour découvrir les fiches). Elles ne figurent pas dans le sitemap et portent le titre suffixé « – Page n ». Le texte d'intro et la FAQ n'apparaissent que sur la page 1 ; les pages 2+ gardent H1, fil d'Ariane et grille.
- `rel=next/prev` : non utilisés (Google : « In the past, Google used… »).
- Taille : 24 fiches par page. Un listing ne doit pas dépasser 6 pages (144 fiches) ; au-delà, on crée des sous-hubs ou des facettes pour partitionner (section 3.9, profondeur de clic).
- Les tris et filtres secondaires ne créent pas d'URL (Google : « Avoid indexing URLs with filters or alternative sort orders »).

### 2.4 Slugs et traduction FR

Règles de slug (EN et FR) :

1. Le slug d'une fiche dérive du titre : minuscules, translittération ASCII, tirets, 2 à 6 mots, sans mots interdits (section 2.1), sans article initial en FR (`le`, `la`, `les`, `un`, `une`, `des`). Les mots-outils internes (`de`, `du`, `a`, `et`) sont conservés quand ils portent le mot-clé cherché (`chasse-au-tresor`, `jeu-de-piste`) et retirés sinon. Apostrophe : on la remplace par un tiret (« jeu de l'oie » → `jeu-de-l-oie`, jamais `jeu-de-loie`).
2. Le slug est **stable** : il ne change pas si le titre change (champ `slug` figé à la création ; renommer = 301 géré dans `redirects`).
3. Unicité par silo et par langue, contrôlée au build.
4. Les slugs de hubs, sous-hubs, facettes et valeurs de taxonomie (occasions, thèmes, âges, joueurs, durée, niveaux, matières, difficulté) viennent d'un **dictionnaire bilingue unique** (`src/data/taxonomy.yml`) : chaque valeur a `slug_en`, `slug_fr`, `label_en`, `label_fr`, `h1_en`, `h1_fr`. Aucune traduction à la volée.
5. Le slug FR d'une fiche est saisi dans `slug_fr` (par défaut : copie du slug EN si le titre est un nom propre, ex. `pocket-imperium`). Les règles de traduction : on traduit le sens, pas les mots (`word-search` → `mots-meles`, pas `recherche-de-mots`), en reprenant le mot-clé FR mesuré (`treasure-hunts` → `chasse-au-tresor` au singulier parce que « chasse au trésor à imprimer » est la forme cherchée).
6. Un slug EN et un slug FR peuvent être identiques (`/bingo/`, `/fr/bingo/`, `/escape-games/`, `/fr/escape-games/`) : le préfixe `/fr/` suffit à les distinguer.

Dictionnaire des hubs (extrait, à compléter dans `taxonomy.yml`) :

| EN | FR |
|---|---|
| board-games | jeux-de-plateau |
| card-games | jeux-de-cartes |
| roll-and-write | roll-and-write |
| dice-games | jeux-de-des |
| escape-games | escape-games |
| treasure-hunts | chasse-au-tresor |
| puzzles | jeux-de-reflexion |
| puzzles/mazes | jeux-de-reflexion/labyrinthes |
| puzzles/word-search | jeux-de-reflexion/mots-meles |
| puzzles/dot-to-dot | jeux-de-reflexion/points-a-relier |
| bingo | bingo |
| rules | regles |
| classroom | classe |
| occasions | occasions |
| themes | themes |
| ages | age |
| players | joueurs |
| time | duree |
| creators | createurs |
| collections | collections |
| guides | guides |
| easy / medium / hard | facile / moyen / difficile |
| kids / teens / adults | enfants / ados / adultes |
| christmas / halloween / easter / birthday / travel | noel / halloween / paques / anniversaire / voyage |

### 2.5 hreflang et x-default

- Codes : `en` et `fr` sans région (Google : « you can specify a language code by itself »). Pas de `en-US`/`en-GB`/`fr-FR`/`fr-CA` : une seule page par langue sert tous les pays.
- Implémentation : balises `<link rel="alternate" hreflang="…">` dans le `<head>`, générées par un composant Astro unique à partir de la collection. On n'utilise **pas** en plus le sitemap pour hreflang, afin de n'avoir qu'une source de vérité (une divergence entre les deux rendrait les annotations incohérentes).
- Chaque page liste **elle-même et l'autre langue** (Google : « Each language version must list itself as well as all other language versions ») :

```html
<link rel="alternate" hreflang="en" href="https://printandplaygame.com/puzzles/mazes/hard/" />
<link rel="alternate" hreflang="fr" href="https://printandplaygame.com/fr/jeux-de-reflexion/labyrinthes/difficile/" />
<link rel="alternate" hreflang="x-default" href="https://printandplaygame.com/puzzles/mazes/hard/" />
```

- `x-default` pointe toujours vers la version **anglaise** (langue dominante du projet et de l'audience mondiale). L'accueil `/` n'auto-redirige pas selon la langue du navigateur ; il affiche un bandeau « Ce site existe en français » (une redirection automatique empêche Googlebot US de voir la version EN et Googlebot FR la version FR).
- Une paire hreflang n'est émise que si **les deux pages existent, sont indexables et canoniques** (Google : « If two pages don't both point to each other, the tags will be ignored » ; Ahrefs : l'hreflang vers une URL non canonique ou `noindex` se contredit). Une page EN sans traduction n'émet que `en` + `x-default` vers elle-même.
- Les pages paginées émettent hreflang vers la page de même numéro dans l'autre langue seulement si elle existe ; sinon rien.
- L'appariement est fait par **identifiant**, pas par URL : une fiche a un `id`, deux slugs ; une facette a une clé de taxonomie, deux slugs. C'est ce qui rend la génération fiable.
- Le sélecteur de langue visible renvoie vers la page équivalente quand elle existe, sinon vers le hub parent de l'autre langue (jamais vers un 404).
- Sitemaps : `sitemap-index.xml` → `sitemap-en-pages.xml`, `sitemap-en-items.xml`, `sitemap-fr-pages.xml`, `sitemap-fr-items.xml` ; déclarés dans `robots.txt`.

---

## 3. Le modèle de maillage interne

### 3.1 Vocabulaire du cocon

Le cocon sémantique (Laurent Bourrelly, repris par HubSpot FR) organise les pages en **mère** (hub), **filles** (sous-hubs, fiches) et **sœurs** (pages de même niveau), et impose que les liens suivent le cheminement de l'utilisateur : on descend vers plus précis, on remonte vers plus général, on glisse vers la page sœur la plus proche. Nos règles traduisent ce principe en blocs obligatoires, générés par le gabarit, et en un algorithme de « related ».

Trois sens de lien, tous obligatoires sur chaque page :

- **Descendant** (mère → filles) : hub → sous-hubs et facettes dans le texte ; listing → fiches.
- **Remontant** (fille → mère) : fil d'Ariane + lien contextuel dans l'intro de la fiche vers son sous-hub.
- **Latéral** (sœurs et cousines) : sous-hubs voisins, fiches « related » du même silo, puis liens transversaux (âge, occasion, thème).

### 3.2 Blocs communs à toutes les pages

| Bloc | Contenu | Liens | Ancre |
|---|---|---|---|
| En-tête (méga-menu) | Les 18 hubs + les sous-hubs principaux (puzzles : 6 ; board games : 2 ; escape : 3 ; bingo : 2 ; treasure : 2 ; classroom : 2) + 4 occasions saisonnières + 5 âges | ≈ 45 liens HTML `<a href>`, rendus dans le HTML (pas injectés au clic) | Label du hub (ex. « Printable mazes ») |
| Fil d'Ariane | Accueil › silo › sous-type › (facette) › page, balisage `BreadcrumbList` (JSON-LD, une seule piste = chemin canonique) | 2 à 4 | Nom court de chaque niveau |
| Pied de page | 8 liens maximum : 4 silos majeurs (puzzles, board games, escape games, bingo), guides, créateurs, « proposer un jeu », bascule EN/FR | 8 | Label |
| Sélecteur de langue | Page équivalente dans l'autre langue | 1 | « Français » / « English » |

Plafond : **150 liens par page** au total (menu, contenu, pied compris), seuil usuel repris par Moz (« rough crawl limit of 150 links per page »). Une page listing standard tombe à ≈ 45 (menu) + 24 (grille) + 20 (facettes, related, FAQ) + 8 (pied) ≈ 100.

### 3.3 Blocs par type de page

#### Accueil (`/`, `/fr/`)

| Bloc | Liens obligatoires |
|---|---|
| Héros | 1 CTA vers `/puzzles/` ou le silo saisonnier (Noël en novembre-décembre, Halloween en octobre, Pâques en mars-avril) |
| Accès rapide | 18 hubs (tous) + 10 sous-hubs à plus fort volume (word-search, mazes, dot-to-dot, bingo blank, classics, escape kids, treasure hunts, rebus, dot-marker, whiteboard-games) |
| « Par âge / joueurs / durée » | 5 âges + 4 joueurs + 1 durée (< 15 min) |
| Occasion du moment | 1 à 2 occasions selon le calendrier |
| Nouveautés | 8 fiches les plus récentes (rotation automatique : chaque nouvelle fiche reçoit un lien depuis l'accueil pendant ses premières semaines) |
| Jeu de la semaine | 1 fiche |
| Collections | 4 collections |
| Créateur à l'honneur | 1 créateur |
| Guides | 2 guides |

#### Hub de silo (`/escape-games/`, `/puzzles/mazes/`…)

| Bloc | Liens obligatoires | Règle d'ancre |
|---|---|---|
| Intro (150-300 mots, unique) | 3 à 6 liens contextuels vers les sous-hubs et facettes clés **dans les phrases** (ex. « Start with our *easy mazes for preschoolers*, then move to *hard mazes* ») | Mot-clé cible de la page liée, formulé naturellement |
| Onglets de sous-hubs et facettes indexables | Toutes les filles indexables (sous-types, difficulté, âges, occasions, thèmes ouverts) | Label + type (« Hard mazes », « Christmas mazes »), jamais le seul mot « Hard » |
| Grille de fiches | 24 par page, triées : mis en avant, puis popularité, puis date | Titre de la fiche |
| Filtres secondaires | Tri, format, couleur, langue du PDF : composants client sans URL (`#` ou état) | aucun lien |
| Guide court (200-400 mots) | « Which maze for which age? » : 2 à 4 liens vers facettes âge + 1 vers le guide pratique | Variante naturelle |
| FAQ (`FAQPage`, 3 à 5 questions) | 1 lien par réponse maximum | Naturel |
| Silos voisins | 3 à 5 hubs de silos proches (mazes → dot-to-dot, word-search, crack-the-code ; roll-and-write ↔ dice-games ; escape ↔ treasure-hunts ↔ crack-the-code) | Label du hub |
| Transversaux | Les 5 âges + 2 occasions actives | Label |
| Collections liées | Jusqu'à 3 collections dont ≥ 3 fiches viennent de ce silo | Titre de la collection |

#### Sous-hub et page facette (`/puzzles/mazes/hard/`, `/escape-games/kids/`, `/bingo/christmas/`)

Même gabarit que le hub, avec :

- Intro unique de **≥ 120 mots** qui parle de la combinaison (pas un texte générique où l'on substitue le mot), rédigée ou relue. Sans ce texte, la page n'est pas générée (section 4.5).
- Lien remontant dans la première phrase vers le hub parent (« part of our *printable mazes* collection »).
- **Sœurs** : toutes les autres facettes de la même dimension sur le même silo (easy ↔ medium ↔ hard ; kids ↔ teens ↔ adults) en onglets, et 2 à 4 **cousines** : la même valeur de facette sur les silos voisins (`/bingo/christmas/` → `/puzzles/word-search/christmas/`, `/escape-games/christmas/`) + le hub transversal correspondant (`/occasions/christmas/`).
- Grille de fiches filtrée, 24 par page.

#### Page transversale (`/occasions/christmas/`, `/themes/pirates/`, `/ages/6-8/`, `/players/solo/`)

| Bloc | Liens obligatoires |
|---|---|
| Intro unique (≥ 150 mots) | 3 à 6 liens vers les pages « silo × cette valeur » existantes |
| Sections par silo | Une section par silo ayant ≥ 3 fiches pour cette valeur : titre de section = lien vers `/<silo>/<valeur>/` si cette facette existe, sinon vers le hub du silo ; 4 à 8 fiches par section |
| Sœurs | Les autres valeurs de la même dimension (toutes les occasions, les 5 âges…) |
| Croisement de dimensions | 3 liens vers les transversaux complémentaires (Noël → `/ages/6-8/`, `/players/party/`, `/time/under-15-minutes/`), choisis par comptage de fiches communes |
| Collections et guides liés | Jusqu'à 3 |

La page transversale n'affiche jamais plus de 60 fiches en direct ; elle renvoie vers les facettes de silo pour le reste. Elle est paginée seulement si aucune facette de silo n'existe pour absorber le volume.

#### Fiche jeu ou puzzle (`/puzzles/mazes/<slug>/`)

| Bloc | Liens obligatoires | Ancre |
|---|---|---|
| Fil d'Ariane | Home › Puzzles › Mazes › (titre sans lien) | Labels |
| Intro / description | 1 lien remontant vers le sous-hub ou la facette la plus précise (« one of our *hard mazes* ») | Mot-clé de la page cible |
| Bandeau métadonnées | Chaque valeur cliquable : âge → `/ages/<band>/` (ou facette silo × âge si elle existe), joueurs → `/players/<band>/`, durée → `/time/<band>/`, difficulté → facette difficulté | Valeur affichée (« 6-8 years », « Solo ») |
| « Also in » (chips) | 1 à 2 thèmes → `/themes/<t>/` ou `/<silo>/<t>/` si la facette existe ; 1 occasion → idem ; contexte classe → `/classroom/<niveau>/` | Label |
| Crédit créateur | 1 lien vers `/creators/<slug>/` + liens externes `rel="nofollow"` vers la source si `hosting_mode: link-only` | Nom du créateur |
| Règles | Si `rules_page_id` : 1 lien vers `/rules/<game>/` (et réciproque) | « How to play <jeu> » |
| Related (section 3.4) | **6 fiches** : 4 du même silo, 2 d'un autre silo | Titre de la fiche |
| Collections | Toutes les collections qui contiennent la fiche (max 3) | Titre |
| Guide pratique | 1 lien vers `/guides/how-to-print-and-play-board-games/` dans le bloc « Ce qu'il vous faut » | « how to print and assemble » |

Total hors menu et pied : 18 à 25 liens.

#### Page de règles (`/rules/checkers/`)

- Fil d'Ariane Home › Rules › Checkers.
- Intro : lien vers le hub `/rules/` et vers le sous-hub de famille.
- Encart « Print this game » : lien vers la fiche PDF correspondante (obligatoire si elle existe ; sinon vers `/board-games/classics/`).
- « Related rules » : 4 jeux de la même famille (dames → échecs, backgammon, petits chevaux, oie).
- Transversaux : 1 âge, 1 joueurs.
- Lien vers 1 guide.

#### Page créateur (`/creators/<slug>/`)

- Fil d'Ariane Home › Creators › Nom.
- Toutes ses fiches (grille complète, paginée au-delà de 48).
- 3 créateurs « voisins » (même pays, même silo dominant ou même concours).
- Lien vers les hubs de silo où il publie (≤ 4).
- Liens externes vers son site, itch, BGG (`rel="nofollow"` sauf partenaires identifiés).

#### Collection (`/collections/best-roll-and-write-games/`)

- Fil d'Ariane Home › Collections › Titre.
- Chaque fiche citée est liée **dans le texte** (titre en ancre) et dans une grille récapitulative.
- Lien vers le hub de silo dominant dans l'intro et 2 collections sœurs.
- Lien vers 1 transversal pertinent (âge ou joueurs).

#### Article de guide (`/guides/<slug>/`)

- Fil d'Ariane Home › Guides › Titre.
- 3 à 5 liens contextuels vers hubs, facettes ou fiches (Ahrefs : « 3–5 contextual links per article is a good starting point »).
- 2 guides sœurs en fin d'article.
- Encadré « Try it » : 3 fiches.

### 3.4 L'algorithme « Related » (fiches similaires)

Calculé au build pour chaque fiche, dans chaque langue (les candidats FR sont les fiches qui ont une page FR).

Score d'un candidat `c` pour la fiche `f` :

| Critère | Points |
|---|---|
| Même silo et même sous-type | +50 |
| Même silo, sous-type différent | +30 |
| Chevauchement de tranche d'âge (au moins une tranche commune) | +20 |
| Thème commun | +15 par thème commun, max +30 |
| Occasion commune | +10 |
| Chevauchement joueurs (bande commune) | +5 |
| Chevauchement durée (bande commune) | +5 |
| Même créateur | +5 |
| Même langue de PDF (ou `language_independent`) | +5 |
| **Bonus anti-orphelin** : le candidat a moins de 3 liens entrants hors navigation dans le graphe courant | +25 |
| Pénalité : candidat en `status != published` ou `noindex` | exclu |
| Égalité | date d'ajout la plus récente, puis popularité |

Sélection : les 4 meilleurs **du même silo**, puis les 2 meilleurs **d'un autre silo** parmi ceux qui partagent une tranche d'âge ou un thème (si aucun ne dépasse 20 points, on prend le meilleur transversal quand même, pour garantir le pont entre silos). Jamais deux fois la même fiche, jamais la fiche elle-même. Le résultat est stable d'un build à l'autre pour une même donnée (tri déterministe), ce qui évite que les liens changent à chaque déploiement.

Le champ `related_override[]` permet d'imposer jusqu'à 3 fiches à la main (ex. l'extension d'un jeu) ; elles prennent les premières places.

Le même principe, avec les mêmes critères sans le +50/+30, sert pour « cousines » des pages facettes et transversales.

### 3.5 Règles d'ancre

1. L'ancre décrit la page cible : mot-clé principal ou une de ses variantes du dictionnaire (`anchor_variants[]` par page de taxonomie : « hard mazes », « difficult mazes to print », « our hardest mazes »). Google : « Good anchor text is descriptive, reasonably concise, and relevant ».
2. Jamais « click here », « read more », « here », « this page » (Google : « Bad (too generic): Click here »).
3. Une même page cible reçoit **au moins deux variantes d'ancre** différentes sur l'ensemble du site ; le générateur alterne les variantes selon le contexte (navigation : label court ; texte : variante longue). Moz et Backlinko : varier les ancres.
4. Deux pages différentes ne reçoivent jamais la même ancre exacte (Backlinko : « Don't use the same anchor text for two different pages ») ; contrôle de build sur les ancres textuelles.
5. Les ancres de fiches = titre de la fiche (unicité garantie par le titre).
6. Les ancres contiennent le type quand le contexte ne l'implique pas : sur une page transversale, « Christmas bingo cards », pas « Christmas ».
7. Pas d'ancre image sans `alt` descriptif ; pas de lien sur une icône seule.
8. Liens internes toujours sans `rel="nofollow"` (Backlinko). `nofollow` réservé aux liens sortants non contrôlés (sources, profils).

### 3.6 Quantité de liens par page

| Type de page | Liens contextuels dans le texte | Liens de listing | Liens structurels (menu, breadcrumb, pied) | Total visé |
|---|---|---|---|---|
| Accueil | 5-10 | 40-60 | 55 | ≤ 130 |
| Hub, sous-hub, facette | 6-12 | 24 | 55 | ≤ 110 |
| Transversal | 6-12 | ≤ 60 | 55 | ≤ 140 |
| Fiche | 4-8 | 6 related + ≤ 3 collections | 55 | ≤ 80 |
| Règles, guide, collection | 5-15 | 3-20 | 55 | ≤ 100 |

### 3.7 Profondeur de clic ≤ 3

Chemins garantis par les blocs ci-dessus :

```
0  /
1  /puzzles/mazes/                       (méga-menu, présent sur toutes les pages)
2  /puzzles/mazes/hard/   ou   /puzzles/mazes/page/3/
3  /puzzles/mazes/<slug>/
```

- Le méga-menu met **tous les hubs et les sous-hubs majeurs** à profondeur 1. Les autres sous-hubs et facettes sont à profondeur 2 (depuis leur hub). Les fiches sont à profondeur 2 ou 3.
- Une fiche qui tomberait en profondeur 4 (page 7 d'un listing non partitionné, par exemple) déclenche la règle de partition : on ouvre un sous-hub ou une facette, ou on l'ajoute à une collection, ou elle reçoit un lien « related » prioritaire (bonus anti-orphelin). Le build échoue si une page indexable est à profondeur > 3 (section 4.6).
- Les pages de règles, créateurs, collections et guides sont à profondeur 2 (hub à 1).

### 3.8 Zéro page orpheline

Définition : page indexable avec moins de **2 liens entrants** venant de pages indexables **hors menu et pied de page** (le menu seul ne suffit pas : Google « discount[s] template elements », Ahrefs).

Garanties structurelles :

- Fiche : ≥ 1 lien depuis son listing parent (grille) + ≥ 1 lien depuis au moins une page transversale ou facette (chaque fiche a toujours au moins une tranche d'âge) + les liens « related » entrants que le bonus anti-orphelin distribue.
- Sous-hub et facette : lien depuis l'intro du hub parent + onglets + depuis les pages sœurs.
- Transversal : lien depuis chaque fiche concernée (bandeau métadonnées) + hub transversal.
- Créateur : lien depuis chacune de ses fiches.
- Collection : lien depuis les fiches qu'elle contient + hub collections + hub de silo dominant.
- Règles : lien depuis la fiche PDF + hub rules + related rules.
- Guide : hub guides + bloc « Ce qu'il vous faut » des fiches (le guide d'impression est le plus lié du site, ce qui est voulu).

Contrôle : après le build, un script parcourt le HTML généré, construit le graphe des liens internes, calcule liens entrants (hors blocs `nav`, `footer`) et profondeur BFS depuis `/` et `/fr/`, et fait échouer le déploiement si une page indexable a < 2 liens entrants ou une profondeur > 3. Le rapport liste les pages en limite (2 liens, profondeur 3) pour les traiter à la main.

### 3.9 Ce qu'on ne fait pas

- Pas de « tag cloud » ni de pages de tags libres : seules les valeurs du dictionnaire deviennent des pages.
- Pas de liens automatiques dans le corps du texte par remplacement de mots-clés (Backlinko : « a plugin can EASILY create 1k+ exact match anchor text internal links overnight »).
- Pas de pied de page listant tout le site.
- Pas de liens internes en JavaScript seulement (`onclick`, boutons) : Google n'exploite que `<a href>`.
- Pas de doubles pistes de breadcrumb : une fiche n'a qu'un chemin ; les appartenances transversales sont des chips, pas un fil d'Ariane.

---

## 4. Génération programmatique : modèle de données, gabarits, volumes, garde-fous

### 4.1 Modèle de données d'une fiche (`items` collection)

```yaml
id: maze-lost-temple                 # identifiant stable, jamais exposé
status: published                    # draft | review | published | retired
type: puzzle                         # board_game | card_game | roll_and_write | dice_game | escape_game | murder_mystery | treasure_hunt | puzzle | bingo | activity
subtype: maze                        # dépend du type (voir dictionnaire)
title_en: Lost Temple Maze
title_fr: Le labyrinthe du temple perdu
slug: lost-temple-maze               # EN, figé
slug_fr: labyrinthe-du-temple-perdu  # FR, figé ; vide = pas de page FR
summary_en: ...                      # 1 phrase, carte
summary_fr: ...
description_en: ...                  # ≥ 80 mots uniques, markdown
description_fr: ...                  # vide = pas de page FR
faq_en: [{q, a}]                     # 0 à 3
faq_fr: [{q, a}]

age_min: 6
age_max: 99                          # 99 = pas de limite
players_min: 1
players_max: 1
players_best: 1
time_min: 5                          # minutes
time_max: 10
difficulty: 4                        # 1-5 (puzzles, escape) ; null pour les jeux
complexity: null                     # 1-5 (poids type BGG, jeux seulement)

themes: [ancient-egypt, adventure]   # clés du dictionnaire
occasions: []                        # christmas, halloween, easter, birthday, travel, baby-shower…
mechanics: []                        # cooperative, deduction, drafting, roll-and-move…
contexts: [classroom, rainy-day]     # classroom, rainy-day, waiting-room, car-trip
subjects: []                         # math, reading, languages, science (classroom)
grade_levels: [k-2, 3-5]             # preschool, k-2, 3-5, middle
adult_friendly: false                # force la présence sur /ages/adults/

languages: [independent]             # langues du PDF : en, fr, de… ou independent
language_independent: true

creator_id: printandplay-studio      # référence à creators collection
publisher_id: null
contest_award: null                  # "9-Card Nanogame 2023, 2nd"
licence: cc-by-nc-4.0                # cc0 | cc-by | cc-by-sa | cc-by-nc | cc-by-nc-sa | public-domain | all-rights-reserved-free | unclear
hosting_mode: mirror                 # mirror | link-only
source_url: null                     # obligatoire si link-only
file: /files/puzzles/mazes/lost-temple-maze-v1.pdf
file_size_kb: 240
version: "1.0"
pages_count: 1
cards_count: null
dots_count: null                     # dot-to-dot
color_mode: bw                       # color | bw | both
paper: both                          # a4 | letter | both
components_included: [board]
components_needed: [pencil]
assembly_minutes: 0
app_required: false
ai_art: false
licensed_universe: false             # univers sous licence ("inspired by")
takedown_risk: low                   # low | medium | high
answer_key_included: true            # puzzles

rules_page_id: null                  # lien vers /rules/<game>/
related_override: []                 # ≤ 3 ids
collections: []                      # rempli par les collections, pas ici (dérivé)
images: [{src, alt_en, alt_fr}]      # ≥ 1 visuel fait par nous
date_added: 2026-11-02
date_updated: 2026-11-02
downloads: 0                         # popularité, mise à jour mensuelle
featured: false
noindex: false                       # forçage manuel
```

Champs **dérivés au build** (jamais saisis) : `silo`, `url_en`, `url_fr`, `age_bands[]`, `player_bands[]`, `time_bands[]`, `difficulty_band`, `related[]`, `inbound_links`, `click_depth`, `indexable_en`, `indexable_fr`.

Autres collections : `creators` (id, name, slug, type designer|publisher, country, bio_en/fr, links[], awards[]), `rules` (id, slug, slug_fr, game_name, family, body_en/fr, item_id), `collections` (id, slug, slug_fr, title, intro, entries[{item_id, blurb_en, blurb_fr}]), `guides` (articles), `taxonomy` (dictionnaire bilingue : occasions, themes, ages, players, time, difficulty, grade_levels, subjects, mechanics, subtypes, avec `intro_en`, `intro_fr`, `anchor_variants`), `facets` (liste blanche des combinaisons silo × valeur avec `intro_en`, `intro_fr`, `keyword`, `volume`).

### 4.2 Comment les pages se déduisent des données

| Page | Générée à partir de | Condition d'existence |
|---|---|---|
| Fiche EN | `items` | `status = published` et description ≥ 80 mots et ≥ 1 image et âge/joueurs/durée renseignés |
| Fiche FR | `items` | fiche EN existante + `slug_fr` + `description_fr` relue |
| Hub de silo | liste fixe | toujours (même avec peu de fiches : c'est la colonne vertébrale du site) |
| Sous-hub (subtype) | `taxonomy.subtypes` | ≥ 5 fiches publiées |
| Facette difficulté | `taxonomy.difficulty` × silo puzzle | ≥ 5 fiches |
| Facette âge/occasion/thème sous silo | `facets` (liste blanche) | inscrite dans la liste blanche **et** ≥ 5 fiches **et** intro unique ≥ 120 mots |
| Transversal valeur | `taxonomy.*` | ≥ 5 fiches (sinon la valeur existe comme chip non cliquable) |
| Règles | `rules` | corps ≥ 400 mots |
| Créateur | `creators` | ≥ 1 fiche (indexable à partir de 2, ou 1 + bio ≥ 150 mots) |
| Collection | `collections` | ≥ 5 entrées et intro ≥ 300 mots |
| Guide | `guides` | toujours |
| Pagination | listing | > 24 fiches |

### 4.3 Estimation du nombre de pages

Hypothèses : 300 fiches au lancement, 3 000 à l'échelle ; répartition au lancement ≈ puzzles 120, bingo 30, board games 40, card games 30, roll & write 20, dice 10, escape 20, treasure hunts 20, activités classe 10 ; FR = 50 % des fiches au lancement, 70 % à l'échelle ; 24 fiches par page de listing.

| Gabarit | Lancement EN | Lancement FR | Échelle EN | Échelle FR | Remarque |
|---|---|---|---|---|---|
| Accueil | 1 | 1 | 1 | 1 | |
| Hubs (silos + transversaux + éditoriaux) | 18 | 18 | 18 | 18 | fixes |
| Sous-hubs (sous-types, niveaux, matières) | 30 | 24 | 48 | 48 | gate ≥ 5 |
| Facettes difficulté (puzzles) | 6 | 6 | 24 | 24 | mazes, rebus, dot-to-dot, sudoku… |
| Facettes silo × occasion | 10 | 8 | 60 | 50 | liste blanche |
| Facettes silo × thème | 8 | 6 | 80 | 60 | liste blanche |
| Facettes silo × âge | 8 | 8 | 30 | 30 | escape kids/teens/adults, treasure hunts, board games… |
| Valeurs transversales (occasions, thèmes, âges, joueurs, durée) | 25 | 22 | 55 | 50 | gate ≥ 5 ; durée partiellement noindex |
| Fiches | 300 | 150 | 3 000 | 2 100 | |
| Pages de règles | 30 | 20 | 150 | 100 | |
| Créateurs (indexables) | 25 | 25 | 200 | 200 | +15 / +100 en noindex |
| Collections | 8 | 6 | 60 | 45 | |
| Guides | 6 | 6 | 40 | 35 | |
| Pages de pagination | 20 | 10 | 260 | 180 | index,follow, hors sitemap |
| **Total indexable** | **≈ 495** | **≈ 310** | **≈ 4 025** | **≈ 2 940** | |
| Total site (EN + FR) | ≈ 805 | | ≈ 6 965 | | |

Ordre de grandeur : **≈ 800 pages au lancement, ≈ 7 000 à 3 000 fiches**. Le ratio pages de navigation / fiches reste autour de 0,35 à l'échelle, ce qui est sain : la majorité du site est du contenu, pas des listes.

### 4.4 Liste blanche des facettes silo × valeur

Une page `/<silo>/<valeur>/` n'est créée que si elle figure dans `facets.yml` avec un mot-clé justifiant son existence (volume mesuré ≥ 30 dans l'une des deux langues, ou demande observée en Search Console) **et** si elle passe les gates. Liste de lancement :

| Silo | Valeurs ouvertes au lancement |
|---|---|
| bingo | christmas, halloween, easter, thanksgiving, valentines-day, baby-shower, wedding, 3-5, 6-8 |
| escape-games | kids, teens, adults, christmas, halloween, easter, birthday, space, pirates, ancient-egypt, detective |
| treasure-hunts | 3-5, 6-8, 9-12, teens, adults, easter, christmas, birthday, halloween, pirates, nature, animals, dinosaurs |
| puzzles/word-search | christmas, halloween, easter, animals, 6-8, 9-12, adults |
| puzzles/mazes | easy, medium, hard, christmas, halloween, animals, dinosaurs, 3-5 |
| puzzles/dot-to-dot | 1-20, 1-50, 1-100, hard, animals, christmas |
| puzzles/rebus | hard, kids, adults |
| puzzles/dot-marker | animals, christmas, halloween, letters, numbers |
| board-games | kids, adults, christmas, halloween |
| card-games | kids, christmas |
| roll-and-write, dice-games | solo (sous-hub), kids |

Tout le reste est ajouté au fil de l'eau, une ligne à la fois, avec son intro rédigée.

### 4.5 Garde-fous qualité (quality gates)

| Gate | Règle | Conséquence si non respectée |
|---|---|---|
| G1 Volume minimal | Sous-hub, facette, transversal, collection : **≥ 5 fiches publiées** (dans la langue de la page) | Page non générée (404 naturel) ; la valeur reste visible comme chip non cliquable |
| G2 Intro unique | Hub ≥ 150 mots, facette ≥ 120 mots, transversal ≥ 150 mots, collection ≥ 300 mots, règles ≥ 400 mots ; texte propre à la page, pas un gabarit à trous ; relu par un humain | Page non générée |
| G3 Fiche complète | description ≥ 80 mots, 1 visuel maison, âge, joueurs, durée, licence, `hosting_mode` | `status` bloqué à `review` |
| G4 Fiche link-only | En plus de G3 : ≥ 120 mots, bloc « ce qu'il vous faut », FAQ ≥ 1 ; la valeur ajoutée doit être évidente (sinon on ne fait que renvoyer ailleurs, ce que Google traite comme page intermédiaire) | `noindex,follow` |
| G5 Créateur | ≥ 2 fiches, ou 1 fiche + bio ≥ 150 mots | `noindex,follow` |
| G6 Durée | `/time/*` sauf under-15-minutes | `noindex,follow` jusqu'à preuve de demande |
| G7 Pagination | ≤ 6 pages par listing | Avertissement de build : partitionner |
| G8 FR | page FR seulement si texte FR rédigé ou relu ; jamais de traduction automatique publiée sans relecture | pas de page FR, pas de hreflang |
| G9 Doublon d'intention | deux pages ne peuvent pas viser le même mot-clé principal (contrôle sur `keyword` dans `facets.yml` et `taxonomy.yml`) | Build échoue |
| G10 Univers sous licence | `licensed_universe: true` → marque absente du slug et du `<title>` ; `hosting_mode: link-only` par défaut ; `takedown_risk` renseigné | Build échoue |
| G11 Titres | `<title>` et H1 uniques par langue sur tout le site (sauf pagination, autorisée par Google) | Build échoue |
| G12 Chaîne canonical/hreflang | canonical auto-référencé, hreflang seulement vers des pages indexables et canoniques | Build échoue |

Règles `noindex` résumées : pages de recherche interne (`/search/`), URL avec paramètres (bloquées en plus par `robots.txt`), créateurs sous G5, fiches link-only sous G4, durées sous G6, pages « coming soon ». Tout le reste est `index,follow`. On n'utilise jamais `noindex` comme outil de canonicalisation (Google : « We don't recommend using noindex to prevent selection of a canonical page »).

### 4.6 Contrôles de build (script post-build, échec = pas de déploiement)

1. Unicité des slugs par silo et par langue ; aucun slug de fiche égal à un slug réservé (facette, sous-type, `page`).
2. Chaque page indexable : canonical absolu auto-référencé, hreflang cohérent (A → B implique B → A), pas de hreflang vers `noindex`.
3. Graphe de liens : profondeur ≤ 3 depuis `/` et `/fr/` ; ≥ 2 liens entrants hors `nav`/`footer` ; aucun lien interne vers un 404, une redirection ou une page `noindex` (hors créateurs et link-only, tolérés).
4. Ancres : aucune ancre générique de la liste noire ; aucune ancre textuelle identique vers deux cibles différentes.
5. Nombre de liens ≤ 150 par page.
6. Titres et H1 uniques (G11).
7. Sitemaps : uniquement des URL indexables canoniques ; chaque URL indexable est dans un sitemap.
8. Rapport : pages à profondeur 3 et à 2 liens entrants (liste de surveillance), listings > 4 pages (candidats à la partition), facettes entre 5 et 7 fiches (fragiles).

---

## 5. Plan de lancement

Priorité = volume × facilité (contenu maison sous licence libre d'abord, sources tierces ensuite) × saisonnalité (nous sommes en octobre : Halloween immédiat, Noël en novembre).

### Phase 1 (semaines 1 à 8) : les piliers à fort volume et sans risque juridique

Silos ouverts : **Puzzles** (word-search 60 500, dot-to-dot 9 900, mazes 6 600 + easy/hard, rebus 1 600 + 2 400, dot-marker 2 900), **Bingo** (cluster > 30 000), **Board games › classics + templates** (checkers 1 900, tic tac toe 1 600, snakes and ladders, blank board game template 880), **Rules** (board game rules 4 400 × 2, 30 pages), **Treasure hunts** (FR : 1 900 + 1 000 + 720 + 390, le silo FR prioritaire), hubs transversaux **Ages** et **Occasions** avec `halloween` et `christmas` ouverts dès le premier déploiement.
Contenu : 300 fiches dont ≈ 200 produites par nous (CC BY-NC), 50 % traduites en FR (toutes les chasses au trésor en FR d'abord).
Facettes : la liste blanche de la section 4.4 limitée à puzzles, bingo, treasure-hunts, board-games.
Éditorial : 6 guides (impression, papier, découpe, plastification, print and play 2026, fabriquer son jeu), 8 collections.
Technique : gabarits, dictionnaire bilingue, script de contrôle de build, sitemaps, hreflang, Search Console EN et FR.

### Phase 2 (semaines 9 à 20) : les jeux et la classe

Silos ouverts : **Escape games** (390 US, 260 + 170 FR ; concurrence élevée mais intention forte, kits maison + démos éditeurs en link-only), **Card games** (7 familles FR ≈ 600, loup-garou 720 FR via un jeu « village et loups » maison, micro-jeux de concours BGG), **Roll & write** (590 + 480 + 170) et **Dice games** (170), **Classroom** (whiteboard games 2 900 et games to play in class 2 900 en activités rédigées, niveaux maternelle → collège), **Creators** (crédit systématique, 40 pages), **Players** (solo, 2 joueurs, ambiance).
Facettes : escape × âge et × occasion, card-games × kids, murder-mystery.
Objectif : 800 fiches, 65 % en FR.

### Phase 3 (mois 6 à 12) : largeur et longue traîne

Silos ouverts : **Themes** (20 univers + 4 « inspirés de » en link-only), **Time** (indexation progressive selon la demande), le reste des facettes silo × thème, **collections** saisonnières et par public, **sudoku / crosswords / logic** si les volumes mesurés le justifient.
Objectif : 3 000 fiches, 70 % en FR ; revue trimestrielle des facettes (Search Console : supprimer ou fusionner celles sans impression après 6 mois, Ahrefs : « remove or de-index pages that still earn nothing after a fair testing period »).
Communauté : page « proposer votre jeu », concours, newsletter, votes, qui alimentent le silo Creators.

---

## 6. Glossaire

- **Silo** : groupe de pages sur un même sujet, avec une page mère (hub) et des pages filles ; chez nous, le dossier d'URL où vit une fiche.
- **Hub (page mère, page pilier)** : la page qui présente un sujet et renvoie vers toutes ses sous-pages.
- **Sous-hub** : page fille d'un hub qui liste un sous-ensemble (ex. les labyrinthes dans les puzzles).
- **Facette** : page de liste filtrée sur une valeur (difficile, Noël, 6-8 ans) ; seules les facettes de la liste blanche ont une URL.
- **Hub transversal** : page qui liste des fiches de plusieurs silos (par âge, occasion, thème) sans en posséder aucune.
- **Cocon sémantique** : méthode de maillage où chaque page lie sa mère, ses filles et ses sœurs les plus proches en sens, pour guider lecteur et moteur.
- **Maillage interne** : l'ensemble des liens entre les pages du site.
- **Ancre** : le texte cliquable d'un lien ; il doit décrire la page d'arrivée.
- **Page orpheline** : page vers laquelle aucune autre page ne pointe ; Google peut ne jamais la trouver.
- **Profondeur de clic** : nombre minimal de clics depuis l'accueil pour atteindre une page.
- **Canonical** : balise qui indique l'URL officielle d'un contenu quand il pourrait exister sous plusieurs adresses.
- **noindex** : instruction qui demande aux moteurs de ne pas afficher une page dans les résultats (mais de suivre ses liens avec `follow`).
- **hreflang** : balise qui relie la version anglaise et la version française d'une même page pour que Google montre la bonne langue.
- **x-default** : la version à montrer quand aucune langue ne correspond ; chez nous, l'anglais.
- **Pagination** : découpage d'une longue liste en pages numérotées, chacune avec sa propre URL.
- **Slug** : la partie lisible de l'URL qui nomme une page (`lost-temple-maze`).
- **Fil d'Ariane (breadcrumb)** : le chemin « Accueil › Puzzles › Labyrinthes » affiché en haut de page et balisé pour Google.
- **Doorway / contenu à grande échelle** : pages créées en masse pour capter des requêtes sans apporter de valeur ; interdit par les règles anti-spam de Google, d'où nos garde-fous.
- **Gate (garde-fou)** : condition minimale (nombre de fiches, longueur de l'intro) pour qu'une page soit générée ou indexée.
- **Programmatique** : génération automatique des pages à partir d'une base de données et de gabarits.
