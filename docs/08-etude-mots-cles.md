# Étude de mots-clés et de concurrence : marchés anglophone (US, UK) et français

Date : 18 octobre 2026. Outil : DataForSEO via `scripts/dfs.py` (Google Ads « keywords for keywords » et « search volume », SERP Google organique live, DataForSEO Labs « ranked keywords »). Données brutes : `data/kw/` (37 fichiers JSON, 1,11 $ d'API consommés sur un budget de 8 $). Liste fusionnée et dédoublonnée : `data/kw/keywords-master.csv` (19 003 lignes : 9 884 US, 7 036 UK, 2 083 FR).

Cette étude complète `01-mots-cles-volumes.md`, `05-mots-cles-decouverte.md` et `05b-mots-cles-complementaires.md` : elle part de 17 requêtes mères par silo pour l'anglais et 20 + 20 pour le français, puis croise avec les SERP réelles et les domaines concurrents.

## 0. Méthode, définitions et limites

**Collecte.**
- `ideas` : 2 appels US (18 + 20 seeds, 11 973 idées), 1 appel UK (20 seeds, 8 818 idées), 2 appels FR (20 + 20 seeds, 2 688 idées). Fichiers `ideas_us_a.json`, `ideas_us_b.json`, `ideas_uk_a.json`, `ideas_fr_a.json`, `ideas_fr_b.json`.
- `serp` : 11 requêtes US et 8 requêtes FR (`serp_us_*.json`, `serp_fr_*.json`).
- `domain` : 13 domaines, 300 mots-clés chacun, triés par volume (`domain_us_*.json`, `domain_fr_*.json`).

**Nettoyage.** Sur 22 697 couples (mot-clé, marché) uniques, 1 226 ont un volume < 10, 1 605 sont hors sujet (jeux en ligne, applis, coloriages, impression de cartes personnalisées, proxies Magic/Pokémon, grilles de journaux NYT/LA Times, casino/loto FDJ, matériel de tableau blanc, marques de concurrents) et 863 sont du bruit sans silo identifiable. Reste 19 003 lignes, chacune affectée à un silo, à une facette (occasion, thème, âge, difficulté), à un type de page cible et à un drapeau « intention imprimable explicite » (présence de printable / print / pdf / template / worksheet / à imprimer / gratuit…).

**Groupes (clusters).** Google Ads renvoie des dizaines de variantes orthographiques avec exactement la même série mensuelle, le même CPC et la même concurrence (ex. « bingo cards printable », « print bingo cards », « bingo board printable »… = 6 600). Ce sont les mêmes recherches comptées plusieurs fois. Toutes les sommes de cette étude sont donc calculées sur des **groupes** (une série mensuelle identique = un groupe, compté une fois), ce qui donne 8 766 groupes US, 6 525 UK et 1 903 FR. Dans les tableaux, « (+N) » indique le nombre de variantes regroupées.

**Lecture des colonnes.** Volume = moyenne mensuelle Google Ads sur 12 mois (les mots-clés saisonniers font 5 à 10 fois leur moyenne sur un ou deux mois). Concurrence = concurrence publicitaire Google Ads (LOW / MEDIUM / HIGH), ce n'est pas la difficulté SEO ; elle sert d'indice de pression commerciale. CPC en dollars (US/UK) ou en euros (FR). Intention : « Téléch. » = l'internaute veut un fichier à imprimer ; « Mixte » = formulation sans marqueur d'impression, partagée avec le jeu en ligne ; « Info » = article, règles ; « Outil » = générateur.

**Limites.** Pas de volume Google Ads pour certaines formulations (ex. « jeux de société à imprimer » au pluriel, « printable puzzles for kids »). Les volumes UK sont faibles (le marché fait 10 à 15 % des États-Unis sur ces thèmes). La répartition par silo est faite par règles de mots, avec une marge d'erreur de quelques pour cent sur les chevauchements (un « christmas bingo » est compté dans Bingo avec la facette « occasion », pas dans Occasions).

**Constat transversal important : AI Overview.** Sur les 19 SERP relevées, 18 affichent un bloc « AI Overview » en tête (10 des 11 requêtes US, 8 des 8 FR). Les positions organiques 1 à 3 sont en réalité des positions 2 à 4 à l'écran. Les pages qui résistent le mieux sont celles qui donnent le fichier tout de suite (hub avec grille de PDF, générateur), pas les articles de blog.

## 1. Vue d'ensemble par silo

Volumes de groupes dédoublonnés, par marché. La colonne « imprimable explicite » ne garde que les groupes dont la formulation contient un marqueur d'impression ou de téléchargement.

### États-Unis

| Silo | Mots-clés | Groupes | Volume groupes | dont intention « imprimable » explicite |
|---|---|---|---|---|
| Mots mêlés | 1 604 | 1 324 | 355 430 | 245 270 (1178 groupes) |
| Puzzles (mots croisés, sudoku, logique…) | 2 197 | 1 924 | 297 600 | 283 700 (1851 groupes) |
| Bingo / loto | 1 666 | 1 467 | 150 850 | 95 350 (1298 groupes) |
| Points à relier | 596 | 511 | 40 220 | 39 040 (493 groupes) |
| Occasions (fêtes) | 615 | 554 | 30 320 | 27 120 (515 groupes) |
| Labyrinthes | 281 | 243 | 27 870 | 26 770 (233 groupes) |
| Classe / éducatif | 314 | 290 | 27 390 | 3 880 (39 groupes) |
| Chasse au trésor | 471 | 453 | 24 440 | 16 720 (403 groupes) |
| Jeux de plateau / PnP | 577 | 540 | 20 570 | 18 120 (517 groupes) |
| Jeux d'ambiance | 733 | 682 | 19 190 | 16 920 (646 groupes) |
| Jeux de cartes | 341 | 312 | 15 550 | 15 090 (306 groupes) |
| Générique « jeux à imprimer » | 180 | 166 | 13 730 | 13 730 (166 groupes) |
| Roll & write / dés | 145 | 145 | 5 400 | 2 560 (68 groupes) |
| Rébus | 40 | 39 | 3 340 | 3 340 (39 groupes) |
| Escape game | 75 | 67 | 2 290 | 2 290 (67 groupes) |
| Autre | 26 | 26 | 980 | 980 (26 groupes) |
| Règles | 23 | 23 | 550 | 520 (22 groupes) |
| **Total** | 9 884 | 8 766 | 1 035 720 | 811 400 |

### Royaume-Uni

| Silo | Mots-clés | Groupes | Volume groupes | dont intention « imprimable » explicite |
|---|---|---|---|---|
| Mots mêlés | 1 351 | 1 175 | 38 410 | 27 020 (1054 groupes) |
| Bingo / loto | 1 427 | 1 318 | 30 060 | 23 350 (1172 groupes) |
| Puzzles (mots croisés, sudoku, logique…) | 1 264 | 1 172 | 27 790 | 27 030 (1138 groupes) |
| Points à relier | 425 | 407 | 7 130 | 6 950 (395 groupes) |
| Jeux de plateau / PnP | 481 | 461 | 7 100 | 6 350 (439 groupes) |
| Occasions (fêtes) | 478 | 466 | 5 980 | 5 370 (435 groupes) |
| Jeux d'ambiance | 354 | 338 | 5 770 | 5 350 (306 groupes) |
| Jeux de cartes | 283 | 267 | 4 670 | 4 560 (264 groupes) |
| Labyrinthes | 212 | 197 | 3 250 | 3 150 (191 groupes) |
| Chasse au trésor | 225 | 218 | 2 730 | 2 160 (183 groupes) |
| Classe / éducatif | 145 | 134 | 2 680 | 350 (26 groupes) |
| Générique « jeux à imprimer » | 145 | 133 | 2 390 | 2 390 (133 groupes) |
| Roll & write / dés | 123 | 123 | 1 490 | 490 (46 groupes) |
| Escape game | 67 | 60 | 820 | 820 (60 groupes) |
| Rébus | 39 | 39 | 460 | 460 (39 groupes) |
| Règles | 15 | 15 | 150 | 140 (14 groupes) |
| Autre | 2 | 2 | 60 | 60 (2 groupes) |
| **Total** | 7 036 | 6 525 | 140 940 | 116 000 |

### France

| Silo | Mots-clés | Groupes | Volume groupes | dont intention « imprimable » explicite |
|---|---|---|---|---|
| Puzzles (mots croisés, sudoku, logique…) | 577 | 503 | 43 730 | 43 390 (499 groupes) |
| Points à relier | 244 | 218 | 15 110 | 5 570 (83 groupes) |
| Chasse au trésor | 175 | 157 | 10 100 | 10 090 (156 groupes) |
| Jeux de cartes | 239 | 223 | 9 960 | 9 960 (223 groupes) |
| Mots mêlés | 84 | 73 | 9 060 | 9 060 (73 groupes) |
| Jeux de plateau / PnP | 177 | 170 | 7 500 | 7 490 (169 groupes) |
| Classe / éducatif | 148 | 139 | 6 400 | 6 360 (136 groupes) |
| Labyrinthes | 44 | 39 | 4 180 | 4 180 (39 groupes) |
| Occasions (fêtes) | 67 | 61 | 3 980 | 3 960 (60 groupes) |
| Bingo / loto | 98 | 97 | 3 510 | 3 510 (97 groupes) |
| Escape game | 63 | 63 | 2 440 | 2 440 (63 groupes) |
| Générique « jeux à imprimer » | 85 | 80 | 2 380 | 2 380 (80 groupes) |
| Jeux d'ambiance | 55 | 54 | 1 400 | 1 370 (53 groupes) |
| Rébus | 16 | 15 | 720 | 720 (15 groupes) |
| Roll & write / dés | 11 | 11 | 400 | 10 (1 groupes) |
| **Total** | 2 083 | 1 903 | 120 870 | 110 490 |

**Ce que disent ces chiffres.**
1. Les puzzles imprimables (mots mêlés, mots croisés, sudoku, points à relier, labyrinthes) pèsent 70 % de la demande US et 60 % de la demande FR. Les « vrais » jeux de société print and play (plateau, cartes, roll & write, escape, chasse au trésor) pèsent moins de 10 %. Le site doit être pensé comme un **site de puzzles et jeux imprimables** dont le print and play est une spécialité, pas l'inverse.
2. Le silo Bingo est le deuxième marché US (150 850 / mois en groupes) et il est saisonnier : 57 270 de ce volume porte une fête (Noël 33 830, Halloween 11 750, Saint-Valentin 4 330, Pâques 1 730).
3. Les mots croisés et le sudoku imprimables (297 600 en groupes US, 43 730 FR) ne sont pas dans l'architecture actuelle (`06-architecture-seo.md`). C'est le plus gros angle mort : ces grilles se génèrent par programme et les concurrents qui les dominent (krazydad.com, justfamilyfun.com) sont des sites d'une ou deux personnes.
4. Le marché FR est 8 à 9 fois plus petit que le marché US sur ces thèmes, mais la concurrence y est plus faible (voir § 5) : `sudoku à imprimer` (9 900), `mots mêlés à imprimer` (4 400), `points à relier` (2 400 + 1 900 + 1 600), `chasse au trésor gratuite à imprimer pdf` (1 900), `labyrinthe à imprimer` (1 300).
5. Les requêtes « escape room printable » (2 290 en groupes US, 2 440 FR) et « roll and write » (5 400 US, 400 FR) sont petites mais à fort CPC (4,36 $ pour « escape room printable free », 7,51 $ pour « free printable escape room pdf », 7,10 € pour « escape game gratuit pdf ») : la demande est commerciale, les kits payants achètent ces clics.

## 2. Top 150 des mots-clés anglophones (groupes, triés par volume US)

Colonnes : groupe (nombre de variantes), volume US, volume UK (meilleure variante du groupe), concurrence Ads, CPC $, intention, silo, type de page cible.

| Groupe de mots-clés | US | UK | Conc. | CPC | Intention | Silo | Page cible |
|---|---|---|---|---|---|---|---|
| word search printable (+8) | 60 500 | 2 900 | LOW | 2.12 | Téléch. | Mots mêlés | hub silo |
| crossword games printable (+1) | 40 500 | – | LOW | 1.42 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| free printable crosswords (+5) | 27 100 | 480 | LOW | 0.69 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| free word search printable (+9) | 27 100 | 1 300 | LOW | 1.84 | Téléch. | Mots mêlés | sous-page silo |
| printable sudoku game (+2) | 27 100 | 1 900 | LOW | 0.54 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| christmas word search (+3) | 18 100 | 4 400 | HIGH | 0.23 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| word search activity sheets (+1) | 18 100 | 1 600 | LOW | 2.02 | Téléch. | Mots mêlés | sous-page silo |
| printable sudoku (+1) | 12 100 | 1 000 | LOW | 2.51 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| thanksgiving word search (+5) | 12 100 | – | HIGH | 0.27 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| word search for halloween (+1) | 12 100 | 1 000 | MEDIUM | 0.13 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| christmas bingo game (+2) | 9 900 | 480 | HIGH | 0.27 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| dot to dot printable (+7) | 9 900 | 1 300 | LOW | 1.89 | Téléch. | Points à relier | sous-page silo |
| blank bingo card | 9 900 | 590 | LOW | 0.11 | Mixte | Bingo / loto | fiche gabarit vierge |
| free printable sudoku games (+2) | 9 900 | 480 | LOW | 0.56 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| adult word search printable (+12) | 8 100 | 590 | LOW | 2.10 | Téléch. | Mots mêlés | sous-page facette |
| bingo card template (+3) | 8 100 | 1 300 | MEDIUM | 0.15 | Téléch. | Bingo / loto | fiche gabarit vierge |
| printable sudoku pages (+5) | 8 100 | 390 | LOW | 0.59 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| hard printable word search (+9) | 8 100 | 390 | LOW | 2.79 | Téléch. | Mots mêlés | sous-page facette |
| holiday christmas bingo | 8 100 | 1 900 | HIGH | 0.27 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| spring word searches (+1) | 8 100 | 390 | LOW | 0.01 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| summer word searches (+2) | 8 100 | 880 | LOW | 0.02 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| bingo cards printable (+6) | 6 600 | 1 600 | HIGH | 0.28 | Téléch. | Bingo / loto | hub silo |
| maze printable (+1) | 6 600 | 480 | LOW | 1.14 | Téléch. | Labyrinthes | hub silo |
| fall word searches | 6 600 | 390 | LOW | 0.14 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| free printable sudoku sheets (+1) | 6 600 | 90 | LOW | 0.85 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| free printable adult word search (+7) | 5 400 | 320 | LOW | 2.17 | Téléch. | Mots mêlés | sous-page facette |
| bingo template (+1) | 5 400 | 1 000 | LOW | 0.09 | Téléch. | Bingo / loto | fiche gabarit vierge |
| printable crosswords (+1) | 5 400 | 880 | LOW | 0.63 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| easy printable sudoku (+4) | 5 400 | 390 | LOW | 0.36 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| winter word searches | 5 400 | 260 | LOW | 0.84 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| bingo sheets (+1) | 4 400 | 1 600 | HIGH | 0.48 | Téléch. | Bingo / loto | hub silo |
| printable adult crosswords (+6) | 4 400 | 90 | LOW | 4.20 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| bingo cards printable free (+4) | 4 400 | 390 | LOW | 1.44 | Téléch. | Bingo / loto | sous-page silo |
| bingo card empty (+1) | 4 400 | 390 | LOW | 0.11 | Mixte | Bingo / loto | fiche gabarit vierge |
| printable puzzles (+1) | 4 400 | 590 | LOW | 3.02 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| christmas bingo cards (+2) | 4 400 | 260 | HIGH | 0.24 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| puzzles to print (+1) | 4 400 | 260 | LOW | 0.98 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| christmas word search printable (+8) | 4 400 | 720 | MEDIUM | 0.15 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| daily free crosswords printable (+1) | 4 400 | 110 | LOW | 0.81 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| big printable word search (+5) | 4 400 | 480 | MEDIUM | 0.49 | Téléch. | Mots mêlés | sous-page silo |
| bingo game halloween | 4 400 | 720 | HIGH | 0.51 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| outdoor scavenger hunt for preschoolers | 3 600 | 210 | HIGH | 0.15 | Mixte | Chasse au trésor | sous-page facette |
| christmas printable games (+1) | 3 600 | 210 | HIGH | 0.18 | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| logic grid printable (+4) | 3 600 | 110 | LOW | 2.08 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| word search printable pdf (+2) | 3 600 | 320 | LOW | 4.12 | Téléch. | Mots mêlés | sous-page silo |
| word search pdf (+2) | 3 600 | 480 | LOW | 4.05 | Téléch. | Mots mêlés | hub silo |
| halloween word search printable (+3) | 3 600 | 210 | LOW | 0.19 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| easter word search (+2) | 3 600 | 1 300 | LOW | 0.02 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| free printable childrens word search | 3 600 | 390 | LOW | 1.77 | Téléch. | Mots mêlés | sous-page facette |
| valentine day word search | 3 600 | 110 | LOW | – | Mixte | Mots mêlés | page programmatique (thème/fête) |
| couples shower games printable | 2 900 | 70 | HIGH | 0.40 | Téléch. | Générique « jeux à imprimer » | sous-page silo |
| blank bingo card printable (+3) | 2 900 | 70 | LOW | 0.48 | Téléch. | Bingo / loto | fiche gabarit vierge |
| christmas bingo printable (+5) | 2 900 | 390 | HIGH | 0.16 | Téléch. | Bingo / loto | page programmatique (thème/fête) |
| whiteboard games (+1) | 2 900 | 590 | LOW | 0.36 | Mixte | Classe / éducatif | hub silo (intention mixte) |
| games to play in class | 2 900 | – | LOW | 4.62 | Mixte | Classe / éducatif | hub silo (intention mixte) |
| dot to dot free printables | 2 900 | 140 | LOW | 2.01 | Téléch. | Points à relier | sous-page silo |
| valentine's day bingo (+1) | 2 900 | 140 | HIGH | 0.84 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| games esl | 2 900 | – | LOW | 2.90 | Mixte | Classe / éducatif | hub silo (intention mixte) |
| large printable word search (+4) | 2 900 | 260 | MEDIUM | 0.33 | Téléch. | Mots mêlés | sous-page facette |
| christmas holiday word scramble | 2 900 | 210 | HIGH | 0.05 | Mixte | Puzzles (mots croisés, sudoku, logique…) | page programmatique (thème/fête) |
| christmas word search free printable (+10) | 2 900 | 320 | LOW | – | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| dot to dot marker printables | 2 900 | 50 | LOW | 0.44 | Téléch. | Points à relier | sous-page silo |
| patrick's day word search (+1) | 2 900 | 110 | LOW | 0.01 | Mixte | Mots mêlés | hub silo (intention mixte) |
| printable thanksgiving word search (+2) | 2 900 | – | MEDIUM | 0.27 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| valentine word searches (+1) | 2 900 | 170 | LOW | – | Mixte | Mots mêlés | page programmatique (thème/fête) |
| word search for 1st grader | 2 900 | 10 | MEDIUM | 0.29 | Mixte | Mots mêlés | sous-page facette |
| printable poker cards (+3) | 2 400 | 880 | HIGH | 2.86 | Téléch. | Jeux de cartes | hub silo |
| free bingo cards (+2) | 2 400 | 390 | LOW | 0.20 | Téléch. | Bingo / loto | hub silo |
| free printable adult crosswords (+1) | 2 400 | 20 | LOW | 2.59 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| word search maker free printable (+5) | 2 400 | 320 | LOW | 0.74 | Outil | Mots mêlés | outil (générateur) |
| crossword pdf printable (+3) | 2 400 | 90 | LOW | 3.64 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| crossword easy printable (+5) | 2 400 | 210 | LOW | 1.92 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| sudoku free printable (+1) | 2 400 | 260 | LOW | 1.10 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| free maze printables (+2) | 2 400 | 90 | LOW | 1.19 | Téléch. | Labyrinthes | hub silo |
| holidays word search | 2 400 | 70 | MEDIUM | 0.51 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| word search for 3rd grader | 2 400 | 10 | LOW | 0.58 | Mixte | Mots mêlés | sous-page facette |
| free printable mazes for kindergarten | 1 900 | 90 | LOW | 1.58 | Téléch. | Labyrinthes | sous-page facette |
| checkers printable | 1 900 | 210 | HIGH | 0.35 | Téléch. | Jeux de plateau / PnP | hub silo |
| scavenger hunt templates | 1 900 | – | MEDIUM | 2.17 | Téléch. | Chasse au trésor | hub silo |
| crossword maker free printable (+5) | 1 900 | 140 | MEDIUM | 1.43 | Outil | Puzzles (mots croisés, sudoku, logique…) | outil (générateur) |
| free childrens word search | 1 900 | 260 | LOW | 1.45 | Téléch. | Mots mêlés | sous-page facette |
| free printable thanksgiving word search (+4) | 1 900 | – | LOW | – | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| kindergarten maze printable | 1 900 | 90 | MEDIUM | 1.24 | Téléch. | Labyrinthes | sous-page facette |
| printable games | 1 600 | 320 | LOW | 0.83 | Téléch. | Générique « jeux à imprimer » | hub silo |
| adult word search free | 1 600 | 390 | LOW | 2.38 | Téléch. | Mots mêlés | sous-page facette |
| free hidden picture printables | 1 600 | 10 | LOW | 1.55 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| printable tic tac toe (+3) | 1 600 | 50 | LOW | 0.16 | Téléch. | Jeux de plateau / PnP | sous-page silo |
| rebus puzzles printable (+1) | 1 600 | 40 | LOW | 0.30 | Téléch. | Rébus | hub silo |
| quick games to play in the classroom | 1 600 | – | LOW | 1.97 | Mixte | Classe / éducatif | hub silo (intention mixte) |
| halloween bingo cards | 1 600 | 70 | HIGH | 0.36 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| free printable christmas games (+3) | 1 600 | 90 | LOW | 0.47 | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| word puzzles printable (+1) | 1 600 | 70 | LOW | 0.97 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| crossword puzzles to print (+3) | 1 600 | 210 | LOW | 2.29 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| blank bingo template (+1) | 1 600 | 140 | LOW | 0.07 | Téléch. | Bingo / loto | fiche gabarit vierge |
| bingo card template free (+4) | 1 600 | 110 | LOW | 0.06 | Téléch. | Bingo / loto | fiche gabarit vierge |
| blank sudoku grid (+1) | 1 600 | – | LOW | 0.32 | Mixte | Puzzles (mots croisés, sudoku, logique…) | fiche gabarit vierge |
| christmas crossword printable (+4) | 1 600 | 210 | MEDIUM | 0.10 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | page programmatique (thème/fête) |
| crossword puzzle summer | 1 600 | 110 | LOW | – | Mixte | Puzzles (mots croisés, sudoku, logique…) | page programmatique (thème/fête) |
| earth day wordsearch | 1 600 | 40 | LOW | – | Mixte | Mots mêlés | hub silo (intention mixte) |
| free halloween printable word search (+2) | 1 600 | 70 | LOW | 0.50 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| maze sheets (+3) | 1 600 | 140 | LOW | 1.20 | Téléch. | Labyrinthes | hub silo |
| new year word search (+1) | 1 600 | 140 | LOW | – | Mixte | Mots mêlés | page programmatique (thème/fête) |
| printable summer word search (+2) | 1 600 | 110 | LOW | 0.02 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| wordsearch for kindergarten (+1) | 1 600 | 10 | MEDIUM | 0.86 | Mixte | Mots mêlés | sous-page facette |
| word searches for middle schoolers | 1 600 | 10 | LOW | 1.98 | Mixte | Mots mêlés | hub silo (intention mixte) |
| printable puzzles for adults (+2) | 1 300 | 140 | LOW | 1.45 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| christmas light scavenger hunt (+1) | 1 300 | 30 | HIGH | 0.03 | Mixte | Chasse au trésor | page programmatique (thème/fête) |
| fall word search printable (+6) | 1 300 | 50 | LOW | 0.17 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| thanksgiving printable games (+1) | 1 300 | – | HIGH | 0.15 | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| halloween bingo printable (+4) | 1 300 | 170 | HIGH | 0.34 | Téléch. | Bingo / loto | page programmatique (thème/fête) |
| halloween bingo game | 1 300 | 50 | HIGH | 0.52 | Mixte | Bingo / loto | page programmatique (thème/fête) |
| christmas scattergories (+1) | 1 300 | 170 | HIGH | 0.16 | Mixte | Occasions (fêtes) | page programmatique (thème/fête) |
| word search worksheets (+1) | 1 300 | 170 | LOW | 0.19 | Téléch. | Mots mêlés | hub silo |
| word find books large print (+2) | 1 300 | 390 | HIGH | 0.52 | Téléch. | Mots mêlés | sous-page facette |
| christmas bingo cards printable (+2) | 1 300 | 50 | HIGH | 0.28 | Téléch. | Bingo / loto | page programmatique (thème/fête) |
| spot the difference printable (+2) | 1 300 | 390 | LOW | 1.60 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| free printable puzzles (+1) | 1 300 | 260 | LOW | 2.75 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| pictionary whiteboard (+2) | 1 300 | 30 | LOW | 0.38 | Mixte | Jeux d'ambiance | hub silo (intention mixte) |
| bingo sheet generator | 1 300 | 320 | LOW | 0.64 | Outil | Bingo / loto | outil (générateur) |
| christmas bingo free printable (+5) | 1 300 | 110 | MEDIUM | 0.33 | Téléch. | Bingo / loto | page programmatique (thème/fête) |
| free christmas word search puzzle (+2) | 1 300 | 170 | LOW | – | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| easy printable word search (+8) | 1 300 | 140 | LOW | 1.25 | Téléch. | Mots mêlés | sous-page facette |
| free printables for easter | 1 300 | – | LOW | – | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| free thanksgiving word search (+4) | 1 300 | – | LOW | – | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| game to play on whiteboard (+3) | 1 300 | 260 | LOW | – | Mixte | Classe / éducatif | hub silo (intention mixte) |
| printable samurai sudoku (+1) | 1 300 | 210 | LOW | 0.05 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| printable sudoku puzzles pdf | 1 300 | 90 | LOW | 1.46 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| thanks giving word scramble | 1 300 | 10 | HIGH | 0.08 | Mixte | Puzzles (mots croisés, sudoku, logique…) | hub silo (intention mixte) |
| printable board games (+1) | 1 000 | 260 | LOW | 1.09 | Téléch. | Jeux de plateau / PnP | hub silo |
| printable playing cards (+4) | 1 000 | 210 | MEDIUM | 1.99 | Téléch. | Jeux de cartes | hub silo |
| bingo printable sheet (+4) | 1 000 | 480 | HIGH | 0.29 | Téléch. | Bingo / loto | hub silo |
| free sight word activities | 1 000 | 10 | MEDIUM | 1.60 | Téléch. | Classe / éducatif | sous-page silo |
| blank bingo card free printable (+5) | 1 000 | 30 | LOW | 0.01 | Téléch. | Bingo / loto | fiche gabarit vierge |
| i spy game printable | 1 000 | 50 | LOW | 0.34 | Téléch. | Générique « jeux à imprimer » | sous-page silo |
| walgreens puzzle | 1 000 | – | HIGH | 0.89 | Mixte | Puzzles (mots croisés, sudoku, logique…) | hub silo (intention mixte) |
| crossword puzzle template | 1 000 | – | LOW | 0.90 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | fiche gabarit vierge |
| 100 hard word search puzzles printable | 1 000 | 50 | LOW | 3.55 | Téléch. | Mots mêlés | sous-page facette |
| 100 word search printable (+3) | 1 000 | 40 | LOW | 4.77 | Téléch. | Mots mêlés | sous-page silo |
| 4th july word search (+4) | 1 000 | 10 | LOW | 0.08 | Mixte | Mots mêlés | hub silo (intention mixte) |
| bingo card generator free printable (+1) | 1 000 | 40 | LOW | – | Outil | Bingo / loto | outil (générateur) |
| extreme dot to dot printable (+3) | 1 000 | 70 | LOW | 1.53 | Téléch. | Points à relier | sous-page silo |
| childrens xmas word search | 1 000 | 390 | HIGH | 0.16 | Mixte | Mots mêlés | page programmatique (thème/fête) |
| connect the dot sheets (+3) | 1 000 | – | LOW | 1.84 | Téléch. | Points à relier | sous-page silo |
| crossword pdf | 1 000 | 110 | LOW | 7.24 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| daily printable sudoku (+2) | 1 000 | 40 | LOW | 0.02 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| free printable word searches for adults pdf | 1 000 | 70 | LOW | 2.95 | Téléch. | Mots mêlés | sous-page facette |
| hard printable sudoku (+1) | 1 000 | 70 | LOW | 0.02 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| printable spring word search (+1) | 1 000 | 40 | LOW | – | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| printable winter word search | 1 000 | 30 | LOW | 1.39 | Téléch. | Mots mêlés | page programmatique (thème/fête) |
| free printable easy crosswords for adults (+1) | 880 | 50 | LOW | 4.11 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |

### Complément : top 25 UK

| Groupe | UK | Conc. | Silo |
|---|---|---|---|
| christmas word search (+3) | 4 400 | HIGH | Mots mêlés |
| word search printable (+8) | 2 900 | LOW | Mots mêlés |
| sudoku printable (+2) | 1 900 | LOW | Puzzles (mots croisés, sudoku, logique…) |
| holiday christmas bingo | 1 900 | HIGH | Bingo / loto |
| printable bingo cards (+5) | 1 600 | HIGH | Bingo / loto |
| bingo sheets (+1) | 1 600 | HIGH | Bingo / loto |
| word search activity sheets (+1) | 1 600 | LOW | Mots mêlés |
| dot to dot printable (+4) | 1 300 | LOW | Points à relier |
| free word search printable (+9) | 1 300 | LOW | Mots mêlés |
| bingo card template (+3) | 1 300 | HIGH | Bingo / loto |
| easter word search (+2) | 1 300 | LOW | Mots mêlés |
| bingo template (+1) | 1 000 | LOW | Bingo / loto |
| word search for halloween (+1) | 1 000 | HIGH | Mots mêlés |
| print sudoku | 1 000 | LOW | Puzzles (mots croisés, sudoku, logique…) |
| printable poker cards (+3) | 880 | HIGH | Jeux de cartes |
| crossword puzzles printable (+1) | 880 | LOW | Puzzles (mots croisés, sudoku, logique…) |
| printable crosswords | 880 | LOW | Puzzles (mots croisés, sudoku, logique…) |
| summer word searches (+2) | 880 | LOW | Mots mêlés |
| christmas word search printable (+8) | 720 | HIGH | Mots mêlés |
| bingo game halloween | 720 | HIGH | Bingo / loto |
| whiteboard games (+1) | 590 | LOW | Classe / éducatif |
| printable puzzles (+1) | 590 | MEDIUM | Puzzles (mots croisés, sudoku, logique…) |
| blank bingo card | 590 | MEDIUM | Bingo / loto |
| printable word searches for adults (+9) | 590 | LOW | Mots mêlés |
| template for word search (+1) | 590 | LOW | Mots mêlés |

Lecture : le Royaume-Uni suit les mêmes thèmes à l'échelle 1/10, avec un poids plus fort du bingo (Noël, Halloween) et du « whiteboard games » (590). Les pages anglaises servent les deux marchés ; seule différence utile : proposer le format A4 à côté du format Letter, et l'orthographe britannique dans quelques textes (colour, favourite).

## 3. Top 100 des mots-clés français (groupes, triés par volume)

| Groupe de mots-clés | FR | Conc. | CPC € | Intention | Silo | Page cible |
|---|---|---|---|---|---|---|
| sudoku à imprimer (+4) | 9 900 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| mots mêlés à imprimer (+3) | 4 400 | LOW | 0.13 | Téléch. | Mots mêlés | sous-page silo |
| point à relier (+2) | 2 400 | LOW | 0.47 | Mixte | Points à relier | hub silo (intention mixte) |
| chasse au trésor gratuite à imprimer pdf | 1 900 | LOW | 0.25 | Téléch. | Chasse au trésor | sous-page silo |
| point a relier (+1) | 1 900 | LOW | 0.16 | Mixte | Points à relier | hub silo (intention mixte) |
| sudoku gratuit à imprimer (+6) | 1 900 | LOW | 0.29 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| point relier à imprimer (+4) | 1 600 | LOW | 0.09 | Téléch. | Points à relier | sous-page silo |
| sudoku a imprimer | 1 600 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| labyrinthe à imprimer (+2) | 1 300 | LOW | 0.13 | Téléch. | Labyrinthes | hub silo |
| mots croisés à imprimer (+1) | 1 300 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| grille sudoku à imprimer (+2) | 1 300 | LOW | 0.00 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| imprimer mots fléchés (+4) | 1 300 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| enigme chasse au trésor à imprimer gratuit | 1 000 | LOW | 0.05 | Téléch. | Chasse au trésor | sous-page silo |
| tangram à imprimer (+1) | 1 000 | LOW | 0.02 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| sudoku à imprimer pdf | 880 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| jeu de l'oie à imprimer (+1) | 720 | LOW | 0.09 | Téléch. | Jeux de plateau / PnP | sous-page silo |
| carte trésor à imprimer (+4) | 720 | LOW | 0.03 | Téléch. | Chasse au trésor | sous-page silo |
| cartes loup garou à imprimer | 720 | LOW | – | Téléch. | Jeux de cartes | sous-page silo |
| activites halloween a imprimer | 720 | LOW | 0.01 | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| sudoku facile à imprimer (+4) | 720 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| mots fléchés à imprimer pdf | 720 | LOW | 0.55 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| imprimer un jeu de cartes (+4) | 590 | HIGH | 0.98 | Téléch. | Jeux de cartes | sous-page silo |
| point a relier adulte | 590 | MEDIUM | 0.08 | Mixte | Points à relier | sous-page facette |
| imprimer carton loto | 590 | HIGH | 0.26 | Téléch. | Bingo / loto | hub silo |
| mots mélés à imprimer gratuit (+3) | 590 | LOW | – | Téléch. | Mots mêlés | sous-page silo |
| mots mêlés à imprimer pdf | 590 | LOW | – | Téléch. | Mots mêlés | sous-page silo |
| puzzle à imprimer (+3) | 480 | HIGH | 1.91 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| jeux éducatif à imprimer pdf | 480 | LOW | 5.81 | Téléch. | Classe / éducatif | sous-page silo |
| e sudoku à imprimer | 480 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| grille de sudoku à imprimer (+2) | 480 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| mots fleches gratuit à imprimer (+5) | 480 | LOW | 0.92 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| jeu point à relier (+3) | 480 | LOW | 0.22 | Mixte | Points à relier | hub silo (intention mixte) |
| point à relier adulte (+4) | 480 | HIGH | 0.16 | Mixte | Points à relier | sous-page facette |
| points à relier pdf gratuit | 480 | LOW | – | Téléch. | Points à relier | sous-page silo |
| puzzle à imprimer et découper pdf | 480 | LOW | 0.63 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| chasse au trésor à imprimer (+4) | 390 | MEDIUM | 0.52 | Téléch. | Chasse au trésor | sous-page silo |
| bataille navale à imprimer (+1) | 390 | LOW | – | Téléch. | Jeux de plateau / PnP | sous-page silo |
| carte dixit à imprimer | 390 | LOW | 0.08 | Téléch. | Jeux de cartes | sous-page silo |
| jeu de piste gratuit à imprimer | 390 | LOW | 0.19 | Téléch. | Chasse au trésor | sous-page silo |
| grilles sudoku vierges (+2) | 390 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| jeu de noel a imprimer (+1) | 390 | LOW | – | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| jeu différences à imprimer (+2) | 390 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| labyrinthe a imprimer | 390 | LOW | – | Téléch. | Labyrinthes | hub silo |
| mots cachés à imprimer (+1) | 390 | LOW | 0.23 | Téléch. | Mots mêlés | sous-page silo |
| mots croisés animaux imprimer | 390 | LOW | 0.01 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | page programmatique (thème/fête) |
| mots croisés à imprimer pdf | 390 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| mots mélés à imprimer adulte (+1) | 390 | LOW | – | Téléch. | Mots mêlés | sous-page facette |
| plusieurs grilles de sudoku à imprimer | 390 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| point à relier à imprimer de 1 à 100 | 390 | LOW | – | Téléch. | Points à relier | sous-page silo |
| points à relier adulte pdf gratuit | 390 | LOW | – | Téléch. | Points à relier | sous-page facette |
| sudoku difficile à imprimer (+2) | 390 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| chasse au trésor à imprimer gratuit (+1) | 320 | LOW | 0.15 | Téléch. | Chasse au trésor | sous-page silo |
| billets monopoly à imprimer | 320 | LOW | 0.27 | Téléch. | Jeux de plateau / PnP | sous-page silo |
| chasse au trésor paques gratuite à imprimer pdf (+1) | 320 | LOW | – | Téléch. | Chasse au trésor | page programmatique (thème/fête) |
| jeux halloween à imprimer | 320 | LOW | 0.29 | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| chasse aux œufs énigmes à imprimer | 320 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| sudoku moyen à imprimer (+2) | 320 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| jeu a imprimer adulte (+2) | 320 | LOW | – | Téléch. | Générique « jeux à imprimer » | sous-page facette |
| jeu labyrinthe à imprimer (+1) | 320 | LOW | – | Téléch. | Labyrinthes | sous-page silo |
| mots croises gratuits à imprimer (+4) | 320 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| mots croisés à imprimer facile | 320 | LOW | 0.03 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| mots fleches à imprimer | 320 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| mots meles a imprimer | 320 | LOW | – | Téléch. | Mots mêlés | sous-page silo |
| mots meles à imprimer pour personnes agees | 320 | LOW | 1.53 | Téléch. | Mots mêlés | sous-page facette |
| escape game à imprimer | 260 | MEDIUM | 0.52 | Téléch. | Escape game | sous-page silo |
| jeu de plateau à imprimer (+1) | 260 | LOW | 0.98 | Téléch. | Jeux de plateau / PnP | sous-page silo |
| memory à imprimer | 260 | LOW | – | Téléch. | Jeux de cartes | hub silo |
| créer un jeu de l oie à imprimer | 260 | LOW | – | Téléch. | Jeux de plateau / PnP | sous-page silo |
| kit escape game gratuit pdf | 260 | LOW | – | Téléch. | Escape game | sous-page silo |
| énigme jeu de piste gratuit a imprimer | 260 | LOW | – | Téléch. | Chasse au trésor | sous-page silo |
| activité pâques à imprimer | 260 | LOW | 0.42 | Téléch. | Occasions (fêtes) | page programmatique (thème/fête) |
| jeu 7 différences à imprimer (+1) | 260 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| jeu de mémoire adulte à imprimer (+1) | 260 | LOW | 2.22 | Téléch. | Classe / éducatif | sous-page facette |
| jeux mathématiques gs à imprimer | 260 | LOW | 0.12 | Téléch. | Classe / éducatif | sous-page silo |
| labyrinthe jeu à imprimer | 260 | LOW | 0.02 | Téléch. | Labyrinthes | sous-page silo |
| mots croisés à imprimer pour adulte pdf | 260 | LOW | 1.44 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| mots fleches a imprimer (+1) | 260 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| mots mélés grande grille à imprimer | 260 | LOW | 0.03 | Téléch. | Mots mêlés | sous-page silo |
| planche loto à imprimer | 260 | MEDIUM | 0.36 | Téléch. | Bingo / loto | sous-page silo |
| point à relier à imprimer de 1 à 200 | 260 | LOW | – | Téléch. | Points à relier | sous-page silo |
| sudoku gratuit à imprimer pdf | 260 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| carte à jouer à imprimer (+3) | 210 | HIGH | 1.40 | Téléch. | Jeux de cartes | sous-page silo |
| jeux pour autiste gratuit à imprimer | 210 | LOW | 2.52 | Téléch. | Classe / éducatif | sous-page silo |
| carte tresor a imprimer (+2) | 210 | MEDIUM | 0.14 | Téléch. | Chasse au trésor | sous-page silo |
| carte de jeu a imprimer (+1) | 210 | LOW | 0.72 | Téléch. | Jeux de cartes | sous-page silo |
| carte de jeu à imprimer (+2) | 210 | MEDIUM | 0.91 | Téléch. | Jeux de cartes | sous-page silo |
| carte time's up à imprimer | 210 | LOW | – | Téléch. | Jeux de cartes | sous-page silo |
| jeu de 7 familles vierge à imprimer | 210 | LOW | – | Téléch. | Jeux de cartes | sous-page facette |
| jeu de carte à imprimer pdf | 210 | LOW | 0.21 | Téléch. | Jeux de cartes | sous-page silo |
| jeu de l oie à imprimer pdf | 210 | LOW | – | Téléch. | Jeux de plateau / PnP | sous-page silo |
| jeu des 10 différences gratuit à imprimer | 210 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| jeux de concentration à imprimer | 210 | MEDIUM | 0.23 | Téléch. | Classe / éducatif | sous-page silo |
| jeux des 12 erreurs gratuit imprimer adulte | 210 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page facette |
| rébus à imprimer | 210 | LOW | – | Téléch. | Rébus | hub silo |
| jeu maternelle à imprimer (+2) | 210 | LOW | 0.89 | Téléch. | Classe / éducatif | sous-page facette |
| e sudoku fr à imprimer | 210 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| enigme a imprimer | 210 | LOW | – | Téléch. | Puzzles (mots croisés, sudoku, logique…) | hub silo |
| grille sudoku à remplir | 210 | LOW | – | Mixte | Puzzles (mots croisés, sudoku, logique…) | hub silo (intention mixte) |
| jeux des différences à imprimer pdf | 210 | LOW | 4.99 | Téléch. | Puzzles (mots croisés, sudoku, logique…) | sous-page silo |
| jeux grande section à imprimer | 210 | LOW | 0.42 | Téléch. | Classe / éducatif | sous-page silo |

## 4. Grappes de mots-clés par silo

Pour chaque silo : nombre de groupes, volume total des groupes, répartition par facette, et les groupes de tête. Les groupes « sans facette » sont les requêtes génériques du hub ; les facettes indiquent les sous-pages à créer.

### Mots mêlés — US : 1324 groupes, 355 430 recherches / mois

Facettes : aucune : 604 groupes / 159 920, occasion : 401 groupes / 131 830, age : 190 groupes / 37 790, difficulte : 228 groupes / 28 880, theme : 89 groupes / 4 650.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| word search printable (+8) | 60 500 | LOW | hub silo |
| free word search printable (+9) | 27 100 | LOW | sous-page silo |
| christmas word search (+3) | 18 100 | HIGH | page programmatique (thème/fête) |
| word search activity sheets (+1) | 18 100 | LOW | sous-page silo |
| thanksgiving word search (+5) | 12 100 | HIGH | page programmatique (thème/fête) |
| word search for halloween (+1) | 12 100 | MEDIUM | page programmatique (thème/fête) |
| adult word search printable (+12) | 8 100 | LOW | sous-page facette |
| hard printable word search (+9) | 8 100 | LOW | sous-page facette |
| spring word searches (+1) | 8 100 | LOW | page programmatique (thème/fête) |
| summer word searches (+2) | 8 100 | LOW | page programmatique (thème/fête) |

### Mots mêlés — FR : 73 groupes, 9 060 recherches / mois

Facettes : aucune : 36 groupes / 7 170, age : 21 groupes / 1 260, difficulte : 12 groupes / 670, occasion : 4 groupes / 40, theme : 1 groupes / 10.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| mots mêlés à imprimer (+3) | 4 400 | LOW | sous-page silo |
| mots mélés à imprimer gratuit (+3) | 590 | LOW | sous-page silo |
| mots mêlés à imprimer pdf | 590 | LOW | sous-page silo |
| mots cachés à imprimer (+1) | 390 | LOW | sous-page silo |
| mots mélés à imprimer adulte (+1) | 390 | LOW | sous-page facette |
| mots meles a imprimer | 320 | LOW | sous-page silo |
| mots meles à imprimer pour personnes agees | 320 | LOW | sous-page facette |
| mots mélés grande grille à imprimer | 260 | LOW | sous-page silo |

**Analyse.** Le plus gros silo. Hub `/puzzles/word-search/` + facettes difficulté (hard 8 100, easy 1 300, large print 2 900 + 4 400 « big printable word search »), public (adults 8 100 + 5 400 + 1 600, kids 3 600 + 1 900, par niveau scolaire : 1st grade 2 900, 3rd grade 2 400, kindergarten 1 600, middle school 1 600) et surtout saison / fête (voir § 7). Le générateur « word search maker free printable » (2 400) justifie un outil en ligne qui produit le PDF. FR : `mots mêlés à imprimer` 4 400, adulte 390, personnes âgées 320, facile 210, gros caractères 110, grande grille 260.

### Puzzles (mots croisés, sudoku, logique…) — US : 1924 groupes, 297 600 recherches / mois

Facettes : aucune : 1093 groupes / 237 060, difficulte : 276 groupes / 22 340, occasion : 349 groupes / 22 240, age : 255 groupes / 18 250, theme : 45 groupes / 1 390.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| crossword games printable (+1) | 40 500 | LOW | hub silo |
| free printable crosswords (+5) | 27 100 | LOW | hub silo |
| printable sudoku game (+2) | 27 100 | LOW | hub silo |
| printable sudoku (+1) | 12 100 | LOW | hub silo |
| free printable sudoku games (+2) | 9 900 | LOW | sous-page silo |
| printable sudoku pages (+5) | 8 100 | LOW | hub silo |
| free printable sudoku sheets (+1) | 6 600 | LOW | sous-page silo |
| printable crosswords (+1) | 5 400 | LOW | hub silo |
| easy printable sudoku (+4) | 5 400 | LOW | sous-page facette |
| printable adult crosswords (+6) | 4 400 | LOW | sous-page facette |

### Puzzles (mots croisés, sudoku, logique…) — FR : 503 groupes, 43 730 recherches / mois

Facettes : aucune : 358 groupes / 36 140, difficulte : 61 groupes / 3 680, age : 69 groupes / 3 250, theme : 10 groupes / 570, occasion : 6 groupes / 110.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| sudoku à imprimer (+4) | 9 900 | LOW | hub silo |
| sudoku gratuit à imprimer (+6) | 1 900 | LOW | sous-page silo |
| sudoku a imprimer | 1 600 | LOW | hub silo |
| mots croisés à imprimer (+1) | 1 300 | LOW | sous-page silo |
| grille sudoku à imprimer (+2) | 1 300 | LOW | sous-page silo |
| imprimer mots fléchés (+4) | 1 300 | LOW | hub silo |
| tangram à imprimer (+1) | 1 000 | LOW | hub silo |
| sudoku à imprimer pdf | 880 | LOW | sous-page silo |

**Analyse.** Silo à créer. Mots croisés (printable crossword puzzles 40 500, free 27 100, crosswords 5 400, easy 2 400, adult 4 400 + 2 400, pdf 2 400), sudoku (27 100 + 12 100 + 9 900 + 8 100 + 6 600, easy 5 400, hard 1 000, samurai 1 300, blank grid 1 600), logic puzzles (3 600), hidden pictures (1 600), spot the difference (1 300), word scramble, brain teasers (880). FR : sudoku à imprimer 9 900 (+ facile 720, difficile 390, moyen 320, grilles vierges 390), mots croisés 1 300, mots fléchés 1 300 + 720 + 480, tangram 1 000, jeu des différences 390 + 260 + 210, jeux de logique 170.

### Bingo / loto — US : 1467 groupes, 150 850 recherches / mois

Facettes : aucune : 842 groupes / 89 770, occasion : 465 groupes / 57 270, theme : 120 groupes / 2 750, age : 63 groupes / 1 890, difficulte : 14 groupes / 180.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| christmas bingo game (+2) | 9 900 | HIGH | page programmatique (thème/fête) |
| blank bingo card | 9 900 | LOW | fiche gabarit vierge |
| bingo card template (+3) | 8 100 | MEDIUM | fiche gabarit vierge |
| holiday christmas bingo | 8 100 | HIGH | page programmatique (thème/fête) |
| bingo cards printable (+6) | 6 600 | HIGH | hub silo |
| bingo template (+1) | 5 400 | LOW | fiche gabarit vierge |
| bingo sheets (+1) | 4 400 | HIGH | hub silo |
| bingo cards printable free (+4) | 4 400 | LOW | sous-page silo |
| bingo card empty (+1) | 4 400 | LOW | fiche gabarit vierge |
| christmas bingo cards (+2) | 4 400 | HIGH | page programmatique (thème/fête) |

### Bingo / loto — FR : 97 groupes, 3 510 recherches / mois

Facettes : aucune : 71 groupes / 2 800, theme : 9 groupes / 280, age : 7 groupes / 260, occasion : 12 groupes / 220.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| imprimer carton loto | 590 | HIGH | hub silo |
| planche loto à imprimer | 260 | MEDIUM | sous-page silo |
| carte de bingo à imprimer pdf | 170 | MEDIUM | sous-page silo |
| loto des animaux à imprimer | 140 | LOW | page programmatique (thème/fête) |
| grille bingo à imprimer | 110 | LOW | sous-page silo |
| grille de bingo à imprimer | 110 | LOW | sous-page silo |
| loto des couleurs à imprimer | 110 | LOW | sous-page silo |
| bingo à imprimer | 90 | LOW | hub silo |

**Analyse.** Deux familles : les cartes vierges / gabarits (blank bingo card 9 900, bingo card template 8 100, bingo template 5 400, bingo card empty 4 400, blank bingo card printable 2 900, template free 1 600) et les cartes thématiques (christmas bingo 9 900 + 8 100 + 4 400 + 2 900 + 1 300 + 1 300, halloween bingo 4 400 + 1 600 + 1 300 + 1 300, valentine 2 900 + 880, easter, thanksgiving, football, baby shower, bridal shower, camping, road trip, animal…). Le générateur (bingo card generator 40 500, bingo sheet generator 1 300) est tenu par myfreebingocards.com en position 1. FR : loto des animaux 140, loto maternelle 90, loto de Noël 50 + 40, bingo de Noël 40 + 30, imprimer carton loto 590, planche loto 260.

### Points à relier — US : 511 groupes, 40 220 recherches / mois

Facettes : aucune : 252 groupes / 30 240, age : 85 groupes / 3 940, difficulte : 53 groupes / 2 860, occasion : 86 groupes / 2 540, theme : 46 groupes / 900.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| dot to dot printable (+7) | 9 900 | LOW | sous-page silo |
| dot to dot free printables | 2 900 | LOW | sous-page silo |
| dot to dot marker printables | 2 900 | LOW | sous-page silo |
| extreme dot to dot printable (+3) | 1 000 | LOW | sous-page silo |
| connect the dot sheets (+3) | 1 000 | LOW | sous-page silo |
| free dot to dot printables | 880 | LOW | sous-page silo |
| printable dot to dot for adults (+3) | 880 | LOW | sous-page facette |
| free dot to dot printables 1 1000 pdf | 590 | LOW | sous-page silo |
| free printable dot to dot hard (+13) | 590 | LOW | sous-page facette |
| extreme dot to dot free printable (+1) | 590 | LOW | sous-page silo |

### Points à relier — FR : 218 groupes, 15 110 recherches / mois

Facettes : aucune : 122 groupes / 10 650, age : 38 groupes / 2 850, difficulte : 24 groupes / 740, occasion : 15 groupes / 600, theme : 26 groupes / 450.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| point à relier (+2) | 2 400 | LOW | hub silo (intention mixte) |
| point a relier (+1) | 1 900 | LOW | hub silo (intention mixte) |
| point relier à imprimer (+4) | 1 600 | LOW | sous-page silo |
| point a relier adulte | 590 | MEDIUM | sous-page facette |
| jeu point à relier (+3) | 480 | LOW | hub silo (intention mixte) |
| point à relier adulte (+4) | 480 | HIGH | sous-page facette |
| points à relier pdf gratuit | 480 | LOW | sous-page silo |
| point à relier à imprimer de 1 à 100 | 390 | LOW | sous-page silo |

**Analyse.** Un seul groupe de 8 variantes à 9 900 (dot to dot printable = connect the dots printable = dot to dot sheets), puis free (2 900 + 880 + 480), dot marker printables (2 900), adults (880 + 390 + 260 + 210), hard / extreme / challenging (1 000 + 590 + 480 + 210), par âge (preschool, kindergarten), par fête (christmas 940, halloween 560, thanksgiving 540 cumulés) et par thème (dinosaurs, unicorn). FR : points à relier 2 400 + 1 900 + 1 600, adulte 590 + 480 + 390 + 170 + 170, de 1 à 100 (390), de 1 à 200 (260), difficile 210, maternelle 170 + 110, Noël 110 + 90.

### Labyrinthes — US : 243 groupes, 27 870 recherches / mois

Facettes : aucune : 75 groupes / 14 330, age : 86 groupes / 7 670, difficulte : 37 groupes / 2 930, occasion : 48 groupes / 2 640, theme : 22 groupes / 650.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| maze printable (+1) | 6 600 | LOW | hub silo |
| free maze printables (+2) | 2 400 | LOW | hub silo |
| free printable mazes for kindergarten | 1 900 | LOW | sous-page facette |
| kindergarten maze printable | 1 900 | MEDIUM | sous-page facette |
| maze sheets (+3) | 1 600 | LOW | hub silo |
| difficult maze printable (+3) | 880 | LOW | sous-page facette |
| free maze | 720 | LOW | hub silo |
| adult mazes printable (+4) | 480 | LOW | sous-page facette |
| christmas maze printable (+1) | 480 | LOW | page programmatique (thème/fête) |
| hard maze printable | 480 | LOW | sous-page facette |

### Labyrinthes — FR : 39 groupes, 4 180 recherches / mois

Facettes : aucune : 21 groupes / 3 030, difficulte : 6 groupes / 690, age : 5 groupes / 310, theme : 7 groupes / 150.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| labyrinthe à imprimer (+2) | 1 300 | LOW | hub silo |
| labyrinthe a imprimer | 390 | LOW | hub silo |
| jeu labyrinthe à imprimer (+1) | 320 | LOW | sous-page silo |
| labyrinthe jeu à imprimer | 260 | LOW | sous-page silo |
| labyrinthe à imprimer difficile | 210 | LOW | sous-page facette |
| labyrinthe à imprimer difficile pdf | 210 | LOW | sous-page facette |
| cahier de labyrinthe à imprimer pdf | 170 | LOW | sous-page silo |
| jeu de labyrinthe à imprimer | 170 | LOW | sous-page silo |

**Analyse.** printable mazes 6 600 (UK 480), free 2 400, maze sheets 1 600, par âge (kindergarten 1 900 + 1 900 + 480, preschool, 5 / 10 year olds 320 + 320, adults 480 + 320), par difficulté (hard 480 + 880 « difficult maze printable », easy 390), par fête (christmas 480, halloween 390, thanksgiving) et par thème (minecraft, pokemon). FR : labyrinthe à imprimer 1 300 + 390 + 320 + 260, difficile 210 + 210 + 110, facile 90, maternelle 90 + 70, adulte 70 + 50, Pokémon 40, Pat Patrouille 30.

### Rébus — US : 39 groupes, 3 340 recherches / mois

Facettes : aucune : 22 groupes / 2 950, occasion : 9 groupes / 180, difficulte : 4 groupes / 140, age : 4 groupes / 70.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| rebus puzzles printable (+1) | 1 600 | LOW | hub silo |
| printable rebus puzzles with answers | 480 | LOW | fiche + réponses |
| free printable rebus puzzles | 320 | LOW | sous-page silo |
| rebus puzzle worksheet | 170 | LOW | hub silo |
| easy rebus puzzles with answers pdf | 70 | LOW | fiche + réponses |
| free printable rebus puzzles with answers | 70 | LOW | fiche + réponses |
| hard rebus puzzles with answers printable pdf | 50 | MEDIUM | fiche + réponses |
| printable rebus | 50 | LOW | hub silo |
| printable rebus puzzles for adults | 40 | LOW | sous-page facette |
| christmas rebus puzzles printable | 40 | LOW | page programmatique (thème/fête) |

### Rébus — FR : 15 groupes, 720 recherches / mois

Facettes : aucune : 11 groupes / 540, difficulte : 2 groupes / 120, occasion : 1 groupes / 30, age : 1 groupes / 30.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| rébus à imprimer | 210 | LOW | hub silo |
| rebus a imprimer | 170 | LOW | hub silo |
| rébus facile avec reponse à imprimer (+1) | 90 | LOW | fiche + réponses |
| rébus à imprimer pdf | 70 | LOW | sous-page silo |
| rébus de pâques à imprimer | 30 | – | page programmatique (thème/fête) |
| rébus facile à imprimer | 30 | LOW | sous-page facette |
| rébus maternelle à imprimer | 30 | LOW | sous-page facette |
| rébus gratuit à imprimer | 20 | LOW | sous-page silo |

**Analyse.** Petit silo très peu concurrentiel : rebus puzzles printable 1 600 (CPC 0,30 $, concurrence LOW), with answers 480 + 70 + 30, free 320, worksheet 170, for adults 40, christmas 40 + 40 + 20 + 20. FR : rébus à imprimer 210, facile avec réponse 90, facile 30, maternelle 30, Pâques 30. La SERP US est faible (PDF Scribd, Pinterest, TPT).

### Chasse au trésor — US : 453 groupes, 24 440 recherches / mois

Facettes : occasion : 194 groupes / 8 110, aucune : 153 groupes / 7 480, age : 54 groupes / 6 320, theme : 83 groupes / 4 700, difficulte : 5 groupes / 50.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| outdoor scavenger hunt for preschoolers | 3 600 | HIGH | sous-page facette |
| scavenger hunt templates | 1 900 | MEDIUM | hub silo |
| christmas light scavenger hunt (+1) | 1 300 | HIGH | page programmatique (thème/fête) |
| printable scavenger hunt (+3) | 720 | HIGH | hub silo |
| camping scavenger hunt for preschoolers | 720 | HIGH | page programmatique (thème/fête) |
| nature scavenger hunt for preschoolers | 720 | HIGH | page programmatique (thème/fête) |
| nature scavenger hunt printable | 590 | HIGH | page programmatique (thème/fête) |
| free scavenger hunt printable | 590 | LOW | sous-page silo |
| fall scavenger hunt printable (+2) | 480 | HIGH | page programmatique (thème/fête) |
| free nature scavenger hunt printable (+1) | 480 | LOW | page programmatique (thème/fête) |

### Chasse au trésor — FR : 157 groupes, 10 100 recherches / mois

Facettes : aucune : 80 groupes / 7 260, occasion : 26 groupes / 1 170, age : 20 groupes / 840, theme : 29 groupes / 810, difficulte : 2 groupes / 20.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| chasse au trésor gratuite à imprimer pdf | 1 900 | LOW | sous-page silo |
| enigme chasse au trésor à imprimer gratuit | 1 000 | LOW | sous-page silo |
| carte trésor à imprimer (+4) | 720 | LOW | sous-page silo |
| chasse au trésor à imprimer (+4) | 390 | MEDIUM | sous-page silo |
| jeu de piste gratuit à imprimer | 390 | LOW | sous-page silo |
| chasse au trésor à imprimer gratuit (+1) | 320 | LOW | sous-page silo |
| chasse au trésor paques gratuite à imprimer pdf (+1) | 320 | LOW | page programmatique (thème/fête) |
| énigme jeu de piste gratuit a imprimer | 260 | LOW | sous-page silo |

**Analyse.** En anglais la demande dit « scavenger hunt », pas « treasure hunt » (printable scavenger hunt 720 contre printable treasure hunt 50). Facettes : public (outdoor scavenger hunt for preschoolers 3 600, for kindergarten), lieu / thème (nature 590 + 480 + 720, outdoor, zoo 210, camping 720 + 330), fête (christmas light scavenger hunt 1 300 + 390, christmas 320, fall 480, halloween, easter, spring), gabarit (scavenger hunt templates 1 900). FR : chasse au trésor gratuite à imprimer pdf 1 900, énigme chasse au trésor 1 000, carte au trésor à imprimer 720 + 210 + 170 (vierge), chasse au trésor à imprimer 390 + 320 + 140, jeu de piste gratuit 390 + 260, Pâques 320 + 90, maternelle 170, Halloween 170 + 90, adulte 140 + 140, pirate 110, nature 110, ado 110, forêt 90, Noël 90.

### Escape game — US : 67 groupes, 2 290 recherches / mois

Facettes : aucune : 43 groupes / 1 880, occasion : 18 groupes / 300, age : 6 groupes / 110, theme : 1 groupes / 10.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| printable escape room (+2) | 390 | HIGH | hub silo |
| printable escape room kit | 320 | MEDIUM | sous-page silo |
| escape room printable free (+3) | 210 | LOW | sous-page silo |
| printable escape room puzzles (+1) | 140 | HIGH | sous-page silo |
| escape room print (+1) | 140 | HIGH | hub silo |
| free escape room printable | 90 | LOW | sous-page silo |
| free printable escape room pdf | 50 | LOW | sous-page silo |
| downloadable escape room | 50 | HIGH | hub silo |
| printable escape room games (+1) | 50 | HIGH | sous-page silo |
| easter escape room free printable | 50 | LOW | page programmatique (thème/fête) |

### Escape game — FR : 63 groupes, 2 440 recherches / mois

Facettes : aucune : 42 groupes / 2 040, age : 14 groupes / 290, occasion : 7 groupes / 150, theme : 1 groupes / 10.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| escape game à imprimer | 260 | MEDIUM | sous-page silo |
| kit escape game gratuit pdf | 260 | LOW | sous-page silo |
| escape game a imprimer | 170 | HIGH | sous-page silo |
| escape game à imprimer gratuit | 170 | LOW | sous-page silo |
| enigme escape game a imprimer | 170 | MEDIUM | sous-page silo |
| escape game gratuit à imprimer | 140 | LOW | sous-page silo |
| escape game maison gratuit pdf | 110 | LOW | sous-page silo |
| énigmes escape game à imprimer gratuit | 110 | LOW | sous-page silo |

**Analyse.** printable escape room 390 (HIGH), kit 320, free 210 + 90 + 50 (CPC 4,36 à 7,51 $), puzzles 140, for adults 40 + 30, christmas / easter / halloween 10 à 50 chacun. Volume modeste, SERP US faible (Reddit, blogs, PDF bruts). FR : escape game à imprimer 260 + 170 + 140 + 40, gratuit pdf 260 + 110 + 70 + 40, énigmes escape game 170 + 110 + 70, adulte 70 + 30 + 30, Noël adulte 50, Pâques 30 + 20 + 20.

### Jeux de plateau / PnP — US : 540 groupes, 20 570 recherches / mois

Facettes : aucune : 479 groupes / 19 720, theme : 26 groupes / 370, occasion : 24 groupes / 360, age : 11 groupes / 120, difficulte : 1 groupes / 10.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| checkers printable | 1 900 | HIGH | hub silo |
| printable tic tac toe (+3) | 1 600 | LOW | sous-page silo |
| printable board games (+1) | 1 000 | LOW | hub silo |
| interactive white board game | 880 | LOW | hub silo (intention mixte) |
| print & play (+1) | 720 | LOW | hub silo |
| print play games (+1) | 590 | LOW | hub silo |
| monopoly board game printable (+4) | 480 | MEDIUM | sous-page silo |
| printable tic tac toe board (+1) | 390 | LOW | sous-page silo |
| whiteboard board game | 390 | LOW | hub silo (intention mixte) |
| blank tic tac toe board | 320 | LOW | fiche gabarit vierge |

### Jeux de plateau / PnP — FR : 170 groupes, 7 500 recherches / mois

Facettes : aucune : 126 groupes / 6 540, age : 19 groupes / 470, theme : 21 groupes / 420, occasion : 7 groupes / 110.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| jeu de l'oie à imprimer (+1) | 720 | LOW | sous-page silo |
| bataille navale à imprimer (+1) | 390 | LOW | sous-page silo |
| billets monopoly à imprimer | 320 | LOW | sous-page silo |
| jeu de plateau à imprimer (+1) | 260 | LOW | sous-page silo |
| créer un jeu de l oie à imprimer | 260 | LOW | sous-page silo |
| jeu de l oie à imprimer pdf | 210 | LOW | sous-page silo |
| print & play (+1) | 170 | LOW | hub silo |
| bataille navale à imprimer pdf | 170 | LOW | sous-page silo |

**Analyse.** printable board games 1 000 (UK 260), print and play 720 + 590 + 170, checkers printable 1 900, printable tic tac toe 1 600 + 390 + 320 (blank), monopoly board game printable 480, candyland 320, chutes and ladders 260, clue cards 480, blank board game template 880 (vu en 05), 3 d'exclus (3D). Peu de facettes : le silo vit par ses pages jeu classique (une page par jeu du domaine public) et par le hub PnP. FR : jeu de l'oie à imprimer 720 + 260 (créer) + 210 (pdf) + 140 (plateau) + 70 (maternelle), bataille navale 390 + 170 + 170 (grille), billets monopoly 320, jeu de plateau à imprimer 260, plateau de jeu vierge 170, imprimer jeux de société 140 + 140, petits chevaux 50 + 40 + 40 + 30, domino maternelle 70, les aventuriers du rail 50, jeu de société à imprimer 90.

### Jeux de cartes — US : 312 groupes, 15 550 recherches / mois

Facettes : aucune : 240 groupes / 12 850, theme : 19 groupes / 930, occasion : 37 groupes / 830, difficulte : 8 groupes / 670, age : 10 groupes / 300.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| printable poker cards (+3) | 2 400 | HIGH | hub silo |
| printable playing cards (+4) | 1 000 | MEDIUM | hub silo |
| printable uno (+1) | 720 | LOW | hub silo |
| scattergories cards printable | 720 | MEDIUM | hub silo |
| game cards printable (+1) | 480 | HIGH | hub silo |
| large print poker cards (+2) | 480 | HIGH | sous-page facette |
| charade cards printable | 480 | MEDIUM | hub silo |
| cluedo cards printable (+2) | 480 | LOW | hub silo |
| print your own playing cards (+1) | 260 | HIGH | sous-page silo |
| memory game printable | 260 | LOW | hub silo |

### Jeux de cartes — FR : 223 groupes, 9 960 recherches / mois

Facettes : aucune : 143 groupes / 7 640, age : 49 groupes / 1 630, theme : 28 groupes / 620, occasion : 10 groupes / 180.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| cartes loup garou à imprimer | 720 | LOW | sous-page silo |
| imprimer un jeu de cartes (+4) | 590 | HIGH | sous-page silo |
| carte dixit à imprimer | 390 | LOW | sous-page silo |
| memory à imprimer | 260 | LOW | hub silo |
| carte à jouer à imprimer (+3) | 210 | HIGH | sous-page silo |
| carte de jeu a imprimer (+1) | 210 | LOW | sous-page silo |
| carte de jeu à imprimer (+2) | 210 | MEDIUM | sous-page silo |
| carte time's up à imprimer | 210 | LOW | sous-page silo |

**Analyse.** printable playing cards 1 000 + 2 400 (poker cards, HIGH, CPC 2,86 $ : c'est de l'impression de jeu de 52 cartes), printable uno 720, scattergories cards 720, charade cards 480, clue cards 480, pictionary cards 260, memory game printable 260, go fish 110, large print 480. Les marques (Uno, Monopoly, Clue) sont des pièges juridiques : à traiter par des équivalents génériques (« crazy eights », « detective cards »). FR : cartes loup garou 720, imprimer jeu de carte 590 (HIGH), carte dixit 390, memory à imprimer 260 + 170, 7 familles 210 (vierge) + 170 + 110 + 110 + 110, time's up 210, jeu de carte à imprimer pdf 210, uno 70 + 70 + 70, dobble 110 + 70, mille bornes, cluedo 110.

### Roll & write / dés — US : 145 groupes, 5 400 recherches / mois

Facettes : aucune : 115 groupes / 4 560, occasion : 23 groupes / 730, age : 3 groupes / 70, theme : 4 groupes / 40.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| roll and write | 590 | LOW | hub silo (intention mixte) |
| roll and write board games | 590 | MEDIUM | hub silo (intention mixte) |
| roll and write games | 480 | MEDIUM | hub silo (intention mixte) |
| bunco free printables | 390 | LOW | hub silo |
| printable dice games | 170 | MEDIUM | hub silo |
| best roll and write games | 170 | HIGH | article / sélection |
| gift exchange dice game free printable | 170 | MEDIUM | sous-page silo |
| bunco cards free printable | 140 | LOW | sous-page silo |
| bunco printables | 140 | HIGH | hub silo |
| christmas dice game free printable | 110 | MEDIUM | page programmatique (thème/fête) |

### Roll & write / dés — FR : 11 groupes, 400 recherches / mois

Facettes : aucune : 11 groupes / 400.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| roll and write | 170 | HIGH | hub silo (intention mixte) |
| jeu roll and write | 70 | HIGH | hub silo (intention mixte) |
| roll and write jeu | 40 | HIGH | hub silo (intention mixte) |
| meilleur roll and write | 30 | HIGH | article / sélection |
| roll & write | 30 | HIGH | hub silo (intention mixte) |
| jeu imperial settlers roll and write | 10 | LOW | hub silo (intention mixte) |
| les meilleurs roll and write | 10 | HIGH | article / sélection |
| meilleur jeu roll and write | 10 | LOW | article / sélection |

**Analyse.** roll and write 590 + 480 (games) + 170 (best, article), printable dice games 170, bunco printables 390 + 140 + 140, christmas dice game 110 + 110 + 50 + 50, gift exchange dice game 170 + 70, farkle / yahtzee score sheets dans la longue traîne. FR : roll and write 170 (HIGH), jeu roll and write 70, meilleur roll and write 30 + 10 ; aucune formulation « à imprimer » n'a de volume. Silo de niche, à garder pour la crédibilité « print and play » et pour le CPC, pas pour le trafic.

### Jeux d'ambiance — US : 682 groupes, 19 190 recherches / mois

Facettes : occasion : 335 groupes / 8 530, aucune : 244 groupes / 8 090, age : 112 groupes / 3 700, theme : 93 groupes / 1 440, difficulte : 17 groupes / 190.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| pictionary whiteboard (+2) | 1 300 | LOW | hub silo (intention mixte) |
| printable christmas party games (+3) | 720 | HIGH | page programmatique (thème/fête) |
| printable games for adults | 590 | HIGH | sous-page facette |
| bachelorette printable games (+2) | 590 | HIGH | hub silo |
| printable murder mystery (+3) | 390 | HIGH | hub silo |
| printable trivia (+3) | 390 | LOW | hub silo |
| printable trivia questions and answers (+1) | 390 | LOW | sous-page silo |
| christmas trivia printable (+2) | 390 | MEDIUM | page programmatique (thème/fête) |
| christmas trivia free printable (+4) | 320 | LOW | page programmatique (thème/fête) |
| printable party games | 260 | HIGH | hub silo |

### Jeux d'ambiance — FR : 54 groupes, 1 400 recherches / mois

Facettes : aucune : 39 groupes / 1 130, occasion : 7 groupes / 150, difficulte : 4 groupes / 70, age : 5 groupes / 70.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| cartes pictionary à imprimer | 90 | LOW | sous-page silo |
| murder party gratuit à imprimer | 90 | LOW | sous-page silo |
| quiz a imprimer gratuit (+1) | 90 | LOW | sous-page silo |
| quiz a imprimer | 70 | LOW | hub silo |
| quiz culture générale à imprimer | 70 | LOW | sous-page silo |
| quiz noel a imprimer | 70 | LOW | page programmatique (thème/fête) |
| jeu de mime à imprimer gratuit | 50 | LOW | sous-page silo |
| quiz musical avec réponse à imprimer | 50 | LOW | fiche + réponses |

**Analyse.** printable christmas party games 720 + 260 + 210, printable games for adults 590, printable murder mystery 390, printable trivia 390 + 390, christmas trivia 390 + 320 + 170, bachelorette party games 590, christmas emoji pictionary 260, pictionary whiteboard 1 300. Fortement saisonnier (Noël = 5 720 sur 202 groupes). FR : quiz à imprimer 30, quiz Noël 70, quizz facile 40, murder party à imprimer 30 : quasi inexistant.

### Occasions (fêtes) — US : 554 groupes, 30 320 recherches / mois

Facettes : occasion : 511 groupes / 28 620, theme : 98 groupes / 3 600, age : 39 groupes / 1 850, aucune : 3 groupes / 50, difficulte : 1 groupes / 10.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| christmas printable games (+1) | 3 600 | HIGH | page programmatique (thème/fête) |
| free printable christmas games (+3) | 1 600 | LOW | page programmatique (thème/fête) |
| thanksgiving printable games (+1) | 1 300 | HIGH | page programmatique (thème/fête) |
| christmas scattergories (+1) | 1 300 | HIGH | page programmatique (thème/fête) |
| free printables for easter | 1 300 | LOW | page programmatique (thème/fête) |
| christmas left right game printable (+3) | 720 | HIGH | page programmatique (thème/fête) |
| free printable christmas left right game (+5) | 720 | MEDIUM | page programmatique (thème/fête) |
| left right christmas game free | 590 | MEDIUM | page programmatique (thème/fête) |
| free printable thanksgiving games (+8) | 480 | LOW | page programmatique (thème/fête) |
| 12 days of christmas printable lyrics | 480 | MEDIUM | page programmatique (thème/fête) |

### Occasions (fêtes) — FR : 61 groupes, 3 980 recherches / mois

Facettes : occasion : 41 groupes / 3 640, age : 4 groupes / 370, theme : 14 groupes / 220, aucune : 8 groupes / 170.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| activites halloween a imprimer | 720 | LOW | page programmatique (thème/fête) |
| jeu de noel a imprimer (+1) | 390 | LOW | page programmatique (thème/fête) |
| jeux halloween à imprimer | 320 | LOW | page programmatique (thème/fête) |
| activité pâques à imprimer | 260 | LOW | page programmatique (thème/fête) |
| jeux de noel a imprimer gratuit | 170 | LOW | page programmatique (thème/fête) |
| jeux de noël à imprimer | 170 | LOW | page programmatique (thème/fête) |
| jeux de pâques à imprimer | 170 | LOW | page programmatique (thème/fête) |
| jeux de noël en famille à imprimer | 170 | LOW | page programmatique (thème/fête) |

**Analyse.** Groupes dont le seul sujet est la fête : christmas printable games 3 600 + 1 600 (free), thanksgiving printable games 1 300, christmas scattergories 1 300, free printables for easter 1 300, christmas left right game 720 + 720 + 590, halloween printable games 390, easter printable games 170. FR : activités halloween à imprimer 720, jeu de Noël à imprimer 390 + 170, jeux halloween à imprimer 320, activité Pâques 260, jeux de Pâques 170. À servir par des pages fête qui agrègent les fiches de tous les silos.

### Classe / éducatif — US : 290 groupes, 27 390 recherches / mois

Facettes : aucune : 210 groupes / 22 410, age : 50 groupes / 3 360, theme : 24 groupes / 1 520, occasion : 11 groupes / 210, difficulte : 6 groupes / 100.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| whiteboard games (+1) | 2 900 | LOW | hub silo (intention mixte) |
| games to play in class | 2 900 | LOW | hub silo (intention mixte) |
| games esl | 2 900 | LOW | hub silo (intention mixte) |
| quick games to play in the classroom | 1 600 | LOW | hub silo (intention mixte) |
| game to play on whiteboard (+3) | 1 300 | LOW | hub silo (intention mixte) |
| free sight word activities | 1 000 | MEDIUM | sous-page silo |
| fun games to do in class (+1) | 880 | LOW | hub silo (intention mixte) |
| game play in classroom (+1) | 880 | LOW | hub silo (intention mixte) |
| printable activities for preschoolers (+1) | 720 | HIGH | sous-page facette |
| fun math games to play in the classroom | 720 | LOW | hub silo (intention mixte) |

### Classe / éducatif — FR : 139 groupes, 6 400 recherches / mois

Facettes : age : 110 groupes / 3 930, aucune : 25 groupes / 2 370, occasion : 6 groupes / 150, difficulte : 3 groupes / 90.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| jeux éducatif à imprimer pdf | 480 | LOW | sous-page silo |
| jeu de mémoire adulte à imprimer (+1) | 260 | LOW | sous-page facette |
| jeux mathématiques gs à imprimer | 260 | LOW | sous-page silo |
| jeux pour autiste gratuit à imprimer | 210 | LOW | sous-page silo |
| jeux de concentration à imprimer | 210 | MEDIUM | sous-page silo |
| jeu maternelle à imprimer (+2) | 210 | LOW | sous-page facette |
| jeux grande section à imprimer | 210 | LOW | sous-page silo |
| jeux phonologie gs à imprimer | 170 | MEDIUM | sous-page silo |

**Analyse.** whiteboard games 2 900 (+ game to play on whiteboard 1 300, whiteboard games for adults 170), games to play in class 2 900 + 1 600 (quick) + 880 + 880 + 480, games esl 2 900, fun math games to play in the classroom 720, printable activities for preschoolers 720, free games for first graders 480. Intention « idées de jeux » plus que « fichier » : articles-listes avec PDF téléchargeables. FR : jeux éducatif à imprimer pdf 480, jeux mathématiques GS 260, jeu de mémoire adulte 260, jeux pour autiste 210, concentration 210, jeux à imprimer maternelle 210, grande section 210, phonologie GS / MS 170 + 170, CE1 / CE2 140 + 140.

### Règles — US : 23 groupes, 550 recherches / mois

Facettes : aucune : 23 groupes / 550.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| mancala rules printable | 110 | LOW | page règles |
| monopoly rules printable | 110 | LOW | page règles |
| printable carbles rules | 50 | LOW | page règles |
| game of life rules printable | 40 | LOW | page règles |
| carbles board game rules | 30 | LOW | page règles |
| sudoku rules printable | 30 | LOW | page règles |
| carbles game rules printable | 20 | LOW | page règles |
| aggravation board game rules printable | 10 | LOW | page règles |
| chinese checkers rules printable | 10 | LOW | page règles |
| crokinole rules printable | 10 | – | page règles |

**Analyse.** Dans les idées Google Ads, seulement 23 groupes (mancala rules printable 110, monopoly rules printable 110, game of life 40…), mais `05b` a mesuré « board game rules » 4 400 et « board games and rules » 4 400. En France, dragono.fr tire la majorité de son trafic de pages de règles (« jeux toc » 4 400, « règle petit chevaux » 3 600, « barricade » 2 900, « jeu de la jungle » 1 600, « la bataille règle du jeu » 1 600). Une bibliothèque de règles liée aux PDF est justifiée dans les deux langues.

### Générique « jeux à imprimer » — US : 166 groupes, 13 730 recherches / mois

Facettes : aucune : 134 groupes / 12 580, age : 10 groupes / 660, theme : 20 groupes / 430, occasion : 1 groupes / 50, difficulte : 1 groupes / 10.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| couples shower games printable | 2 900 | HIGH | sous-page silo |
| printable games | 1 600 | LOW | hub silo |
| i spy game printable | 1 000 | LOW | sous-page silo |
| dot game printable | 880 | LOW | hub silo |
| dots and boxes game printable | 880 | LOW | sous-page silo |
| pin the tail game printable (+2) | 590 | MEDIUM | sous-page silo |
| free printable games | 390 | LOW | hub silo |
| printable matching games | 320 | LOW | hub silo |
| paper games printable | 320 | MEDIUM | hub silo |
| printable brain games | 320 | LOW | hub silo |

### Générique « jeux à imprimer » — FR : 80 groupes, 2 380 recherches / mois

Facettes : age : 22 groupes / 1 320, aucune : 57 groupes / 1 040, occasion : 1 groupes / 20.

| Groupe de mots-clés | Volume | Conc. | Page cible |
|---|---|---|---|
| jeu a imprimer adulte (+2) | 320 | LOW | sous-page facette |
| jeu gratuit à imprimer (+1) | 170 | LOW | sous-page silo |
| jeux à imprimer adultes (+1) | 170 | LOW | sous-page facette |
| jeu à imprimer pour adulte | 170 | LOW | sous-page facette |
| logique jeux a imprimer adulte | 170 | LOW | sous-page facette |
| agoralude jeux à imprimer | 110 | LOW | sous-page silo |
| jeu à imprimer adulte gratuit | 90 | LOW | sous-page facette |
| jeux de mots à imprimer pour adultes | 90 | LOW | sous-page facette |

**Analyse.** printable games 1 600, free printable games 390 (CPC 5,76 $), i spy game printable 1 000, dots and boxes game printable 880, printable matching games 320, paper games printable 320, printable brain games 320. FR : jeux à imprimer gratuit 170 + 70, jeu à imprimer adulte 320 + 170 + 170 + 90. Ce sont les mots-clés de l'accueil et des pages « tous les jeux ».

## 5. Concurrents

### 5.1 Qui occupe les SERP (19 requêtes, top 10 organique)

Hors Pinterest (13 apparitions US, 12 FR), Facebook, Reddit, Etsy et YouTube, aucun domaine n'apparaît plus de 3 fois : les SERP sont fragmentées entre portails généralistes et petits sites spécialisés. Domaines relevés au moins deux fois : justfamilyfun.com, education.com, boardgamegeek.com, superteacherworksheets.com, myfreebingocards.com (US) ; momes.parents.fr, tipirate.net, dragono.fr, tidudi.fr, chasse-tresor.net, logicieleducatif.fr, dessinemoiunehistoire.net (FR).

Type de page qui se classe, requête par requête :

| Requête | Qui est devant (position organique) | Type de pages |
|---|---|---|
| free printable board games (US) | print-and-play.asmodee.fun (2), Pinterest, Reddit, justfamilyfun.com/category/printable-board-games/ (6), education.com (7, listing filtré), BGG geeklist (8), twinkl.com (9), printandgame.com (10) | Hubs / listings de catégorie + forums. Aucun site indépendant n'a de hub propre devant Asmodee. |
| print and play games (US) | BGG geeklist (1), Shut Up & Sit Down (vidéo), 3 groupes Facebook, forum, randomskill.games (liste), Reddit, boardanddice.com (boutique) | Communauté et listes. **Aucun hub éditorial** : place à prendre avec `/board-games/print-and-play/`. |
| printable escape room free (US) | Reddit (1), teachingideas.ca (article), artwithtrista.com (tuto), seraphimescape.com.au (listing), Pinterest, 123homeschool4me.com (article), 2 PDF bruts (vaasl.org, activity-mom.com), YouTube | Articles de blog et PDF directs. SERP faible. |
| printable treasure hunt for kids (US) | littlebinsforlittlehands.com (1), Pinterest ×2, runwildmychild.com, treasure-hunt-ideas.co.uk (listing gratuit), letsdiyitall.com, Etsy, scribbledincco.com (produit) | Articles de blog « mom blogs » + listing. |
| printable mazes (US) | krazydad.com/mazes/ (1), printablemazes.net (3), justfamilyfun.com (4), mazesforfun.com (5, catégorie), mathequalslove.net, Pinterest, highlights.com, doyoumaze.com | **Hubs dédiés avec grille de PDF** et générateurs. Pour se classer il faut un hub profond (des centaines de labyrinthes), pas un article. |
| dot to dot printable (US) | thesprucecrafts.com (1, article), theworks.co.uk (2, page « free activity sheets » d'un détaillant), Pinterest ×2, woojr.com, myteachingstation.com (listing), monkeyingaround.com (échantillons), twopinkpeonies.com (catégorie) | Mélange article / listing. Pas de hub dominant : opportunité. |
| printable rebus puzzles (US) | Scribd PDF (1), superteacherworksheets.com ×2 (listing), Pinterest ×2, teacherspayteachers.com, weareteachers.com (article) | SERP faible. |
| word search printable (US) | abcmouse.com (1), pzzl.com (PDF), Pinterest, brightsprout.com (6, browse), whenwewordsearch.com (7, hub), treevalleyacademy.com (catégorie), freeprintablepuzzles.co.uk (9, accueil), washingtontimes.com | Hubs à gros catalogue, générateurs. Entrée coûteuse mais le volume le justifie. |
| free printable bingo cards (US) | toolsforeducators.com (2, générateur), myfreebingocards.com (3 et 6 : liste de 30 cartes + thèmes), Pinterest ×2, PDF, activityconnection.com (produit), natashalh.com (catégorie) | **Générateurs** + pages thème. |
| christmas printable games (US) | yahoo.com (article), reachallreaders.com, Pinterest ×2, foxfarmhome.com, Etsy, teachmama.com, littlesizzle.com (collection boutique) | Articles-listes « 20 free printable christmas games ». |
| classroom games printable (US) | Facebook (1), education.com (2, listing), chalkandapples.com, classroomscreen.com (templates), classroomgames.net (blog), carsondellosa.com (ressources gratuites), twinkl.jp, partyprintpress.com | Listings de ressources pédagogiques + articles. |
| jeu de société à imprimer (FR) | dragono.fr/jeux-de-société/ (1, catégorie), momes.parents.fr/jeux/jeux-a-imprimer/jeux-de-societe (2, listing), Facebook, print-and-play.asmodee.fun (5, article blog FR « 25 jeux à imprimer »), wooloo.ca (article), Pinterest ×2, lululataupe.com (listing) | Catégories / listings de portails. |
| escape game à imprimer gratuit (FR) | escapehunt.com (1, article blog d'une enseigne de salles), lelapinblanc-enigmes.com (listing), tidudi.fr (page produit), Pinterest, anniversaire-en-or.com (guide), escaperoomgeeks.com/fr, escape-games.net (page tag), chasse-tresor.net (produit gratuit) | Articles et pages produit de vendeurs de kits. escape-kit.com n'est pas dans le top 10 sur cette requête. |
| chasse au trésor à imprimer gratuit (FR) | hugolescargot.journaldesfemmes.fr (1, article), ludeek.com/jeux/gratuit/ (2, listing), chasse-tresor.net (3, page gratuite), Pinterest, escape-kit.com (6, page « chasse au trésor gratuite à imprimer »), taleming.com, tidudi.fr (catégorie), unjourunjeu.fr (listing) | Pages « gratuit » de vendeurs de kits + portails. |
| labyrinthe à imprimer (FR) | monsieurmathieu.fr (2, PDF direct d'un enseignant), tipirate.net (3, fiche unique), Pinterest ×2, toupty.com (5, listing), bloghoptoys.fr (article), pinata-magazine.com (catégorie), dragono.fr (10, catégorie) | SERP faible : un PDF d'enseignant est 2e. |
| mots mêlés à imprimer (FR) | mots-meles.net (2, site dédié), 20minutes.fr (jeu en ligne), Pinterest, logicieleducatif.fr (fiches CM1), recapitout.fr (article), PDF d'école, happinessmaker.fr (article), jeux.lefigaro.fr (en ligne) | Un seul site dédié ; le reste est en ligne ou PDF épars. |
| loto à imprimer (FR) | canva.com (2, outil), Pinterest, dessinemoiunehistoire.net (4, catégorie lotos), yakafaire.eu (5, générateur de cartons), momes.parents.fr (listing), tipirate.net (fiche), vsinel.fr (appli), Scribd | Générateurs et catégories. |
| jeux à imprimer maternelle (FR) | momes.parents.fr/jeux/jeux-a-imprimer (1, hub), tipirate.net/imprimer (2, hub), educatifenfants.com (listing), placote.com (tag blog), lumni.fr, Pinterest, logicieleducatif.fr (fiches MS), toutpourlejeu.com | Hubs de portails famille. |
| jeux de noël à imprimer gratuit (FR) | dismoitout-livres.com (article), dessinemoiunehistoire.net (catégorie Noël), amedenfant.fr (produit gratuit), Pinterest ×2, mamancomete.com (article), kidsayeah.com (blog), ef.fr (article) | Articles de blog. |

### 5.2 Profils des domaines (DataForSEO Labs, Google US ou FR, top 300 par volume)

| Domaine | Marché | Mots-clés classés (total) | Trafic estimé / mois (ETV) | Positions 1 | Top 10 | Mots-clés « jeux/imprimables » dans son top 300 | ETV de ces mots-clés |
|---|---|---|---|---|---|---|---|
| twinkl.com | US | 611 632 | 912 640 | 7 183 | 150 614 | 2 | 69 |
| myfreebingocards.com | US | 5 870 | 257 133 | 998 | 3 812 | 292 | 221 236 |
| superteacherworksheets.com | US | 110 167 | 247 862 | 3 502 | 38 115 | 99 | 4 972 |
| education.com | US | 143 674 | 168 782 | 2 100 | 31 626 | 57 | 9 267 |
| momes.parents.fr | FR | 50 099 | 96 435 | 864 | 12 079 | 14 | 254 |
| dessinemoiunehistoire.net | FR | 13 620 | 77 480 | 1 799 | 7 253 | 24 | 273 |
| krazydad.com | US | 2 951 | 32 909 | 318 | 1 586 | 270 | 20 631 |
| justfamilyfun.com | US | 18 983 | 28 971 | 255 | 4 451 | 161 | 1 167 |
| tipirate.net | FR | 3 942 | 15 829 | 189 | 1 190 | 82 | 861 |
| escape-kit.com | FR | 3 120 | 6 431 | 79 | 1 116 | 132 | 1 013 |
| printablemazes.net | US | 561 | 4 948 | 63 | 265 | 299 | 4 594 |
| dragono.fr | FR | 1 380 | 2 413 | 52 | 440 | 157 | 394 |
| print-and-play.asmodee.fun | US | 661 | 615 | 8 | 178 | 174 | 343 |

ETV = trafic organique mensuel estimé par DataForSEO à partir des positions et des volumes ; indicatif, à lire en ordre de grandeur.

**justfamilyfun.com (US).** Site familial à large catalogue de printables (word search, mazes, sudoku, crosswords, bingo generator, deck of cards, stencils, bubble letters). 18 983 mots-clés classés, 28 971 visites/mois estimées, 255 positions 1. Se classe sur « word searches » (450 000, pos. 61-73), « mazes » (90 500, pos. 48), « printable word puzzles » (49 500, pos. 21), « playing deck of cards » (90 500, pos. 48). Pages qui classent : **une page hub par type de puzzle** (`/printable-wordsearch-puzzles/`, `/printable-maze-puzzles-for-kids/`, `/printable-deck-of-cards/`, `/bingo-card-generator/`) listant des dizaines de PDF. Force : couverture ; faiblesse : pages longues et peu structurées, pas de facettes indexables (une seule URL pour tous les mazes). Brèche : facettes difficulté / âge / thème en URL propres.

**krazydad.com (US).** Référence historique des puzzles imprimables (sudoku, mazes, kakuro, slitherlink, crosswords), tenu par une personne. 2 951 mots-clés seulement mais 32 909 visites/mois : positions fortes sur des têtes de requête (« mazes » 90 500 en position 2, « maze » 16, « printable word puzzles » 49 500 en position 6, « sudoku puzzles » 135 000 en position 30). 207 des 300 premiers mots-clés sont des puzzles. Pages : hubs par type (`/mazes/`, `/sudoku/`) avec des livrets PDF par niveau. Brèche : design daté, aucun contenu par thème ni par fête, pas de version française.

**printablemazes.net (US).** Site mono-thème : 561 mots-clés, 4 948 visites/mois, 63 positions 1. Position 1 sur « printable mazes » (6 600), « mazes to print », « maze printouts » ; 2 sur « difficult mazes » (2 900) ; 8 sur « children's mazes to print » (4 400). Pages : accueil = hub (222 des 300 mots-clés), `/category/hard` (73), `/category/medium`, `/category/simple`, fiches `/preview/Dinosaur_Mazes_Set_1`. Preuve que **hub + 3 pages de difficulté suffisent** pour prendre la tête d'un silo de 27 000 recherches ; les sets thématiques (dinosaures, animaux) sont déjà là mais peu poussés.

**myfreebingocards.com (US).** Générateur de cartes de bingo : 5 870 mots-clés, 257 133 visites/mois, 998 positions 1 (« bingo card generator » 40 500 et toutes ses variantes, « bingo » 201 000 en position 4 avec sa page « virtual bingo »). 292 des 300 premiers mots-clés sont du bingo. Pages : le générateur (98 mots-clés), l'accueil (76), des pages **par occasion** (`/occasions/christmas/edit` 35 mots-clés, `/occasions/thanksgiving/edit`), par usage scolaire (`/school/math`), et des templates. C'est le modèle à suivre pour le silo Bingo : un outil + une page par fête / thème qui pré-remplit l'outil. Brèche : pas de PDF prêts à l'emploi « sans outil », pas de français.

**superteacherworksheets.com (US).** Portail de fiches scolaires (110 167 mots-clés, 247 862 visites/mois). Les puzzles passent par des **générateurs** (`generator-word-search.html` classé sur « word search » 450 000 en position 25, `generator-crossword-puzzle.html`) et des pages catégorie (`word-search-puzzles.html`, `tangrams.html`, `brainteasers-rebus-puzzles.html`). Le gros du trafic vient des coloriages, cartes et tables de multiplication. Brèche : l'accès aux fichiers est payant (abonnement) sur une partie du site.

**education.com (US).** 143 674 mots-clés, 168 782 visites/mois. Classe sur « word search » (450 000, pos. 39), « tangrams » (135 000, pos. 20), « mazes » (90 500, pos. 38) avec des **listings filtrés** (`/resources/worksheets/?game-type=mazes`, `?game-type=printable-board-games`, `?game-type=word-puzzles`) et des générateurs de worksheets. Téléchargement derrière inscription. Brèche : expérience fermée, aucune page éditoriale par thème.

**twinkl.com (US).** 611 632 mots-clés, 912 640 visites/mois, mais son top 300 est fait de pages « teaching wiki » (spelling bee, panther, zeus…) : un seul mot-clé de jeu imprimable dans ses 300 premiers. Twinkl pèse par sa masse et son abonnement, pas par les jeux imprimables ; il apparaît dans nos SERP (printable board games pos. 9) via des pages de ressources parent. Pas un concurrent frontal.

**print-and-play.asmodee.fun (US + FR).** Le site officiel PnP d'Asmodee : 661 mots-clés, 615 visites/mois estimées seulement, 8 positions 1. Classe sur les noms de ses jeux (« citadels » 201 000 en position 11, « dixit » 9 900 pos. 12, « love letter card game » 8 100 pos. 24, « spot it card game » 3 600) et sur « free board games » (2 900, pos. 13), « board game free » (2 900, pos. 14). 118 mots-clés pointent sur l'accueil `/en`, le reste sur des fiches `/en/game/<slug>` et des articles de blog (« Best strategy board games for 2 players », « Building board games »). Il est 2e sur « free printable board games » US et 5e en FR avec un article. Force : marques connues ; faiblesse : petit catalogue (extraits de jeux commerciaux), pas de puzzles, pas de pages par public ou occasion.

**momes.parents.fr (FR).** Portail famille de Reworld : 50 099 mots-clés, 96 435 visites/mois, mais seulement 5 mots-clés « jeux imprimables » dans son top 300 (fêtes, coloriages, dictionnaire). Ses pages jeux (`/jeux/jeux-a-imprimer`, `/jeux/jeux-a-imprimer/jeux-de-societe`, `/jeux/jeux-a-imprimer/cartes-lotos-memory`) prennent les positions 1-2 sur « jeux à imprimer maternelle » et « jeu de société à imprimer » par autorité de domaine. Brèche : pages magazine lourdes en publicité, fichiers de qualité inégale, pas de facettes.

**tipirate.net (FR).** 3 942 mots-clés, 15 829 visites/mois, 189 positions 1. 82 mots-clés « jeux » dans le top 300 : « mots meles » (49 500, pos. 71), « rebus » (27 100, pos. 32), « puzzle gratuit » (165 000, pos. 43, puzzles en ligne). Pages : hub `/imprimer`, `/educatif/678-mots-meles`, fiches unitaires (`/imprimer/labyrinthe/334-labyrinthe-8`, `/imprimer/jeux-de-societe/jeu-de-loto`). C'est le concurrent FR le plus proche de notre modèle (petit site, contenu maison, une fiche par printable). Brèche : design années 2000, pas de niveaux, pas de thèmes.

**dessinemoiunehistoire.net (FR).** 13 620 mots-clés, 77 480 visites/mois, mais le trafic vient des comptines et poésies ; 22 mots-clés « jeux » dans le top 300 (« tangram » 12 100 en position 6 avec `/modeles-jeu-tangram/`, lotos). Classe sur « loto à imprimer » (catégorie `/category/lotos/`) et « jeux de noël à imprimer gratuit » (`/category/n/`). Brèche : pages catégorie sans éditorial.

**escape-kit.com (FR).** Vendeur de kits d'escape game : 3 120 mots-clés, 6 431 visites/mois, 79 positions 1. Le trafic SEO vient d'articles larges (« devinette » 27 100 pos. 11, « enigme pere fouras » 4 400 pos. 3, olympiades, kermesse, nom des doigts), de `/enigmes-gratuites/` et de `/jeux/chasse-au-tresor-gratuite-a-imprimer/` (pos. 6 sur « chasse au trésor à imprimer gratuit », pos. 13 sur « chasse au trésor » 9 900). Stratégie : aimants gratuits + blog pour vendre les kits payants. Brèche : contenu gratuit limité à quelques pages ; absent du top 10 sur « escape game à imprimer gratuit ».

**dragono.fr (FR).** Petit site de jeux de société traditionnels : 1 380 mots-clés, 2 413 visites/mois, 52 positions 1, mais 153 mots-clés « jeux » dans le top 300. Position 1 sur « jeu de société à imprimer » avec sa page catégorie `/jeux-de-société/`. Ses meilleures pages sont des **règles de jeux** (« jeux toc » 4 400, « règle petit chevaux » 3 600, « barricade » 2 900, « jeu de la jungle » 1 600 pos. 5, « la bataille règle du jeu » 1 600). Preuve que les pages règles tirent du trafic en français avec peu d'autorité.

### 5.3 Brèches exploitables (synthèse)

1. **Aucun hub « print and play » éditorial** ne se classe sur « print and play games » (US) : forums, Facebook, BGG. Une page hub + fiches structurées (joueurs, durée, âge, pages à imprimer) peut prendre la place.
2. **Les facettes indexables** (difficulté, âge, fête, thème) n'existent chez aucun concurrent de puzzles sauf printablemazes.net (3 niveaux). justfamilyfun et krazydad ont une URL par type. La demande est pourtant facettée (word search : 401 groupes par fête, 228 par difficulté, 190 par public).
3. **Escape game et chasse au trésor** : SERP faibles dans les deux langues (blogs, PDF bruts, Reddit, pages « gratuit » de vendeurs). Un hub gratuit avec 10 à 20 kits bien produits suffit à entrer.
4. **Rébus, points à relier, labyrinthes FR** : un PDF d'enseignant est 2e sur « labyrinthe à imprimer », Scribd est 1er sur « printable rebus puzzles ». Contenu maison générable.
5. **Bingo** : myfreebingocards verrouille le générateur, mais les requêtes « printable » et « blank / template » (9 900 + 8 100 + 5 400 + 4 400 + 2 900) sont servies par des PDF statiques, Pinterest et Canva. Des pages « 30 cartes PDF prêtes + générateur léger » couvrent les deux intentions.
6. **Règles de jeux** : dragono.fr (FR) montre que des pages règles bien faites classent sans autorité ; en anglais « board game rules » (4 400) n'est tenu par aucun concurrent de notre panel.
7. **Bilingue** : aucun concurrent n'est sérieusement bilingue EN/FR (Asmodee PnP l'est, mais avec 661 mots-clés). Les fichiers sans texte (labyrinthes, points à relier, bingo images, jeu de l'oie) se partagent entre les deux langues à coût nul.

## 6. Dix « quick wins » et dix « big bets »

### 6.1 Quick wins (concurrence faible, SERP faible observée, volume correct, contenu produisible en interne)

| # | Cible | Volume | Preuve de faiblesse | Page |
|---|---|---|---|---|
| 1 | rebus puzzles printable (+ with answers 480, free 320) | 1 600 US, LOW, CPC 0,30 $ | Top 10 : Scribd, Pinterest ×2, TPT, un article | `/puzzles/rebus/` + `/puzzles/rebus/with-answers/` |
| 2 | escape room printable free / free printable escape room pdf | 210 + 90 + 50 US, LOW, CPC 4,36 à 7,51 $ | Top 10 : Reddit, 2 PDF bruts, blogs, YouTube | `/escape-games/free/` avec 5 kits maison |
| 3 | labyrinthe à imprimer (+ difficile 210 + 210, facile, maternelle, adulte) | 1 300 + 390 + 320 + 260 FR, LOW | 2e résultat = PDF d'enseignant, 3e = fiche unique tipirate | `/fr/puzzles/labyrinthes/` + facettes |
| 4 | mots mêlés à imprimer (+ adulte 390, personnes âgées 320, facile 210, gros caractères 110) | 4 400 FR, LOW, CPC 0,13 € | Un seul site dédié (mots-meles.net), le reste en ligne ou PDF | `/fr/puzzles/mots-meles/` + facettes public / difficulté |
| 5 | points à relier à imprimer (+ adulte 590 + 480 + 390, de 1 à 100 / 200, maternelle) | 1 600 + 2 400 + 1 900 FR, LOW | Pas de hub dédié dans les SERP relevées, Pinterest omniprésent | `/fr/puzzles/points-a-relier/` + facettes |
| 6 | free printable mazes for kindergarten / kindergarten maze printable / hard maze printable | 1 900 + 1 900 + 480 US, LOW/MEDIUM | printablemazes.net n'a que 3 niveaux, aucune page par âge | `/puzzles/mazes/kindergarten/`, `/hard/`, `/easy/` |
| 7 | blank bingo card printable / bingo card template free / blank bingo card free printable | 2 900 + 1 600 + 1 000 US, LOW, CPC ≤ 0,48 $ | Servi par PDF statiques, Canva, Pinterest | `/bingo/blank-templates/` (3×3, 4×4, 5×5, A4 + Letter) |
| 8 | jeu de l'oie à imprimer (+ pdf 210, plateau 140, maternelle 70) + bataille navale à imprimer (390 + 170 + 170) | 720 + 390 FR, LOW | Jeux du domaine public, SERP de portails sans fiche dédiée | `/fr/jeux-de-plateau/classiques/jeu-de-l-oie/`, `/bataille-navale/` |
| 9 | print and play games / print and play / print and play board games | 590 + 720 + 170 US, LOW | Top 10 sans hub éditorial (BGG, Facebook ×3, Reddit, forum) | `/board-games/print-and-play/` hub + guide « how to print and play » |
| 10 | printable tic tac toe (+ board 390, blank 320) + checkers printable (1 900, HIGH) + chutes and ladders (260) | 1 600 + 1 900 US | Jeux du domaine public, demandes de gabarits simples | `/board-games/classics/<jeu>/` avec PDF A4/Letter et page règles |

Bonus FR à faible coût : `cartes loup garou à imprimer` 720, `carte dixit à imprimer` 390, `carte time's up` 210 (LOW, aucune page dédiée) — mais ce sont des marques déposées : à traiter avec des jeux « inspirés de » sous nom générique (« jeu des villageois », « cartes images à raconter »), jamais avec la marque dans l'URL.

### 6.2 Big bets (gros volume, effort ou concurrence élevés, rendement sur 12-24 mois)

| # | Pari | Volume en jeu | Ce qu'il faut |
|---|---|---|---|
| 1 | **Word search programmatique** : hub + fêtes (christmas 18 100, thanksgiving 12 100, halloween 12 100, spring 8 100, summer 8 100, fall 6 600, winter 5 400, easter 3 600, valentine 3 600) + difficulté (hard 8 100) + public (adults 8 100 + 5 400, kids 3 600, par niveau scolaire) | 60 500 tête + ~130 000 facettes US ; 2 900 UK ; 4 400 FR | Générateur interne de grilles (thèmes = listes de mots), 300 à 500 PDF, pages facettes avec texte, générateur public « make your own » (2 400) |
| 2 | **Mots croisés imprimables** (nouveau silo) : printable crossword puzzles 40 500, free 27 100, easy 2 400, adult 4 400 + 2 400, pdf 2 400 ; FR mots croisés 1 300, mots fléchés 1 300 + 720 + 480 | ~100 000 US ; 3 500 FR | Générateur de grilles + banque de définitions par thème ; qualité éditoriale nécessaire (les grilles automatiques sont médiocres sans relecture) |
| 3 | **Sudoku imprimable** : 27 100 + 12 100 + 9 900 + 8 100 + 6 600, easy 5 400, hard 1 000, samurai 1 300 ; FR 9 900 + 1 900 + 1 600 + 1 300 + 880 | ~70 000 US ; 16 000 FR | Générateur (facile à coder), livrets PDF par niveau, pages par niveau ; krazydad est la référence à dépasser sur le design |
| 4 | **Bingo saisonnier + générateur** : christmas bingo 9 900 + 8 100 + 4 400 + 2 900 + 1 300 + 1 300, halloween 4 400 + 1 600 + 1 300 + 1 300, valentine 2 900, bingo cards printable 6 600 (HIGH), bingo card generator 40 500 | ~60 000 US saisonnier + 40 500 outil ; 3 500 FR | Une page par fête / thème (myfreebingocards le fait) + générateur simple côté client ; concurrence HIGH sur les fêtes |
| 5 | **Dot to dot hub** : 9 900 (8 variantes), free 2 900 + 880, dot marker 2 900, adults 880, hard / extreme 1 000 + 590 + 480, FR points à relier 2 400 + 1 900 + 1 600 | ~40 000 US ; 15 000 FR | Génération vectorielle de tracés numérotés (1-100, 1-200, 1-1000 : « free dot to dot printables 1 1000 pdf » 590) ; pas de hub dominant aujourd'hui |
| 6 | **Printable mazes hub profond** : 6 600 + 2 400 + 1 600 + âges + difficultés + fêtes + thèmes ; FR labyrinthe 1 300 + 390 + 320 | 27 870 US ; 4 180 FR | Plusieurs centaines de labyrinthes générés (3 formes × 4 tailles × thèmes), pages facettes ; battre printablemazes.net et krazydad sur la profondeur |
| 7 | **Bibliothèque de règles** : board game rules 4 400 + board games and rules 4 400 (05b), <jeu> rules printable ; FR règles (dragono : toc 4 400, petits chevaux 3 600, barricade 2 900) | ~10 000 US ; ~15 000 FR | Une page règle par jeu classique du domaine public (60 à 100 jeux), balisage HowTo, liée au PDF du plateau |
| 8 | **Classroom / whiteboard** : whiteboard games 2 900 + 1 300 + 170, games to play in class 2 900 + 1 600 + 880 + 880 + 480, games esl 2 900 | ~13 000 US, 590 UK | Articles-listes avec fiches PDF téléchargeables, par matière et par niveau ; intention « idées » (CPC 2,9 à 4,6 $, forte valeur) |
| 9 | **Chasse au trésor / scavenger hunt programmatique** : FR 1 900 + 1 000 + 720 + 390 + 390 + 320 + thèmes ; US printable scavenger hunt 720, templates 1 900, preschoolers 3 600, nature 590 + 480 + 720, christmas light 1 300 + 390 | 10 100 FR ; 24 440 US | Kits par thème (pirate, nature, Pâques, Noël, Halloween, maternelle, adulte) avec énigmes, cartes au trésor vierges (720 FR) et listes « scavenger hunt » par lieu |
| 10 | **Escape games gratuits bilingues** : US 2 290, FR 2 440 en groupes, CPC 4 à 7 $ ; pages par public (adults, kids) et par fête | ~5 000 EN + FR | 10 à 20 kits originaux bilingues, pages par âge et par fête ; faible volume mais le CPC indique une valeur commerciale (partenariats, kits premium) |

## 7. Grappes qui justifient des pages programmatiques

Critère : un même gabarit de page, des dizaines ou centaines de valeurs de variable avec un volume mesuré pour chacune, et des concurrents qui ne les servent pas par des URL dédiées.

| Gabarit | Variable | Preuves (groupes US sauf mention) | Pages estimées |
|---|---|---|---|
| `/puzzles/word-search/<fête-ou-saison>/` | fête, saison | 401 groupes « occasion » = 131 830 recherches : christmas 30 370 (91 groupes), thanksgiving 19 960, halloween 19 590, summer 11 770, spring 10 760, fall 10 110, winter 7 960, valentine 6 570, easter 5 390, st patrick's 3 640, new year 1 600, earth day 1 600, holidays 2 400 | 15 à 20 |
| `/puzzles/word-search/<public>/` et `/<difficulté>/` | âge, niveau scolaire, difficulté | 190 groupes « âge » = 37 790 (adults 15 150, 1st grade 2 900, 3rd grade 2 400, kindergarten 1 600, middle school 1 600, childrens 6 520) ; 228 groupes « difficulté » = 28 880 (hard 14 180, large print 10 600, easy 3 440) | 12 à 15 |
| `/puzzles/word-search/<thème>/` | thème (animaux, espace, sport, océan…) | 89 groupes « thème » = 4 650 ; longue traîne individuellement faible (≤ 500) mais nombreuse ; à produire en masse car chaque PDF = une liste de mots | 100 à 300 |
| `/bingo/<fête-ou-thème>/` | fête, thème, événement | 465 groupes « occasion » = 57 270 : christmas 33 830 (178 groupes), halloween 11 750, holiday 8 990, valentine 4 330, easter 1 730, fall 780, winter 770, football 540, bridal shower 460, baby shower, camping 430, road trip 410, summer 420 ; thèmes animaux 380 ; myfreebingocards a déjà `/occasions/<fête>/` | 30 à 50 |
| `/bingo/blank/<grille>/` | 3×3, 4×4, 5×5, avec/sans numéros 1-75 | blank bingo card 9 900, bingo card template 8 100, bingo template 5 400, bingo card empty 4 400, blank printable 2 900, template free 1 600, blank sheets 880, print bingo cards 1 75 (90), with numbers 70 + 260 | 6 à 10 |
| `/puzzles/mazes/<difficulté>/`, `/<âge>/`, `/<fête>/`, `/<thème>/` | difficulté, âge, fête, thème | âge 86 groupes = 7 670 (kindergarten 4 610, « X year olds » 1 210 + 1 220, preschool 370 + 180, adults 590 + 480), difficulté 37 groupes = 2 930 (hard 990 + difficult 910, easy 640, simple 270), fête 48 groupes = 2 640 (christmas 810, halloween 630, thanksgiving 400, easter 200), thème 22 groupes (minecraft 180, pokemon 110). FR : difficile 550, maternelle 160, adulte 150, facile 140, Pokémon 90 | 25 à 40 par langue |
| `/puzzles/dot-to-dot/<facette>/` | public, difficulté, fête, thème, plage de numéros | adults 2 200 (20 groupes), hard 1 580, christmas 940, halloween 560, thanksgiving 540, easy 520, preschool 480, kindergarten 410, medium 370, dinosaurs 290, unicorn 160 ; FR adulte 2 380 (26 groupes), difficile 520, maternelle 390, Noël 330, « de 1 à 100 » 390, « de 1 à 200 » 260 | 20 à 30 par langue |
| `/puzzles/sudoku/<niveau>/` et `/puzzles/crossword/<facette>/` | niveau, public, fête | sudoku easy 5 400, hard 1 000, blank grid 1 600, samurai 1 300 ; crossword easy 2 400, adult 4 400 + 2 400, christmas 1 600, halloween 720, summer 1 600 ; FR sudoku facile 720, difficile 390 + 210, moyen 320, grilles vierges 390 ; mots croisés facile 320, adulte 260, CE1 140 | 10 à 20 par langue |
| `/treasure-hunts/<thème-ou-fête>/` (FR `/fr/chasses-au-tresor/<thème>/`) | thème, lieu, fête, public | FR : Pâques 490 (7 groupes), adulte 420, Halloween 410, maternelle 270, pirate 250, ado 140, Noël 130, nature 110, forêt 110, Pokémon 90, jardin 60, automne 60, anniversaire 50, princesse 40 ; US : preschoolers 5 470, outdoor 3 760, christmas 3 620, nature 2 680, christmas light 1 970, camping 1 050, fall 1 020, elf 750, halloween 620, zoo 450, road trip 350 | 20 à 30 par langue |
| `/rules/<jeu>/` (FR `/fr/regles/<jeu>/`) | jeu classique | board game rules 4 400 + 4 400 (05b) ; mancala rules printable 110, monopoly rules printable 110, game of life 40, chinese checkers, crokinole, aggravation… ; FR dragono : toc 4 400, petits chevaux 3 600, barricade 2 900, jeu de la jungle 1 600, bataille 1 600 | 60 à 100 par langue |
| `/card-games/<jeu-classique>/` | jeu de cartes traditionnel / cartes de jeu générées | go fish 110 + 50, old maid, crazy eights, memory game 260 (+ christmas 260, adults 90), charade cards 480, pictionary cards 260, trivia cards ; FR memory 260 + 170 + 110 (animaux) + 90 (adulte), 7 familles 210 + 170 + 110 + 110 + 110 (thèmes : famille, animaux, Disney), dobble 110 + 70 | 20 à 40 par langue |
| `/occasions/<fête>/` | fête | christmas printable games 3 600 + 1 600, thanksgiving 1 300, halloween 390, easter 170 + 1 300, christmas party games 720, christmas trivia 390 + 320, left right game 720 + 720 + 590 ; FR Halloween 720 + 320, Noël 390 + 170, Pâques 260 + 170 | 10 à 12 par langue |
| `/classroom/<matière-ou-niveau>/` | matière, niveau | math games classroom 720, esl games 2 900, first graders 480, preschoolers 720 ; FR GS 260 + 170 + 210, MS 170, CE1 140, CE2 140, maternelle 210, autisme 210, concentration 210 | 15 à 25 par langue |

Deux grappes **ne justifient pas** de pages programmatiques : les escape games (facettes de 10 à 70 recherches chacune : 5 à 8 pages manuelles suffisent) et le roll & write (aucune facette mesurable).

## 8. Conséquences pour l'architecture (`06-architecture-seo.md`)

1. Ajouter un silo **Crosswords & Sudoku** (ou élargir Puzzles) : `/puzzles/crossword/`, `/puzzles/sudoku/`, avec niveaux et thèmes. C'est le plus gros volume non couvert (≈ 300 000 recherches en groupes US).
2. Donner au silo **Puzzles** le rang de premier silo du site (navigation, accueil, maillage), avant Board games. Le print and play reste la signature de la marque mais pas la source de trafic.
3. Créer les facettes indexables **par fête / saison** dans Word search, Bingo, Mazes, Dot-to-dot, Treasure hunts, et pas seulement dans Occasions : la demande saisonnière vit dans la formulation « christmas word search », pas « christmas printable games ».
4. Prévoir des **générateurs** légers (bingo, word search, sudoku) : les requêtes outil (bingo card generator 40 500, word search maker 2 400, crossword maker 1 900) sont celles qui ont le plus de volume et myfreebingocards montre qu'elles créent un site entier.
5. Nommer le hub chasse au trésor EN **Scavenger hunts** (`/scavenger-hunts/`), « treasure hunt » restant un synonyme dans le texte (720 contre 50).
6. Conserver la **bibliothèque de règles** en EN et FR ; l'alimenter d'abord avec les jeux dont le plateau est téléchargeable (jeu de l'oie, petits chevaux, dames, tic tac toe, bataille navale, mancala, backgammon, ludo).
7. Formats : chaque PDF en **Letter et A4** (US/UK + FR) ; les puzzles sans texte sont partagés entre les deux langues avec une seule production.
8. Pour l'AI Overview présent sur 18 des 19 SERP : mettre la grille de téléchargement au-dessus de la ligne de flottaison, le texte éditorial dessous, et le balisage (ItemList, FAQPage, HowTo pour les règles).

## 9. Fichiers produits

- `data/kw/keywords-master.csv` : 19 003 lignes, colonnes `keyword, lang, market, volume, competition, cpc, silo, page_type, facet, explicit_print_intent`.
- `data/kw/ideas_*.json` (5), `data/kw/serp_us_*.json` (11), `data/kw/serp_fr_*.json` (8), `data/kw/domain_us_*.json` (8), `data/kw/domain_fr_*.json` (5).
- Les regroupements (clusters) sont recalculables à partir du CSV : deux lignes de même marché, même série mensuelle, même concurrence et même CPC appartiennent au même groupe Google Ads.
