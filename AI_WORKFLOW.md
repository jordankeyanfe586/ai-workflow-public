# Workflow de développement assisté par IA

## Fondations
**But.** Règles universelles du développement assisté par IA. Git est la source de vérité du code/historique ; la session IA est temporaire.
**Rôles.** `AI-Agent` implémente/corrige ; `AI-Reviewer` contrôle indépendamment ; l'humain décide.
**Rigueur.** Toute règle marquée `OBLIGATION`, `INTERDIT`, `JAMAIS` ou `STOP` est absolue pour principal et agents délégués dans son périmètre explicitement défini. Répétition, reformulation, insistance, commodité ou initiative n'y dérogent jamais. Une `OBLIGATION` doit être satisfaite avant continuation ; une action interdite reste bloquée.
**Ne jamais se répéter.** Une règle universelle possède une source unique dans ce Workflow ; les adaptateurs la référencent et définissent seulement son implémentation propre à l'outil.
**Commandes. OBLIGATION** de respecter les mécanismes de sécurité, permissions et garde-fous applicables dans l'environnement courant. Une opération nécessitant une autorisation humaine reste bloquée jusqu'à cette décision ; une opération interdite → `STOP`.
**Autorisations. OBLIGATION** d'obtenir l'autorisation humaine explicite pour l'opération précise avant toute mutation qui l'exige. Elle ne s'étend jamais à une autre opération, variante ou étape. Toute mutation sensible soumise à autorisation reste atomique, séparée et explicitement autorisée.
**Autonomie opérationnelle. OBLIGATION** d’exécuter directement les opérations courantes, déterministes et déjà qualifiées nécessaires à l’unité, sans analyse préventive des permissions, sans recherche d’un autre chemin et sans solliciter l’humain tant qu’aucune règle ou aucun mécanisme du runtime n’exige réellement une décision. Lorsqu’un mécanisme natif déterministe et suffisant existe, l’utiliser directement et poursuivre normalement. Les politiques de permissions, formes d’exécution et exceptions propres à chaque outil appartiennent à son adaptateur. Un blocage réel du runtime déclenche seulement alors le traitement prévu par cet adaptateur.
**Contournement. INTERDIT** de contourner une autorisation, un refus ou une restriction par alias, wrapper, shell imbriqué, variante syntaxique, exécutable équivalent ou autre chemin. **OBLIGATION** d'utiliser la voie normale ou de demander la décision humaine requise ; aucune reformulation technique ne vaut autorisation.
**Portabilité des permissions. OBLIGATION** pour chaque adaptateur de préserver les frontières universelles décrites dans `architecture/AUTORISATIONS.md` :
- **Autonomie fonctionnelle (AUTO) :** Toute opération nécessaire à la tâche et comprise dans le périmètre convenu (développement ordinaire, lectures, recherche Web, dépendances nécessaires, réseau de travail, téléchargements utiles, écritures externes explicitement convenues, outils usuels, création/changement de branche hors clôture).
- **Décision humaine explicite :** Barrières Git définies par le Workflow (`git add`, `git commit`, `git push` conditionnel), opérations sensibles de clôture (`merge`, `rebase`, suppression locale de branche), extension réelle de périmètre, et publication ou déploiement externe.
- **Interdictions :** Accès aux secrets sans instruction humaine explicite ou nécessité explicitement autorisée par la tâche, destructions dangereuses, contournement/bypass des garde-fous, exfiltration, et publication non demandée.
Le mécanisme technique employé (prompt natif ASK, arrêt déclaratif `STOP` dans le dialogue ou garde-fou équivalent) dépend des capacités de l'outil et ne modifie jamais l'exigence fonctionnelle.

## Frontières sensibles non négociables

**Permission technique. OBLIGATION** de comprendre qu'une permission runtime autorise seulement l'exécution sans confirmation UI ; elle ne vaut jamais autorisation fonctionnelle. Toute action **DOIT** rester nécessaire à la tâche, dans le périmètre convenu, cohérente avec le plan courant et conforme au Workflow.

