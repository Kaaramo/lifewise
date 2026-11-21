# Travailler sur le dépôt LIFEWISE

Tout le code du projet vit dans ce dépôt : https://github.com/Kaaramo/lifewise. Chacun travaille sur **sa
propre branche**, qui existe déjà ; personne n'écrit directement sur `main`. Le référent de ta sous-équipe relit
ton travail avant qu'il rejoigne `main`.

## Une seule fois

1. Créer un compte sur https://github.com si tu n'en as pas, et envoyer ton identifiant GitHub à Karamo, qui
   t'ajoute au dépôt. Accepter l'invitation reçue par e-mail.
2. Installer Git : https://git-scm.com/downloads.
3. Dans un terminal, te présenter à Git avec ton vrai nom :

```
git config --global user.name "Prénom Nom"
git config --global user.email "ton-email@etu.uae.ac.ma"
```

4. Récupérer le dépôt et te placer sur ta branche :

```
git clone https://github.com/Kaaramo/lifewise.git
cd lifewise
git checkout prenom-nom
```

## Les branches

| Sous-équipe | Branches | Référent (relecteur) |
|---|---|---|
| 1. IoT et matériel | `adila-yassir`, `mohamed-abrini`, `mohamed-channa` | Adila |
| 2. Data | `michel-sagesse-kolie`, `zakaria-tahiri`, `amine-sbah` | Michel |
| 3. Vision (VLM) | `bachirou-konate`, `yasser-nadi` | Bachirou |
| 4. Décision et backend | `adnane-qassiri`, `aymane-azaagag` | Adnane |
| 5. Application web | `said-jadli`, `aymane-hayoun` | Saïd |
| 6. Application mobile et coordination | `karamo-sylla` | Karamo |

Le travail d'un référent est relu par Karamo.

## À chaque séance de travail

```
git checkout prenom-nom
git pull origin main          # récupérer ce que les autres ont validé
# ... travailler dans le dossier de ta sous-équipe ...
git add .
git commit -m "vision : premier test de Moondream2 sur les photos de départ"
git push
```

Le message de commit dit ce que tu as fait, précédé du nom du module.

## Faire valider ton travail

Sur la page du dépôt, **Pull requests → New pull request**, de ta branche vers `main`. Écris en deux lignes ce
qui change et comment le vérifier, puis désigne le référent de ta sous-équipe comme relecteur. Il fusionne quand
c'est bon, ou te répond en commentaire.

## Où ranger ton travail

Chaque sous-équipe a son dossier : `01-iot-materiel/`, `02-data/`, `03-vision/`, `04-decision-backend/`,
`05-application-web/`, `06-application-mobile/`. Dedans, les mêmes sous-dossiers :

| Sous-dossier | Ce qu'on y range |
|---|---|
| `code/` | Le code de la sous-équipe |
| `documents/` | Fiches de choix, tableaux de mesures, notes techniques |
| `rapport/` | Tes sections du rapport LaTeX, un fichier `.tex` par section |
| `guide/` | Tes diapositives du guide PowerPoint |

La Data a en plus `02-data/donnees/` pour le jeu de scénarios. À la racine, `docs/` contient ce qui vaut pour
tous (ce guide, les missions, le contrat d'interface) et `rapport/` le rapport assemblé par la coordination.

On ne touche pas au dossier d'une autre sous-équipe sans passer par son référent. Un changement du format des
données se propose dans `docs/contrat-interface.md`, par une demande de fusion relue par les équipes concernées.

On ne dépose jamais de mot de passe, de clé d'API ni de photo où l'on reconnaît une personne.
