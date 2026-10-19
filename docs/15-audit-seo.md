# Audit SEO du 19 octobre 2026

Site audité : https://printandplaygame.com, 355 URL dans le sitemap, le jour de l'inscription à Google Search Console.

Méthode : crawl complet du site compilé (`dist/`, 381 pages HTML, script dans le scratchpad de la session), contrôle du site en ligne avec `curl` (codes HTTP, redirections, en-têtes, robots.txt, accès des robots d'IA), relecture des 34 hubs et de leurs FAQ face aux données des fiches, vérification d'un échantillon de 15 fiches jeux face à leur source et à BoardGameGeek.

Limite : l'état réel de l'indexation (pages découvertes, explorées, indexées, exclues) ne se voit que dans Search Console. Il faudra exporter le rapport *Pages* dans deux semaines environ pour compléter cet audit.


## En bref

La base technique est saine. Aucun lien interne cassé, aucune page orpheline, aucun titre en double, des URL canoniques correctes partout, un sitemap qui correspond exactement aux pages indexables, et toutes les pages à 2 clics maximum de l'accueil.

Les défauts trouvés étaient surtout des détails répétés sur des centaines de pages (titres trop longs, dates du sitemap qui bougeaient à chaque build) et des affirmations inexactes dans les textes des hubs. Ils sont corrigés dans ce lot, sauf ceux qui demandent une action dans Cloudflare ou une décision (voir plus bas).

Le vrai chantier qui reste est éditorial : les hubs, qui visent les plus gros volumes de recherche, n'ont qu'une vingtaine de mots de texte propre.


## 1. Indexabilité

| Point vérifié | Résultat |
|---|---|
| robots.txt | Correct. Bloque seulement les URL à paramètres et `/search/`, déclare le sitemap. |
| Robots d'IA (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, CCBot) et Bingbot | Tous reçoivent un 200 (test avec leur signature). Cloudflare ne les bloque pas. |
| http → https | 301, correct. |
| URL sans slash final, `index.html` | 308 vers l'URL canonique, correct. |
| Page inexistante | Vrai 404, correct. |
| Anciennes URL de dot to dot supprimées | 301 vers leur remplaçant, correct. |
| Sitemap | 355 URL, aucune en noindex, aucune page indexable oubliée. Identique au site en ligne. |
| Pages en noindex | 26 : recherche, 404, une catégorie de blog trop maigre et 23 pages créateurs avec un seul jeu. Choix cohérent. |
| **www.printandplaygame.com** | **Répond 200 au lieu de rediriger.** La balise canonical limite les dégâts, mais une redirection 301 est la règle. À faire dans Cloudflare (section 8). |
| **printandplaygame.pages.dev** | **Copie complète du site, accessible et indexable.** Corrigé : en-tête `X-Robots-Tag: noindex` sur ce domaine et sur les URL de prévisualisation (`public/_headers`). |

La publication programmée des articles fonctionne : le workflow GitHub tourne bien toutes les heures sur la branche de production.


## 2. Balises techniques

**Titres.** 344 titres sur 355 dépassaient 60 caractères, à cause du suffixe « | Print & Play Game » (20 caractères) ajouté partout. Google coupe vers 60 caractères et affiche déjà le nom du site au-dessus de chaque résultat. Le suffixe n'est désormais ajouté que s'il tient (`src/lib/seo.ts`). Il reste 7 titres entre 61 et 64 caractères, ce qui est acceptable.

**Meta descriptions.** Toutes présentes et uniques. 220 dépassent 160 caractères, parce qu'elles reprennent le résumé de la fiche (jusqu'à 220 caractères) suivi des infos pratiques. Google coupera la fin, ou réécrira la description, ce qu'il fait de toute façon souvent. Non corrigé : priorité basse.

Les descriptions des pages créateurs étaient coupées au milieu d'un mot (« …the whole family can play, f »). Corrigé : elles s'arrêtent sur la première phrase ou sur un mot entier.

**Canonical, robots, langue.** Corrects sur toutes les pages. Pas de hreflang tant que la version française n'existe pas, ce qui est normal.

