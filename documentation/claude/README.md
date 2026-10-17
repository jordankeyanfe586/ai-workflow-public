> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Adaptateur Claude Code

> **Statut : 2.1.280 installé et qualifié sur le périmètre requalifié** (ExitPlanMode non requalifié ; notifications avancées partielles/reportées ; limites sandbox documentées). Claude Code est le Principal / orchestrateur naturel de l’écosystème actif Claude + Codex + Antigravity (`architecture/PORTABLE.md`).

## Navigation

| Besoin | Document |
|---|---|
| Fichiers maintenus et installation | [INVENTAIRE.md](../../adaptateurs/claude/INVENTAIRE.md) |
| Réglages `settings.json` du Workflow | [configuration-workflow.json](../../adaptateurs/claude/configuration-workflow.json) |
| Configuration installée | [CONFIGURATION.md](CONFIGURATION.md) |
| Fonctionnement et limites | [MECANISMES.md](MECANISMES.md) |
| Preuves et verdicts | [REQUALIFICATION.md](../../tests/claude/REQUALIFICATION.md) |

## Architecture

```text
AI_WORKFLOW.md ──@import──► ~/.claude/CLAUDE.md (adaptateur mince + préférences)
Claude principal · Opus 5.5 · effort medium · mode auto par défaut
 ├── Explore · Plan · general-purpose (nombre minimal suffisant, selon les axes indépendants, sans plafond fixe)
 ├── permissions.deny (destructions Git, secrets) · permissions.ask (barrières Git canoniques)
 ├── barriere-git.py (classes Git : STOP → ask ; push destructif, suppression forcée de branche → deny) · classifieur auto · sandbox
 ├── SessionStart → empreinte-git.py --initial · Notification · Status Line
 ├── ai-reviewer : Reviewer dédié en lecture seule, non systématique
 └── Claude auteur → Review finale externe : Antigravity ; Antigravity + Codex si risque élevé
```

Les règles universelles restent dans `AI_WORKFLOW.md`.
