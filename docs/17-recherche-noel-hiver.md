# Recherche de sujets : Noël, hiver et fêtes de fin d'année

Date : 19 octobre 2026. Pas de nouvel appel DataForSEO : les identifiants ne sont pas configurés dans la session. Les chiffres viennent des exports déjà présents dans `data/kw/` (Google Ads, volume mensuel moyen aux États-Unis sur 12 mois). Les requêtes de Noël font plusieurs fois ce volume en décembre.

## Ce que montrent les données

| Requête | Vol. US | Concurrence pub | Page qui la couvre |
|---|---|---|---|
| christmas games for family (groupe) | 27 100 | faible | **à créer** : `christmas-games-for-family` (7/11) |
| christmas bingo game | 9 900 | forte | fiche `/bingo/christmas-bingo/` |
| christmas word search printable | 4 400 | moyenne | fiche `/puzzles/word-search/christmas-word-search/` |
| printable christmas games | 3 600 | forte | hub `/occasions/christmas/` |
| free printable christmas games | 1 600 | faible | hub `/occasions/christmas/` |
| christmas board games | 1 300 | forte | intention d'achat, pas de page |
| exit advent calendar | 1 300 | forte | produit vendu, hors sujet |
| best family games christmas | 880 | faible | `christmas-games-for-family` |
| christmas left right game printable | 720 | moyenne | une section de `christmas-games-for-family` |
| printable christmas family games | 720 | forte | `christmas-games-for-family` |
| printable christmas party games | 720 | forte | `printable-christmas-games-for-adults` (12/11) |
| christmas puzzles for adults | 480 | forte | `printable-christmas-games-for-adults` |
| printable christmas games for adults (groupe) | 390 | faible | **à créer** : `printable-christmas-games-for-adults` (12/11) |
| adult christmas word search | 390 | forte | pas de fiche (voir piste 2) |
| christmas trivia printable | 390 | moyenne | quiz dans `printable-christmas-games-for-adults` |
| christmas board games for families | 320 | forte | `christmas-games-for-family` |
| christmas scavenger hunt printable | 320 | forte | article du 13/11 déjà programmé |
| winter word search printable | 1 000 | faible | fiche `/puzzles/word-search/winter-word-search/` |
| winter word search for adults | 70 | faible | — |
| printable winter games | 20 | faible | — |

## Conclusions

**Hiver.** La demande pour un article « jeux d'hiver en famille » est presque nulle (20 recherches pour « printable winter games »). Les gens cherchent Noël ou le Nouvel An, pas « l'hiver ». L'article du Nouvel An (16/11) couvre la fin d'année, et la fiche mots mêlés d'hiver capte la seule requête « hiver » qui compte. Pas d'article hiver.

**Thanksgiving.** « Thanksgiving games for family » (8 100) sort le 20/10 et couvre aussi « printable thanksgiving games » (1 300) avec le hub. Un deuxième article ferait doublon.

**Noël.** Deux articles ajoutés au calendrier, sur deux intentions distinctes : la famille (7/11) et les adultes (12/11). Ils complètent les trois articles de Noël déjà programmés (classe le 30/10, maternelle le 2/11, chasse au trésor le 13/11) sans viser les mêmes requêtes.

## Pistes pour la suite

1. **Christmas left right game** (720) : une histoire « gauche-droite » à imprimer, écrite par nous, mériterait sa propre fiche PDF. L'article familial en contient déjà une version courte.
2. **Mots mêlés de Noël pour adultes** (390 + 140 « free printable christmas word search for adults ») : une grille 20 × 20 dans toutes les directions, sur le modèle de `hard-word-search-for-adults`. Un générateur existe déjà (`scripts/puzzles/`).
3. **Christmas trivia printable** (390) : le quiz de l'article adultes pourrait devenir une fiche PDF avec les réponses.
4. **Mots mêlés du Nouvel An** (1 600 pour « new year word search ») : aucune fiche aujourd'hui, alors que la requête est forte et peu disputée. C'est la meilleure opportunité trouvée pour l'hiver. `docs/13a` prévoyait déjà un bingo et des mots mêlés du Nouvel An pour l'article du 16/11 : il faut les créer avant cette date.