**Données structurées** (le code invisible qui décrit la page aux moteurs) : toutes valides en JSON.

| Type | Pages | Remarque |
|---|---|---|
| BreadcrumbList (fil d'Ariane) | 376 | Correct |
| CreativeWork | 236 | Les puzzles n'avaient ni description, ni image, ni date : ajoutées. |
| Product | 124 | Voir la question 1 en fin de rapport. |
| Article (règles) | 63 | Image ajoutée. |
| CollectionPage (hubs) | 36 | Correct |
| FAQPage | 23 | Correct, mais 13 hubs n'ont pas de FAQ (section 4). |
| WebSite | 1 | Contient une `SearchAction` que Google n'utilise plus depuis fin 2024. Sans effet négatif, laissée. |

**Images de partage.** Aucune page n'avait de balise `og:image` (l'image affichée quand on partage le lien, et un signal pour Google Discover). Ajoutée sur les 300 fiches qui ont une couverture.

**Sitemap, champ lastmod.** La date de mise à jour de l'accueil, des pages fixes et des pages créateurs était celle du jour du build : elle changeait à chaque déploiement sans que la page change. Google finit par ignorer ce champ quand il n'est pas fiable. Corrigé : les listes prennent la date de leur élément le plus récent, les pages fixes n'ont plus de date.


## 3. Maillage interne

Le maillage est solide. Toutes les pages du sitemap reçoivent au moins 3 liens internes, aucune n'est à plus de 2 clics de l'accueil, et aucun lien ne pointe vers une page inexistante ou vers une URL avec paramètres.

Les liens sortants sont tous en `nofollow`, comme prévu par la règle de la maison.

Une piste d'amélioration : les liens des fiches vers les hubs passent surtout par le fil d'Ariane et les étiquettes. Un lien dans le texte (« more Halloween printables ») vers le hub d'occasion ou de thème, avec une ancre descriptive, renforcerait les hubs saisonniers.


## 4. Contenu

### Exactitude des hubs

Les FAQ et les introductions des 34 hubs ont été comparées aux données des fiches qu'ils listent. Onze affirmations étaient fausses ou dépassées, toutes corrigées :

| Hub | Erreur | Correction |
|---|---|---|
| Halloween | « Le dot to dot citrouille et le bingo dès 4–5 ans » : les deux sont classés 6–8 ans. | Les dot to dots fantôme et chauve-souris et le labyrinthe facile pour les 4–5 ans, le reste dès 6 ans. |
| Dot to dot | « Jusqu'à 90 points » : les puzzles experts vont jusqu'à 172. | 172 dans l'intro et la description. |
| Party games | « 5 à 30 joueurs » : six jeux du hub se jouent à moins de 5. | 2 à 30 joueurs. |
| Labyrinthes, labyrinthes moyens | « 6 à 9 ans » : 4 labyrinthes moyens sur 10 sont pour les 9–13 ans. | 6 à 12 ans. |
| Été | « Des labyrinthes océan » : il n'y en a aucun, et un seul labyrinthe d'été. | Liste réelle du hub. |
| Noël | Bingo « pour 6 à 30 personnes » : le PDF a 20 cartes. | 6 à 20 personnes. |
| Bingo | « Chaque PDF a des cartes uniques et une feuille d'appel » : faux pour les deux modèles vierges. | Précisé. |
| Plateaux imprimables | « Chaque plateau est relié à ses règles » : une dizaine (shogi, xiangqi, fox and geese, shut the box…) n'ont pas de lien vers une page de règles. | « quand nous en avons une ». |
| Règles, règles jeux de plateau, papier-crayon | « Tous les jeux du domaine public ont un plateau ou une feuille » : faux pour le backgammon, les dames chinoises, Sim, Sprouts et la plupart des jeux de cartes. | « La plupart », avec les exceptions nommées. |
| Roll and write | « Une page et deux dés » : certains jeux demandent 6 ou 7 dés et plusieurs feuilles. | « Une page ou deux et une poignée de dés ». |
| Jeux de cartes | Cribbage et la bataille « faits pour deux » : ils se jouent à 2–4. | Nuancé. |

