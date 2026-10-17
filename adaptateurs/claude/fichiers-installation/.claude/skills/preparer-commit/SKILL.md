---
name: preparer-commit
description: "Préparer un commit sans le créer : périmètre, preuves, staging proposé et message."
---

# Préparer un commit

Projette les procédures universelles. Ne les redéfinis pas.

Références portables, indépendantes du CWD :

- `~/.ai-workflow/procedures/PREPARER_COMMIT.md`
- `~/.ai-workflow/architecture/REVIEW_ET_PREUVES.md`

**But.** Prépare le commit sans l'exécuter. Ce Skill ne vaut jamais autorisation de staging ni de commit.

Séquence :

1. **ETAT** — `python3 ~/.ai-workflow/outils/empreinte-git.py`
2. **Périmètre atomique** — uniquement l'unité courante ; préserver et exclure l'existant
3. **Preuves réutilisables** — ne pas rejouer une preuve encore valide sur l'`ETAT`
4. **Review** — Claude auteur : verdict externe requis selon le risque (Antigravity ; Antigravity + Codex si risque élevé) ; un pré-contrôle interne n'en tient pas lieu
5. **Barrière Staging** — présenter exactement les fichiers → **STOP** → validation humaine explicite → seulement ensuite `git add <fichiers>` canonique
6. **Barrière Commit** — présenter l'unité stagée, l'`ETAT`/preuves, le verdict de Review et le message français avec trailers réels (`AI-Agent:`, `AI-Reviewer:`) → **STOP** ; aucun commit dans ce Skill

**Retour.** `ETAT` ; fichiers proposés au staging ; validations ; verdict de Review ; problème ouvert ; message/trailers ; décision requise.
