> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Adaptateur Codex

L’adaptateur applique le Workflow universel avec les permissions natives Codex.
Une permission technique ne remplace aucune décision fonctionnelle.

| Information | Source principale |
|---|---|
| Règles universelles | [AI_WORKFLOW.md](../../AI_WORKFLOW.md) |
| Paramètres maintenus | [configuration-workflow.json](../../adaptateurs/codex/configuration-workflow.json) |
| Installation et capacités observées | [CONFIGURATION.md](CONFIGURATION.md) |
| Exécution, autorisations et limites | [MECANISMES.md](MECANISMES.md) |
| Résultats et preuves | [REQUALIFICATION.md](../../tests/codex/REQUALIFICATION.md) |
| Correspondance source / installation | [INVENTAIRE.md](../../adaptateurs/codex/INVENTAIRE.md) |

Charger seulement la source utile à l’étape courante. Le Workflow n’est pas
activé automatiquement dans une session générale.

## Maintenance

Modifier la source versionnée, valider le delta, synchroniser uniquement les
fichiers concernés, comparer source et installation, puis consigner les preuves.
Le manifeste n’est jamais une copie complète de `~/.codex/config.toml`.
Les anciens laboratoires restent conservés jusqu’à décision de nettoyage distincte.
