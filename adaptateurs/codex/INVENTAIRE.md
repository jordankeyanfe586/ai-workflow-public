> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Inventaire de l’adaptateur Codex

Ce document inventorie uniquement les fichiers maintenus pour l’adaptateur Codex.

La documentation fonctionnelle se trouve dans `documentation/codex/`.

## Sources installables

| Source du dépôt | Installation |
|---|---|
| `fichiers-installation/.codex/AGENTS.md` | `~/.codex/AGENTS.md` |
| `fichiers-installation/.codex/hooks.json` | `~/.codex/hooks.json` |
| `fichiers-installation/.codex/hooks/notification.py` | `~/.codex/hooks/notification.py` |
| `fichiers-installation/.codex/rules/default.rules` | `~/.codex/rules/default.rules` |
| `fichiers-installation/.codex/bin/review-native-codex` | `~/.codex/bin/review-native-codex` |
| `fichiers-installation/.codex/skills/preparer-commit/SKILL.md` | `~/.codex/skills/preparer-commit/SKILL.md` |
| `fichiers-installation/.codex/skills/cloturer-branche/SKILL.md` | `~/.codex/skills/cloturer-branche/SKILL.md` |
| `fichiers-installation/.local/bin/review-native-codex` | `~/.local/bin/review-native-codex` |

Le dernier élément est un lien symbolique relatif vers :

    ../../.codex/bin/review-native-codex

## Sources communes

Ces fichiers restent directement dans le Workflow :

    AI_WORKFLOW.md
    outils/empreinte-git.py

La racine installée `~/.ai-workflow` pointe vers le dépôt `AI-Workflow`.

## config.toml

`~/.codex/config.toml` appartient à Codex/OpenAI et contient également de l’état local.

Il n’est jamais remplacé par une copie complète du dépôt.

Les choix appartenant au Workflow sont recensés dans :

    adaptateurs/codex/configuration-workflow.json

Cycle de maintenance :

    configuration-workflow.json
    → modification minimale de config.toml
    → validation TOML
    → vérification des valeurs effectives

## Source et installation

Pour les fichiers statiques :

    source du dépôt
    → candidat isolé si le risque le justifie
    → validation
    → promotion dans la source
    → installation
    → comparaison exacte
    → requalification ciblée

La copie sous `~/.codex` n’est pas la source de maintenance.

Une divergence entre source et installation signifie que la maintenance n’est pas terminée.

## Portabilité

### Portable directement

    .codex/AGENTS.md
    .codex/rules/default.rules
    .codex/skills/preparer-commit/SKILL.md
    .codex/skills/cloturer-branche/SKILL.md

### Dépendances d’installation

    .codex/hooks.json
    .local/bin/review-native-codex

### Dépendances macOS actuelles

    .codex/hooks/notification.py
    .codex/bin/review-native-codex

Le lanceur de Review résout une fois `codex` via le `PATH` utilisateur et vérifie
que le résultat est exécutable. Aucun chemin ChatGPT.app ou Homebrew n’est imposé.
Les utilitaires système conservent leurs chemins macOS qualifiés.

## Hors inventaire

Ne jamais copier comme source du Workflow :

    authentification
    secrets
    sessions
    caches
    mémoires internes
    état dynamique Codex
    plugins fournis par des tiers
    __pycache__
    .tmp

## Ancien système supprimé

Round 5 a supprimé de l’architecture active :

    wrapper ~/.local/bin/codex
    routage-codex.zsh
    reprendre-codex
    permission_request.py
    empreinte-environnement-codex.py
    environnement-codex.json
    référence persistante de hashes
    checkpoints Codex du Workflow

Git conserve leur historique.

Ils ne doivent pas être réintroduits sans problème réel et reproductible.
