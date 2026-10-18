# Analyse des concurrents et inspirations design

Rapport de recherche (18 octobre 2026). Limite importante : le réseau de l'environnement bloquait l'accès direct aux sites, l'analyse repose donc sur les extraits des résultats de recherche et sur la connaissance préalable des sites, signalée « non vérifié » quand c'est le cas.

## 1. Sites analysés

### PNP Arcade — https://www.pnparcade.com/
- Boutique Shopify utilitaire. Sa valeur est la discipline des métadonnées, pas le visuel.
- Chaque fiche produit a un bloc constant : `Players: 1-4`, `Ages: 8+`, `Length: 25-35 minutes`, `Designer(s)`, `Artist`, `Printed Components`, `Additional components needed: 3 dés, crayon`, `Page count: 8`.
- Pattern intéressant : une version « free trial » de 4 pages à côté du jeu complet payant.
- Exemples : https://www.pnparcade.com/products/paper-pinball-ski-93, https://pnparcade.com/products/retrograde

### Button Shy Games — https://buttonshygames.com/
- Shopify, propre et lumineux, la photo produit (jeu format portefeuille) porte la marque.
- Bandeau métadonnées : `Players: 1 · Length: 10 minutes · Age: 8+ · Designer · Artist`.
- Promotion : un nouveau jeu par mois, abonnement, démo PnP gratuite, concours de création.

### itch.io, section print & play — https://itch.io/physical-games/tag-print-and-play
- La meilleure expérience de navigation du lot pour un gros catalogue gratuit, visuellement brut.
- Listing : facettes en barre latérale gauche + grille de cartes (4-5 colonnes). Carte = visuel 630×500, titre, accroche, auteur, badge « Free », genre, puces de tags.
- Filtres : prix (Free / Paid…), récence, tags combinables dans l'URL. Tri : Popular, New & Popular, Top rated, Most recent.
- Fiche jeu : description → « More information » (date, auteur, genre, tags, langues, durée moyenne) → zone téléchargement. Le CTA est sous la description, pas au-dessus de la ligne de flottaison.

### BoardGameGeek — https://boardgamegeek.com/wiki/page/Game_entry
- Référence pour le vocabulaire des métadonnées, pas pour l'esthétique.
- Bandeau : joueurs (éditeur vs communauté), durée min-max, âge, **poids / complexité 0-5**. Crédits : designer, artiste, éditeur. Classification : type, catégorie, mécanisme, famille.

### Good Little Games — https://www.goodlittlegames.co.uk/
- Petit site statique, l'analogue le plus proche du projet (gratuit, curaté, tenu par des designers).
- Liste de jeux avec visuel, description et bouton « Cards & Rules » (zip de PDF). Contrainte affichée comme argument : « 9 cartes sur une seule feuille ». Matériel commun listé (pions, pièces, dés).

### Escape Kit — https://escape-kit.com/
- Leader français de l'escape game à imprimer, coloré, orienté conversion.
- Segmentation par **tranche d'âge** (dès 3 ans, 4-6, 7-12, 9-13, ados, adultes), **thème**, **durée** (30 min gratuit / 60 min payant), **joueurs**, **difficulté choisie avant téléchargement**, **matériel** (imprimante couleur, ciseaux, scotch, smartphone).
- Aimants à trafic gratuits : invitations, chasse au trésor, mini-énigmes. Gros blog SEO.
- Concurrents FR similaires : Adios Casa, Happy Kits, Escape The City, Wescape, Mystère Feuille Ciseaux, Murder Mystery Time.

### Lock Paper Scissors — https://lockpaperscissors.co/
- Couvertures illustrées audacieuses, longues pages de vente avec témoignages.
- Champs propres aux escape games : difficulté, tranche d'âge, espace nécessaire, système d'indices, deck d'indices éditable.

