# Documents Data : contrat JSON

Le contrat commun est dans [docs/contrat-interface.md](../../docs/contrat-interface.md), à l'emplacement attendu par les six équipes. Ses fichiers de validation et ses exemples sont regroupés ici.

| Fichier | Utilité |
| --- | --- |
| [Contrat d'interface](../../docs/contrat-interface.md) | Les sept échanges, les champs, les types, les règles et les exemples commentés. |
| [Schéma JSON](schemas/contrat-interface.schema.json) | Validation d'un message au format JSON Schema 2020-12. |
| [Chaîne d'exemples](exemples/chaine-complete.json) | Neuf messages couvrant les sept types, du capteur à la réponse utilisateur. |

**Version 0.1.0 : proposition à faire valider par les six référents.** Les chemins d'image et les identifiants des exemples sont fictifs ; ce dossier ne contient pas les images ni l'implémentation des modules.

## Vérifier les exemples

Depuis la racine du dépôt, avec Python et le paquet `jsonschema` :

```sh
python -m pip install "jsonschema[format]"
python -c "import json; from pathlib import Path; from jsonschema import Draft202012Validator, FormatChecker; p = Path('02-data/documents'); s = json.loads((p / 'schemas/contrat-interface.schema.json').read_text(encoding='utf-8')); Draft202012Validator.check_schema(s); v = Draft202012Validator(s, format_checker=FormatChecker()); messages = json.loads((p / 'exemples/chaine-complete.json').read_text(encoding='utf-8')); [v.validate(m) for m in messages]; print(str(len(messages)) + ' messages valides')"
```

Résultat attendu : `9 messages valides`. Une erreur de schéma ou de message provoque un échec de la commande. La validation des formats de date est activée.

Le schéma contrôle les messages séparément. Les modules doivent aussi vérifier les références entre messages, la cohérence des sources, la fraîcheur des mesures et l'unicité des identifiants, comme précisé dans le contrat.

Toute évolution du format doit modifier ensemble le contrat, le schéma et les exemples dans une pull request relue par les équipes concernées, selon le [guide du dépôt](../../docs/GUIDE-BRANCHES.md).
