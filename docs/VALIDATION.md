# Rapport de vérification — 6 octobre 2026

## Vérifications exécutées
- 15 tests Node réussis : schéma de 600 observations de démonstration, recherche (accent, territoire, années, comparaison), refus de confusion étrangers/immigrés, recommandations, CSV et injection de formules, CSV à guillemets, granularité et confidentialité, adaptateurs WDI/Eurostat/religions, courbes discontinues, graphiques vides, pyramide, histogramme à densité, nuage et signature du drill-down.
- Test Python réussi : acquisition sur réponses simulées ; conservation byte pour byte du dernier instantané après erreur réseau et après valeur invalide ; métadonnées de récupération.
- Vérification de chaque module JavaScript par `node --check`.
- Validateur réussi : imports relatifs existants, assets HTML présents, JSON lisibles, quatorze thèmes, champs et statuts, catalogue pointant vers les fichiers existants, absence d’URL de développement dans le code applicatif.
- Données de production livrées : fichiers vides, distincts de demo. Aucun secret API et aucun backend requis par l’architecture. Un workflow Pages valide les modules avant publication.

## Vérifications non exécutées ou non concluantes
- Test visuel navigateur / iPhone 15 : non exécuté. Le runtime Playwright était installé mais aucun navigateur n’était présent ; le téléchargement du navigateur a échoué. Le CSS vise notamment 393 px, mais cela ne remplace pas une validation sur appareil réel.
- Parcours utilisateur complet, clics, téléchargement CSV natif, impression, service worker et navigation hors ligne : pas validés dans un vrai navigateur dans cet environnement. Les fonctions CSV et le rendu SVG ont des tests de modules réussis.
- Banque mondiale en direct : tentative expirée dans l’environnement de livraison. Le connecteur est testé sur une réponse de structure WDI, pas sur une récupération réseau complète. Le fichier de production antérieur (vide) est resté inchangé.
- Publication GitHub Pages : workflows et chemins préparés ; aucun dépôt n’a été créé ni déployé pour cette livraison. Le déploiement effectif dépend des réglages du dépôt.
- CORS et modalités d’accès de toutes les sources : pas de validation réseau exhaustive. INSEE et Eurostat nécessitent des correspondances de dimensions et des jeux ciblés.

## Recette à faire après publication
1. Accueil : ouvrir chaque thème, vérifier la vue vide des thèmes sans source.
2. Rechercher population Rennes, immigration Bretagne, chômage France depuis 2000, religions Japon, comparer Bretagne Normandie, revenu médian Ille-et-Vilaine.
3. Vérifier les choix proposés pour les recherches ambiguës.
4. Filtrer puis ouvrir un point/barre, lire sa source et ses dimensions ; descendre France → Bretagne → Ille-et-Vilaine → Rennes quand disponible.
5. Chômage, Côtes-d’Armor, 2022 : valeur manquante ; immigrés, Rennes, 2021 : non diffusable. Aucun zéro imputé.
6. Comparer 2, puis 5 territoires ; vérifier le refus du sixième et la période commune des écarts.
7. CSV : vérifier les en-têtes, les statuts, le label de démonstration et les métadonnées.
8. Impression PDF : vérifier le bandeau de démonstration, les sources et le tableau complet depuis l’explorateur.
9. Enregistrer puis retirer un favori ; recharger le navigateur ; changer de thème visuel.
10. Religions : confirmer la vue vide initiale ; importer uniquement un fichier national réel et sourcé ; confirmer le refus d’une granularité régionale et d’une déduction à partir de l’origine.
11. Réseau : tester un échec API, une dernière consultation en cache et un instantané statique ; sans données, vérifier le bouton de démonstration explicite.
12. Sur iPhone 15 : navigation basse, filtres tactiles, défilement du tableau, aucun débordement général ; hors connexion après une consultation complète.
