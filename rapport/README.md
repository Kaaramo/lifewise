# rapport/

Le rapport LIFEWISE, sur le modèle LaTeX du professeur. La mise en forme du modèle est respectée à 100 % : le
fichier principal `LIFEWISE_Rapport.tex` est celui du professeur, seul le chemin de la page de garde change. Seul
le contenu est propre au projet.

## Compiler

Avec **XeLaTeX** (pas pdfLaTeX), trois passes pour la table des matières. Dans TeXmaker : Options, Configurer
TeXmaker, Compilation rapide : XeLaTeX. La police XCharter doit être installée (`miktex packages install xcharter`
puis `fc-cache -f`). En ligne de commande, depuis ce dossier :

```
xelatex LIFEWISE_Rapport.tex
xelatex LIFEWISE_Rapport.tex
xelatex LIFEWISE_Rapport.tex
```

## Où écrire

| Partie | Fichier |
|---|---|
| Pages préliminaires, introduction, chapitre 1, conclusion, perspectives, annexe | `main chapters/` (coordination) |
| Sections de chaque sous-équipe, chapitres 2 à 5 | `../0N-.../rapport/chapitre-N.tex` |
| Webographie | `References.tex` (chaque sous-équipe y ajoute ses références) |
| Résumé en arabe | `Resume_Arabe.tex` |
| Page de garde | `Figures/Cover/source/page_de_garde.html`, imprimée en `Figures/Cover/LIFEWISE_Page_de_garde.pdf` |

Chaque section encore vide porte un encadré « À rédiger par la sous-équipe N » qui dit ce qu'elle doit contenir.
On retire l'encadré (`\aRediger{...}{...}`) une fois la section écrite. Les figures d'une sous-équipe vont dans
`../0N-.../rapport/` ou dans `Figures/`, et s'appellent par leur chemin depuis ce dossier.

On ne modifie ni `LIFEWISE_Rapport.tex`, ni les formats de titres, d'en-têtes et de pieds de page des fichiers de
chapitre : c'est la mise en forme du professeur.
