<!-- CONTEXT_METADATA
Context-Version: 2026-10-17.1
Updated: 2026-10-17
Scope: AI-Workflow
-->

> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Cap du Workflow IA

## Rôle et nature du document
Point de reprise synthétique et portable du projet `AI-Workflow`. Il fournit un résumé opérationnel de **comment** fonctionne actuellement le Workflow IA.
Ce fichier est purement **INFORMATIF** : il ne remplace jamais les sources normatives et techniques du dépôt.

## Principe personnel non négociable
> **« Je ne délègue jamais à une IA une tâche ou une décision technique que je ne comprends pas. »**

L’IA accélère l'exécution, mais ne remplace jamais la compréhension humaine. L'humain conserve la responsabilité des choix d'architecture, du périmètre et de chaque décision matérielle :
- **En phase d'apprentissage** : l'IA sert à expliquer, challenger, expliciter les erreurs et guider ; l'humain résout et apprend.
- **En phase de production sur domaine compris** : l'IA exécute et implémente de manière bornée ; l'humain supervise, valide et contrôle.

## Sources de vérité
- `AI_WORKFLOW.md` : règles universelles du développement assisté par IA (source unique, indépendante des outils).
- `PLAN_MAITRE.md` : gouvernance globale, état d'avancement et feuille de route.
- `architecture/PORTABLE.md` : architecture multi-fournisseurs, orchestration, dispatch et gestion du contexte.
- `architecture/AUTORISATIONS.md` : frontières universelles de sécurité (AUTO, décisions explicites, DENY).
- `architecture/REVIEW_ET_PREUVES.md` : règles universelles de Review indépendante et gestion des preuves.
- `documentation/<outil>/` : configuration et mécanismes propres à chaque runtime.
- `tests/<outil>/REQUALIFICATION.md` : preuves de requalification des adaptateurs.
- `Git` : source de vérité matérielle du code et de l'historique.

## Trio actif et affinités naturelles
L'écosystème actif s'articule autour de trois outils qualifiés :
- **Claude Code** : Principal / orchestrateur naturel ; travail transversal, planification et coordination. Fonctionnement normal en Opus 5.5 effort Medium ; lorsqu'un High serait justifié par une difficulté concrète, Claude Code 2.1.280 ne permettant pas au Principal de changer lui-même son effort, signalement non bloquant puis poursuite en Medium. Escalade automatique de modèle des sous-agents natifs (Sonnet → Opus) selon la politique Claude qualifiée. Concurrence proportionnée à la tâche, sans plafond fixe (nombre minimal suffisant de sous-agents natifs selon les axes réellement indépendants).
- **Codex** : affinité naturelle pour l'implémentation technique substantielle, refactorings, corrections de bugs, plans techniques et exécution rigoureuse de plans validés. Principal et Plan en GPT-6.1 Sol Medium ; sous-agents en GPT-6.1 Sol Low pour une mission bornée, escalade explicite Medium puis High sur signal concret (la taille seule ne suffit pas) ; Reviewer Codex en GPT-6.1 Sol High ; Astra exceptionnel, sans escalade automatique ; Terra historique uniquement. Mécanismes et preuves dans la documentation Codex. Concurrence normale : jusqu'à 3 sous-agents.
- **Antigravity** : affinité naturelle pour la Review indépendante, le challenge, la recherche et l'intégration de l'environnement. Fonctionnement normal en Gemini 3.8 Flash Medium ; Flash High sur difficulté concrète motivée et pour la Review indépendante formelle ; Flash Medium possible pour une micro-review ciblée/corrective si suffisant. Gemini 3.1 Pro High comme seconde opinion exceptionnelle explicitement motivée, jamais Reviewer par défaut ni étape automatique après Flash High ; la taille seule ne suffit pas. Concurrence normale : jusqu'à 3 sous-agents (`research` / `self`).

Grok est sorti de l'écosystème actif ; son adaptateur et son historique restent dans le projet privé et ne sont pas distribués ici.

> **Règle clé : AFFINITÉ ≠ RÔLE OBLIGATOIRE.** Aucun fournisseur n’est enfermé dans un rôle exclusif. Claude Code peut implémenter, Codex peut reviewer (sandbox lecture seule) et Antigravity peut implémenter.

## Dispatch multi-fournisseurs
Le choix du fournisseur pour une unité repose sur : la nature de la tâche, les capacités requises, les mécanismes natifs adaptés, le périmètre, la complexité, le besoin d'indépendance et l'état du quota comme facteur supplémentaire.
Le quota ne décide jamais seul (aucun routeur ni bascule automatique). Le chemin retenu est toujours le **chemin minimal suffisant** (détail dans `architecture/PORTABLE.md`).

## Review indépendante et preuves
- Invariant fondamental : **AUTEUR ≠ REVIEWER** (le reviewer ne modifie jamais le code et opère dans un contexte isolé).
- Preuve suffisante et toujours compatible → réutilisation obligatoire ; changement pertinent d'ETAT, de périmètre ou de besoin → invalidation proportionnelle des preuves affectées.
- Escalade proportionnée (N0 analyse statique → N1 preuves existantes → N2 validation ciblée → N3 délégation → N4 constat de défaut).
- Indépendance renforcée possible via Review croisée multi-fournisseurs (cross-provider), sans obligation systématique sur les petites unités (détail dans `architecture/REVIEW_ET_PREUVES.md`).

## Autorisations et discipline Git
- **Autonomie fonctionnelle (AUTO)** : toute action légitime, nécessaire et comprise dans le périmètre convenu s'exécute directement.
- **Décisions humaines explicites** : barrières Git fonctionnelles obligatoires (`git add`, `git commit`, `git push` conditionnel) et clôtures de branche (`merge`/`rebase`).
- **Frontières non négociables** : interdiction d'accéder aux secrets sans instruction, interdiction de contourner les sécurités, interdiction de détruire des données hors périmètre.

## État actuel du Workflow
- Architecture portable stabilisée et dédupliquée.
- Trio Claude Code / Codex / Antigravity qualifié (Claude Code 2.1.280 qualifié sur le périmètre requalifié : ExitPlanMode non requalifié, notifications avancées partielles/reportées, limites sandbox documentées), avec politiques de modèles, reasoning et concurrence propres à chaque adaptateur.
- Politique de dispatch souple formalisée.
- Ponts de contexte portables (`CAP_WORKFLOW_IA.md` / `PROJECT_CONTEXT.md`) et protocole `CHATGPT_SYNC` établis.

## Reprise depuis un contexte externe ou incomplet
Pour un humain ou une IA ne disposant pas déjà du contexte injecté du Workflow :
1. Lire `CAP_WORKFLOW_IA.md` pour appréhender la méthode, la gouvernance et les outils actifs.
2. Lire `PROJECT_CONTEXT.md` à la racine du projet pour comprendre les enjeux, la stack et les commandes du dépôt.
3. Vérifier l'état Git matériel (`python3 ~/.ai-workflow/outils/empreinte-git.py`).
4. Charger des sources normatives détaillées uniquement si l'unité le requiert expressément.

Les agents locaux configurés (Claude Code / Codex / Antigravity) utilisent directement leur injection native et `PROJECT_CONTEXT.md`, sans recharger le CAP.

## Prochaine grande étape
Appliquer directement le Workflow qualifié sur des projets de développement réels (ex. `gestion-personnes`), sans continuer d'optimiser l'infrastructure à vide. Les ajustements futurs découleront uniquement de retours d'expérience concrets.
