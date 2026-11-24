# Sous-équipe 3. Vision (VLM)

**Membres.** Bachirou Konate (référent), Yasser Nadi.

Missions, tâches, attentes et livrables : `docs/equipes/03 Vision (VLM).md`.

| Dossier | Contenu |
|---|---|
| `code/` | Essais et module de vision : Moondream2, LLaVA quantifié, détecteur léger |
| `documents/` | Les documents de la sous-équipe : fiches de choix, tableaux de mesures, notes techniques |
| `rapport/` | Ses sections du rapport LaTeX, un fichier `.tex` par section |
| `guide/` | Ses diapositives du guide PowerPoint |

## Point d'avancement

*Dernière mise à jour : 24 novembre 2026.*

- Une proposition de contrat JSON Vision -> backend est disponible dans [`docs/proposition-contrat-vision-backend.md`](../docs/proposition-contrat-vision-backend.md). C'est un brouillon à discuter avec le backend et à aligner sur le contrat commun de Data ; il n'est pas encore validé.
- Un premier prompt système est rédigé dans [`documents/prompt-systeme.md`](documents/prompt-systeme.md). Il décrit le contexte LIFEWISE et demande au VLM de retourner seulement les objets visibles (`keys`, `wallet`, `phone`) au format JSON. Son échelle de confiance reste à évaluer sur des exemples annotés.
- Le format exact des métadonnées d'entrée reste à convenir avec Data. Aucun candidat n'a encore été comparé sur le jeu de scénarios ni retenu.

**Prochaines étapes :** présenter la proposition au backend, confirmer avec Data le format d'entrée et le vocabulaire des catégories, récupérer les scénarios annotés, puis tester Moondream2, LLaVA quantifié et un détecteur léger sur les mêmes images.