### Printable Heroes — https://printableheroes.com/
- Catalogue sombre et dense de figurines papier, modèle Patreon.
- Pattern à reprendre : **version gratuite + extras pour soutiens** sur la même carte, et « votez pour la prochaine sortie ».

### DriveThruCards — https://www.drivethrucards.com/
- Vitrine datée mais taxonomie instructive : type de produit, thème, âge, éditeur, prix (dont Free et Pay What You Want), format PDF / imprimé.

### The Game Crafter — https://www.thegamecrafter.com/games
- Bloc « Requirements » : durée, joueurs, âge. Département → catégorie, tags libres.

### Sites français de « jeux à imprimer » (Mômes, Tête à modeler, Hugo l'Escargot)
- Gros portails familiaux, look magazine générique, beaucoup de publicité, navigation par âge.
- Ils gagnent sur le volume SEO, pas sur le design : c'est l'espace où se différencier.

### Inspirations design (catalogue / e-commerce)
- Escape Coffee (Awwwards SOTD 2024) : puces de filtres, grille avec changement de visuel au survol.
- Gumroad Discover : look néo-brutaliste (bordures noires, accent rose), cartes 600×600, filtres note / prix / tri.
- Cotton Bureau : « we love the grid », typographie Brandon Grotesque + Minion Pro pour le contraste.
- Galerie de templates Notion : recherche → catégories → populaires → collections → créateurs mis en avant.
- Baymard : multi-sélection dans une facette, 5 valeurs puis « voir plus », filtres en panneau latéral sur mobile.

## 2. Synthèse

### Structures de pages qui fonctionnent

**Accueil**
1. Héros : une phrase forte (« Des jeux gratuits à imprimer ce soir ») + CTA « Parcourir » + « Jeu de la semaine ».
2. Puces d'accès rapide : par type, par joueurs (solo, 2, groupe), par durée (≤ 15 min), par âge.
3. « Nouveautés du mois » (cadence mensuelle façon Good Little Games).
4. Jeu de la semaine en grande carte.
5. Collections : « jeux sur une feuille », « escape games en famille », « solo », « imprimable en noir et blanc ».
6. « Comment ça marche » en 3 étapes : télécharger → imprimer → découper et jouer.
7. Créateur à l'honneur.
8. Newsletter + communauté.
9. Pied de page avec bascule EN / FR.

**Catégorie / listing**
- Barre latérale de filtres collante (panneau coulissant sur mobile), facettes avec compteurs et multi-sélection, puces des filtres actifs au-dessus de la grille, tri (récent / populaire / mieux noté / plus court / moins de pages).
- Grille 3 colonnes ≥ 1200 px, 2 sur tablette. Carte : visuel 4:5 ou carré, badge type en haut à gauche, badges « Free / New / EN·FR » en haut à droite, titre, accroche, bandeau icônes joueurs · minutes · âge · pages, créateur.

**Fiche jeu**
1. Héros : visuel à gauche (galerie), à droite titre, badge type, créateur, bandeau métadonnées, **gros bouton « Télécharger le PDF »** au-dessus de la ligne de flottaison, taille du fichier, version, licence.
2. « Ce qu'il vous faut » : imprimante couleur ou N&B, papier, ciseaux, dés, pions.
3. Description, résumé des règles, vidéo éventuelle.
4. Aperçu des feuilles à imprimer (carrousel).
5. Tags : thème, mécaniques, occasion.
6. Carte crédit créateur (designer, illustrateur, liens, « soutenez-les »).
7. Jeux similaires.
8. Communauté : notes, commentaires, photos.

