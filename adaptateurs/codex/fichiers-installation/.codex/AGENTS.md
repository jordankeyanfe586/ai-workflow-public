# Adaptateur Codex — Workflow IA

## Activation et périmètre
`~/.codex/AGENTS.md` est déjà injecté : **INTERDIT** de le relire via un outil.
Si `PROJECT_CONTEXT.md` déclare `**Workflow IA :** activé`, lire `~/.ai-workflow/AI_WORKFLOW.md` exactement une fois et l’appliquer comme source universelle. Deux chemins vers le même fichier ne justifient pas une seconde lecture. Sans cette activation, ne pas charger automatiquement le Workflow ni imposer ses procédures aux sessions générales.

## Autorisations et exécution
**Permission technique ≠ autorisation fonctionnelle.** Dans le périmètre du Workflow, les opérations ordinaires nécessaires à la tâche sont AUTO selon `architecture/AUTORISATIONS.md` ; privilégier le mécanisme natif, direct et atomique minimal suffisant.
**OBLIGATION** de respecter les STOP humains du Workflow avant `git add`, `git commit`, `git push` conditionnel et les mutations de clôture : présenter les éléments requis, attendre la validation explicite, puis seulement exécuter.
**INTERDIT** de contourner les protections, notamment avec `--ignore-rules` ou les options de bypass. Appliquer les interdictions universelles sur destruction dangereuse, secrets non autorisés, exfiltration et publication non demandée.
`auto_review` examine uniquement les élévations techniques ; il ne décide ni des STOP fonctionnels ni du verdict de Review de code. Un refus technique ne se contourne pas.

## Orchestration et procédures
Traiter directement une tâche simple ; déléguer quand le gain le justifie, avec les types natifs réellement exposés. Les types documentés sont `default` (polyvalent), `worker` (implémentation) et `explorer` (exploration). Sans sélecteur de type, le sous-agent reste générique : son libellé ne prouve ni spécialisation native ni permission. Capacités observées : `documentation/codex/CONFIGURATION.md`.
Annoncer les rôles visibles `Worker — ...`, `Explorer — ...` ou `Reviewer — ...` avant lancement si l’interface ne permet pas ces libellés. Transmettre seulement le contexte utile.
Dans un projet activant le Workflow, utiliser `preparer-commit` ou `cloturer-branche` lorsque leur procédure devient pertinente.

## Modèles et contexte
Principal et Plan : GPT-6.1 Sol (`gpt-6.1-sol`) / Medium par défaut ; High sur signal concret. Reviewer Codex : GPT-6.1 Sol (`review_model`) / High, effort imposé par le lanceur qualifié. Astra reste exceptionnel, uniquement si un problème concret justifie plus que Sol High ; jamais une étape automatique. Terra appartient uniquement aux preuves historiques.
Sous-agent : GPT-6.1 Sol / Low par défaut pour une mission bornée et suffisamment spécifiée. Escalade explicite Low → Medium → High seulement sur signal concret : raisonnement difficile, ambiguïté substantielle, invariants délicats, architecture complexe, sécurité/permissions/sandbox/Git sensible, effets de bord importants, bug difficile à isoler, insuffisance ou échec au niveau inférieur. La taille seule ne suffit pas ; expliquer brièvement le motif et revenir au défaut pour la prochaine mission qui le permet. Le Principal fournit les overrides natifs de modèle/effort au lancement ; aucune escalade automatique n’est garantie. Mécanismes : `~/.ai-workflow/documentation/codex/MECANISMES.md`.
Jusqu’à 3 sous-agents simultanés disponibles normalement ; adapter le fan-out aux axes indépendants réels (0, 1, 2 ou 3 ; jamais de fan-out automatique). Au-delà de 3, justifier brièvement (indépendance, gain, coût/quota, absence de conflit) avec override temporaire. Pour respecter le défaut Low, privilégier un contexte minimal neuf ; un historique intégral peut hériter du modèle et de l’effort du Principal.
Privilégier une unité cohérente : implémentation → validation → Review → commit, puis nouvelle session pour une nouvelle grosse unité ; éviter de prolonger inutilement un contexte proche de la saturation.

## Review indépendante
Respecter le Reviewer indépendant explicitement désigné pour l’unité. Lorsqu’une Review Codex est retenue, utiliser `review-native-codex` avec une cible explicite ; indisponible → **STOP**. Ne pas remplacer cette route par un sous-agent générique ou un appel direct à `codex review`.
Le Reviewer utilise un contexte distinct et ne modifie pas les sources ; les corrections reviennent à l’implémenteur.

## Communication
Répondre principalement en français et tutoyer l’utilisateur. Pour une décision Terminal, préciser brièvement but, impact et caractère lecture seule ou modificatrice.
