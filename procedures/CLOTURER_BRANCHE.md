# Procédure universelle : Clôturer une branche

Ce document décrit la procédure universelle pour préparer et orchestrer la clôture sûre d'une branche logique sous décision humaine explicite. Il définit les besoins d'intégration et les décisions requises, indépendamment des outils spécifiques.

---

## 1. Principes directeurs

- **Séparation Review d'unité vs Validation d'intégration :** La Review d'unité (jugement qualitatif indépendant sur la conception et la conformité de l'unité logique) et la validation d'intégration (attestation matérielle déterministe que l'assemblage avec la branche cible fonctionne) sont deux garanties distinctes et complémentaires.
- **Minimalité pour toute opération autonome :** Pour toute inspection ou analyse (vérification d'état, comparaison de révisions, détection d'interaction), privilégier le mécanisme direct le plus simple sans composition shell complexe dès lors qu'un mécanisme élémentaire suffit.
- **Mutations sous contrôle atomique :** Toute mutation de l'arbre ou des références Git (`rebase`, `merge`, changement de branche, suppression locale) relève impérativement d'une autorisation humaine explicite préalable. Aucune étape post-merge n'est réputée autorisée d'office. La suppression forcée non sécurisée (`git branch -D`) est formellement interdite.

---

## 2. Séquence universelle

1. **Constater l'état local :**
   Vérifier que l'arbre de travail est propre et que tous les commits constitutifs de l'unité logique ont été posés.
2. **Identifier la branche cible :**
   Déterminer la branche de destination du dépôt (ex. `main`, `master`, `develop` ou branche de version).
3. **Vérifier la Review d'unité :**
   Rechercher la Review existante de l'unité. Réutiliser le verdict acquis sans réévaluation superflue. Si aucune Review n'a été menée, évaluer le risque réel de l'unité : une Review indépendante n'est déclenchée que si ce risque concret la justifie (un changement purement documentaire ou trivial n'impose pas de Review indépendante).
4. **Évaluer l'évolution de la branche cible :**
   Analyser le delta de la branche cible depuis le point de divergence :
   - *Cible inchangée ou évolution orthogonale sans interaction :* la Review d'unité suffit, aucune validation d'intégration supplémentaire n'est imposée par défaut.
   - *Interaction potentielle ou concrète constatée :* proposer la synchronisation préalable et déterminer la validation d'intégration proportionnée au risque.
5. **Synchronisation autorisée :**
   Toute opération de synchronisation (`rebase` ou `merge` d'intégration) requiert une autorisation humaine explicite. Après exécution :
   - Recalculer l'état matériel ;
   - Réutiliser les preuves unitaires encore valides ;
   - Exécuter la preuve d'intégration nécessaire (build et tests combinés) ;
   - Ne solliciter de Review ciblée que si un changement matériel, une modification sémantique ou un nouveau risque concret le nécessite.
6. **Proposition de merge :**
   Présenter le bilan complet de clôture (preuves réutilisées, intégration validée, stratégie de fusion par défaut en squash ou fast-forward si historique cohérent) et attendre l'autorisation humaine explicite pour exécuter la fusion.
7. **Finalisation post-merge sécurisée :**
   Après la fusion autorisée :
   - Basculer sur la branche cible sous décision humaine ;
   - Vérifier l'état final de la branche cible et la conformité matérielle du commit d'intégration ;
   - Proposer la suppression sûre de la branche locale avec le mécanisme de suppression douce (`git branch -d` exclusivement, sans jamais forcer avec `-D`).
8. **Barrière Publication (`git push`, conditionnelle) :**
   La clôture de branche s'effectue normalement en local sans push obligatoire. Si et seulement si une publication distante est expressément demandée ou nécessaire :
   - Présenter la branche, la révision exacte et le remote/destination → **STOP** → attendre la validation humaine explicite → seulement ensuite exécuter `git push`.