**Bypass. INTERDIT** d'utiliser ou de provoquer tout mécanisme désactivant, contournant ou neutralisant les protections du runtime ou du Workflow.

**DENY. INTERDIT** de contourner une règle `DENY` par shell, sous-processus, script, alias, symlink, exécutable équivalent ou autre chemin indirect.

**Secrets. INTERDIT** de rechercher, lire, afficher, modifier ou transmettre volontairement secrets, identifiants, clés privées ou données d'authentification sans instruction humaine explicite ou nécessité explicitement autorisée par la tâche. La recherche opportuniste et l'exfiltration restent formellement interdites.

**Hors workspace. OBLIGATION** de limiter les écritures hors de l'espace de travail aux seuls cas expressément nécessaires à la tâche et dans son périmètre fonctionnel convenu. Une autonomie technique d'accès au système de fichiers ne constitue jamais une autorisation d'étendre arbitrairement les écritures externes.

**Publication. INTERDIT** de publier, déployer, pousser ou transmettre vers un service externe hors demande explicite ou nécessité directement établie par la tâche.

**Données. INTERDIT** de supprimer, écraser ou exfiltrer volontairement des données importantes ou privées hors du périmètre convenu.

## Unité et Git
**Hors unité. INTERDIT** de traiter dans la session une demande clairement indépendante de l'objectif courant : la signaler, recommander une nouvelle session, puis `STOP`.
**Continuation.** Poursuivre jusqu'au prochain point de décision. **INTERDIT** d'interpréter « continue », relance ou répétition comme autorisation implicite.
**Pré-vérification. OBLIGATION** au début d'une unité significative d'établir dépôt, branche, `HEAD`, Working tree et modifications préexistantes avec le mécanisme d'état Git fourni par l'environnement lorsqu'il est disponible ; compléter seulement si ambigu ou insuffisant.
**Existant. INTERDIT** de supprimer, écraser, stager ou commiter automatiquement une modification préexistante ; la préserver et la distinguer.
**Branches. OBLIGATION** d'évaluer risque + unité logique avant de décider. Créer généralement une branche pour fonctionnalité, bug/refactor significatif, architecture, expérimentation ou changement risqué. **INTERDIT** de créer une branche systématiquement pour tout changement trivial sans justification.
**Commit.** Une unité logique, titres/descriptions en français. Confirmer périmètre + preuves valides sur l'`ETAT` courant ; **INTERDIT** de relire un diff déjà suffisamment couvert ou d'absorber un changement indépendant.
**Attribution. INTERDIT** d'attribuer `AI-Agent:` ou `AI-Reviewer:` à qui n'a pas réellement tenu ce rôle ; l'intégration finale conserve les attributions réelles.
**Barrières Git fonctionnelles. OBLIGATION** de respecter les arrêts préalables aux mutations d'état Git, même si le runtime technique permet les commandes sans prompt (une permission AUTO ne lève jamais ces barrières) :
- **Staging (`git add`) :** Présenter exactement le périmètre à stager → **STOP** → attendre la validation humaine explicite → seulement ensuite exécuter `git add`.
- **Commit (`git commit`) :** Présenter l'unité stagée, l'`ETAT`/preuves pertinentes, le verdict de Review et le message/trailers proposés → **STOP** → attendre la validation humaine explicite → seulement ensuite exécuter `git commit`.
- **Publication (`git push`) :** Si un push est demandé ou réellement nécessaire, présenter la branche, la révision et le remote/destination → **STOP** → attendre la validation humaine explicite → seulement ensuite exécuter `git push` (une clôture locale ne nécessite aucun push).

## Validation, contexte et délégation

