# Déployer sur Cloudflare Pages

Le site est statique (Astro). Le plus simple et le plus robuste est de brancher Cloudflare Pages sur le dépôt GitHub : chaque push déclenche un build et un déploiement, sans jeton d'API à partager.

## Étapes (une fois, 5 minutes)

1. Sur https://dash.cloudflare.com, menu **Workers & Pages** → **Create** → onglet **Pages** → **Connect to Git**.
2. Autoriser Cloudflare sur GitHub et choisir le dépôt `Antho-352/jeux-societe`.
3. Réglages du build :
   - **Production branch** : `main` (ou la branche de travail `ccr-205f3937-62xvhk` tant que rien n'est fusionné).
   - **Framework preset** : Astro.
   - **Build command** : `npm run build`
   - **Build output directory** : `dist`
   - **Variables d'environnement** : `NODE_VERSION` = `22.22.0` (le fichier `.node-version` du dépôt le dit déjà, la variable est une ceinture de sécurité).
4. **Save and Deploy**. Le premier build prend 1 à 2 minutes. Le site est servi sur `https://<projet>.pages.dev`.
5. **Custom domains** → ajouter `printandplaygame.com` et `www.printandplaygame.com`. Si le domaine est chez Cloudflare, les enregistrements DNS sont créés automatiquement. Sinon, créer un CNAME `www` vers `<projet>.pages.dev` et suivre l'assistant pour l'apex.
6. Dans **Settings → Builds**, activer les **Preview deployments** pour toutes les branches : chaque branche de travail obtient une URL de prévisualisation.

## Ce qui est déjà prévu dans le dépôt

- `public/_headers` : en-têtes de sécurité, cache long sur `/pdf/`, `/img/` et `/_astro/`, PDF servis en téléchargement.
- `public/robots.txt` : bloque les URL avec paramètres et la recherche, déclare `sitemap.xml`.
- `src/pages/sitemap.xml.ts` : sitemap généré au build, sans les pages en noindex (hubs trop fins, recherche, 404).
- Limites Cloudflare Pages à garder en tête : 25 Mo par fichier, 20 000 fichiers par déploiement. Les PDF hébergés sont tous sous 25 Mo ; au-delà, on les mettra sur R2.

## Statistiques

Cloudflare Web Analytics (gratuit, sans cookie) s'active dans **Workers & Pages → le projet → Metrics → Enable Web Analytics**. Aucun script à ajouter si le domaine est sur Cloudflare : l'injection est automatique.

## Pour que je puisse déployer moi-même plus tard

Si tu veux que je lance des déploiements depuis cette session (par exemple pour tester sans push), ajoute dans l'environnement cloud deux variables : `CLOUDFLARE_API_TOKEN` (jeton « Cloudflare Pages: Edit ») et `CLOUDFLARE_ACCOUNT_ID`. J'utiliserai alors `npx wrangler pages deploy dist`. Ce n'est pas nécessaire avec l'intégration Git.
