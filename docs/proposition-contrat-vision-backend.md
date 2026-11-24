# Proposition de contrat JSON — Vision vers backend

**Statut :** proposition de la sous-équipe Vision, à valider avec le backend et l'équipe Data.  
**Périmètre :** résultat de l'analyse d'une image par le module Vision. Ce document ne remplace pas le contrat d'interface commun, qui doit être validé par les équipes concernées.

## Objectif

Transmettre au backend les objets reconnus dans une image, leur score de confiance et les identifiants permettant de rattacher le résultat à l'image et à l'événement correspondant.

Le résultat décrit uniquement ce que le modèle voit dans l'image. Une liste vide signifie qu'aucun objet de la liste de catégories attendues n'a été détecté dans cette image ; elle ne prouve pas que ces objets sont absents de la scène ou oubliés.

## Exemple de résultat réussi

```json
{
  "schema_version": "1.0",
  "event_id": "evt-001",
  "image": {
    "id": "img-001",
    "source": "phone_camera",
    "captured_at": "2026-11-24T06:40:00Z"
  },
  "vision": {
    "status": "success",
    "model": {
      "name": "moondream2",
      "version": "2",
      "quantization": null
    },
    "inference_ms": 842,
    "objects": [
      {
        "label": "keys",
        "confidence": 0.92
      },
      {
        "label": "wallet",
        "confidence": 0.87
      }
    ]
  }
}
```

Les valeurs sont illustratives. `source` indique l'origine de l'image, pas l'appareil qui exécute le modèle. La photo elle-même n'est pas incluse dans ce résultat JSON : elle est traitée localement et associée au résultat par son identifiant.

## Exemple réussi sans objet reconnu

```json
{
  "schema_version": "1.0",
  "event_id": "evt-002",
  "image": {
    "id": "img-002",
    "source": "raspberry_pi",
    "captured_at": "2026-11-24T06:42:00Z"
  },
  "vision": {
    "status": "success",
    "model": {
      "name": "moondream2",
      "version": "2",
      "quantization": null
    },
    "inference_ms": 791,
    "objects": []
  }
}
```

`status: "success"` avec `objects: []` signifie que l'analyse a été effectuée correctement, mais qu'aucun objet des catégories recherchées n'a été reconnu dans cette image. Le backend ne doit pas interpréter ce résultat seul comme la preuve d'un oubli.

## Exemple d'échec d'analyse

```json
{
  "schema_version": "1.0",
  "event_id": "evt-003",
  "image": {
    "id": "img-003",
    "source": "raspberry_pi",
    "captured_at": "2026-11-24T06:44:00Z"
  },
  "vision": {
    "status": "error",
    "model": {
      "name": "moondream2",
      "version": "2",
      "quantization": null
    },
    "error": {
      "code": "inference_failed",
      "message": "L'analyse de l'image n'a pas abouti."
    }
  }
}
```

En cas d'erreur, `objects` est omis : un échec ne doit jamais être représenté par une liste vide, qui ressemblerait à une analyse réussie sans détection. Le backend peut journaliser l'erreur ou appliquer sa politique de reprise, mais ne doit pas traiter cet événement comme une absence d'objets.

## Définition des champs

| Champ | Type | Règle proposée |
|---|---|---|
| `schema_version` | chaîne | Version du format de ce message. |
| `event_id` | chaîne | Identifiant stable de l'événement, fourni par la chaîne commune, pour rattacher le résultat au contexte. |
| `image.id` | chaîne | Identifiant stable de l'image analysée, fourni par le prétraitement. |
| `image.source` | chaîne | Origine de l'image, selon le vocabulaire commun à définir avec Data (par exemple `phone_camera`, `webcam`, `raspberry_pi`). |
| `image.captured_at` | chaîne date-heure | Date de capture au format RFC 3339, avec fuseau explicite, de préférence UTC (`Z`). |
| `vision.status` | chaîne | `success` ou `error`. |
| `vision.model.name` | chaîne | Nom de la famille ou du détecteur utilisé. |
| `vision.model.version` | chaîne | Version exacte du modèle ou du checkpoint, à renseigner pour rendre les résultats reproductibles. |
| `vision.model.quantization` | chaîne ou `null` | Méthode de quantification, si applicable ; `null` si le modèle n'est pas quantifié. |
| `vision.inference_ms` | entier positif | Durée de traitement de l'image en millisecondes ; champ de mesure proposé, à confirmer avec le backend. |
| `vision.objects` | tableau | Obligatoire si `status` vaut `success`, y compris quand il est vide ; absent si `status` vaut `error`. |
| `vision.objects[].label` | chaîne | Identifiant canonique d'une catégorie reconnue, choisi dans un vocabulaire commun, à définir avec Data. Exemples : `keys`, `wallet`, `phone`. |
| `vision.objects[].confidence` | nombre entre 0 et 1 | Score retourné par le modèle pour cette catégorie. C'est un score de confiance, pas nécessairement une probabilité calibrée. |
| `vision.error.code` | chaîne | Code stable d'erreur, présent uniquement si `status` vaut `error` ; valeurs à convenir avec le backend. |
| `vision.error.message` | chaîne | Message bref destiné aux journaux de diagnostic ; ne pas y inclure de chemin local, de donnée personnelle ni de trace technique détaillée. |

## Règles d'interprétation proposées

- Une entrée `objects` représente une catégorie distincte reconnue dans l'image ; chaque `label` apparaît au plus une fois. Si plusieurs instances de cette catégorie sont visibles, la valeur `confidence` est le score le plus élevé retenu pour cette catégorie. Le comptage d'instances et les boîtes englobantes ne sont pas inclus dans cette première version.
- Les labels doivent être normalisés vers le vocabulaire commun plutôt que transmis sous forme de phrases libres générées par un VLM.
- Le seuil de confiance servant à inclure un objet est fixé et documenté lors de l'évaluation. Les scores de modèles différents ne sont pas directement comparables sans calibration.
- La sortie ne contient ni affirmation d'absence dans la scène, ni conclusion telle que « l'utilisateur a oublié ses clés ». Ces décisions appartiennent au backend et doivent tenir compte des autres informations du contexte.
- Le résultat est lié à une seule image. Si un événement comporte plusieurs images, chacune possède son propre `image.id` et son propre résultat ; la fusion des résultats relève du backend.

## Points à valider avec Data et le backend

- Les noms définitifs des champs et leur cohérence avec le contrat d'interface commun.
- La source de `event_id`, de `image.id`, de `image.source` et de `image.captured_at`, et la façon de corréler plusieurs images d'un même événement.
- Le vocabulaire canonique des catégories (`keys`, `wallet`, `phone`, etc.) et la langue des identifiants.
- La nécessité de retourner `model` et `inference_ms` dans les événements de production ou de réserver ces informations aux mesures et journaux.
- Les codes d'erreur, les reprises éventuelles et le comportement de la chaîne lorsqu'une image ne peut pas être traitée.
- La nécessité future d'ajouter un nombre d'instances ou des boîtes englobantes ; ces champs sont volontairement exclus du périmètre initial.
