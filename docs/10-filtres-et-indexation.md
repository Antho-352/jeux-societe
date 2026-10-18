# Filtres et indexation : facettes, URL, Astro statique

Rapport de recherche (18 octobre 2026). Complète `06-architecture-seo.md` (silos et URL) et `03-analyse-concurrents.md` (liste brute des filtres). Les volumes cités viennent de `01-mots-cles-volumes.md`, `05-mots-cles-decouverte.md` et `05b-mots-cles-complementaires.md` ; aucun nouvel appel DataForSEO n'a été fait, les facettes marquées « à valider » doivent passer par une mesure de volume avant d'être indexées.

## 0. Les décisions en dix lignes

1. Une facette = un seul mécanisme : soit page statique indexable (chemin dans l'URL, lien `<a href>`), soit filtre JavaScript (query string, jamais de lien). Jamais les deux pour la même facette au même niveau.
2. Règle d'indexation d'une valeur de facette : demande ≥ 200 recherches US/mois (≥ 50 FR) sur l'expression « facette + catégorie » ou ses variantes proches, **et** ≥ 8 fiches, **et** intention distincte de la page parente (SERP différente, intro et FAQ spécifiques possibles).
3. Facettes indexables : type (sous-catégorie), difficulté (puzzles), tranche d'âge (tous silos), joueurs (solo, 2 joueurs ; jeux seulement), mécanique (jeux : coopératif, stratégie, classiques…), occasion et thème (silos transversaux + liste blanche de combinaisons type × occasion).
4. Facettes JavaScript seulement : durée, matériel, langue, couleur / N&B, pages à imprimer, complexité, format, créateur, licence, taille de grille, solutions incluses, espace requis, maître du jeu, tri.
5. Combinaisons indexables : 2 facettes maximum, uniquement depuis une liste blanche éditoriale (`facet-pages.json`), familles autorisées : type × difficulté, type × âge, type × occasion/thème, silo × joueurs, difficulté × âge (mazes). Tout le reste n'existe pas en URL (404).
6. URL : `/puzzles/mazes/hard/`, `/puzzles/mazes/adults/hard/` (ordre fixe âge → joueurs → difficulté → occasion/thème), pagination `/page/2/` auto-canonique hors sitemap, tri et filtres JS en `?` avec canonical vers le chemin propre et `Disallow: /*?` dans robots.txt.
7. Astro : les pages facettes sont générées par `getStaticPaths` depuis la collection + la liste blanche ; chaque catégorie expose un JSON minimal (≈ 150 octets par fiche, chargé à l'ouverture du panneau) pour le filtrage client ; la grille non filtrée (24 cartes) est dans le HTML.
8. Qualité : sous 4 fiches la page n'est pas générée, de 4 à 7 elle est `noindex, follow` et hors sitemap, à partir de 8 elle est indexée ; chaque page indexable a une phrase écrite à la main obligatoire, un gabarit de titre propre à son type de facette et un contrôle d'unicité des titres au build.
9. Mobile : bouton « Filtres · Tri » collant, panneau plein écran (`<dialog>`), bouton « Voir N résultats » collant en bas avec compteur vivant, puces des filtres actifs retirables au-dessus de la grille, CTA « Télécharger » présent sur chaque carte, pas seulement au survol.
10. Exemples traités : mazes → `/easy/`, `/medium/`, `/hard/`, `/preschool/`, `/kids/`, `/adults/` + 3 combos (`/kids/easy/`, `/kids/hard/`, `/adults/hard/`) ; escape games → `/kids/`, `/teens/`, `/adults/`, durée en JS, aucun combo âge × durée ; board games → `/solo/`, `/2-player/`, durée en JS, aucun combo joueurs × durée (collection éditoriale « jeux rapides à 2 » à la place).

## 1. Sources consultées et ce qu'elles disent

Toutes les pages ci-dessous ont été lues le 18 octobre 2026 (texte complet, pas seulement les extraits de recherche).

| Source | Points retenus |
|---|---|
| Google Search Central, *Managing crawling of faceted navigation URLs* (mis à jour 2025-12-18) — https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation | Deux voies : **bloquer** le crawl des URL facettes non nécessaires (robots.txt `disallow: /*?*color=`, ou fragments `#` « sans impact sur le crawl, positif ou négatif »), ou les **rendre crawlables** en respectant : séparateur `&`, « si vous encodez les filtres dans le chemin, l'ordre logique des filtres doit rester constant et aucun filtre dupliqué ne doit exister », **HTTP 404 quand une combinaison ne renvoie rien**. `rel=canonical` et `rel=nofollow` sont « généralement moins efficaces à long terme » ; le nofollow doit être sur **tous** les liens vers l'URL. |
| Google Search Central Blog, *Crawling December: Faceted navigation*, Gary Illyes, 17 déc. 2024 — https://developers.google.com/search/blog/2024/12/crawling-december-faceted-nav | « La navigation à facettes est de loin la source la plus fréquente de sur-crawl signalée », évitable « dans la grande majorité des cas ». Même résumé : bloquer ou optimiser ; 404 sur les combinaisons vides ; canonical « prend du temps à être pris en compte ». |
| Google, *Pagination, incremental page loading* (2025-12-10) — https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading | Lier les pages séquentiellement en `<a href>` ; lier chaque page vers la page 1 ; **une URL unique par page, chaque page a son propre canonical, « ne pas utiliser la page 1 comme canonique »** ; pas de numéro de page après `#` ; les titres identiques sont tolérés dans une séquence ; **« Google n'utilise plus `rel=next/prev`, même si d'autres moteurs peuvent encore les utiliser »** ; « évitez d'indexer les URL avec filtres ou tris alternatifs » via `noindex` ou robots.txt ; Google ne clique pas sur « Load more ». |
| Google, *Fix lazy-loaded content* (2025-12-10) — https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading | Charger au passage dans le viewport (IntersectionObserver, `loading="lazy"`), jamais sur action utilisateur ; pour l'infinite scroll, chaque tranche a une URL persistante (`?page=12`), liée séquentiellement, et l'URL affichée est mise à jour par History API. |
| Google, *Optimize your crawl budget* (2026-07-22) — https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget | Guide destiné aux sites de **1 M+ pages** ou **10 000+ pages changeant quotidiennement** : notre site n'est pas concerné par le budget au sens strict. Reste utile : consolider les doublons, bloquer en robots.txt les pages triées / dupliquées, **« n'utilisez pas noindex [pour économiser le crawl], Google demandera quand même la page »**, 404 ferme pour le supprimé, sitemap à jour avec `lastmod`. |
| Google, *How to specify a canonical URL* (2026-07-10) — https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | Force des signaux : redirection > `rel=canonical` > sitemap ; ils se cumulent. Canonical auto-référent recommandé ; URL absolue ; pas de robots.txt ni de noindex pour canonicaliser ; en cas de rendu JS, **« spécifiez le canonical dans le HTML source et assurez-vous que JavaScript ne le modifie pas »** ; avec hreflang, canonical dans la même langue ; lier en interne vers la version canonique. |
| Google, *JavaScript SEO basics* (2026-03-04) — https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics | Google ne découvre que les liens `<a href>` ; History API plutôt que fragments pour router du contenu à indexer ; le `noindex` peut être injecté en JS (mais la page passe quand même en file de rendu) ; pré-rendu « reste une excellente idée ». |
| Google, *Help Google understand your ecommerce site structure* (2025-12-10) — https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure | Google déduit l'importance d'une page du nombre de liens internes et de la profondeur, « pas de la structure des URL » ; les pages catégorie doivent lier toutes les fiches, sinon sitemap. |
| Google, *Block Search indexing with noindex* (2025-12-10) — https://developers.google.com/search/docs/crawling-indexing/block-indexing | Un `noindex` n'est vu que si la page n'est pas bloquée par robots.txt ; `X-Robots-Tag` pour les non-HTML (PDF, JSON). |
| Google Search Central Blog, *Changes to HowTo and FAQ rich results*, 8 août 2023 — https://developers.google.com/search/blog/2023/08/howto-faq-changes | **Les résultats enrichis FAQ ne sont plus affichés que pour des sites gouvernementaux et de santé ; HowTo n'est plus affiché du tout.** Le balisage « n'a pas d'effet visible » mais ne nuit pas. Conséquence pour `06-architecture-seo.md` : la FAQ reste un bloc de contenu utile, pas un levier de rich result. |
| Ahrefs, *Faceted Navigation: Definition, Examples & SEO Best Practices*, Sam Underwood, mis à jour 7 févr. 2025 — https://ahrefs.com/blog/faceted-navigation/ | Architecture recommandée pour un nouveau site : **filtres en AJAX sans aucun `<a href>`**, URL partageable (`#` idéal, ou `?` + canonical vers la version sans paramètre), et **« chemins de crawl alternatifs » (sous-navigation en liens HTML) vers les versions indexables créées éditorialement** à partir des mêmes attributs. Choisir les facettes à indexer par recherche de mots-clés longue traîne (99,84 % des mots-clés font < 1 000 recherches/mois mais 39 % de la demande). Le canonical peut être ignoré si la page facette est beaucoup liée en interne. |
| Semrush, *Faceted Navigation: An SEO Win Waiting to Happen*, 20 déc. 2024 — https://www.semrush.com/blog/faceted-navigation/ | Exemple Nike : catégorie et facette « marque » auto-canoniques, 2e facette canonicalisée vers la page à une facette. Exemple Sephora : H1, fil d'Ariane, title et contenu réécrits pour la combinaison « Night creams for dry sensitive skin ». Les paramètres de tri et de vue « n'ont pas besoin de nouvelles URL ». Sitemap limité aux pages facettes de valeur. |
| Moz, *Faceted Navigation Intro* (Whiteboard Friday, 5 oct. 2018) — https://moz.com/blog/faceted-navigation-intro | Schéma classique : catégories ouvertes, 1 facette indexable, **2 facettes et plus en noindex**, puis « whitelist » des combinaisons à volume. Ancien mais toujours la référence du « max 1–2 facettes ». |
| Baymard, *What Is an Ecommerce Filter? UI Best Practices* — https://baymard.com/learn/ecommerce-filter-ui | Multi-sélection par cases à cocher (14 % des sites l'interdisent) ; compteurs à côté des options ; filtres actifs visibles (20 % des sites échouent) ; **desktop : filtrage temps réel ; mobile : tiroir plein écran ou bottom sheet, bouton déclencheur collant, bouton « Show X results » avec compte vivant** ; l'état des filtres doit être dans l'URL pour survivre au bouton Retour ; pas de « bon nombre » de filtres, ce qui compte est la lisibilité. |
| Baymard, *Display "Applied Filters" in an Overview (28 % Don't)* — https://baymard.com/research-articles/how-to-design-applied-filters | Sans récapitulatif des filtres actifs : pas de confirmation, pas de retrait rapide, perte de contexte ; aussi important « qu'un titre de page ou un fil d'Ariane ». |
| Baymard, *6 Guidelines for Truncation Design* — https://baymard.com/research-articles/truncation-design | Afficher **6 à 10 valeurs** avant « Voir plus », 15+ pose problème ; lien de troncature au style de lien standard, juste sous la liste ; pas de zone de défilement interne. |
| Baymard, *Always Allow Users to Combine Multiple Filtering Values of the Same Type (15 % Don't)* — https://baymard.com/research-articles/allow-applying-of-multiple-filter-values | Logique OU à l'intérieur d'une facette ; l'option choisie reste à sa place dans la liste. |
| Baymard, guideline #1125 *"Apply" Buttons in Mobile Filtering Interfaces* — https://baymard.com/guidelines/1125-apply-buttons-in-mobile-filtering-interfaces | Énoncé public : « les filtres auto-appliqués ralentissent les utilisateurs qui veulent choisir plusieurs options » (le détail est réservé aux abonnés). |
| Astro docs, *Routing › Pagination* et *Nested pagination* — https://docs.astro.build/en/guides/routing/ ; *@astrojs/sitemap* (`filter`, `serialize`, `i18n`) — https://docs.astro.build/en/guides/integrations-guide/sitemap/ | `paginate()` renvoie `page.data`, `page.url.prev/next/first/last`, `page.total` ; la pagination imbriquée se fait en renvoyant un tableau de `paginate()` avec `params` ; le sitemap se filtre par URL et par `serialize()`. |
| Pagefind, *Filtering* — https://pagefind.app/docs/filtering/ | Index de recherche statique avec filtres par `data-pagefind-filter`, chargé par fragments : option retenue pour la **recherche globale**, pas pour les grilles de catégorie. |

Ce que ces sources ne disent pas et que nous décidons nous-mêmes : les seuils chiffrés (volume, nombre de fiches), l'ordre des facettes dans le chemin et la liste blanche. Ils sont justifiés au § 3.

## 2. Les facettes par silo

Conventions : **Lien** = valeurs rendues comme liens HTML vers des pages statiques (onglets) ; **JS** = contrôle sans lien, filtrage client ; **Multi** = plusieurs valeurs cumulables en OU dans la facette (Baymard) ; les facettes sont combinées entre elles en ET.

### 2.1 Facettes communes à tous les silos

| Facette | Champ de la fiche | Valeurs (EN / FR) | UI | Multi | Mécanisme |
|---|---|---|---|---|---|
| Tranche d'âge | `ageMin` (3–18) → segment dérivé par silo | Preschool 3–5 · Kids 6–10 · Teens 11–15 · Adults 16+ / Maternelle · Enfants · Ados · Adultes | Onglets-pilules | Non | **Lien** (segments) ; la valeur fine `ageMin` est affichée sur la carte, pas filtrable |
| Occasion | `occasions[]` | christmas, halloween, easter, thanksgiving, valentines, birthday, travel, rainy-day, classroom, family-night / Noël, Halloween, Pâques… | Cases à cocher (10 visibles puis « Voir plus ») | Oui | **JS** dans les catégories ; **Lien** vers `/occasions/<x>/` (silo transversal) et combos en liste blanche |
| Thème (univers) | `themes[]` | pirates, space, dinosaurs, animals, princesses, detective, jungle, ocean, farm, robots, sport, wizards… | Cases à cocher + champ « rechercher un thème » au-delà de 15 valeurs | Oui | **JS** dans les catégories ; **Lien** vers `/themes/<x>/` ; combos en liste blanche |
| Langue | `language` | en, fr, language-independent | Puces | Oui | **JS** (le site EN préselectionne en + independent, le site FR fr + independent) ; jamais d'URL, hreflang s'en charge |
| Couleur / N&B | `print.color` | color, bw-friendly | Interrupteur « Imprimable en noir et blanc » | — | **JS** |
| Pages à imprimer | `print.pages` | 1 · 2–5 · 6–10 · 11+ | Puces | Non | **JS** |
| Matériel nécessaire | `components[]` | none (paper only), dice, pawns, pencil, scissors, glue, smartphone, card-sleeves, envelopes | Cases à cocher + interrupteur « Rien d'autre que du papier » | Oui | **JS** |
| Format papier | `print.format` | A4, Letter, both | Affiché sur la fiche, **pas un filtre** (on vise « both » partout) | — | — |
| Créateur | `creator` | slug | Liste déroulante avec recherche | Non | **JS** ; les pages `/creators/<slug>/` existent mais sont des pages auteur, pas des facettes |
| Licence | `license` | cc-by, cc-by-nc, cc-by-nc-nd, free-personal | Cases à cocher (section repliée par défaut) | Oui | **JS** |
| Tri | — | newest, popular, top-rated, shortest, fewest-pages | `<select>` | — | **JS**, jamais dans une URL indexable |

### 2.2 Jeux (board games, card games, roll & write, dice, party)

| Facette | Champ | Valeurs | UI | Multi | Mécanisme |
|---|---|---|---|---|---|
| Type | silo | board, card, roll-and-write, dice, party, trivia, bingo | Navigation principale | — | **Lien** (hubs de silo, déjà décidés dans 06) |
| Joueurs | `players.min/max`, `players.best` | Solo · 2 · 3–4 · 5–6 · 7+ (large group) | Puces | Oui | **Lien** pour `solo` et `2-player` ; `3-4`, `5-6`, `7+` en **JS** |
| Durée | `playTime.min/max` | ≤ 10 min · 10–20 · 20–45 · 45–90 · 90+ | Puces | Oui | **JS** |
| Âge | `ageMin` | Kids 4–8 · Family 8+ · Adults 16+ (segments jeux) | Onglets | Non | **Lien** (`/kids/`, `/family/`, `/adults/`) |
| Mécanique / genre | `mechanics[]` | cooperative, strategy, classics, dexterity, deduction, bluffing, racing, memory, drawing, word, educational | Cases à cocher (10 visibles) | Oui | **Lien** pour les valeurs de 06 (`/cooperative/`, `/family/`, `/strategy/`, `/classics/`, `/micro/`, `/party/`, `/solo/`) ; les autres en **JS** |
| Complexité | `weight` 1–5 | Light · Medium · Heavy | Puces | Non | **JS** |
| Temps d'assemblage | `assembly` | < 5 min · 5–15 · 15+ | Puces | Non | **JS** |
| Jeu complet sur une feuille | `print.pages == 1` | interrupteur « One-sheet game » | Interrupteur | — | **JS** (collection éditoriale possible, pas de facette indexable) |

### 2.3 Puzzles (mazes, word search, dot-to-dot, rebus, dot marker, sudoku, crosswords)

| Facette | Champ | Valeurs | UI | Multi | Mécanisme |
|---|---|---|---|---|---|
| Type de puzzle | catégorie | mazes, word-search, dot-to-dot, rebus, dot-marker, sudoku, crosswords, spot-the-difference | Navigation | — | **Lien** (`/puzzles/<type>/`) |
| Difficulté | `difficulty` | easy · medium · hard | Onglets | Non | **Lien** pour mazes, rebus, word search, sudoku, crosswords ; **JS** pour dot marker (pas de demande) |
| Âge / niveau | `ageMin` | Preschool 3–5 · Kids 6–10 · Adults (ados et adultes) | Onglets | Non | **Lien** (`/preschool/`, `/kids/`, `/adults/`) quand la demande existe (mazes : oui ; word search : `kids`/`adults` à valider) |
| Nombre de points (dot-to-dot) | `dots` | 1–20 · 1–50 · 1–100 · 100+ | Puces | Non | **Lien** pour `1-20`, `1-50`, `1-100` (« dot to dot 1-100 » : demande probable, **à valider**), sinon JS |
| Taille de grille (word search, sudoku) | `grid` | 10×10 · 15×15 · 20×20 | Puces | Non | **JS** |
| Solutions incluses | `answers` | oui / non | Interrupteur | — | **JS** (la demande « rebus puzzles with answers » 480 est traitée dans l'intro du hub rebus, pas par une page) |
| Occasion / thème | voir 2.1 | | | Oui | **JS** + combos en liste blanche (`/puzzles/word-search/christmas/`, `/puzzles/mazes/halloween/`…) |
| Pack / livret | `bundle` | single page · booklet 5+ | Puces | Non | **JS** |

### 2.4 Escape games et chasses au trésor

| Facette | Champ | Valeurs | UI | Multi | Mécanisme |
|---|---|---|---|---|---|
| Âge | `ageMin` | Kids 6–10 · Teens 11–15 · Adults 16+ | Onglets | Non | **Lien** (`/escape-games/kids/`, `/teens/`, `/adults/`), idem chasses au trésor |
| Durée | `duration` | 30 min · 45 · 60 · 90+ | Puces | Oui | **JS** |
| Joueurs / équipe | `players` | 1–2 · 3–5 · 6+ · several teams | Puces | Oui | **JS** |
| Difficulté des énigmes | `difficulty` | easy · medium · hard | Puces | Non | **JS** (pas de demande distincte « hard printable escape room » mesurée ; à revoir dans GSC) |
| Thème | `themes[]` | detective, pirates, haunted-house, space, jungle, egypt, spy, christmas… | Cases à cocher | Oui | **JS** + combos liste blanche (`/escape-games/christmas/`, `/escape-games/halloween/` : « escape game noël » FR confirmé) |
| Occasion | `occasions[]` | birthday, classroom, christmas, halloween, team-building | Cases à cocher | Oui | **JS** + liste blanche (`/escape-games/birthday/` à valider : « escape game anniversaire à imprimer » 10 FR) |
| Lieu / espace | `space` | table only · one room · whole house · outdoor | Puces | Oui | **JS** |
| Maître du jeu requis | `gameMaster` | oui / non | Interrupteur | — | **JS** |
| Matériel | `components[]` | scissors, envelopes, smartphone (QR), padlocks, color printer, tape | Cases à cocher | Oui | **JS** |
| Nombre d'énigmes | `puzzleCount` | affiché sur la carte | — | — | pas un filtre |

### 2.5 Classroom et occasions (silos transversaux)

| Facette | Valeurs | Mécanisme |
|---|---|---|
| Niveau scolaire (`grade`) | K · 1–2 · 3–5 · 6–8 | **Lien** `/classroom/by-grade/<x>/` (déjà décidé) |
| Matière (`subject`) | math, vocabulary, spelling, science, geography, history | **JS** ; `/classroom/math/` en liste blanche (« math board games printable » à valider) |
| Occasion × silo | Noël × puzzles, Halloween × escape… | Pages `/occasions/<x>/` listent tout ; les combos type × occasion vivent sous le silo type (`/puzzles/mazes/christmas/`), la page occasion y renvoie. Une seule URL par combinaison. |

## 3. Indexable ou pas : la règle et son application

### 3.1 La règle (les quatre conditions)

Une valeur de facette (ou une combinaison) obtient une page statique indexable si et seulement si :

1. **Demande** : ≥ 200 recherches US/mois (EN) ou ≥ 50 FR/mois sur « facette + catégorie » en additionnant les variantes proches (ex. « hard mazes » 2 900 + « difficult maze » 2 900). Sous le seuil, exception éditoriale possible (max 10 sur le site, revue trimestrielle contre Search Console) pour une intention e-commerce classique : `solo`, `2-player`.
2. **Inventaire** : ≥ 8 fiches pour une facette simple, ≥ 12 pour une combinaison, avec une production prévue. C'est le seuil au-dessus duquel la grille remplit un écran desktop (3 colonnes) sans paraître vide, et au-dessus duquel une intro de 120 mots ne représente plus la majorité du contenu.
3. **Intention distincte** : la SERP de la requête n'est pas celle de la catégorie parente (résultats de tête différents) et on peut écrire une intro et trois questions spécifiques qui n'auraient pas leur place sur la page parente. « Medium mazes » passe (volume via « printable mazes medium »), « medium rebus » ne passe pas.
4. **Vocabulaire contrôlé** : la valeur est une énumération du schéma Zod, pas un texte libre. Les thèmes sont une énumération maintenue à la main.

Si une page indexable repasse sous 8 fiches (retrait d'un créateur), le build la bascule en `noindex, follow` ; sous 4 elle n'est plus générée et les liens disparaissent (§ 6.3).

### 3.2 Décision facette par facette

| Facette | Décision | Justification |
|---|---|---|
| Type / sous-catégorie | **Indexable** (navigation) | Volumes de 06 (printable mazes 6 600, word search printable 60 500, dot to dot 9 900…). |
| Difficulté (puzzles) | **Indexable** pour mazes, rebus, word search, sudoku, crosswords | easy maze 2 400, hard mazes 2 900, difficult maze 2 900, difficult rebus puzzles 2 400 ; « hard word search printable » à valider mais même schéma. |
| Difficulté (escape, jeux) | **JS** | Pas de demande mesurée distincte ; la difficulté d'un escape se choisit à la fiche (modèle Escape Kit). |
| Âge | **Indexable** (segments) | children's mazes to print 4 400 ; printable escape room for adults 40 + escape game adulte à imprimer 30–70 FR + segmentation de tous les concurrents (Escape Kit, Mômes) ; printable board games for adults 20 + jeu de société adulte à imprimer 10 → exception éditoriale pour `/board-games/adults/`. |
| Joueurs | **Indexable** `solo`, `2-player` ; reste **JS** | solo print and play games 50, 2 player print and play games 10 : sous le seuil mais intention e-commerce classique, pages déjà prévues dans 01 (« Filtre solo », « Filtre 2 joueurs ») → 2 des 10 exceptions. `3-4`, `5-6`, `7+` : pas de demande, risque de pages quasi identiques à la catégorie. |
| Durée | **JS** | Aucune requête « 15 minute printable games » mesurée ; la durée sert à trier, pas à atterrir. |
| Mécanique | **Indexable** pour les sous-pages de 06, **JS** pour le reste | cooperative/strategy/classics ont une demande propre (checkers printable 1 900, tic tac toe 1 600) ; dexterity, bluffing… non. |
| Occasion | **Indexable** au niveau silo `/occasions/`, **JS** dans les catégories, combos en liste blanche | christmas printable games free 1 600, halloween 390, easter 170. |
| Thème | **Indexable** `/themes/<x>/`, **JS** dans les catégories, combos en liste blanche | Longue traîne ; licences (06 § 7) : jamais de marque dans l'URL. |
| Langue | **JS** | Doublon de hreflang ; une page « jeux en français » sur le site EN ferait concurrence à `/fr/`. |
| Couleur / N&B, pages, matériel, format, complexité, assemblage, grille, solutions, espace, maître du jeu, créateur, licence, tri | **JS** | Aucun volume, intention de tri ou de contrainte matérielle, pas d'intro possible sans redite. |
| Niveau scolaire | **Indexable** | Décidé dans 06 (`/classroom/by-grade/`). |
| Matière | **JS** + liste blanche | « math board games printable » à valider. |

### 3.3 Combinaisons : 2 facettes maximum, liste blanche obligatoire

Pourquoi une liste blanche et pas une règle automatique : avec 7 sous-catégories de puzzles × 3 difficultés × 3 âges × 10 occasions × 20 thèmes, la génération automatique des paires donnerait plus de 5 000 pages, dont l'immense majorité à 0–3 fiches. Moz et Ahrefs convergent : catégorie + 1 facette ouvertes, 2 facettes sur whitelist, jamais 3.

Familles de combinaisons **autorisées** (chacune doit en plus passer les quatre conditions, inventaire ≥ 12) :

| Famille | Exemples retenus ou candidats | Statut |
|---|---|---|
| type × difficulté | `/puzzles/mazes/hard/`, `/puzzles/rebus/hard/`, `/puzzles/word-search/easy/` | retenu (mazes, rebus), à valider (word search) |
| type × âge | `/puzzles/mazes/kids/`, `/puzzles/mazes/preschool/`, `/escape-games/kids/`, `/board-games/adults/` | retenu |
| type × occasion ou thème | `/puzzles/word-search/christmas/`, `/puzzles/mazes/halloween/`, `/escape-games/christmas/`, `/board-games/christmas/` | à valider un par un (« christmas word search printable », « halloween maze printable ») |
| silo × joueurs | `/board-games/solo/`, `/board-games/2-player/`, `/card-games/solo/` | retenu (exceptions éditoriales) |
| âge × difficulté (puzzles seulement) | `/puzzles/mazes/kids/easy/`, `/puzzles/mazes/kids/hard/`, `/puzzles/mazes/adults/hard/` | retenu pour mazes (§ 8.1), à valider ailleurs |
| niveau scolaire × matière | `/classroom/by-grade/3-5/math/` | à valider |

Combinaisons **interdites** (jamais d'URL, le build refuse l'entrée dans la liste blanche) :

- toute combinaison avec une facette JS (durée, matériel, langue, couleur, pages, tri, créateur, licence, grille, complexité) ;
- occasion × thème (« pirate christmas ») ;
- âge × joueurs (« 2 player games for kids » : traité par l'intro de `/2-player/`) ;
- difficulté × occasion (« hard christmas maze ») ;
- trois facettes et plus ;
- deux valeurs de la même facette (« easy-and-medium ») ;
- une facette dont la valeur couvre > 80 % de la catégorie (ex. « N&B » sur les puzzles) : la page serait un doublon de la catégorie.

## 4. Design des URL

### 4.1 Grammaire

```
/{silo}/                                  hub de silo              /puzzles/
/{silo}/{categorie}/                      catégorie                /puzzles/mazes/
/{silo}/{categorie}/{facette}/            1 facette                /puzzles/mazes/hard/
/{silo}/{categorie}/{f1}/{f2}/            2 facettes, ordre fixe   /puzzles/mazes/adults/hard/
.../page/{n}/                             pagination (n ≥ 2)       /puzzles/mazes/hard/page/2/
.../?theme=pirates&components=dice        filtres JS, non indexés  canonical → /puzzles/mazes/hard/
/{silo}/{categorie}/{fiche}/              fiche                    /puzzles/mazes/lost-temple/
/fr/puzzles/labyrinthes/difficile/        miroir FR, slugs traduits
```

Ordre fixe des facettes dans le chemin, imposé par le build (Google : « l'ordre logique des filtres doit rester constant ») : **âge → joueurs → difficulté → occasion/thème → mécanique**. `/puzzles/mazes/hard/adults/` n'est jamais généré ; s'il est demandé, c'est un 404 (pas de redirection : le site est statique et Google préfère le 404 pour une combinaison inexistante).

Les slugs de valeurs sont réservés : un slug de fiche ne peut pas être `hard`, `kids`, `page`, etc. Le schéma Zod refuse les collisions au build.

### 4.2 Pourquoi chemin pour l'indexable, query string pour le reste

- Le chemin est stable, lisible, sans paramètre à normaliser ; c'est la forme que les concurrents qui rankent utilisent (Nike, Sephora dans l'exemple Semrush).
- La query string est la forme que Google documente pour bloquer en masse (`Disallow: /*?`), et un hébergeur statique sert le même fichier HTML quelle que soit la query string : le canonical présent dans ce HTML pointe donc automatiquement vers le chemin propre, sans logique supplémentaire.
- Alternative acceptable : le fragment (`#theme=pirates`), « sans impact sur le crawl » selon Google et préféré par Ahrefs. Nous gardons la query string parce que GA4 et la plupart des outils ignorent le fragment, et parce que le fragment entre en conflit avec les ancres de page (`#faq`). Si Search Console montre un jour des URL `?` indexées malgré robots.txt et canonical, on bascule en fragment : c'est un changement d'une ligne dans le script.

### 4.3 Éviter le doublon `/mazes/hard/` vs `/mazes/?difficulty=hard`

Le doublon est évité par construction, pas par correction :

1. Une facette indexable n'est **jamais** un contrôle JS au même niveau. Sur `/puzzles/mazes/`, « Hard » est un onglet `<a href="/puzzles/mazes/hard/">`, pas une case à cocher. Le script de filtrage n'accepte pas de clé `difficulty` : si un lien partagé arrive avec `?difficulty=hard`, le script fait `location.replace('/puzzles/mazes/hard/')`.
2. Depuis `/puzzles/mazes/hard/`, les filtres JS ajoutent `?theme=pirates` : l'URL `/puzzles/mazes/hard/?theme=pirates` sert le HTML de `/puzzles/mazes/hard/`, dont le canonical absolu est `https://printandplaygame.com/puzzles/mazes/hard/`. JavaScript ne touche jamais au canonical (consigne Google).
3. robots.txt : `Disallow: /*?` pour tous les user-agents. Google ne crawle pas, donc n'indexe pas (sauf lien externe : alors l'URL peut apparaître sans contenu, risque accepté et surveillé).
4. Aucun `<a href>` vers une URL à query string nulle part sur le site : ni dans les filtres, ni dans les puces actives, ni dans le footer. Les puces et cases sont des `<button>` / `<input>`.
5. Les clés de la query string sont triées alphabétiquement et les valeurs dédoublonnées avant `replaceState`, pour qu'un même état donne toujours la même URL partageable.

### 4.4 Tri

Le tri est un `<select>` qui réordonne la grille côté client et écrit `?sort=popular`. Jamais de chemin `/popular/`. Le tri par défaut (HTML) est « recommandé » : mis en avant éditorial puis date. Les pages facettes indexables ont le même ordre par défaut que leur catégorie.

### 4.5 Pagination

- Taille : **24 fiches par page** (3 colonnes × 8 lignes desktop, 2 × 12 tablette). Pour les puzzles produits en masse, 36.
- URL : `/puzzles/mazes/hard/page/2/`. La page 1 est `/puzzles/mazes/hard/` ; `/page/1/` n'est pas généré (404).
- Chaque page a son **canonical auto-référent** (Google : ne pas canonicaliser vers la page 1). Chaque page est `index, follow`, mais les pages ≥ 2 sont **exclues du sitemap** (Google : le sitemap signale ce qu'on veut voir crawlé en priorité ; les pages 2+ sont découvertes par les liens).
- Liens : « Suivant », « Précédent », numéros, et un lien explicite vers la page 1 sur chaque page (recommandation Google). Les `<link rel="next/prev">` sont **émis quand même** : Google ne les lit plus depuis mars 2019 (confirmé dans la doc actuelle), Bing s'en sert pour la découverte ; ils ne coûtent rien.
- Titre : « Hard mazes – page 2 » (Google tolère un titre identique, mais le suffixe évite les alertes d'outils). Intro, FAQ et bloc guide **ne sont rendus que sur la page 1** : les pages suivantes ont H1, fil d'Ariane, onglets, grille, pagination. Cela évite 10 copies du même texte.
- Côté client, « Afficher plus » est un lien `<a href=".../page/2/">` amélioré en JS (fetch de la page suivante, insertion des cartes, `history.replaceState` vers l'URL de la page devenue visible, selon la recette Google pour l'infinite scroll). Sans JS, c'est une pagination classique.
- Quand un filtre JS est actif, la pagination serveur est masquée et la liste filtrée est rendue par tranches de 24 avec un bouton « Afficher plus » purement JS (l'état filtré n'a pas d'URL indexable, donc pas d'URL de page).

### 4.6 Fiches, hreflang, sitemap

- Une fiche vit sous une seule URL (06 § 2) ; les pages facettes la listent, elles ne la dupliquent pas.
- hreflang entre `/puzzles/mazes/hard/` et `/fr/puzzles/labyrinthes/difficile/` seulement si les deux pages existent et sont indexables ; une page FR `noindex` n'est jamais citée en hreflang (Google préfère les URL en cluster hreflang comme canoniques, inutile de l'y inviter avec une page vide).
- Le sitemap ne contient que les URL canoniques indexables : hubs, catégories, pages facettes ≥ 8 fiches, fiches, pages règles, articles. Pas de `/page/n/`, pas de `?`, pas de `noindex`, pas de JSON.

## 5. Mise en œuvre dans Astro (sortie statique)

### 5.1 Données

```
src/content/games/<silo>/<slug>.md         une fiche (frontmatter typé par Zod : silo, category,
                                           ageMin, players, playTime, difficulty, themes[], occasions[],
                                           components[], language, print{pages,color,format}, …)
src/data/facets.ts                         énumérations, libellés EN/FR, slugs EN/FR, ordre des facettes
src/data/facet-pages.json                  LISTE BLANCHE des pages facettes et combos (voir 5.2)
src/data/age-segments.ts                   ageMin → segment, par silo
```

Le schéma Zod énumère toutes les valeurs : une valeur hors liste fait échouer le build, ce qui garantit la condition « vocabulaire contrôlé ».

### 5.2 Liste blanche `facet-pages.json`

```json
{
  "path": "puzzles/mazes/adults/hard",
  "silo": "puzzles", "category": "mazes",
  "filters": { "age": "adults", "difficulty": "hard" },
  "locales": {
    "en": { "slug": "puzzles/mazes/adults/hard", "h1": "Hard mazes for adults",
            "lead": "Phrase écrite à la main, obligatoire.",
            "faq": [ { "q": "...", "a": "..." } ] },
    "fr": { "slug": "fr/puzzles/labyrinthes/adultes/difficile", "h1": "Labyrinthes difficiles pour adultes",
            "lead": "...", "faq": [] }
  },
  "status": "live",
  "evidence": "hard mazes 2900 + difficult maze 2900 ; 'hard mazes for adults' à valider",
  "reviewedAt": "2026-10-18"
}
```

Règles de validation au build (script `scripts/validate-facet-pages.ts`) : max 2 clés dans `filters`, clés dans l'ordre global, aucune clé JS-only, `lead` non vide pour chaque locale `live`, slug unique, pas de collision avec un slug de fiche. Une entrée `status: "draft"` est générée en `noindex` pour relecture.

### 5.3 Génération des pages

Deux fichiers de route partagent un helper `buildListings()` :

```
src/pages/[...path]/index.astro          page 1 de chaque listing (catégorie, facette, combo)
src/pages/[...path]/page/[page].astro    pages 2..n
```

`buildListings()` : pour chaque catégorie, puis chaque entrée de `facet-pages.json`, filtre la collection (`getCollection('games', …)`), calcule `count`, décide `robots` (`index` si ≥ 8, `noindex, follow` si 4–7, **pas de route** si < 4), puis `paginate(items, { params: { path }, pageSize: 24, props: { listing } })` (pagination imbriquée Astro : un tableau de `paginate()` avec `params`). Les segments d'âge sont dérivés de `ageMin` par `age-segments.ts` avant le filtrage.

Les compteurs des onglets indexables (« Hard (37) ») sont calculés ici et gelés dans le HTML.

Le même helper alimente `@astrojs/sitemap` via `filter` (exclut `/page/`, les `noindex`, `/_data/`) et `i18n` (`defaultLocale: 'en', locales: { en: 'en', fr: 'fr' }`), et le rendu des `<link rel="alternate" hreflang>` (seulement si la contrepartie est `index`).

### 5.4 Filtrage client, amélioration progressive

1. **Le HTML contient la grille** : 24 cartes complètes (lien, image `loading="lazy"` sauf les 6 premières, titre, bandeau joueurs · minutes · âge · pages, bouton Télécharger), les onglets indexables en `<a>`, la pagination en `<a>`. Sans JavaScript, tout fonctionne ; Googlebot indexe ce HTML.
2. **Un index JSON par catégorie** : endpoint Astro `src/pages/_data/[category].json.ts` qui écrit `/_data/puzzles-mazes.json`. Par fiche : `["slug","Titre","thumb.webp",ageMin,pMin,pMax,tMin,tMax,"d",["t1","t2"],["o1"],["c1"],"en",pages,color,popularity,date]`, soit ≈ 120–180 octets. Les facettes indexables ne sont pas dans le JSON de la page facette (déjà filtrées), elles y sont pour la catégorie.
3. **Chargement différé** : le JSON est demandé au premier geste de filtrage (ouverture du panneau, clic sur un chip, changement de tri) ou en `requestIdleCallback` après le chargement, jamais de façon bloquante. Entête `Cache-Control: max-age=3600, stale-while-revalidate` et `X-Robots-Tag: noindex` via le fichier `_headers` de l'hébergeur.
4. **Rendu** : un `<template>` de carte dans le HTML ; au filtrage, le script remplace le contenu de la grille par les cartes correspondantes, 24 à la fois, « Afficher plus » JS ; `aria-live="polite"` sur le compteur « 37 résultats ».
5. **État** : lu depuis `location.search` au chargement (restaure les filtres après un Retour, exigence Baymard), écrit par `history.replaceState` (pas `pushState` : un clic sur un chip ne doit pas créer une entrée d'historique).
6. **Facettes dynamiques** : les compteurs par option sont recalculés à chaque changement (OU dans une facette, ET entre facettes) ; les options à 0 restent visibles, grisées.
7. Aucun contrôle de filtre n'est un lien ; le panneau est un `<dialog>` natif ; le script pèse < 8 ko gz, sans framework.

### 5.5 À 3 000 fiches

- Hypothèse : 3 000 fiches réparties en 25 catégories ; la plus grosse (mazes ou word search, contenu maison) peut atteindre 600–800 fiches.
- JSON : 800 × 160 octets ≈ 130 ko brut, **≈ 25–35 ko en Brotli**. Seuil d'alerte au build : 300 ko brut par fichier ; au-delà, on scinde par page facette indexable (`/_data/puzzles-mazes-hard.json`) et la catégorie charge les morceaux à la demande. Pas de limite technique côté navigateur à ces tailles ; la limite est le temps d'analyse sur mobile bas de gamme (≈ 10 ms pour 130 ko).
- Pages statiques : 25 catégories + ≈ 120 pages facettes et combos + pagination (3 000 / 24 ≈ 125 pages de pagination en tout, ×2 langues) ≈ 600 pages de listing, 6 000 fiches EN+FR : loin du seuil de 10 000 pages à changements quotidiens de Google. Le crawl budget n'est pas notre sujet ; **la qualité de l'index l'est** (pas de pages minces).
- Images : vignettes 400 px WebP ≈ 15–25 ko, `srcset` 2× ; au plus 24 chargées par page ; au-delà de 100 cartes affichées en JS, les cartes hors écran sont retirées du DOM (virtualisation simple par tranches de 48).
- Build : 6 000 pages + 50 JSON se construisent en 1–2 minutes ; si cela dépasse 5 minutes, activer le cache de build de l'hébergeur avant de penser à autre chose.
- Recherche globale : Pagefind (index statique, chargé par fragments, filtres `data-pagefind-filter`), sur une page `/search/` en `noindex`.

### 5.6 robots.txt et entêtes

```
User-agent: *
Disallow: /*?
Disallow: /search/
Allow: /

Sitemap: https://printandplaygame.com/sitemap-index.xml
```

`Disallow: /*?` bloque toute URL avec query string (filtres, tri, UTM). Les PDF restent crawlables : ils ont un `X-Robots-Tag: noindex` **ou** un `Link: <fiche>; rel="canonical"` selon qu'on veut les voir ou non en résultat (décision à prendre dans le doc fiches ; par défaut canonical vers la fiche pour consolider). `/_data/*.json` : `X-Robots-Tag: noindex`, non bloqué (Googlebot peut le charger au rendu, sans conséquence).

## 6. Règles de qualité d'une page facette indexable

### 6.1 Gabarit (ordre dans le DOM)

1. Fil d'Ariane : Puzzles › Mazes › Hard mazes (BreadcrumbList).
2. H1 depuis le gabarit du type de facette (§ 6.4), suivi du **lead** : 2–3 phrases = 1 phrase de gabarit à variables + **1 phrase écrite à la main** (champ `lead` obligatoire, sinon la page reste `noindex`).
3. Onglets des facettes sœurs (liens HTML) avec compteurs.
4. Puces des filtres JS actifs (vide au chargement) + bouton Filtres · Tri.
5. Grille.
6. Bloc guide de 120–250 mots spécifique à la page (gabarit à variables pour le squelette, 2–3 phrases à la main), liens vers les pages sœurs et la page parente.
7. FAQ : 3 questions en `<details>`. Deux viennent de gabarits à variables (« What counts as a hard maze? », « Are these mazes free to print? »), une est propre à la page. Balisage `FAQPage` conservé mais **sans attente de rich result** (Google, août 2023).
8. « Related » : 3–5 liens vers des pages facettes d'autres catégories partageant la valeur (`/puzzles/word-search/hard/`, `/puzzles/rebus/hard/`) et vers la page occasion/thème la plus proche.

Les pages de pagination ≥ 2 ne rendent que 1, 2 (H1 seul), 3, 5 et la pagination.

### 6.2 Seuils et états

| Fiches | Route | `<meta name="robots">` | Sitemap | hreflang | Liée depuis le parent |
|---|---|---|---|---|---|
| 0–3 | non générée | — | non | non | non (la valeur reste disponible dans le filtre JS) |
| 4–7 | générée | `noindex, follow` | non | non | oui, lien normal (pas de nofollow : Google peut suivre, et la page redeviendra indexable) |
| ≥ 8 (≥ 12 pour un combo) | générée | `index, follow` | oui | oui si la contrepartie est aussi `index` | oui |

Une page qui passe de `index` à `noindex` reste à la même URL (pas de redirection) : on ne veut pas perdre l'historique quand elle repasse au-dessus du seuil.

### 6.3 Titres et meta descriptions sans doublon

Un gabarit par **type de facette**, pas un gabarit unique à variables, pour que « Hard mazes » et « Mazes for adults » ne se ressemblent pas :

| Type | `<title>` (EN) | Meta description (EN) |
|---|---|---|
| Catégorie | `Free Printable {Category} – PDF to Print` | `{count}+ free printable {category}: {sub1}, {sub2} and {sub3}. Download, print, play.` |
| Difficulté | `{Difficulty} {Category} – Free Printable PDF` | `{count}+ {difficulty} {category} to print at home or in class. {leadSentence}` |
| Âge | `{Category} for {Age} – Free Printables` | `Printable {category} suited to {ageRange}: {count}+ PDFs, {colorNote}. {leadSentence}` |
| Joueurs | `{PlayersLabel} {Category} – Print and Play` | `{count}+ {category} for {playersLabel}, {timeRange} per game. {leadSentence}` |
| Occasion / thème | `{Occasion} {Category} – Free Printable` | `{count}+ {occasion}-themed {category} to print. {leadSentence}` |
| Combo âge × difficulté | `{Difficulty} {Category} for {Age}` | `{count}+ {difficulty} {category} for {ageRange}. {leadSentence}` |

Règles : `{count}` arrondi à la dizaine inférieure (« 30+ »), jamais exact (sinon le titre change à chaque ajout) ; `{leadSentence}` est la phrase manuelle, tronquée à 90 caractères ; le build construit une map `title → url` et `description → url` et **échoue** sur doublon ; longueur title ≤ 60, description 120–155.

Même mécanique en FR avec les gabarits FR (« Labyrinthes difficiles à imprimer – PDF gratuit »).

### 6.4 Maillage entre pages facettes

- Horizontal : la barre d'onglets lie toutes les sœurs de la même facette (`easy ↔ medium ↔ hard`) et la page parente (« All mazes »).
- Vertical : chaque fiche affiche « More hard mazes » et « Mazes for adults » (ses pages facettes), en plus du fil d'Ariane (06 § 4).
- Transversal : « Related » (§ 6.1 point 8), et la page occasion `/occasions/christmas/` lie `/puzzles/mazes/christmas/` dans son texte.
- Le hub de silo cite en texte ses sous-pages indexables les plus demandées ; le footer ne liste que les 4 silos + 5 puzzles (06 § 4).
- Jamais de lien vers une page `noindex` depuis le footer ou le hub ; seulement depuis les onglets de sa catégorie.

## 7. UX mobile

- **Déclencheur** : bouton « Filtres · Tri » collant sous l'entête, avec pastille du nombre de filtres actifs. Les onglets indexables (Easy · Medium · Hard · Kids · Adults) sont une rangée de pilules défilante horizontalement, au-dessus, en liens HTML.
- **Panneau** : `<dialog>` plein écran (bottom sheet sur tablette), facettes en accordéon, les 3 facettes les plus utiles ouvertes (âge/joueurs, durée, thème), le reste replié ; 10 valeurs visibles puis « Voir plus » (Baymard : 6–10, 15+ nuit) ; champ de recherche dans Thème dès 15 valeurs ; compteur à côté de chaque option ; options à 0 grisées mais visibles ; une option cochée reste à sa place.
- **Application** : sur mobile, **pas de filtrage auto** ; bouton collant en bas « Voir 37 résultats » dont le chiffre se met à jour à chaque coche, « Tout effacer » à côté. Sur desktop, filtrage en temps réel dans une colonne collante (Baymard : attentes différentes selon l'écran).
- **Filtres actifs** : rangée de puces retirables au-dessus de la grille (« Pirates ×  · Dés × · Tout effacer »), visible sans ouvrir le panneau (28 % des sites n'ont pas ce récapitulatif, et c'est la première cause de désorientation).
- **Compteur de résultats** : « 37 mazes » sous le H1, mis à jour en `aria-live`.
- **CTA Télécharger** : sur chaque carte, un bouton « Télécharger » visible en permanence (pas au survol : il n'y a pas de survol sur mobile), en lien direct vers la fiche ancrée sur le bouton PDF (`/puzzles/mazes/lost-temple/#download`) pour garder la page fiche comme passage obligé (compteur, licence, crédit créateur). Sur la fiche, barre inférieure collante « Télécharger le PDF · 3 pages · N&B ok ». Le panneau de filtres ne recouvre jamais cette barre : il la remplace par son propre bouton « Voir N résultats ».
- **Retour** : l'état des filtres est dans l'URL (`?`) et restauré ; le scroll est restauré par `history.scrollRestoration = 'auto'` et le rendu synchrone des cartes depuis le JSON mis en cache.
- **Performance** : panneau et script chargés en `defer`, JSON à la demande ; cible LCP < 2,5 s sur mobile avec les 6 premières vignettes en `fetchpriority="high"`.
- **Accessibilité** : `role="group"` + `aria-labelledby` par facette, focus piégé dans le `<dialog>`, Échap ferme, cibles ≥ 44 px.

## 8. Exemples traités

### 8.1 Mazes : difficulté × âge

Inventaire visé à 12 mois : 400 mazes maison. Facettes : difficulté (easy/medium/hard), âge (preschool 3–5, kids 6–10, adults).

| Page | Demande (US/mois) | Fiches prévues | Décision | URL |
|---|---|---|---|---|
| Mazes (catégorie) | printable mazes 6 600 | 400 | index | `/puzzles/mazes/` |
| Easy | easy maze 2 400 | 150 | index | `/puzzles/mazes/easy/` |
| Medium | « printable mazes medium » (à valider, probablement 200–500) | 130 | index (exception éditoriale si < 200 : symétrie de la navigation) | `/puzzles/mazes/medium/` |
| Hard | hard mazes 2 900 + difficult maze 2 900 | 120 | index | `/puzzles/mazes/hard/` |
| Preschool | « preschool mazes » (à valider) | 60 | index si ≥ 200 | `/puzzles/mazes/preschool/` |
| Kids | children's mazes to print 4 400 (+ mazes for kids printable, sans donnée) | 220 | index | `/puzzles/mazes/kids/` |
| Adults | « mazes for adults » (à valider) | 90 | index si ≥ 200 | `/puzzles/mazes/adults/` |
| Preschool × easy | — | 55 | **non** : ≈ 90 % de preschool est easy, page doublon | — |
| Kids × easy | « easy mazes for kids » (à valider) | 100 | index si ≥ 200 | `/puzzles/mazes/kids/easy/` |
| Kids × medium | — | 80 | non (pas d'intention distincte) | — |
| Kids × hard | « hard mazes for kids » (à valider) | 40 | index si ≥ 200 et ≥ 12 fiches | `/puzzles/mazes/kids/hard/` |
| Adults × easy / medium | — | 30 / 25 | non | — |
| Adults × hard | « hard mazes for adults » (à valider) | 70 | index si ≥ 200 | `/puzzles/mazes/adults/hard/` |
| Mazes × Christmas / Halloween | « christmas maze printable », « halloween maze » (à valider) | 20 / 20 | liste blanche si ≥ 200 et ≥ 12 | `/puzzles/mazes/christmas/` |

Résultat : 6 pages à une facette, 3 combos au maximum, 9 cases de la matrice 3 × 3 dont 6 n'existent pas en URL. Filtres JS sur toutes ces pages : thème, occasion, N&B, pages, solutions incluses, tri. Ordre dans l'URL : âge avant difficulté (`/kids/hard/`, jamais `/hard/kids/`). Titre de `/puzzles/mazes/adults/hard/` : « Hard Mazes for Adults – Free Printable PDF » ; lead manuel : « These are the mazes our testers took more than ten minutes to solve: multiple dead-end loops, narrow corridors and no shortcuts. »

### 8.2 Escape games : âge × durée

Inventaire visé : 60 kits (maison + créateurs), 30 FR.

| Page | Demande | Fiches | Décision |
|---|---|---|---|
| Escape games (catégorie) | printable escape room (06), escape game à imprimer gratuit 170 FR | 60 | index `/escape-games/` |
| Kids 6–10 | free printable escape room for kids (sans donnée US), escape game enfant à imprimer gratuit (FR, sans donnée) + segmentation Escape Kit | 25 | index `/escape-games/kids/` (décidé dans 06) |
| Teens 11–15 | — | 15 | index `/escape-games/teens/` (décidé dans 06 ; surveiller : si < 8 fiches à 6 mois → noindex automatique) |
| Adults 16+ | printable escape room for adults 40 ; escape game adulte gratuit à imprimer 70 FR | 20 | index `/escape-games/adults/` |
| 30 min / 60 min / 90 min | aucune requête mesurée (« escape game 1 heure à imprimer » : à valider FR) | — | **JS** (puces multi) |
| Kids × 30 min, Adults × 60 min… | aucune | 8–12 | **non** : combinaison avec une facette JS, interdite par la règle ; la durée est affichée sur chaque carte et l'intro de `/kids/` dit « la plupart durent 30 à 45 minutes » |
| Christmas × escape | escape game noël adulte gratuit à imprimer 50 FR, « christmas escape room printable » (à valider) | 10 | liste blanche `/escape-games/christmas/` dès 12 fiches |
| Birthday × escape | escape game anniversaire à imprimer 10 FR | 8 | **non** pour l'instant (sous les seuils) ; traité par `/occasions/birthday/` |

Filtres JS sur ces pages : durée, joueurs, difficulté, thème, lieu, maître du jeu, matériel, langue. Ordre d'URL si un combo apparaissait un jour : âge puis occasion (`/escape-games/kids/christmas/`).

### 8.3 Board games : joueurs × durée

Inventaire visé : 250 jeux (classiques du domaine public + créateurs).

| Page | Demande | Fiches | Décision |
|---|---|---|---|
| Board games (catégorie) | printable board games 1 000, free printable board games 210 | 250 | index `/board-games/` |
| Solo | solo print and play games 50, print and play solo games 50 | 30 | index `/board-games/solo/` (exception éditoriale 1/10 ; aussi `/card-games/solo/` décidé dans 06) |
| 2 players | 2 player print and play games 10 ; jeu de société 2 joueurs à imprimer (FR, sans donnée) | 90 | index `/board-games/2-player/` (exception 2/10 : intention e-commerce universelle, page distincte des autres) |
| 3–4 / 5–6 / 7+ | aucune | 180 / 60 / 25 | **JS** ; « 7+ » renvoie vers `/card-games/party/` dans l'intro |
| ≤ 10 min, 10–20, 20–45, 45–90, 90+ | aucune | — | **JS** |
| 2 players × ≤ 20 min | aucune mesurée (« quick two player games » est générique, non imprimable) | 40 | **non** comme facette ; si l'envie éditoriale est là : **collection** `/collections/quick-two-player-games/` curatée à la main (sélection fixe, texte original), qui n'est pas générée par la grille de facettes et ne compte pas dans la liste blanche |
| Adults | printable board games for adults 20, jeu de société adulte à imprimer 10 | 35 | index `/board-games/adults/` (exception 3/10) |
| Kids / Family | free printable board games for kids (sans donnée), free printable family board games (sans donnée) ; `/family/` décidé dans 06 | 80 / 120 | index `/board-games/kids/`, `/board-games/family/` |

Filtres JS : joueurs limité aux valeurs 3–4, 5–6 et 7+ (solo et 2 joueurs restent des onglets en liens HTML, jamais des puces JS, conformément à la règle « un seul mécanisme par facette »), durée, complexité, matériel, pages, N&B, langue, tri. Ordre d'URL pour un futur combo : âge puis joueurs (`/board-games/kids/2-player/`), mais cette famille est interdite (§ 3.3) ; l'intro de `/2-player/` mentionne les jeux pour enfants.

## 9. Ce qui reste à faire

1. Mesurer (DataForSEO, US + FR) les expressions marquées « à valider » dans ce document (une vingtaine, dont une douzaine de pages candidates) avant d'activer les pages correspondantes ; tout ce qui est « à valider » est créé en `status: "draft"` (`noindex`) en attendant.
2. Écrire les gabarits EN/FR de titres, descriptions, leads et FAQ par type de facette (§ 6.3) et les 2 phrases manuelles par page `live`.
3. Implémenter `buildListings()`, `facet-pages.json`, le validateur de build, l'endpoint JSON, le script de filtrage (< 8 ko), robots.txt et `_headers`.
4. Mettre à jour `06-architecture-seo.md` : FAQPage et HowTo ne donnent plus de rich results (Google, août 2023) ; `/puzzles/mazes/` gagne `/preschool/`, `/kids/`, `/adults/` et 3 combos ; `/board-games/` gagne `/solo/`, `/2-player/`, `/adults/`, `/kids/`.
5. Après 3 mois d'indexation : exporter de Search Console les requêtes qui atterrissent sur les catégories avec un modificateur non couvert (« medium », « for toddlers », « 1 hour »…) et réviser la liste blanche ; vérifier dans le rapport Pages qu'aucune URL `?` n'est « Indexée » ou « Explorée, non indexée ».
