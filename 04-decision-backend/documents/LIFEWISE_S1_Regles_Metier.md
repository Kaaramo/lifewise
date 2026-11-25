# LIFEWISE — Moteur de Décision : Règles Métier (Semaine 1)

> **Équipe :** Partie 4 — Sous-équipe IA / Décision  
> **Sprint :** Semaine 1 (S1)  
> **Mission :** Mission 1 — Développer le moteur de décision

---

## 1. Contexte et Objectif

LIFEWISE est un assistant intelligent conçu pour aider l'utilisateur à ne pas oublier ses objets personnels (portefeuille, clés, téléphone, etc.) au moment de quitter son domicile.

Le moteur de décision est le **cerveau** du système. Il reçoit des informations provenant de la caméra (objets détectés ou non) ainsi que du calendrier de l'utilisateur, puis décide si une alerte doit être générée, et de quel type.

> [!IMPORTANT]
> **Principe fondamental :** La caméra ne peut que constater l'**absence visuelle** d'un objet dans son champ de vision. Elle ne peut **pas affirmer** qu'un objet est réellement oublié. Par conséquent, toutes les alertes générées sont des **vérifications suggérées**, jamais des certitudes.

---

## 2. Entrées du Moteur de Décision

| Entrée | Type | Description |
|---|---|---|
| `departure_detected` | `bool` | `True` si l'utilisateur a été détecté en train de partir |
| `objects_in_frame` | `list[str]` | Liste des objets visibles dans le champ de la caméra |
| `expected_objects` | `list[str]` | Liste des objets que l'utilisateur doit normalement emporter |
| `calendar_events` | `list[Event]` | Événements du calendrier pour la journée (heure, type, importance) |
| `current_time` | `datetime` | Heure actuelle |

---

## 3. Règles Métier

### Règle 0 — Aucun départ détecté

```
SI departure_detected == False
ALORS  → aucune action, système en veille
```

> [!NOTE]
> Le système ne surveille activement que si un départ est détecté. En veille, il économise les ressources et ne génère aucune notification.

---

### Règle 1 — Départ détecté, tous les objets visibles

```
SI departure_detected == True
ET  tous les objets de expected_objects sont dans objects_in_frame
ALORS  → Alerte de type : AUCUNE (tout semble en ordre)
        → Message optionnel : « Bonne journée ! »
```

---

### Règle 2 — Départ détecté, objet non visible dans le champ de la caméra

```
SI departure_detected == True
ET  un objet de expected_objects N'EST PAS dans objects_in_frame
ALORS  → Alerte de type : VÉRIFICATION SUGGÉRÉE
        → Message : « Pensez à vérifier votre [objet]. »
```

> [!WARNING]
> On ne dit jamais « Vous avez oublié votre [objet] ». On dit toujours « Pensez à vérifier votre [objet] ». L'objet peut être dans la poche, le sac, ou hors champ de caméra.

---

### Règle 3 — Départ détecté, rendez-vous important imminent

```
SI departure_detected == True
ET  il existe un événement dans calendar_events
    dont l'heure est dans les 60 prochaines minutes
    ET dont l'importance == "haute"
ALORS  → Alerte de type : ALERTE CONTEXTUELLE
        → Message : « Vous avez [événement] dans [X] minutes. 
                      Pensez à emporter ce qu'il faut. »
        → Si des objets sont absents du champ : combiner avec Règle 2
```

---

### Règle 4 — Départ détecté, téléphone visible mais autres objets absents

```
SI departure_detected == True
ET  "téléphone" ∈ objects_in_frame
ET  d'autres objets de expected_objects sont ABSENTS du champ
ALORS  → Le téléphone est visible : l'utilisateur est probablement encore là
        → Alerte de type : VÉRIFICATION DOUCE
        → Message : « Avant de partir, pensez à vérifier : [liste des objets absents]. »
```

> [!TIP]
> Si le téléphone est visible dans le champ de la caméra juste avant un départ, cela signifie souvent que l'utilisateur est encore en train de se préparer. L'alerte peut être plus légère.

---

### Règle 5 — Départ détecté, aucun objet visible du tout

```
SI departure_detected == True
ET  objects_in_frame == []  (liste vide)
ALORS  → La caméra ne voit aucun objet : situation ambiguë
        → Alerte de type : VÉRIFICATION GÉNÉRALE
        → Message : « Pensez à vérifier vos affaires avant de partir. »
```

---

## 4. Tableau de Synthèse des Règles

| # | Départ détecté | Objets visibles | Calendrier | Décision | Type d'alerte |
|---|---|---|---|---|---|
| 0 | ❌ Non | — | — | Aucune action | — |
| 1 | ✅ Oui | Tous présents | — | Rien à signaler | AUCUNE |
| 2 | ✅ Oui | Objets manquants | — | Vérification suggérée | `VERIFICATION` |
| 3 | ✅ Oui | Objets manquants | RDV important ≤ 60 min | Alerte contextuelle | `CONTEXTUELLE` |
| 4 | ✅ Oui | Téléphone visible + manques | — | Vérification douce | `DOUCE` |
| 5 | ✅ Oui | Aucun objet visible | — | Vérification générale | `GENERALE` |

---

## 5. Priorité des Règles

En cas de combinaison de conditions, la priorité est :

```
CONTEXTUELLE > VERIFICATION > GENERALE > DOUCE > AUCUNE
```

---

## 6. Distinctions Importantes

| Situation | Interprétation correcte | Message à afficher |
|---|---|---|
| Portefeuille non visible | Peut être dans la poche/sac | « Pensez à vérifier votre portefeuille. » |
| Clés non visibles | Peuvent être déjà prises | « Pensez à vérifier vos clés. » |
| Téléphone visible au moment du départ | Utilisateur peut encore être là | Alerte légère / douce |
| Aucun objet visible | Champ vide, situation ambiguë | Vérification générale |

---

*Document rédigé dans le cadre du projet LIFEWISE — Partie 4, Mission 1, Sprint S1.*
