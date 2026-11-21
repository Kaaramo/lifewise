# Guide de coopération sur GitHub

Tout le code du projet vit dans un seul dépôt : https://github.com/Kaaramo/lifewise. Chacun travaille sur **sa
propre branche**, qui existe déjà ; personne n'écrit directement sur `main`. Le référent de ta sous-équipe relit
ton travail avant qu'il rejoigne `main`, et `main` contient toujours une version qui fonctionne.

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
git pull origin main
git add .
git commit -m "vision : premier test de Moondream2 sur les photos de départ"
git push
```

Commence toujours par `git pull origin main` : tu récupères ce que les autres ont validé avant d'écrire une
ligne. Le message de commit dit ce que tu as fait, précédé du nom du module.

## Faire valider ton travail

Sur la page du dépôt, **Pull requests → New pull request**, de ta branche vers `main`. Écris en deux lignes ce
qui change et comment le vérifier, puis désigne le référent de ta sous-équipe comme relecteur. Il fusionne quand
c'est bon, ou te répond en commentaire.

Le référent vérifie quatre choses avant de fusionner : le travail fonctionne, il est rangé dans le bon dossier, il
respecte le contrat d'interface, et il ne contient ni secret ni fichier lourd.

## Travailler à plusieurs

- Ta branche est à toi : on ne pousse jamais sur la branche d'un autre.
- Tu restes dans le dossier de ta sous-équipe. Pour modifier le fichier d'une autre équipe, ouvre une demande de fusion et désigne son référent comme relecteur.
- Un changement du format des données se propose dans `docs/contrat-interface.md`, par une demande de fusion relue par toutes les équipes concernées.
- Mieux vaut plusieurs petites demandes de fusion qu'une grosse à la fin : elles se relisent plus vite et créent moins de conflits.

## En cas de conflit

Un conflit arrive quand deux personnes ont modifié les mêmes lignes. Git l'annonce au moment du `git pull origin
main`, et marque l'endroit dans le fichier entre `<<<<<<<` et `>>>>>>>`. Ouvre le fichier, garde la bonne
version, retire les marques, puis :

```
git add chemin/du/fichier
git commit -m "fusion de main dans ma branche"
git push
```

Si tu ne sais pas quelle version garder, demande au référent avant de valider.

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

## Ce qu'on ne dépose jamais

- Un mot de passe, une clé d'API ou un fichier `.env`.
- Une photo où l'on reconnaît une personne : le dépôt est public.
- Les modèles téléchargés (fichiers `.gguf`, `.safetensors`, `.pt`) : ils sont trop lourds et se retéléchargent.
