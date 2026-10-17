---
name: cloturer-branche
description: Préparer ou poursuivre la clôture sûre d'une branche selon le Workflow.
---

# Clôturer une branche (Adaptateur Antigravity)

Applique `~/.ai-workflow/AI_WORKFLOW.md`, `~/.ai-workflow/architecture/REVIEW_ET_PREUVES.md` et `~/.ai-workflow/procedures/CLOTURER_BRANCHE.md`.

**But.** Préparer la clôture sûre d'une branche sous décision humaine explicite.

**Adaptation Antigravity :**
1. **État local :** Vérifier que le working tree est propre (`git status --short`) et que l'unité est commitée.
2. **Review d'unité :** Réutiliser la Review valide de l'unité sans rejeu superflu. Si aucune Review n'a eu lieu, en solliciter une uniquement si le risque réel de l'unité le justifie.
3. **Évolution de la branche cible :** Identifier la branche cible (ex. `main`, `develop`) et comparer via révisions relatives directes (`git log <cible>..HEAD --oneline` et `HEAD..<cible>`).
   - Cible inchangée ou évolution orthogonale : pas de nouvelle validation imposée.
   - Interaction potentielle : proposer la synchronisation et déterminer la validation d'intégration proportionnée.
4. **Mutations Git sous décision humaine :** Toute synchronisation (`rebase`/`merge`), tout changement de branche et toute suppression locale requièrent une décision humaine explicite préalable. `git branch -D` reste formellement interdit.
5. **Après synchronisation autorisée :** Recalculer l'`ETAT` (`python3 ~/.ai-workflow/outils/empreinte-git.py`), exécuter la preuve d'intégration nécessaire, et ne solliciter de Review ciblée que si un changement matériel, sémantique ou un risque concret apparaît.
6. **Post-merge sécurisé :** Après fusion autorisée (squash par défaut), basculer sur la branche cible sous décision humaine, vérifier l'état final et proposer la suppression douce avec `git branch -d`.
7. **Barrière Publication (`git push`, conditionnelle) :** Si et seulement si un push distant est expressément demandé ou nécessaire : présenter branche, révision et remote/destination → **STOP** → attendre la validation humaine explicite avant `git push` (une clôture locale ne nécessite aucun push).

**Retour.** `ETAT` ; validations d'intégration ; verdict de Review réutilisé ou produit ; proposition de clôture ; décision requise ; état final post-merge.
