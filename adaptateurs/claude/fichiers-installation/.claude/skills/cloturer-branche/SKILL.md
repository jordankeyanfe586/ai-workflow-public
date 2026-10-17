---
name: cloturer-branche
description: "Préparer la clôture sûre d'une branche sous décision humaine explicite."
---

# Clôturer une branche

Projette les procédures universelles. Ne les redéfinis pas.

Références portables, indépendantes du CWD :

- `~/.ai-workflow/procedures/CLOTURER_BRANCHE.md`
- `~/.ai-workflow/architecture/REVIEW_ET_PREUVES.md`

**But.** Orchestre la clôture selon les preuves encore valides, les décisions nécessaires, l'intégration autorisée et la vérification finale. Ce Skill ne vaut jamais autorisation de merge, rebase, push ou suppression de branche.

Séquence :

1. Constater l'état local et l'`ETAT` (`python3 ~/.ai-workflow/outils/empreinte-git.py`)
2. Identifier la **branche cible** du dépôt (`main`, `master`, `develop` ou équivalent)
3. **Review d'unité** ≠ **validation d'intégration** — deux garanties distinctes ; Review finale `PRÊTE AU MERGE` requise
4. Réutiliser les preuves encore valides ; une divergence Git n'invalide pas automatiquement les preuves
5. Mutations de clôture (`merge`, `rebase`, bascule vers la branche cible, `branch -d`) : présenter → **STOP** → validation humaine explicite → une commande canonique à la fois. `git branch -D` est interdit
6. **Barrière Publication (`git push`, conditionnelle)** — seulement si demandé ou nécessaire : présenter branche, révision et remote → **STOP** → validation humaine avant `git push`
7. Après intégration et bascule autorisée : vérifier l'état final sur la branche cible et recalculer l'`ETAT`

**Retour.** `ETAT` ; validations ; verdict de Review ; décision requise ; état final.
