> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Configuration Claude Code — 2.1.280

> **Statut : installé et qualifié sur le périmètre requalifié** (ExitPlanMode non requalifié ; notifications avancées partielles/reportées ; limites sandbox documentées ; preuves : [REQUALIFICATION.md](../../tests/claude/REQUALIFICATION.md)). Le journal complet de la configuration historique 2.1.227 (architecture `ai-agent` / `ai-reviewer`, hook `pre-tool-use.py`) est conservé dans Git (`4802a2b`, `documentation/claude/CONFIGURATION.md`).

## Installation observée

- Binaire : `~/.local/bin/claude` → `~/.local/share/claude/versions/2.1.280`.
- Abonnement Claude Pro, authentification OAuth ; aucune clé API.
- Racine du Workflow : `~/.ai-workflow` → dépôt `AI-Workflow`.

## Rôle

Claude Code est le Principal et l’orchestrateur naturel de l’écosystème actif (Claude, Codex, Antigravity ; politique de dispatch : `architecture/PORTABLE.md`) : travail transversal, planification, coordination et implémentation. `AFFINITÉ ≠ RÔLE OBLIGATOIRE` : il peut aussi reviewer le travail d’un autre fournisseur ou explorer.

## Réglages maintenus

Les valeurs appartiennent à [configuration-workflow.json](../../adaptateurs/claude/configuration-workflow.json) (`fragment_settings`). Résumé :

| Domaine | Valeur installée |
|---|---|
| Modèle / effort | `opus` (Opus 5.5), `effortLevel: medium` |
| Mode | `permissions.defaultMode: auto` (réglages utilisateur) |
| Contournement | `disableBypassPermissionsMode: disable` |
| Sandbox | `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands: false` |
| Barrières Git | politique par classes (MECANISMES.md) : `permissions.ask` (formes canoniques) + hook `barriere-git.py` (STOP → `ask`, push destructif et suppression forcée de branche → `deny`) ; `git pull` exclu du chemin autonome |
| DENY | Git destructif canonique ; lecture/édition des secrets connus (`ask` : 20 règles, `deny` : 58) |
| Contexte | `autoMemoryEnabled: false`, `includeGitInstructions: false`, `language: French` |
| Hooks | `PreToolUse` Bash → `barriere-git.py` ; `SessionStart` → `empreinte-git.py --initial` ; `Notification` |
| Status Line | `statusline-command.sh` |

Clés non gérées : thème, `modelSettings`, authentification, sessions, plugins, `~/.claude.json`.

## Sous-agents et modèles

Politique normative : [adaptateur, § Modèles, effort et escalade](../../adaptateurs/claude/fichiers-installation/.claude/CLAUDE.md). Résumé :

| Besoin | Agent | Modèle normal | Escalade automatique | Effort |
|---|---|---|---|---|
| Exploration | `Explore` (natif) | `sonnet` | `opus` | hérité |
| Implémentation bornée | `general-purpose` | `sonnet` | `opus` | hérité |
| Planification | `Plan` (natif) | `opus` | — | hérité ; `high` non automatisable |
| Review isolée | `ai-reviewer` | `opus` (frontmatter) | — | hérité ; `high` non automatisable |
| Rédacteurs parallèles | `isolation: "worktree"` | selon la mission | selon la politique | hérité |

Concurrence proportionnée à la tâche, sans plafond Workflow fixe : le Principal choisit le nombre minimal suffisant de sous-agents selon les axes réellement indépendants (0 sans gain réel ; davantage si la tâche le requiert), sans parallélisme artificiel. Aucun plafond natif n’a été observé (6 agents acceptés).

## Review

Claude conserve un Reviewer dédié, `ai-reviewer` ([source](../../adaptateurs/claude/fichiers-installation/.claude/agents/ai-reviewer.md)) : agent personnalisé en contexte neuf, outils `Read` et `Bash` uniquement (aucun `Edit`/`Write`), `model: opus`, jamais correcteur, aucune mutation Git, `ETAT` initial et final, verdict normalisé. Son usage n’est jamais systématique.

| Auteur | Rôle d’`ai-reviewer` | Review finale |
|---|---|---|
| Claude | Review isolée supplémentaire ou diagnostic interne | externe par relais humain : Antigravity ; Antigravity + Codex si risque élevé |
| Codex ou Antigravity | peut être désigné Reviewer indépendant externe | `ai-reviewer` si désigné |

Les pré-contrôles internes (`/code-review` sans `--fix`) ne valent jamais Review indépendante finale d’un travail écrit par Claude.

## Contexte

`~/.claude/CLAUDE.md` importe `AI_WORKFLOW.md` puis porte l’adaptateur et les préférences humaines (64 + 82 = 146 lignes permanentes ; heuristique ≤ 150). `PROJECT_CONTEXT.md` est lu une seule fois s’il existe ; aucun `CLAUDE.md` projet n’est requis. `modeles-projet/claude/CLAUDE.md` reste un modèle facultatif.

## Retraits effectués

`ai-agent`, `pre-tool-use.py`, `allow-workspace-read.py`, `config-change.py`, `session-start-git.sh` et leurs caches Python ont quitté l’installation (voir l’inventaire). L’`ai-reviewer` historique a été remplacé par sa version modernisée. Sont conservés sans nettoyage : `~/.claude/logs/config-changes.log`, les fichiers `*.backup*` et la sauvegarde `~/.claude/sauvegardes-workflow/2026-09-23-avant-claude-2.1.280/`.

Les mécanismes et limites sont expliqués dans [MECANISMES.md](MECANISMES.md) ; les preuves dans [REQUALIFICATION.md](../../tests/claude/REQUALIFICATION.md).
