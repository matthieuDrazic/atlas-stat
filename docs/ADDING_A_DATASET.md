# Ajouter un jeu
1. Télécharger un jeu public auprès du producteur. Vérifier licence, définition, couverture et secret statistique.
2. Utiliser un adaptateur ou un script pour obtenir un tableau d’observations normalisées (voir `data/demo/demo-france.json` pour la structure, jamais pour de vraies valeurs).
3. Mettre le tableau dans `data/production/votre-jeu.json` ; ne pas réutiliser le dossier demo.
4. Ajouter un indicateur dans `data/catalog.json` avec identifiant unique, libellé, thème, unité, `mode: "static"`, `file: "./data/production/votre-jeu.json"`, mots-clés, définition, URL de définition, calcul, périmètre, collecte, limites et dimensions publiées.
5. Ajouter les territoires et leurs parents dans `data/territories.json`. Ne pas inventer de parents ou de granularité.
6. Chaque observation doit contenir `datasetId`, `indicatorId`, `indicatorLabel`, `theme`, `value`, `unit`, `period`, `geoCode`, `geoLabel`, `geoLevel`, `dimensions`, `source`, `dataType`, `methodologyNote`, `confidenceInterval`, `status`, `isDemo: false`.
7. La source contient au minimum `publisher`, `datasetTitle`, `url` HTTPS, `license`, `retrievedAt` ; `lastUpdate` peut être nul si inconnu. Ne pas remplacer la date de publication par la date de récupération.
8. `dimensions` : null pour une dimension inexistante. Un intervalle doit décrire bornes et méthode si disponible. Ne pas l’inventer.
9. Valider : `python3 scripts/validate.py`, `node --test tests/core.test.mjs`. Tester le jeu dans l’interface. Maintenir les dates AAAA ou AAAA-MM et des codes uniques par combinaison de dimensions.
10. Religions : utiliser `religionAdapter` lors de la conversion, ajouter une méthode explicite et respecter la granularité nationale. Aucune estimation locale à partir d’une origine. Pour le module religieux V1, conserver l’identifiant `religions` ou étendre son routage.

Pour un CSV, utilisez l’écran Sources pour un test local puis normalisez et enregistrez le JSON dans le dépôt. Un adaptateur API ajouté doit renvoyer ce même schéma et être explicitement appelé dans `loadDataset` ; ajouter un nom de fichier d’adaptateur ne suffit pas.
