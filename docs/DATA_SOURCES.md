# Sources et connexions — V2

Trois bases sont réellement utilisées :
- **INSEE Melodi** : population municipale, jeu `DS_POPULATIONS_REFERENCE`, mesure PMUN. National France hors Mayotte, régions, départements et communes proposés. Une commune supplémentaire peut être cherchée dans le référentiel administratif officiel puis interrogée dans Melodi.
- **Eurostat** : taux de chômage annuel des 15–74 ans, `une_rt_a`, filtres A / T / Y15-74 / PC_ACT, quatre pays. Les codes de qualité sont conservés, notamment les ruptures de séries.
- **Banque mondiale WDI** : cinq indicateurs, sept pays, périodes publiées. Les définitions INSEE et WDI restent distinctes.

Les extractions réelles livrées ont été récupérées le 6 octobre 2026 et validées. `data/source-status.json` donne la couverture et la date exacte de chaque copie. Le connecteur lit prioritairement une copie sourcée couvrant la recherche, puis la base si nécessaire ; le bouton de mise à jour demande une lecture en direct. Le cache et la dernière copie utilisable servent de secours.

La collecte GitHub Actions utilise `scripts/refresh_public_data.py` : une base défaillante conserve son dernier fichier valide et n’empêche pas les autres bases de se mettre à jour. Les valeurs absentes restent nulles. Aucun jeton n’est nécessaire pour ces requêtes publiques.

## Autres sources
`data.gouv.fr` est un catalogue : les liens donnent accès aux jeux et à leurs producteurs, pas à une statistique inventée. Pew est un lien vers des études, pas un module religieux déjà alimenté. Immigration, niveau de vie et religions sont explicitement signalés lorsqu’aucun jeu n’est encore connecté dans Atlas. Les adaptateurs génériques restent disponibles pour de futurs imports vérifiés.

## Documentation officielle
- INSEE : https://catalogue-donnees.insee.fr/fr/catalogue/recherche/DS_POPULATIONS_REFERENCE
- API INSEE : https://www.insee.fr/fr/information/8184146
- Eurostat : https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
- WDI : https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api
- Communes : https://geo.api.gouv.fr/decoupage-administratif/communes

## Licences et attribution
La population INSEE est sous Licence Ouverte 2.0. Eurostat requiert l’attribution et le respect de la politique de réutilisation de la Commission. WDI conserve ses conditions propres, généralement CC BY 4.0 avec les réserves du jeu et de ses producteurs initiaux. Les URL, licences, dates et organismes figurent sur chaque observation.

CO₂ : `EN.GHG.CO2.PC.CE.AR5`, hors UTCATF, t CO₂e/personne. Producteurs initiaux : JRC/EDGAR et IEA. Source : https://data.worldbank.org/indicator/EN.GHG.CO2.PC.CE.AR5
