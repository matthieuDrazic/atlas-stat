# ATLAS DATA CENTER — V1

Application statique française pour explorer, comparer et exporter des statistiques avec leur source. Sans serveur, compte ni dépendance CDN obligatoire. Compatible avec une URL GitHub Pages contenant le nom du dépôt.

**Important : les chiffres français locaux fournis sont des DONNÉES DE DÉMONSTRATION. Ils sont artificiels et ne proviennent pas de l’INSEE. Aucun chiffre religieux n’est fabriqué.** Les séries nationales internationales sont demandées à la Banque mondiale ; leur disponibilité dépend du réseau et du producteur.

## Ce qui fonctionne
Accueil et 14 thèmes ; recherche locale avec accents, mots-clés, suggestions et choix en cas d’ambiguïté ; filtres ; graphiques SVG en courbes et barres, donut uniquement pour une composition pertinente ; comparaison de 2–5 territoires ; calculs d’écarts sur période commune ; navigation géographique selon les données ; détail cliquable ; tableaux paginés ; export CSV traçable ; impression/PDF ; favoris ; clair/sombre ; cache local ; service worker ; imports CSV et JSON sourcés ; actualisation et publication par GitHub Actions.

## Périmètre transparent de la V1
- 4 indicateurs locaux synthétiques (population, immigrés, chômage, revenu), 6 territoires, années 2000–2024.
- 5 indicateurs WDI pour France, Allemagne, Espagne, Italie, Japon, Inde et Chine. Ajouter d’autres codes pays au catalogue est possible.
- Religions : écran et import validé, sans observations livrées. Aucun niveau infranational n’est autorisé par cet adaptateur V1. Les projections restent identifiées.
- Les 14 thèmes sont disponibles dans la navigation, mais plusieurs n’ont encore aucun jeu connecté.
- Pas de carte mondiale réelle ni de fond géographique intégré. Le classement remplace la carte ; un GeoJSON fourni et documenté active la choroplèthe.
- Pas de connecteur INSEE universel prêt à toutes les requêtes : adaptateur avec mapping par jeu. BDM et métadonnées demandent une conversion en amont. Eurostat : adaptateur JSON-stat disponible, jeu à configurer.
- Pyramide des âges, histogramme et nuage de points disponibles pour des jeux importés portant les dimensions explicites nécessaires. Hiérarchie : barres comme alternative au treemap ; avant/après : barres plutôt que slope chart. Les jeux livrés utilisent principalement les courbes et barres.
- Export PDF via l’impression native, sans téléchargement PDF automatique. Aucun serveur n’est nécessaire.

## 1. Créer le dépôt GitHub
Connectez-vous sur https://github.com, cliquez sur **+ → New repository**, choisissez `atlas-data-center`, la visibilité **Public** pour l’hébergement gratuit usuel, puis **Create repository**. Ne publiez aucun jeton ni donnée privée.

## 2. Quels fichiers ajouter
Décompressez le ZIP. Ajoutez **le contenu du dossier atlas-data-center à la racine du dépôt** : `index.html` doit être directement à la racine. Conservez `assets`, `adapters`, `data`, `geo`, `docs`, `scripts`, `tests`, et le dossier `.github` (parfois masqué). Ne téléversez pas seulement le ZIP : GitHub Pages ne le décompresse pas.

## 3. Importer depuis ordinateur ou mobile
Sur le site GitHub du dépôt : **Add file → Upload files**, glissez les fichiers et dossiers puis **Commit changes**. Sur mobile/iPhone, l’application GitHub ne fournit pas une importation complète de dossiers ZIP : utilisez Safari, éventuellement « Version pour ordinateur », ou un ordinateur pour conserver tous les sous-dossiers et fichiers cachés. Pour un gros téléversement, GitHub Desktop ou Git est plus fiable.

Avec Git : créez un clone du dépôt, copiez les fichiers, puis `git add .`, `git commit -m "Add Atlas V1"`, `git push`. Vérifiez la présence de `.github/workflows`.

## 4. Activer GitHub Pages
Deux méthodes, choisissez-en une :
- **Simple** : dépôt → **Settings → Pages → Build and deployment → Deploy from a branch**, branche `main`, dossier **/(root)**, Save. Le fichier `.nojekyll` permet de servir les fichiers tels quels.
- **Avec les workflows fournis** : **Settings → Pages → Source : GitHub Actions**. Onglet Actions → « Publier Atlas sur GitHub Pages » → Run workflow. Un push sur `main` relance la publication. Documentation : https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

La méthode Actions est recommandée si vous activez l’actualisation automatique des données. Une actualisation réussie déclenche la publication via `workflow_run` ; un push créé par le jeton Actions ne déclenche pas à lui seul un autre workflow push.

