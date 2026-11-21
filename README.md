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

| Dossier | Contenu | Sous-équipe |
|---|---|---|
| `acquisition/` | Raspberry Pi, caméra, capteurs | 1. IoT et matériel |
| `pretraitement/` | Horodatage, filtrage, objet « contexte » | 2. Data |
| `donnees/` | Scénarios annotés, schéma SQLite | 2. Data |
| `vision/` | Modèles vision-langage et détection | 3. Vision (VLM) |
| `decision/` | Règles et petit modèle de langage | 4. Décision et backend |
| `backend/` | Service qui enchaîne les modules, API | 4. Décision et backend |
| `dashboard/` | Tableau de bord web | 5. Application web |
| `application/` | Application mobile | 6. Application mobile et coordination |
| `docs/` | Guide, contrat d'interface, missions | Tous |
| `rapport/` | Rapport LaTeX, une section par fichier | Tous |
