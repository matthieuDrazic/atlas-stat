# Sources et connexions

V1 : les séries françaises locales livrées sont **DONNÉES DE DÉMONSTRATION**. Aucun chiffre réel INSEE ou Pew n’est intégré. Le module religieux contient un tableau vide.

## Connexion activée
Banque mondiale WDI : API v2 sans clé, cinq indicateurs, sept pays ; requêtes limitées aux pays et années sélectionnés. Cache de 24 h ; à défaut de réseau, dernier cache ou instantané GitHub Actions. Un échec sans instantané propose explicitement une démonstration, jamais un remplacement silencieux.
Documentation : https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api
Licence : https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets
La qualification prudente `estimate` du connecteur n’est pas une classification détaillée de chaque observation WDI. Pour une analyse publiée, compléter cette classification à partir des métadonnées de l’indicateur.

## Adaptateurs nécessitant un jeu et un mapping
- INSEE : `inseeAdapter(rows, indicator, {source, mapRow})`. Chaque cube nécessite de lire son schéma ; ne pas deviner les dimensions. Catalogue officiel : https://www.insee.fr/fr/information/8184146 ; documentation Melodi : https://www.insee.fr/fr/information/1302169?question=comment-utiliser-l-api-melodi
- BDM, Données locales et Métadonnées : pas de connecteur universel activé ; extraire/normaliser les fichiers en amont. Vérifier leurs modalités d’accès et leur migration vers Melodi dans le catalogue INSEE.
- Eurostat : `eurostatAdapter(jsonStat, indicator, {source, dimensionMap})` ; `dimensionMap` retourne l’observation brute ou `null` pour une combinaison exclue. API : https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction
- CSV : `csvAdapter(text, indicator, source)` ; champs documentés dans le README.
- Religions : `religionAdapter(rows, indicator, source)` ; pays/continent/monde seulement. Aucune génération, inférence à partir de l’origine ou de la nationalité.
- data.gouv.fr, OCDE, ONU, OWID, Pew : imports documentés possibles, pas de collecte automatisée livrée pour ces sources.

Les licences varient selon les jeux et leurs sources initiales. Conserver les conditions exactes dans `source.license`, la publication originale dans `source.url`, et toute attribution requise. Un lien vers un organisme ne constitue pas une licence de réutilisation.

CO₂ : indicateur actuel `EN.GHG.CO2.PC.CE.AR5`, hors UTCATF, t CO₂e/personne. Producteurs initiaux explicitement indiqués : JRC/EDGAR et IEA. Métadonnées originales : https://data.worldbank.org/indicator/EN.GHG.CO2.PC.CE.AR5
