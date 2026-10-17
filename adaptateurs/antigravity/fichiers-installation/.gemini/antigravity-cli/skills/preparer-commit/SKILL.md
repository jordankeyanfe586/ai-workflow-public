---
name: preparer-commit
description: "Préparer un commit sans le créer : périmètre, preuves, staging proposé et message."
---

# Préparer un commit (Adaptateur Antigravity)

Applique `~/.ai-workflow/AI_WORKFLOW.md`, `~/.ai-workflow/architecture/REVIEW_ET_PREUVES.md` et `~/.ai-workflow/procedures/PREPARER_COMMIT.md`.

**But.** Garde de cohérence préparant le commit d'une unité logique sans l'exécuter.

**Adaptation Antigravity :**
1. **État et périmètre :** Établir l'`ETAT` initial via `python3 ~/.ai-workflow/outils/empreinte-git.py` et `git status --short`. Isoler l'unité en distinguant les préexistants.
2. **Preuves existantes :** Réutiliser obligatoirement les preuves et la Review valides sur cet arbre sans réexécuter.
3. **Évaluation du delta :** Selon le risque réel et l'impact potentiel, déterminer si une preuve ciblée ou une Review minimale par sous-agent `research` est nécessaire.
4. **Minimalité d'exécution :** Privilégier les commandes directes (ex. `git diff --check`, `git diff`) sans composition shell évitable (`awk`, pipelines ou sous-shells superflus).
5. **Garde-fous :** Bloquer la préparation si un test échoue, si un finding bloquant subsiste ou si des secrets/caches sont présents.
6. **Barrières Git fonctionnelles :**
   - **Staging (`git add`) :** Présenter exactement les fichiers constitutifs de l'unité logique à stager → **STOP** → attendre la décision humaine explicite avant tout `git add`.
   - **Commit (`git commit`) :** Présenter l'unité stagée, les preuves rattachées et le message en français (trailers `AI-Agent:` et `AI-Reviewer:` réels) → **STOP** → attendre la décision humaine explicite avant tout `git commit`.

**Retour.** `ETAT` ; fichiers proposés ; preuves valides ; verdict de Review ; message proposé ; décision requise.
