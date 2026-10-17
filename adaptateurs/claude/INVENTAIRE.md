> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Inventaire de l’adaptateur Claude Code

> **Statut : 2.1.280 — installé et qualifié sur le périmètre requalifié** (ExitPlanMode non requalifié ; notifications avancées partielles/reportées ; limites sandbox documentées ; preuves : `tests/claude/REQUALIFICATION.md`).

Ce document inventorie uniquement les fichiers maintenus pour l’adaptateur Claude Code.
La documentation fonctionnelle se trouve dans `documentation/claude/`.

## Sources installables

| Source du dépôt | Installation |
|---|---|
| `fichiers-installation/.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| `fichiers-installation/.claude/agents/ai-reviewer.md` | `~/.claude/agents/ai-reviewer.md` (remplace la version historique) |
| `fichiers-installation/.claude/hooks/barriere-git.py` | `~/.claude/hooks/barriere-git.py` |
| `fichiers-installation/.claude/hooks/notification.py` | `~/.claude/hooks/notification.py` |
| `fichiers-installation/.claude/skills/preparer-commit/SKILL.md` | `~/.claude/skills/preparer-commit/SKILL.md` |
| `fichiers-installation/.claude/skills/cloturer-branche/SKILL.md` | `~/.claude/skills/cloturer-branche/SKILL.md` |
| `fichiers-installation/.claude/statusline-command.sh` | `~/.claude/statusline-command.sh` |

`CLAUDE.md` contient l’adaptateur et les préférences humaines : c’est une source statique entièrement maintenue ici, installée par copie (pas d’import direct du dépôt, pour qu’une branche de travail ne modifie jamais l’adaptateur actif).

## settings.json

`~/.claude/settings.json` appartient conjointement à Claude Code et au Workflow (thème, `modelSettings`, état local).

Il n’est jamais remplacé par une copie complète du dépôt. Les clés appartenant au Workflow sont recensées dans :

    adaptateurs/claude/configuration-workflow.json → fragment_settings

Cycle de maintenance :

    fragment_settings
    → fusion minimale des seules clés listées
    → validation JSON
    → nouvelle session : vérification des valeurs effectives

## Sources communes

    AI_WORKFLOW.md
    outils/empreinte-git.py

La racine installée `~/.ai-workflow` pointe vers le dépôt `AI-Workflow`.

## Retraits effectués à l’installation

| Élément installé | Raison |
|---|---|
| `~/.claude/hooks/pre-tool-use.py` | analyseur de shell général remplacé par `permissions.ask/deny`, mode `auto`, sandbox et `barriere-git.py` |
| `~/.claude/hooks/allow-workspace-read.py` | lecture native autonome en mode `auto` |
| `~/.claude/hooks/config-change.py` | a réellement produit `~/.claude/logs/config-changes.log` (journal conservé) ; retiré car le risque est couvert par la protection native d’auto-modification et le sandbox |
| `~/.claude/hooks/session-start-git.sh` | remplacé par `empreinte-git.py --initial` |
| `~/.claude/agents/ai-agent.md` | routage systématique remplacé par les sous-agents natifs (`Explore`, `Plan`, `general-purpose`) |

Les caches Python correspondants ont également été retirés. `ai-reviewer` n’est pas retiré : il est remplacé par sa version modernisée (Reviewer dédié en lecture seule, non systématique).

Conservés sans nettoyage : `~/.claude/logs/config-changes.log`, fichiers `*.backup*`, sauvegarde `~/.claude/sauvegardes-workflow/2026-09-23-avant-claude-2.1.280/` (au moins jusqu’au commit final et à la stabilisation de l’intégration).

## Hors inventaire

Ne jamais copier comme source du Workflow :

    authentification et secrets
    ~/.claude.json
    sessions, projects, history, file-history, paste-cache, shell-snapshots
    caches, stats, jobs, daemon, state
    plugins et marketplaces
    fichiers *.backup* (conservés, aucun nettoyage décidé)
    __pycache__, .DS_Store

## Principe d’architecture

    mécanismes natifs Claude Code (mode auto, permissions, sandbox, sous-agents, Skills)
    → adaptation minimale
    → garde-fou ciblé uniquement là où une preuve montre une lacune (barrière Git)
    → requalification par comportement réel
