# SEO programmatique : quels gabarits de pages, pour quelle demande

Étude du 18 octobre 2026. Données DataForSEO (Google Ads, US), fichiers bruts dans `data/kw/`.
Attention : Google Ads regroupe les variantes proches sous un même volume (« uno rules », « uno game rules », « rules for playing uno » affichent toutes 49 500). Les totaux par grappe ci-dessous sont donc gonflés ; ils servent à comparer les grappes entre elles, pas à prédire un trafic.

## 1. Ce qu'est le SEO programmatique ici

Un gabarit de page + une base de données = des centaines de pages, chacune ciblant une requête précise.
Exemple : le gabarit « règles du jeu » × 150 jeux classiques = 150 pages « How to play X » sans écrire 150 pages à la main.
Conditions pour que ça marche sans pénalité : chaque page apporte une vraie valeur unique (un PDF, des règles réécrites, des données spécifiques), un minimum de contenu, un maillage propre, et pas de page vide.

## 2. Les grappes mesurées (US, volume mensuel)

| Grappe (gabarit) | Mots-clés trouvés | Volume cumulé (gonflé) | Têtes de grappe | Ce qu'on publie |
|---|---|---|---|---|
| **Règles / how to play** | 4 424 | ≈ 4,8 M | kings cup rules 74 000 · uno rules 49 500 · how to play chess 49 500 · go fish rules 40 500 · rummy rules 33 100 · farkle rules 33 100 · phase 10 rules 33 100 · how to play checkers 33 100 · spades 33 100 | Une page règles par jeu classique ou populaire, avec un PDF imprimable (règles, feuille de score, plateau si domaine public) |
| **Crossword** | 863 | ≈ 486 k | crossword printable 40 500 · free printable crosswords 27 100 | Mots croisés maison par thème et niveau |
| **Bingo** | 1 415 | ≈ 340 k | christmas bingo game 9 900 · blank bingo card 9 900 · bingo card template 8 100 | Cartes de bingo par occasion + générateur + modèles vierges |
| **Christmas** (toutes formes) | 1 347 | ≈ 311 k | christmas word search 18 100 · christmas bingo 9 900 · printable christmas games 3 600 | Hub Noël : word search, bingo, jeux, trivia, chasse au trésor |
| **Sudoku** | 557 | ≈ 290 k | sudoku printable 27 100 | Sudoku maison par niveau (facile → diabolique) |
| **Word search** | 338 | ≈ 212 k | christmas 18 100 · thanksgiving 12 100 · halloween 12 100 · adult 8 100 · summer 1 600 · winter 1 000 | Mots mêlés par thème, occasion, âge |
| **Template / blank** | 794 | ≈ 141 k | blank bingo card 9 900 · bingo card template 8 100 · blank board game template 880 | Modèles vierges : bingo, plateau, cartes, feuilles de score |
| **Thanksgiving** | 266 | ≈ 130 k | thanksgiving word search 12 100 | Hub Thanksgiving |
| **Halloween** | 353 | ≈ 65 k | halloween word search 12 100 · halloween bingo 4 400 | Hub Halloween |
| **Scavenger hunt** | 551 | ≈ 31 k | outdoor scavenger hunt for preschoolers 3 600 · scavenger hunt template 1 900 | Chasses au trésor par lieu, âge, occasion |
| **Bridal shower** | 199 | ≈ 23 k | printable bridal shower games 2 900 | Jeux pour fêtes : bridal shower, baby shower, couples |
| **Trivia** | 608 | ≈ 20 k | christmas trivia questions pdf 720 | Quiz imprimables par thème |
| Easter / Valentine | 96 | ≈ 6 k | easter word search 590 · valentines word search 720 | Hubs saisonniers secondaires |
| Print and play (jeux de société) | voir docs/01 et 05 | ≈ 5 k | print and play games 590 | Le cœur éditorial du site, faible volume mais forte valeur de marque et de liens |

Lecture : le trafic est dans les **règles de jeux classiques**, les **puzzles** (crossword, sudoku, word search), le **bingo** et les **occasions**. Les print and play de créateurs restent la vitrine et la source de liens entrants, pas le moteur de trafic.

## 3. Gabarits retenus et dimensions

| Gabarit | Dimension(s) | Exemple d'URL | Pages estimées |
|---|---|---|---|
| Fiche jeu (PnP de créateur) | 1 jeu | `/board-games/bandido/` | 300 → 3 000 |
| Règles du jeu | 1 jeu classique | `/rules/go-fish/` | 150 → 400 |
| Puzzle par thème × niveau | type × thème × niveau | `/puzzles/word-search/halloween/`, `/puzzles/mazes/hard/` | 200 → 1 500 |
| Bingo par occasion | occasion | `/bingo/christmas/`, `/bingo/blank-template/` | 30 → 80 |
| Hub occasion | occasion × type | `/occasions/christmas/`, `/occasions/christmas/word-search/` | 15 → 60 |
| Hub thème | thème (animaux, pirates, espace, « inspired by » films) | `/themes/pirates/` | 40 → 150 |
| Hub âge / joueurs / durée | tranche | `/age/4-6/`, `/players/2/`, `/time/under-15-min/` | 15 |
| Créateur | 1 créateur | `/creators/gus-and-co/` | 50 → 300 |
| Collection éditoriale | liste manuelle | `/collections/rainy-sunday/` | 20 → 100 |

Total : environ 800 pages au lancement, 5 000 à 6 000 à maturité. Chaque combinaison n'est publiée que si elle a au moins 5 items et une demande mesurée ; sinon elle reste en `noindex, follow`.

## 4. Ce qu'on peut associer au site (idées validées par la demande)

1. **Bibliothèque de règles** : la grappe la plus énorme. Pages « How to play X » avec règles réécrites, variantes, PDF de règles, feuille de score, et pour les jeux du domaine public (dames, échecs, petits chevaux, dominos, jeux de cartes traditionnels) le matériel à imprimer. Lien naturel vers nos print and play.
2. **Générateurs** : bingo, word search, sudoku, crossword, labyrinthes. Un générateur côté client (pas de serveur) crée un PDF unique ; les pages thématiques pré-générées assurent l'indexation.
3. **Calendrier des occasions** : Christmas, Thanksgiving, Halloween, Easter, Valentine, été, rentrée, bridal shower, baby shower. Chaque hub combine word search + bingo + trivia + chasse au trésor + jeux.
4. **Classroom** : whiteboard games, games to play in class, par matière (math, science, spelling) et par niveau.
5. **Modèles vierges** : blank bingo, blank board game, score sheets, cartes vierges.

## 5. BoardGameGeek

Le site est protégé par Cloudflare et son API XML renvoie désormais 401 sans jeton : impossible de récupérer la liste des catégories et mécaniques depuis ce conteneur. Deux options :
- Créer un jeton d'API BGG sur ton compte (paramètres du compte, section API) et me le donner : on récupère alors les 84 catégories, les ~190 mécaniques et les métadonnées de milliers de jeux (joueurs, âge, durée, poids), ce qui alimentera les fiches et les pages règles.
- Sinon, partir des taxonomies qu'on connaît déjà (liste de mémoire à vérifier) et les croiser avec DataForSEO.

Les catégories BGG les plus utiles comme **thèmes** (demande mesurée ci-dessus via word search / bingo / games) : animals, pirates, space, dinosaurs, zombies, horror, sports, trains, medieval, mythology, science fiction, western, nautical, farm, fantasy, superhero, detective / murder mystery, spy.