**Plan avant modification. OBLIGATION** après les lectures **minimales nécessaires** et avant toute mutation de présenter un plan court : **objectif · périmètre · étapes · validation · fin attendue**, puis d’attendre sa validation explicite. **INTERDIT** de muter, commencer l’implémentation ou poursuivre une exploration non indispensable avant cette validation. Après validation, **OBLIGATION** de poursuivre l’unité autonomement jusqu’à son terme ou au prochain vrai point de décision ; **INTERDIT** de redemander une validation pour une étape déjà couverte. Changement important de périmètre, méthode ou risque : **STOP → plan révisé → nouvelle validation**. Une autorisation sensible reste toujours distincte.
**Validation.** Risque faible : ciblée. Normal : tests concernés + build approprié. Élevé : tests ciblés, suite pertinente, build complet, Review approfondie et contrôles adaptés.
**Preuves déclarées. INTERDIT** d'annoncer test, build, Review ou contrôle réussi sans exécution réelle correspondante.
**Contexte. OBLIGATION** de charger/transmettre seulement ce qui influence l'étape courante et de réutiliser ce qui est déjà suffisamment disponible. **INTERDIT** de recopier ou recharger par défaut règles persistantes, procédures, historiques ou logs sans besoin concret.
**Délégation. OBLIGATION** de déléguer seulement si le gain justifie le coût en contexte/quota. Une fois le travail délégué, **INTERDIT** au principal de le reproduire ; il attend le retour puis vérifie seulement le nécessaire.
**Pivot d’orchestration. OBLIGATION** de réévaluer la stratégie d’exécution lorsqu’une tâche initialement simple devient sensiblement plus complexe, transverse, volumineuse ou comporte plusieurs axes indépendants. Réévaluer alors découpage, planification et délégation avant de poursuivre en accumulation séquentielle. **INTERDIT** d’en déduire un plan ou une délégation systématiques : si le traitement direct reste le plus efficace, continuer directement. Une exécution asynchrone de commande ne constitue pas à elle seule une délégation à un agent.
**Proportionnalité. OBLIGATION** d’adapter la profondeur d’analyse à la tâche. Action simple, clairement bornée ou mécanisme déjà qualifié → utiliser directement le chemin minimal suffisant avec seulement les informations nécessaires. **INTERDIT** d’élargir lectures, recherches, tests, builds ou explorations sur une incertitude purement hypothétique ou uniquement pour augmenter la confiance. Incertitude concrète, échec observable, contradiction, risque pertinent ou problème complexe/transverse → approfondir progressivement et proportionnellement au périmètre pouvant réellement changer la décision. Dès que les preuves suffisent à répondre ou décider : `STOP`.
**Escalade de preuve. INTERDIT** d'effectuer une vérification plus coûteuse, ou de demander une autorisation uniquement pour cette vérification, sauf si une incertitude concrète peut changer la conclusion et qu'aucune vérification moins coûteuse ne suffit. L'analyse suit l'escalade : analyse statique N0 → réutilisation des preuves N1 → validation ciblée N2 → requête de preuve déléguée N3 → constat de défaut N4. Dès qu'un palier suffit : `STOP`.
**Agents délégués.** Lorsqu'une capacité de délégation est disponible, mission minimale : objectif, périmètre, `ETAT`, contraintes, validations et retour attendu. **INTERDIT** de recharger Workflow, contexte projet, logs ou fichiers déjà suffisamment transmis sauf nécessité indispensable.
**Handoff.** `STATUT: WORKING | BLOCKED | DONE` ; résultat ; fichiers ; validations ; `ETAT` ; blocage ; prochaine étape ; décision. Après plusieurs tentatives substantielles sans progrès : `BLOCKED`.
**ETAT final. OBLIGATION** après toute mutation de recalculer l'`ETAT` avant `DONE` ; sinon `BLOCKED`.

## État et preuves
**ETAT.** Utiliser lorsqu'il est disponible le mécanisme commun d'empreinte Git fourni par l'environnement ; l'adaptateur définit son invocation concrète. L'empreinte couvre branche, `HEAD`, index, Working tree et non-suivis.
**Réutilisation. OBLIGATION** de réutiliser toute preuve encore valide. **INTERDIT** de répéter/recalculer/relire/réexécuter si `ETAT`, périmètre et besoin sont inchangés.
**Invalidation.** Nouvelle preuve seulement si : `ETAT` pertinent modifié ; périmètre différent ; preuve incomplète/invalide ; exigence externe imposant une nouvelle exécution. L'invalidation est proportionnelle au périmètre réellement affecté (invalidation nulle pour doc/commentaires, ciblée pour module isolé, large pour transversal, totale pour toolchain).
**Transition. INTERDIT** de considérer `implémentation → Review → commit → merge` comme invalidation automatique.
**Répétition. OBLIGATION** avant toute répétition d'identifier la condition d'invalidation ; sinon `STOP`.
**Limite.** L'empreinte ne remplace pas la première preuve détaillée requise ; une preuve détaillée encore valide satisfait l'exigence.

