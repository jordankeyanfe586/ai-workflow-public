# Modèle de Rule Claude Code

Une Rule contient uniquement des instructions persistantes et spécifiques à un contexte donné.

Ne pas y recopier les règles déjà présentes dans `AI_WORKFLOW.md`, les `CLAUDE.md` ou les Skills.

## 1. Rule valable dans tout le projet

Fichier :

`.claude/rules/[theme].md`

Modèle :

```md
# [Thème]

- [instruction précise]
- [instruction précise]
- [instruction précise]
```

Utiliser cette forme uniquement lorsque les instructions doivent s'appliquer dans l'ensemble du repository.

## 2. Rule conditionnelle

Fichier :

`.claude/rules/[theme].md`

Modèle :

```md
---
paths:
  - "[pattern]"
---

# [Thème]

- [instruction précise]
- [instruction précise]
- [instruction précise]
```

Utiliser `paths:` lorsque les instructions ne concernent que certains fichiers ou répertoires.

## Convention de nommage

- minuscules ;
- kebab-case ;
- nom descriptif du domaine.

Exemples :

- `java.md`
- `tests.md`
- `api-security.md`
- `error-handling.md`

## Choix du mécanisme

- règle universelle du Workflow → `AI_WORKFLOW.md`
- contexte permanent du projet → `CLAUDE.md`
- instruction spécialisée persistante → Rule
- procédure ponctuelle ou multiétapes → Skill
- garantie déterministe → Hook