## 5. Vérifier le site
Ouvrez l’URL affichée dans Settings → Pages (après la fin du déploiement). Essayez `population Rennes`, vérifiez le bandeau **DONNÉES DE DÉMONSTRATION**, cliquez sur un point puis sa source. Comparez Bretagne et Normandie. Exportez CSV. Ouvrez Religions : sans import, une vue vide est attendue. Sur iPhone : les menus se trouvent en bas ; le tableau défile horizontalement.
Le bouton **Imprimer / enregistrer en PDF** ouvre l’impression du navigateur. Sur iOS, utilisez l’aperçu d’impression puis les options de partage/enregistrement du système.

## 6. Modifier le catalogue
Éditez `data/catalog.json` depuis GitHub (icône crayon). Chaque indicateur possède un `id` unique, un `theme` parmi les 14, une unité, une source d’accès, une définition et ses limites. Les thèmes restent vides tant qu’aucun jeu n’est connecté. Consultez `docs/ADDING_A_DATASET.md`.

## 7. Ajouter un CSV
Dans l’application : **Sources et méthode → Importer un fichier sourcé**. Choisissez l’indicateur cible et un CSV ; fournissez producteur, titre, URL originale HTTPS, licence, type et méthode. Colonnes requises : `geoCode,geoLabel,geoLevel,period,value` ; facultatives : `unit,status,religion,category`. Séparateur virgule ou point-virgule, guillemets possibles, décimale française entre guillemets si séparateur virgule. `NA`, `ND`, `..`, `:` et vide deviennent des manques, jamais des zéros.
L’import reste en mémoire et est perdu au rechargement. Pour le rendre permanent : convertissez en observations JSON normalisées, placez-le dans `data/production`, puis ajoutez un indicateur statique au catalogue. Un import doit respecter l’unité de l’indicateur cible. Pour un nouveau concept, ajoutez d’abord un indicateur au catalogue.

## 8. Connecter une source
Les adaptateurs séparés se trouvent dans `adapters`. INSEE demande un `mapRow` explicite, Eurostat un `dimensionMap`. Réduisez le cube à la période et au périmètre nécessaires. Ne déclarez que des dimensions effectivement publiées. Les fichiers normalisés statiques constituent la voie la plus simple pour GitHub Pages.

## 9. Activer les Actions
Onglet **Actions → I understand my workflows, go ahead and enable them** si demandé. Dans **Settings → Actions → General**, autorisez les actions nécessaires et les permissions de lecture/écriture pour le workflow d’actualisation si les règles du dépôt le nécessitent.
« Actualiser les données publiques » s’exécute le premier jour de chaque mois à 05:15 UTC, ou avec **Run workflow**. Il collecte uniquement WDI, valide les lots, et écrit un nouvel instantané seulement après succès de tous les lots. Le dernier fichier valide est conservé en cas d’erreur. Les délais de GitHub peuvent décaler les horaires.
Aucun secret nécessaire pour WDI. Si un futur connecteur en exige un, utilisez **Settings → Secrets and variables → Actions → New repository secret**, et lisez-le seulement dans l’environnement du script Actions. Ne le mettez jamais dans le JS, un JSON public, les journaux ou le YAML en clair. Les secrets ne sont pas transmis au navigateur.

## 10. Résoudre CORS et les erreurs réseau
CORS est une décision du serveur source, pas un filtre à supprimer dans le navigateur. N’ajoutez pas de proxy public inconnu et ne désactivez pas la sécurité. Préférez la collecte GitHub Actions et des fichiers JSON dans le dépôt. Si WDI échoue : le dernier cache/instantané est proposé ; sans cache, un message permet d’ouvrir explicitement la démonstration.

## 11. Vérifier les licences
Avant chaque import, lisez les conditions du fichier source, pas seulement celles de l’organisme. Conservez attribution et URL originale. Le code est MIT ; démonstrations synthétiques CC0 ; sources réelles et géométries ont leurs licences propres. Pew et d’autres producteurs peuvent imposer des conditions spécifiques.

## 12. Mettre à jour les données et l’application
Utilisez le workflow ou remplacez un JSON validé par un fichier du même format. `retrievedAt` décrit la récupération, `lastUpdate` la date fournie par le producteur. Actualiser dans l’application vide le cache de données mais conserve les favoris. Le service worker essaie le réseau avant son cache. Après une modification du code, incrémentez le nom de cache dans `service-worker.js` si vous changez les assets précachés.

## Tester en local (facultatif)
Avec Python et Node : `python3 -m http.server 8000` depuis le dossier, puis ouvrez le serveur dans votre navigateur. Ne double-cliquez pas sur `index.html` : les modules et fetch ne fonctionnent pas correctement en `file://`.
Validation : `python3 scripts/validate.py` et `node --test tests/core.test.mjs`. Aucun `npm install` nécessaire.

## Architecture
ES modules natifs ; graphiques SVG accessibles au clavier et doublés par un tableau ; adaptateurs vers un schéma commun ; cache local plafonné ; routeur par hash pour éviter les 404 de GitHub Pages. Les fichiers sont relatifs, aucune clé. Deux workflows séparent acquisition et publication. Le GeoJSON vide évite d’afficher des frontières fictives. Voir `docs/METHODOLOGY.md`, `DATA_SOURCES.md`, `PRIVACY.md` et `ADDING_A_DATASET.md`.
