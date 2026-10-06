# Atlas V2 — trouver un chiffre sans connaître les bases de données

1. Sur l’accueil, choisissez une question dans **Que cherchez-vous ?**.
2. Choisissez le lieu dans **Pour quel territoire ?**. La liste s’adapte à la base.
3. Choisissez **Dernière année disponible**, une évolution sur 5/10 ans ou vos propres années.
4. Vérifiez la **Base de données** puis appuyez sur **Afficher les chiffres**.

Le résultat montre le chiffre, son année et son producteur. **Que signifie ce chiffre ?** explique sa définition. **D’où vient ce chiffre ?** donne la publication, la date de récupération et les limites. Les tableaux et les filtres supplémentaires sont facultatifs.

## Exemples
- Habitants de Rennes : INSEE, population municipale issue du recensement. La date du recensement peut être plus ancienne que la date de consultation.
- Chômage en France : Eurostat, moyenne annuelle des 15–74 ans, hommes et femmes réunis ; ce n’est pas le nombre d’inscrits à France Travail.
- Espérance de vie au Japon : Banque mondiale, en années ; ce n’est pas une prédiction individuelle.

## Choisir une autre commune
Dans la question population avec la base INSEE, ouvrez **Ma commune n’est pas dans la liste**, entrez son nom et choisissez parmi les communes proposées. Le référentiel géographique officiel fournit le nom et le code ; la statistique de population est ensuite demandée séparément à l’INSEE. Une erreur réseau reste une erreur, jamais un chiffre fictif.

## Plusieurs bases, plusieurs définitions
INSEE, Eurostat et Banque mondiale ont des connecteurs effectivement utilisés dans l’application. Les observations réelles sont aussi conservées dans de petites copies locales avec leurs sources, pour limiter les pannes et les problèmes CORS. Le bouton **Mettre à jour** demande une nouvelle lecture de la base.

Population municipale INSEE et population totale WDI ne sont pas fusionnées. Le nom du jeu et le périmètre permettent de choisir. Une période ou une commune absente ne devient pas zéro.

## Sujets encore incomplets
Une question sans série reliée est indiquée comme telle ; le lien mène au producteur. data.gouv.fr est un catalogue de jeux, pas le producteur des chiffres. Pew est une source d’études religieuses, pas une connexion chiffrée déjà alimentée.

## Exemples fictifs
Ils sont séparés des vraies statistiques. Le bouton **Essayer avec des exemples fictifs** les active volontairement ; **Revenir aux vrais chiffres** les quitte. Ne pas citer ces nombres.
