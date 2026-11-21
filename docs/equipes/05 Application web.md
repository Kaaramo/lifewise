# Sous-équipe 5 : Application web

**Membres.** Saïd Jadli, Aymane Hayoun. **Référent :** Saïd.

## Mission

Donner à l'utilisateur un tableau de bord web où il consulte son historique, comprend ses indicateurs et règle son
assistant. Chaque alerte y est expliquée : ce qui a été vu, ce qui a été décidé, ce que l'utilisateur a répondu,
avec la possibilité de corriger une observation. L'équipe prépare aussi l'accès au projet en ligne via un
serveur, demandé par le professeur.

## Reçoit et produit

- **Reçoit** l'API du backend et l'historique SQLite conçu par la Data.
- **Produit** le tableau de bord web et l'accès en ligne au projet.
- **Travaille avec** le backend (API) et la Data (contenu de l'historique, indicateurs).

## Tâches

| # | Tâche | Livrable | Échéance |
|---|---|---|---|
| 5.1 | Maquetter les écrans dans la charte LIFEWISE : historique, indicateurs, réglages | Maquettes validées par la coordination | S1 |
| 5.2 | Mettre en place le projet web et le relier à l'API, sur données simulées d'abord | Squelette relié à l'API | S2 |
| 5.3 | Écrire l'historique consultable, avec correction d'une observation | Écran historique | S3 |
| 5.4 | Écrire les indicateurs du sujet : types d'alertes, routines, taux d'alertes jugées utiles | Écran indicateurs | S3 |
| 5.5 | Écrire les réglages : fréquence des alertes, plages de fonctionnement, suppression de l'historique | Écran réglages | S4 |
| 5.6 | Préparer l'accès au projet en ligne via un serveur | Adresse d'accès et procédure | S4 |

## Ce qu'on attend

- Les écrans suivent la charte LIFEWISE : fond noir, couleur réservée aux états, aucune police hors charte.
- Le tableau de bord fonctionne sur données simulées avant que la chaîne réelle soit prête.
- Pour chaque alerte de l'historique, on lit ce qui a été vu, décidé et répondu, et on peut corriger une observation.
- Les indicateurs sont ceux du sujet, et chacun dit d'où vient son chiffre.
- Supprimer l'historique fonctionne vraiment, et se montre en démonstration.

## Livrables

- **Code** : `05-application-web/code/` dans le dépôt.
- **Documents** : maquettes, procédure d'accès en ligne.
- **Rapport** : conception (architecture web, écrans), réalisation du tableau de bord, tests d'usage des écrans.
- **Guide** : diapositives du tableau de bord.
