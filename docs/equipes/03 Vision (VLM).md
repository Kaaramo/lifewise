# Sous-équipe 3 : Vision (VLM)

**Membres.** Bachirou Konate, Yasser Nadi. **Référent :** Bachirou.

## Mission

Dire, pour chaque image de départ, quels objets sont vus et avec quelle confiance. L'équipe compare trois
options (Moondream2, LLaVA quantifié et un détecteur léger type YOLO), choisit sur des chiffres, puis fait tourner
le modèle retenu sur deux montages : une photo du téléphone traitée sur ordinateur, et le Raspberry Pi en local.
Elle ne conclut jamais à un oubli : elle dit ce qui est vu, le reste appartient à la décision.

## Reçoit et produit

- **Reçoit** les images sélectionnées par le prétraitement, quelle que soit la caméra.
- **Produit** la liste des objets vus, chacun avec sa confiance, au format du contrat d'interface.
- **Travaille avec** la Data (scénarios annotés), l'IoT (Raspberry Pi) et le backend, qui reçoit ses résultats.

## Tâches

| # | Tâche | Livrable | Échéance |
|---|---|---|---|
| 3.1 | Installer et faire tourner Moondream2 et LLaVA quantifié sur ordinateur | Premiers essais documentés | S1 |
| 3.2 | Tester un détecteur léger type YOLO pour les objets simples | Essai comparatif | S2 |
| 3.3 | Évaluer les trois options sur le jeu de scénarios : objets bien vus, manqués, inventés, selon la caméra | Tableau de résultats par modèle et par caméra | S2 |
| 3.4 | Choisir le modèle sur la qualité, la mémoire, la latence et la licence | Décision écrite avec ses chiffres | S2 |
| 3.5 | Faire tourner le modèle retenu sur les deux montages : téléphone et ordinateur, Raspberry Pi en local (quantifié si nécessaire) | Module de vision testé sur les deux montages | S3 |
| 3.6 | Mesurer ce que coûte le passage au Raspberry Pi : latence, mémoire, qualité | Tableau comparatif des montages | S3 |
| 3.7 | Documenter les limites du champ visuel et les erreurs de reconnaissance | Note d'analyse des erreurs | S4 |

## Ce qu'on attend

- Le tableau comparatif donne, pour chaque option et chaque caméra : objets bien vus, manqués, inventés, temps par image et mémoire.
- Le choix du modèle s'appuie sur ces chiffres, écrits avant la décision.
- La sortie respecte le contrat : des objets et des confiances, jamais une phrase sur un oubli.
- La différence entre l'ordinateur et le Raspberry Pi est mesurée, pas supposée.
- Chaque type d'erreur est illustré par un exemple réel tiré des scénarios.

## Livrables

- **Code** : `03-vision/code/` dans le dépôt.
- **Documents** : tableau comparatif des modèles, décision argumentée, comparaison des montages, analyse des erreurs.
- **Rapport** : état de l'art (vision par ordinateur, détection d'objets, modèles vision-langage), conception de la chaîne visuelle, réalisation, évaluation (précision, rappel, erreurs, temps d'inférence), annexe des paramètres des modèles.
- **Guide** : diapositives de la perception visuelle.