### Liste complète des filtres et champs
- **Cœur** : type (plateau / cartes / dés / roll & write / escape / ambiance / puzzle / JDR), joueurs (min-max, solo, idéal à), durée (min-max), âge (3+, 6+, 8+, 10+, 12+, 14+), langue (EN, FR, indépendant de la langue).
- **Impression** : pages à imprimer, nombre de cartes / feuilles, format (A4 / Letter), couleur vs noir et blanc, matériel nécessaire (dés, pions, crayon, smartphone, ciseaux, colle, protège-cartes), temps d'assemblage.
- **Découverte** : thème, mécaniques, occasion (soirée famille, classe, fête, voyage, Noël, anniversaire), complexité (1-5).
- **Escape game** : difficulté des énigmes, indices disponibles, espace nécessaire, nombre d'énigmes, maître du jeu requis.
- **Social** : note, téléchargements, date d'ajout, version, créateur, licence, concours / prix.

### Pistes de design (polices vérifiées sur Google Fonts)
1. **Arcade Poster** : Unbounded + Space Grotesk. Bleu électrique #1E3CFF, jaune acide #F2FF3D, rose #FF3D8A, blanc cassé #FBF8F2, encre #111. Bordures 2 px, ombres dures décalées (néo-brutalisme).
2. **Wonky Serif Playroom** : Fraunces (axe WONK) + Outfit. Tomate #FF4F1F, moutarde #FFC53D, menthe #BDE8CA, crème #FFF6E5, cacao #3B2A20. Cartes arrondies 24 px, badges « sticker » inclinés.
3. **Bricolage Studio** : Bricolage Grotesque + Instrument Sans. Forêt #0F3D2E, citron vert #CFFF5E, corail #FF6B57, papier #F3EFE6. Grille éditoriale, gros chiffres pour joueurs / durée.
4. **Candy Chromatic** : Cherry Bomb One ou Honk (héros seulement) + Nunito. Bubblegum #FF7AD9, ciel #6FD3FF, citron #FFF27A, raisin #5B2A86. Orienté enfants / famille.
5. **Cardboard & Ink** : Chango + DM Sans, accent Instrument Serif italique. Kraft #D9B98A, noir #121212, rouge tampon #D7263D, blanc. Formes découpées, pointillés « découper ici » comme motif.
6. **Syne Gallery** : Syne ExtraBold + Manrope. Ultraviolet #4B1DFF, orange #FF7A00, pistache #D7F171, graphite #1C1C1E. Gros titres, filtres en rangées de pilules.
7. **Young Serif Picnic** : Young Serif + Figtree. Sarcelle #137C74, pêche #FFB996, cerise #E63946, sable #F7EFE3. Chaleureux, légèrement rétro.
8. **Climate Crisis Stunt** : Climate Crisis (héros animé) + Big Shoulders Display + Inter Tight. Noir, blanc, un néon #39FF14. Très conceptuel, à doser.

Note technique (sans Tailwind) : CSS maison avec jetons de design (`--c-ink`, `--c-pop`, `--radius`, `--shadow-hard`), grille `auto-fill, minmax(260px, 1fr)`, container queries pour les cartes, variante sombre via `prefers-color-scheme`, polices variables via `font-variation-settings`.

### Sections d'accueil et leviers de promotion
- Jeu de la semaine avec compte à rebours jusqu'à la prochaine sortie.
- Quiz « Trouve-moi un jeu » : joueurs → durée → âge → ambiance → 3 résultats.
- Créateurs à l'honneur + page « Proposer votre jeu » + saisons de concours (« défi 9 cartes »).
- Indicateur de coût d'impression sur chaque carte : « ≈ 3 pages, N&B ok ».
- Collections / packs : « dimanche pluvieux », « pack classe », « escape de Noël » (zip de plusieurs PDF).
- Newsletter mensuelle ; option Ko-fi / Patreon « soutenez les créateurs » avec extras.
- Vote pour le prochain jeu ou la prochaine traduction.
- Galerie « je l'ai joué » : photos des jeux assemblés, votes de difficulté ressentie.
- Hub de contenu SEO façon Escape Kit : un article par tranche d'âge et par intention.
- Page « Comment imprimer et jouer » : papier, protège-cartes, découpe, plastification.
