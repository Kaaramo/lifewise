# LIFEWISE

Assistant personnel contextuel qui associe IoT, vision par ordinateur et Edge AI. Projet du module Computer
Vision (BDAI3), encadré par le Pr. Otman Aghzout.

Le prototype vise le scénario pilote, l'assistance à la sortie du domicile : au moment où l'utilisateur part,
LIFEWISE repère les objets habituels (téléphone, clés, portefeuille) et, s'il en manque un dans le champ de la
caméra, l'invite à vérifier.

```
Capteurs → Prétraitement → Analyse VLM → Fusion contextuelle → Décision SLM → Notification mobile → Historique local
```

## Pour commencer

Lis `docs/GUIDE-BRANCHES.md` : il explique comment récupérer le dépôt, travailler sur ta branche et faire
valider ton travail. Les missions de chaque sous-équipe sont dans `docs/equipes/`.

## Organisation du dépôt

Un dossier par sous-équipe, et dans chacun les mêmes sous-dossiers : `code/`, `documents/`, `rapport/` (ses
sections du rapport), `guide/` (ses diapositives).

| Dossier | Sous-équipe |
|---|---|
| `01-iot-materiel/` | 1. IoT et matériel |
| `02-data/` | 2. Data (avec `donnees/` pour le jeu de scénarios) |
| `03-vision/` | 3. Vision (VLM) |
| `04-decision-backend/` | 4. Décision et backend |
| `05-application-web/` | 5. Application web |
| `06-application-mobile/` | 6. Application mobile et coordination |
| `docs/` | Tous : guide des branches, missions, contrat d'interface |
| `rapport/` | Le rapport assemblé par la coordination |
