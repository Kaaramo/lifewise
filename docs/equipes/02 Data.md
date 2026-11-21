# Sous-équipe 2 : Data

**Membres.** Michel Sagesse Kolie, Zakaria Tahiri, Amine Sbah. **Référent :** Michel.

## Mission

Fixer le langage commun de la chaîne et fournir les données sur lesquelles chaque maillon se prouve : contrat
d'interface, prétraitement, scénarios annotés, base de l'historique. C'est l'équipe qui démarre le plus tôt :
sans son contrat, les autres ne peuvent pas brancher leurs maillons.

## Reçoit et produit

- **Reçoit** les mesures et les images de l'IoT, ou des caméras de test (téléphone, webcam).
- **Produit** le contrat d'interface, l'objet « contexte », les scénarios annotés, le schéma SQLite, la vérité terrain.
- **Travaille avec** toutes les équipes (contrat), le backend qui écrit dans la base, le web qui l'affiche.

## Tâches

| # | Tâche | Livrable | Échéance |
|---|---|---|---|
| 2.1 | Écrire le contrat d'interface JSON avec un représentant de chaque sous-équipe, source de chaque image comprise | `docs/contrat-interface.md`, validé par les six référents | S1 |
| 2.2 | Constituer le jeu de scénarios : départs avec et sans téléphone, clés, portefeuille, pris avec plusieurs caméras, annotés | Jeu de scénarios et fichier d'annotations | S1 |
| 2.3 | Ajouter un agenda simulé aux scénarios (le rendez-vous qui rend le départ important) | Agenda de test au format du contrat | S1 |
| 2.4 | Écrire le prétraitement : horodatage, filtrage, normalisation, sélection des images utiles | Module de prétraitement | S2 |
| 2.5 | Construire l'objet « contexte » : mesures récentes, qualité des données, événements connus | Objet contexte conforme au contrat | S2 |
| 2.6 | Concevoir le schéma SQLite de l'historique | Schéma et script de création | S2 |
| 2.7 | Écrire la politique de conservation et de consentement : activation, suspension, suppression | Note d'une page | S3 |
| 2.8 | Fournir la vérité terrain pour les mesures finales | Résultat attendu pour chaque scénario | S4 |

## Ce qu'on attend

- Le contrat est validé par les six référents avant la fin de S1, puis ne change que par une demande de fusion relue par les équipes concernées.
- Chaque objet apparaît présent et absent plusieurs fois, sur chaque caméra ; cible proposée : vingt départs par caméra, dont la moitié avec un objet absent.
- Chaque image a son annotation : objets réellement présents, caméra, lumière.
- Le prétraitement écarte les images inutilisables (floues, trop sombres) et dit pourquoi.
- Le schéma SQLite permet de retrouver, pour chaque alerte, ce qui a été vu, décidé et répondu.

## Livrables

- **Code** : dossiers `pretraitement/` et `donnees/` du dépôt.
- **Documents** : contrat d'interface, protocole d'annotation, politique de conservation et de consentement.
- **Rapport** : état de l'art (jeux de données, métriques), conception du contrat et du modèle de données, prétraitement et scénarios, protocole de test, annexe de protection des données.
- **Guide** : diapositives du contrat d'interface et des données.
