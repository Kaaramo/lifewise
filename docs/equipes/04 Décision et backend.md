# Sous-équipe 4 : Décision et backend

**Membres.** Adnane Qassiri, Aymane Azaagag. **Référent :** Adnane.

## Mission

Transformer ce qui est vu et ce qui est connu en une décision justifiée, puis la rendre accessible aux deux
applications. Des règles écrites valident d'abord la situation (départ détecté, objet habituel non vu,
rendez-vous à l'agenda) ; un petit modèle de langage formule ensuite la décision et sa justification. L'équipe
écrit aussi le service qui enchaîne les modules, l'API des applications et l'inscription de chaque événement dans
l'historique.

## Reçoit et produit

- **Reçoit** l'objet « contexte » de la Data et les objets vus de la Vision.
- **Produit** la décision et sa justification, l'API commune aux applications, l'envoi de la notification, les événements inscrits dans SQLite.
- **Travaille avec** la Data (contexte, base), la Vision (objets vus), le web et le mobile (API, notification).

## Tâches

| # | Tâche | Livrable | Échéance |
|---|---|---|---|
| 4.1 | Écrire les règles de validation du scénario pilote | Règles écrites et codées | S1 |
| 4.2 | Comparer des petits modèles de langage (Phi, Qwen, Mistral) sur les scénarios | Tableau comparatif | S2 |
| 4.3 | Produire la décision et sa justification concise au format du contrat | Module de décision | S2 |
| 4.4 | Écrire le service qui enchaîne les modules, de l'image à la décision | Chaîne complète sur ordinateur | S2 |
| 4.5 | Publier l'API commune : notifications, réponses (rappeler dans 5 min, ignorer), historique, réglages | API documentée avec exemples, projet publié en S2 | S3 |
| 4.6 | Choisir avec le mobile le mode d'envoi de la notification, puis le mettre en place | Notification reçue sur le téléphone | S3 |
| 4.7 | Inscrire chaque événement et la réponse de l'utilisateur dans SQLite | Historique alimenté | S3 |
| 4.8 | Mesurer décisions correctes, fausses alertes et latence de bout en bout | Tableau de mesures | S4 |

## Ce qu'on attend

- Les règles sont écrites en clair avant d'être codées, et chaque équipe peut les lire.
- Chaque décision vient avec sa justification ; une alerte invite à vérifier (« Pensez à vérifier votre portefeuille »), elle n'affirme jamais un oubli.
- Sans départ détecté, aucune alerte ; les fausses alertes sont comptées sur les scénarios.
- Le projet d'API est publié en S2, pour que le web et le mobile codent dessus sans attendre la version finale.
- À la fin de S2, une seule commande lance la chaîne complète sur données simulées.

## Livrables

- **Code** : `04-decision-backend/code/` dans le dépôt.
- **Documents** : règles de validation, comparatif des modèles de langage, documentation de l'API, tableau des mesures.
- **Rapport** : état de l'art (petits modèles de langage, fusion multimodale), conception (moteur de décision, architecture logicielle, API), réalisation, évaluation des décisions et de la latence, annexes des contrats d'API et du guide d'installation.
- **Guide** : diapositives de la décision et de l'architecture logicielle.
