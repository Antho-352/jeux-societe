# Architecture SEO : silos, URL et maillage interne

Domaine : printandplaygame.com (anglais à la racine, français sous `/fr/`).
Principe : un silo = un sujet, un hub par silo, des sous-pages par facette à forte demande, et chaque fiche rattachée à un seul silo principal.

## 1. Les silos

| Silo | Hub (EN) | Sous-pages indexables | Mots-clés visés (volume US) |
|---|---|---|---|
| Board games | `/board-games/` | `/board-games/cooperative/`, `/family/`, `/strategy/`, `/classics/` (checkers, snakes & ladders, tic tac toe, ludo…) | printable board games (1 000), print and play games (590), checkers printable (1 900), tic tac toe printable (1 600) |
| Board game rules | `/rules/` | `/rules/<jeu>/` : une page de règles par jeu classique, liée au PDF | board game rules (4 400), board games and rules (4 400) |
| Card games | `/card-games/` | `/card-games/micro/`, `/party/`, `/solo/` | print and play card games, printable playing cards (1 000) |
| Roll & write + dés | `/roll-and-write/` | `/dice-games/` | roll and write games (480), printable dice games (170) |
| Escape games | `/escape-games/` | `/escape-games/kids/`, `/teens/`, `/adults/` | printable escape room, escape room printable free |
| Treasure hunts | `/treasure-hunts/` | par âge et par thème (FR : chasse au trésor, 1 900) | printable treasure hunt |
| Puzzles | `/puzzles/` | `/puzzles/mazes/` (+ `/easy/`, `/medium/`, `/hard/`), `/puzzles/dot-to-dot/`, `/puzzles/rebus/`, `/puzzles/word-search/`, `/puzzles/dot-marker/` | printable mazes (6 600), hard mazes (2 900), easy maze (2 400), dot to dot (9 900 ×3), rebus (2 400 + 1 600), word search printable (60 500), dot marker (2 900) |
| Classroom | `/classroom/` | `/classroom/whiteboard-games/`, `/games-to-play-in-class/`, `/by-grade/` | whiteboard games (2 900), games to play in class (2 900) |
| Occasions | `/occasions/` | `/occasions/christmas/`, `/halloween/`, `/easter/`, `/birthday/`, `/travel/` | christmas printable games free (1 600), halloween (390), easter (170) |
| Themes (univers) | `/themes/` | `/themes/pirates/`, `/space/`, `/dinosaurs/`, `/wizards/`… | longue traîne ; voir note licences |

Les deux silos « Puzzles » et « Occasions » sont transversaux : une fiche « Christmas maze » a pour silo principal Puzzles › Mazes, et apparaît dans Occasions › Christmas par un lien, pas par une seconde URL.

## 2. Règles d'URL

- Une seule URL canonique par contenu. Les fiches vivent sous leur silo principal : `/puzzles/mazes/lost-temple/`.
- Les pages facettes indexables sont des vraies URL statiques avec leur propre H1, intro et FAQ : `/puzzles/mazes/hard/`.
- Les autres filtres (thème, format, langue) sont appliqués en JavaScript côté client, sans changer l'URL ou avec un `?` qui porte `rel=canonical` vers la page parente. Google ne voit donc jamais deux pages pour le même contenu.
- Pagination : `/puzzles/mazes/page/2/`, auto-canonique, avec un lien « page suivante ».
- Pas de mot-clé en double dans l'URL (`/puzzles/mazes/hard/` et non `/puzzles/hard-mazes-printable/`).

## 3. Gabarit d'une page catégorie

1. Fil d'Ariane (avec balisage BreadcrumbList).
2. H1 contenant le mot-clé principal, sous-titre de 2 à 3 phrases qui citent les variantes (easy, medium, hard, kids).
3. Onglets de facettes indexables : liens HTML, pas des boutons.
4. Filtres secondaires + grille de cartes.
5. Bloc guide de 200 à 400 mots (« Which maze for which age? ») avec liens vers les sous-pages et les silos voisins.
6. FAQ en `<details>` avec balisage FAQPage.
7. « Related » vers 3 à 5 catégories sœurs.

## 4. Maillage interne

- **Descendant** : accueil → hubs → sous-pages → fiches. Chaque hub liste ses sous-pages dans le texte, pas seulement dans les filtres.
- **Remontant** : chaque fiche renvoie vers son hub (fil d'Ariane) et vers sa sous-page facette (« Hard mazes »).
- **Latéral** : chaque fiche propose 4 fiches du même silo (« More cooperative games ») et 2 à 3 liens transversaux (âge, occasion, thème).
- **Hubs de rules** : chaque page règle lie le PDF du jeu, et chaque fiche de jeu classique lie sa page règle.
- Ancre = mot-clé de la page cible, jamais « cliquez ici ».
- Le pied de page ne liste que les 4 silos principaux et les puzzles les plus demandés, pas tout le site.

## 5. International

- `/` en anglais, `/fr/` en français, même structure et mêmes slugs traduits (`/fr/puzzles/labyrinthes/difficile/`).
- `hreflang` en `<link>` dans le `<head>` de chaque page, en paire EN ↔ FR plus `x-default` vers l'anglais. Généré automatiquement par Astro à partir de la collection.
- Un sitemap par langue, déclaré dans `robots.txt`.
- Une page n'existe en FR que si sa traduction est prête ; sinon pas de hreflang vers elle.

## 6. Données structurées

- Fiche jeu : `Product` (gratuit, `offers.price = 0`) + `CreativeWork` avec `author` (le créateur), `license`, `inLanguage`, `numberOfPages`.
- Page catégorie : `CollectionPage` + `ItemList`.
- FAQ : `FAQPage`.
- Règles : `HowTo`.

## 7. Notes

- **Faux amis écartés** : « input output games » (regroupé par Google avec les jeux .io en ligne), « custom poker cards » (intention d'achat), « classroom resources games online » et « safe kid games » (jeux en ligne).
- **Univers sous licence** (Harry Potter, Disney, Pokémon) : seules des créations indépendantes « inspirées de » peuvent être hébergées. Éviter la marque dans le titre de la fiche et dans l'URL, la garder dans le texte. Risque de retrait à prévoir.
- **Contenu maison** : mazes, dot-to-dot, rebus, word search, bingo et jeux classiques du domaine public peuvent être produits par nous, sous licence Creative Commons. C'est le contenu le plus sûr juridiquement et le plus demandé.
