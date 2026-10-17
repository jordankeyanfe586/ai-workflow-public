> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Inventaire de l’adaptateur Antigravity

Ce document inventorie uniquement les fichiers maintenus pour l’adaptateur Antigravity.

La documentation fonctionnelle se trouve dans `documentation/antigravity/`.

## Sources installables

| Source du dépôt | Installation |
|---|---|
| `fichiers-installation/.gemini/GEMINI.md` | `~/.gemini/GEMINI.md` |
| `fichiers-installation/.gemini/antigravity-cli/skills/preparer-commit/SKILL.md` | `~/.gemini/antigravity-cli/skills/preparer-commit/SKILL.md` |
| `fichiers-installation/.gemini/antigravity-cli/skills/cloturer-branche/SKILL.md` | `~/.gemini/antigravity-cli/skills/cloturer-branche/SKILL.md` |
| `fichiers-installation/.gemini/antigravity-cli/statusline.sh` | `~/.gemini/antigravity-cli/statusline.sh` |

## Politique maintenue

| Source du dépôt | Installation |
|---|---|
| `permissions.json` | fusion dans `~/.gemini/antigravity-cli/settings.json` → clé `permissions` |

## Sources communes

Ces fichiers restent directement dans le Workflow :

- `AI_WORKFLOW.md`
- `outils/empreinte-git.py`

La racine installée `~/.ai-workflow` pointe vers le dépôt `AI-Workflow`.

## Source et installation

Pour les fichiers statiques :

source du dépôt → validation → installation → comparaison exacte → requalification ciblée

La copie sous `~/.gemini` n’est pas la source de maintenance.

Une divergence entre source et installation signifie que la maintenance n’est pas terminée.

## Hors inventaire

Ne jamais copier comme source du Workflow :

- authentification
- secrets
- sessions
- caches
- brain
- transcripts
- scratch
- mémoire interne
- plugins tiers

## Principe d’architecture

L’adaptateur Antigravity reste minimal :

mécanismes natifs Antigravity → adaptation minimale → garde-fous ciblés → requalification par comportement réel
