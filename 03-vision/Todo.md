# Todo — partie Vision (VLM)

## Objectif

Pour chaque image retenue par le prétraitement, produire les objets effectivement visibles avec leur niveau de confiance, au format convenu avec le backend. Comparer Moondream2, LLaVA quantifié et un détecteur léger de type YOLO, choisir sur la base de mesures, puis tester le modèle retenu sur les deux montages prévus. La vision décrit ce qu'elle voit : elle ne conclut pas qu'un objet est oublié ou absent de la maison.

## 0. Préparer l'évaluation

- [ ] Récupérer auprès de l'équipe Data le jeu de scénarios annoté et les catégories d'objets à évaluer ; confirmer qu'il représente les différentes caméras.
- [x] Rédiger une proposition de contrat JSON Vision -> backend (`../docs/proposition-contrat-vision-backend.md`). Elle reste une proposition et ne remplace pas le contrat commun.
- [ ] Présenter la proposition à l'équipe backend et aligner avec Data les champs communs : identifiants, source de l'image, horodatage, catégories, erreurs et champs de mesure.
- [ ] Valider avec Data le format d'entrée et les métadonnées de l'image.
- [x] Rédiger un premier prompt système pour les VLM (`documents/prompt-systeme.md`), avec les catégories cibles, les règles de perception et le format de sortie.
- [ ] Tester le prompt sur les VLM retenus et ajuster son échelle de confiance sur les scénarios annotés ; le prompt seul ne garantit pas une calibration statistique.
- [ ] Définir un protocole reproductible : mêmes images, catégories et conditions de mesure pour chaque modèle ; préciser le matériel et les paramètres utilisés.
- [ ] Définir comment compter les objets bien vus, manqués et inventés, puis calculer précision et rappel par modèle et par caméra.
- [ ] Préparer un tableau de mesures incluant aussi le temps d'inférence par image et la mémoire utilisée.

**Résultat attendu :** jeu d'évaluation et protocole communs, établis avant les essais comparatifs.

## Grille de comparaison des modèles

| Critère | Mesure à relever | Comment comparer |
|---|---|---|
| Détection correcte | Vrais positifs (objets attendus et détectés), faux positifs (objets annoncés à tort) et faux négatifs (objets manqués) ; précision, rappel et F1 | Calculer au niveau des objets, globalement puis par catégorie et par caméra. Une détection attendue ne peut être comptée qu'une fois ; les doublons sont des faux positifs. |
| Fiabilité des sorties | Pourcentage de sorties conformes au contrat, sorties vides ou invalides, doublons et exemples d'objets inventés | Vérifier sur l'ensemble des essais que le modèle retourne les champs attendus et ne transforme pas « non visible » en « oublié ». |
| Confiance | Scores de confiance retournés et erreurs associées | Rapporter les scores et les seuils utilisés. Ne pas comparer directement les valeurs de confiance entre modèles : elles ne sont pas nécessairement calibrées de la même façon. |
| Robustesse visuelle | Résultats selon la caméra et, si les scénarios le permettent, l'éclairage, la distance et l'occlusion | Chercher les écarts et les cas d'échec, pas seulement la moyenne globale. Ne tirer de conclusion que sur les conditions réellement testées. |
| Latence | Temps de traitement par image, de la réception de l'image à la sortie exploitable ; médiane et 95e percentile | Mesurer sur le même matériel et avec les mêmes images ; séparer les essais de chauffe et préciser les paramètres d'exécution. |
| Ressources | Pic de RAM, mémoire GPU si utilisée, et taille du modèle sur disque | Comparer les mesures sur ordinateur et Raspberry Pi et vérifier qu'elles restent compatibles avec le matériel visé. |
| Déploiement | Exécution hors ligne sur Raspberry Pi, compatibilité, dépendances et éventuelle quantification | Noter les étapes nécessaires, les erreurs et les compromis de qualité causés par la quantification. |
| Licence et reproductibilité | Licence du checkpoint exact, version, paramètres, quantification et configuration matérielle | Vérifier les conditions d'utilisation et consigner les informations nécessaires pour répéter chaque mesure. |

**Règles pour que la comparaison soit équitable :**

- Utiliser les mêmes images annotées et catégories pour les trois candidats. Garder un jeu de validation pour choisir les paramètres/seuils et un jeu de test distinct pour les résultats finaux, si la taille du jeu de données le permet.
- Fixer et consigner les consignes données aux VLM, les seuils de confiance et les paramètres de chaque détecteur avant l'évaluation finale.
- Rapporter les résultats par catégorie et par caméra ; ne pas choisir uniquement sur une moyenne globale ou sur une démonstration isolée.
- Ne pas imposer de score global pondéré sans accord préalable sur les priorités. Présenter les mesures côte à côte et justifier le compromis retenu.

