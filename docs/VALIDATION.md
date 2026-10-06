# Validation de la V2 — 6 octobre 2026

- 24 tests de modules réussis : traitement des observations, exports, graphiques, recherche guidée, choix de source et sélection des périodes.
- Validation des fichiers et test de sécurité des mises à jour réussis.
- Collecte réelle réussie : 12 observations INSEE, 92 Eurostat et 910 Banque mondiale. Les instantanés conservent leurs sources et dates.
- Parcours navigateur exécutés et réussis sur GitHub Actions : menus guidés, résultats réels, définition et source du chiffre, export CSV, favoris, comparaison, sujets indisponibles, recherche de commune et registre des sources.
- Format mobile de 393 pixels testé sans débordement, ainsi que le thème sombre. Ce contrôle ne remplace pas un essai sur un iPhone physique.
- Publication GitHub Pages réussie pour le commit `69a0a77d831193cd558700c24bdef58b1929a15f`.

Exécution navigateur : https://github.com/matthieuDrazic/atlas-stat/actions/runs/37477763964

Les tests navigateur utilisent les instantanés sourcés et une réponse contrôlée pour la recherche de commune. La disponibilité future des API externes ne peut pas être garantie ; les instantanés permettent de consulter les dernières données collectées.