Deux erreurs trouvées sur les pages puzzles elles-mêmes :

- Les modèles de bingo vierges affichaient « Answers: Included » alors qu'il n'y a rien à corriger. Corrigé dans les fiches et dans le générateur (`scripts/puzzles/build_batch.py`).
- Le conseil d'impression de toutes les pages bingo disait de ne pas imprimer la dernière page « pour cacher la solution ». Or cette page contient les cartes à appeler, indispensables pour jouer. Le texte dépend maintenant du type de puzzle.

### Exactitude des fiches jeux (échantillon de 15)

<!-- résultats de l'échantillon -->

### Profondeur du contenu des hubs

C'est le point faible principal. Les hubs visent les requêtes les plus recherchées (« word search printable », « printable bingo cards », « dot to dot »), mais leur texte propre se limite à une introduction de 15 à 50 mots. Seuls 5 hubs ont un paragraphe de plus, et 13 n'ont pas de FAQ : mots mêlés, bingo, puzzles, dot to dot, les trois niveaux de labyrinthes, jeux de dés, party games, chasse au trésor, roll and write, jeux pour 2 et jeux pour enfants.

Le reste de la page est une grille de cartes, identique dans sa structure à celle des concurrents. Pour Google comme pour les IA, une page qui n'explique rien donne peu de raisons d'être citée.

Recommandation : pour les 6 hubs aux plus gros volumes (mots mêlés, bingo, puzzles, dot to dot, chasse au trésor, Halloween puis Noël), ajouter sous la grille un court guide de 150 à 300 mots (comment choisir, par âge ou par usage) et 3 à 4 questions de FAQ. Ces textes doivent rester factuels et s'appuyer sur ce que contient vraiment le hub.

### Fraîcheur

Aucun texte daté ou périmé trouvé dans les hubs, en dehors du nombre de points des dot to dots. Le site a moins d'une semaine, la fraîcheur deviendra un sujet dans quelques mois. Pour les règles et les fiches, il faudra un champ « mis à jour le » le jour où une fiche est revue, pour que la date affichée et celle du sitemap reflètent une vraie mise à jour.


## 5. Lisibilité par les IA

Bonne base. Tout le texte est dans le HTML livré au navigateur, sans JavaScript nécessaire pour le lire. Les fiches commencent par un résumé d'une phrase, suivi des faits clés (joueurs, durée, pages, licence) dans une liste structurée. Les règles suivent un plan fixe avec une FAQ. Les robots d'IA ne sont pas bloqués.

Ajouté : un fichier `/llms.txt` généré au build. C'est un plan du site en texte brut pour les assistants IA, construit à partir des mêmes hubs que le sitemap. Google a déclaré ne pas l'utiliser, et son effet sur les autres assistants n'est pas démontré. Il ne coûte rien et ne peut pas nuire.

Ce qui aiderait le plus les IA, c'est la même chose que pour Google : des hubs qui répondent à une question (« quel labyrinthe pour un enfant de 5 ans ? ») en une ou deux phrases claires, que l'IA peut reprendre en citant la source.


## 6. Performance

Le HTML est léger (10 à 13 Ko par page), avec une seule feuille de style de 33 Ko et des polices auto-hébergées. Les images des grilles sont chargées en différé (`loading="lazy"`).