## 1. Installer et tester les candidats sur ordinateur — S1

- [ ] Installer Moondream2 et LLaVA quantifié dans l'environnement de test.
- [ ] Exécuter quelques scénarios représentatifs avec chaque modèle et conserver les paramètres nécessaires à la reproduction.
- [ ] Vérifier que les résultats permettent d'identifier les objets visés et leur confiance ; noter les limites ou sorties non conformes.
- [ ] Ranger le code d'essai dans `code/` et les premières observations dans `documents/`.

**Résultat attendu :** premiers essais documentés et exécutables sur ordinateur.

## 2. Ajouter un détecteur léger à la comparaison — S2

- [ ] Tester un détecteur léger de type YOLO sur les mêmes scénarios et catégories d'objets.
- [ ] Adapter ses sorties au format de comparaison commun sans confondre son score de détection avec une probabilité calibrée.
- [ ] Consigner ses résultats, son temps d'inférence, sa mémoire et ses contraintes d'utilisation.

**Résultat attendu :** résultats comparables pour Moondream2, LLaVA quantifié et le détecteur léger.

## 3. Évaluer et choisir le modèle — S2

- [ ] Évaluer chaque option sur l'ensemble des scénarios annotés, séparément par caméra.
- [ ] Remplir le tableau : objets bien vus, manqués, inventés, précision, rappel, temps par image et mémoire.
- [ ] Examiner des exemples concrets d'erreurs et vérifier que les scores ne masquent pas de différences importantes entre caméras.
- [ ] Vérifier la licence et les conditions d'utilisation de la version exacte de chaque candidat.
- [ ] Choisir le modèle en explicitant les compromis entre qualité, latence, mémoire, licence et compatibilité avec le Raspberry Pi.
- [ ] Consigner les mesures et la justification du choix dans `documents/`.

**Résultat attendu :** tableau comparatif complet et décision argumentée par des mesures.

## 4. Construire le module de vision — S3

- [ ] Implémenter le traitement d'une image sélectionnée et l'adaptation des résultats au contrat d'interface validé.
- [ ] Produire une liste structurée d'objets vus et de leurs confiances ; ne pas produire de conclusion sur un oubli ou sur ce qui n'est pas visible.
- [ ] Ajouter des vérifications sur les entrées, la sortie et les cas incertains, en suivant les conventions du projet.
- [ ] Tester le module avec les scénarios annotés et vérifier sa compatibilité avec le backend.

**Résultat attendu :** module testable dont les sorties respectent le contrat partagé.

## 5. Tester les deux montages et mesurer le coût du Raspberry Pi — S3

- [ ] Tester le modèle retenu sur une photo issue du téléphone, traitée sur ordinateur.
- [ ] Tester le même modèle en local sur le Raspberry Pi ; quantifier le modèle si nécessaire et documenter les paramètres.
- [ ] Comparer, dans des conditions aussi proches que possible, la qualité, le temps d'inférence et la mémoire des deux montages.
- [ ] Noter les problèmes de compatibilité, de ressources ou de qualité observés sur le Raspberry Pi.

**Résultat attendu :** module testé sur les deux montages et tableau comparatif ordinateur/Raspberry Pi.

## 6. Analyser les erreurs et finaliser les livrables — S4

- [ ] Documenter les limites dues au champ de vision, à l'éclairage, à l'occlusion et aux erreurs de reconnaissance observées.
- [ ] Illustrer chaque type d'erreur par un exemple réel du jeu de scénarios.
- [ ] Rédiger les sections du rapport de l'équipe : état de l'art, chaîne visuelle et format de sortie, mise en place et choix des modèles, résultats et analyse des erreurs.
- [ ] Préparer les diapositives du guide sur la perception visuelle.
- [ ] Vérifier que les tableaux, paramètres, résultats et décisions sont cohérents entre le code, les documents et le rapport.
- [ ] Faire relire le travail par le référent de l'équipe et le transmettre aux équipes backend, Data et IoT pour validation des interfaces et du montage.

**Résultat attendu :** rapport, guide, analyse des erreurs et documents de mesure finalisés.

## Critères de fin

- [ ] Le modèle retenu a été choisi à partir des résultats mesurés, pas d'une supposition.
- [ ] Les performances sont rapportées par modèle et par caméra, avec erreurs, latence et mémoire.
- [ ] La sortie contient uniquement les objets vus et leurs confiances, conformément au contrat validé.
- [ ] Le comportement sur ordinateur et Raspberry Pi a été mesuré et documenté.
- [ ] Aucun poids de modèle volumineux, secret ou photo permettant d'identifier une personne n'est ajouté au dépôt.