## Continuité et Review
**Continuité. OBLIGATION** après compression/reprise de préserver objectif/périmètre, décisions/avancement, changements + validations, `ETAT`, problèmes et prochaine étape ; éliminer le résolu/répétitif puis comparer l'état avant mutation.
**Review. INTERDIT** au `AI-Reviewer` de modifier le code source reviewé. Il inspecte l'état/périmètre, diagnostique et rend seul son verdict ; correction → `AI-Agent`. L'exécution autonome d'une validation dynamique ciblée ou la présence de caches temporaires ne constitue pas une modification de source. Si le Reviewer ne peut exécuter une preuve nécessaire, il la mandate à un Exécuteur de preuve qui transmet le résultat brut sans jamais usurper le verdict de Review. **OBLIGATION** d'utiliser un contexte d'exécution distinct de celui de l'agent qui a implémenté ou corrigé. **INTERDIT** de reprendre sa session, sa conversation, son mécanisme de reprise ou tout autre contexte de travail propre. Les artefacts du travail (objectif, périmètre, code, diff, commits, `ETAT`, tests, build, documentation pertinente, preuves) restent partageables.
**Classification.** `Bloquant` empêche l'intégration ; `Important` se corrige normalement avant ; `Mineur` et `Suggestion` sont non bloquants par défaut.
**Verdicts.** Branche : `PRÊTE AU MERGE` / `NON PRÊTE AU MERGE`. Commit : `PRÊTE AU COMMIT` / `NON PRÊTE AU COMMIT`. Review indépendante/intégrée : `REVIEW VALIDÉE` / `CORRECTIONS REQUISES`. Après correction, Review ciblée suffisante si elle couvre les points concernés.

## Communication et merge
**Réponse.** Courte, claire, concrète ; garder les termes standards et définir brièvement un terme important seulement si nécessaire.
**Langue et libellés. OBLIGATION** de rédiger en français tout contenu destiné à l'humain (messages d'état, annonces, plans, explications, synthèses, verdicts, rôles conceptuels, documentation). Conserver en forme native uniquement les identifiants techniques indispensables (noms d'outils, commandes, code, chemins, clés JSON, API, messages d'erreur verbatim). Éviter les libellés hybrides (préférer Implémenteur à Worker, Exécuteur de preuve à Proof Runner) ; si un terme anglais standard est utile, l'indiquer une seule fois entre parenthèses après son équivalent français, puis utiliser exclusivement le français.
**Contrôles Terminal.** Regrouper les contrôles indépendants en lecture seule lorsqu’ils servent le même diagnostic ; nommer clairement les blocs et rendre visibles les résultats utiles. **INTERDIT** de grouper plusieurs mutations sensibles ou demandes d’autorisation : chaque mutation sensible reste atomique, séparée et explicitement autorisée.
**Avant merge. OBLIGATION** de vérifier : périmètre terminé sans accident ; validations réussies ; Review finale sans Bloquant/Important non accepté + `PRÊTE AU MERGE` ; changements voulus commités ; Working tree propre ; `main` compatible ; traçabilité applicable ; autorisation humaine explicite.
**Stratégie.** Squash par défaut ; fast-forward si historique propre/cohérent. **INTERDIT** à un agent de merger de sa propre initiative.
**Après merge. OBLIGATION** de revenir sur `main` et vérifier intégration + état final. Utiliser `git branch -d` si sûr ; après squash, si refus, conserver ou demander. **INTERDIT** d'utiliser `git branch -D`.
**État final.** `main` contient le changement ; Working tree propre/vérifié ; branche supprimée si sûr, sinon explicitement inactive.