Douze couvertures dépassaient 700 Ko (jusqu'à 1 Mo), dont Dracula's Feast, Brains! et Night of the Mummy, affichées sur la page Halloween. Elles ont été recompressées en PNG 256 couleurs, sans différence visible, soit 3 à 4 fois plus légères. Le dossier `public/img/` passe de 23 à 16 Mo.


## 7. Corrections faites dans ce lot

| Fichier | Changement |
|---|---|
| `src/lib/seo.ts` | Suffixe du titre seulement s'il tient dans 60 caractères. |
| `src/layouts/Base.astro`, `GamePage`, `PuzzlePage`, règles, blog | Balise `og:image` à partir de la couverture. |
| `src/components/PuzzlePage.astro` | Conseil d'impression selon le type de puzzle, données structurées complétées. |
| `src/pages/rules/[slug].astro` | Image dans les données structurées. |
| `src/pages/creators/[slug].astro` | Meta description sans mot coupé. |
| `src/pages/sitemap.xml.ts` | lastmod fiable. |
| `src/pages/llms.txt.ts` | Nouveau fichier `/llms.txt`. |
| `public/_headers` | noindex sur pages.dev et les prévisualisations. |
| 13 fichiers de `src/content/hubs/` | Affirmations corrigées (section 4). |
| 2 fiches bingo vierges et `scripts/puzzles/build_batch.py` | Pas de corrigé. |
| `src/content/hubs/puzzles__mazes__hard.md`, `src/pages/how-to-print.astro` | Titres raccourcis. |
| 12 images de `public/img/games/` | Recompressées. |

Ces corrections sont sur la branche `claude/fervent-turing-5cvddc`. Elles seront en ligne quand elles seront fusionnées dans la branche de production (`ccr-205f3937-62xvhk`).


## 8. À faire dans les tableaux de bord (Anthony)

**Redirection www → sans www.** Cloudflare Pages ne sait pas le faire avec le fichier `_redirects`. La méthode officielle passe par les *Bulk Redirects* : créer une liste avec la source `www.printandplaygame.com`, la cible `https://printandplaygame.com`, le code 301, et cocher *preserve query string*, *subpath matching*, *preserve path suffix* et *include subdomains*. Ensuite, créer la règle qui utilise cette liste. L'enregistrement DNS `www` doit rester proxifié (nuage orange). Guide : https://developers.cloudflare.com/pages/how-to/www-redirect/

**Bing Webmaster Tools.** Sur https://www.bing.com/webmasters, page *My Sites*, bouton *Import* : on se connecte avec le compte Google, Bing reprend le site déjà vérifié et son sitemap. Les données apparaissent sous 48 heures.

**IndexNow via Cloudflare.** Dans Cloudflare, *Caching → Configuration → Crawler Hints*, activer l'option. Cloudflare prévient alors Bing et les autres moteurs compatibles IndexNow à chaque changement de contenu, sans rien coder. Gratuit sur tous les plans.

**Search Console.** Le sitemap est envoyé. Pour les demandes manuelles, l'ordre conseillé est : d'abord l'accueil, Halloween, les mots mêlés, le bingo, les puzzles et Thanksgiving, puis Noël et les autres hubs principaux (détail dans la conversation du 19 octobre).


## 9. Questions ouvertes

1. **Données structurées `Product` sur les fiches jeux.** Elles déclarent une offre à 0 $ « en stock », alors que le site ne vend rien et que le téléchargement est souvent sur le site du créateur. Google réserve ses fiches marchandes aux pages où l'on peut acheter, avec un prix supérieur à zéro. Au mieux, le prix « gratuit » peut apparaître dans le résultat. Au pire, Search Console affichera des avertissements « Fiches de marchand », et Google peut juger le balisage trompeur. Je recommande de le retirer et de garder `CreativeWork`, mais c'était un choix noté dans `docs/06`. À trancher.
2. **Âges des sudokus enfants.** Les pages disent « 4×4 dès 5 ans » et « 6×6 pour les 8–12 ans », alors que les fiches sont classées 6–8 et 9–13 ans. Lequel est juste : le texte ou le classement ?
3. **Textes des hubs.** Est-ce que je rédige les guides et FAQ des 6 hubs prioritaires (section 4) ? Ce sont des ajouts éditoriaux importants, d'où la question avant de les faire.


## 10. Prochain audit

Dans deux semaines environ : export du rapport *Pages* de Search Console (pages indexées et exclues, avec leur motif) et du rapport *Performances* (premières requêtes et impressions). Ce sera l'occasion de vérifier l'indexation réelle et de choisir les pages à renforcer selon les requêtes qui apparaissent.
