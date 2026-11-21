# Sous-équipe 1 : IoT et matériel

**Membres.** Adila Yassir, Abrini Mohamed, Mohamed Channa. **Référent :** Adila.

## Mission

Monter le banc d'essai qui voit l'utilisateur partir : un Raspberry Pi, une caméra et des capteurs qui produisent
des mesures et des images horodatées. Le banc sert à prouver que la chaîne tourne en local, sur un petit
appareil ; il ne bloque personne, car les autres équipes peuvent travailler avec la caméra du téléphone ou une
webcam en attendant. L'équipe est aussi la référence matérielle du groupe et forme les autres si besoin.

## Reçoit et produit

- **Reçoit** le matériel du professeur.
- **Produit** les mesures (mouvement, porte, luminosité) et les images de départ, au format du contrat d'interface.
- **Travaille avec** la Data, qui reçoit ses mesures, et la Vision, qui fait tourner son modèle sur le Raspberry Pi.

## Tâches

| # | Tâche | Livrable | Échéance |
|---|---|---|---|
| 1.1 | Récupérer le matériel au bureau du professeur et l'inventorier | Liste du matériel avec références | S1 |
| 1.2 | Définir les caractéristiques de la nouvelle caméra, la choisir, étudier son branchement au Raspberry Pi | Fiche de choix de la caméra | S1 |
| 1.3 | Installer le Raspberry Pi : système, Python, accès réseau, accès à distance | Carte opérationnelle et procédure écrite | S2 |
| 1.4 | Brancher la caméra et les capteurs de mouvement, de porte et de luminosité | Script d'acquisition qui produit des mesures horodatées | S2 |
| 1.5 | Déclencher la capture d'images sur l'indice de départ, quelle que soit la caméra branchée | Images envoyées au prétraitement | S3 |
| 1.6 | Valider la liaison avec le téléphone (réseau local, Bluetooth si le matériel le permet) | Essai de liaison documenté | S3 |
| 1.7 | Mesurer processeur, mémoire et temps de traitement sur le Raspberry Pi pendant la démonstration | Tableau de mesures | S4 |
| 1.8 | Former les autres membres au matériel | Séance de prise en main | à la demande |

## Ce qu'on attend

- Le choix de la caméra se justifie par ses caractéristiques : résolution, champ de vision, branchement au Raspberry Pi, prix, disponibilité.
- Le Raspberry Pi démarre et lance l'acquisition en suivant la procédure écrite, sans réglage fait de mémoire.
- Chaque mesure porte son horodatage et sa source, exactement au format du contrat d'interface.
- Une porte ouverte ou un mouvement devant la caméra déclenche une capture, et ce déclenchement se montre en vidéo.
- Un membre d'une autre équipe sait brancher et lancer le banc avec la seule procédure.

## Livrables

- **Code** : `01-iot-materiel/code/` dans le dépôt.
- **Documents** : liste du matériel, fiche de choix de la caméra, procédure d'installation, tableau des mesures.
- **Rapport** : état de l'art (architectures IoT, caméras, Raspberry Pi, Edge AI), conception de l'architecture matérielle, réalisation du montage, mesures matérielles, annexe des fiches techniques et du coût.
- **Guide** : diapositives du matériel et de l'acquisition.
