# Fonds géographiques
Aucune frontière fictive n’est fournie. Le fichier de démonstration est vide ; l’interface affiche un classement à la place d’une carte.
Pour activer une choroplèthe, ajoutez un GeoJSON WGS84 Polygon/MultiPolygon de moins de 2 Mo, documentez sa source et sa licence, puis ajoutez `geoFile` à l’indicateur du catalogue. Chaque entité doit avoir `properties.geoCode` identique au code des observations et `properties.label`.
Le moteur utilise une projection plane simple, adaptée aux petites emprises. Pour une carte mondiale ou des géométries traversant l’antiméridien, utilisez une projection cartographique dédiée avant import. Une carte mondiale complète n’est pas livrée dans cette V1.
