# Architecture universelle : Review indépendante et Gestion des Preuves

Ce document constitue la référence architecturale détaillée du Workflow IA pour la Review indépendante, l'escalade des vérifications et la gestion rigoureuse des preuves dynamiques.

---

## 1. Principes et Vision Universelle

Le Workflow IA repose sur un principe fondateur : **Git est la source de vérité matérielle**, tandis que les sessions et contextes des agents sont éphémères et volatils.

Pour garantir la sûreté et la qualité du code sans tomber dans une bureaucratie stérile ni multiplier les réexécutions redondantes, l'architecture sépare rigoureusement :
1. **Les faits matériels vérifiables** (l'`ETAT` Git cryptographique et les sorties d'exécution réelles) de la simple déclaration d'intention des LLM.
2. **Le RÔLE de l'agent** (ce dont il est responsable) de ses **CAPACITÉS TECHNIQUES** (ce que son runtime lui permet d'exécuter).
3. **L'intégrité du code source** des **artefacts éphémères** nécessaires à l'observation.

### 1.1 Invariant fondamental : Le Reviewer non-implémenteur
Le rôle de l'`AI-Reviewer` est d'auditer impartialement le travail réalisé par l'`AI-Agent` (implémenteur) et d'émettre un verdict normé.
- **Règle absolue : INTERDIT au Reviewer de modifier le code reviewé.** Il ne corrige jamais une coquille, ne refactore pas et ne commite rien.
- **Contexte isolé obligatoire :** Le Reviewer opère obligatoirement dans un contexte d'exécution neuf, distinct de celui de l'agent ayant produit ou modifié le code (interdiction de reprendre une conversation ou une session de travail de l'implémenteur).

### 1.2 Rôle vs Capacité technique : Fin du mythe du "filesystem strictement read-only"
Une ancienne hypothèse considérait qu'un Reviewer devait être confiné dans un environnement privé de tout terminal ou outil d'exécution. L'expérience montre que les linters, vérificateurs de syntaxe, compilateurs et suites de tests peuvent générer des caches temporaires (`.pytest_cache/`, `__pycache__/`, `.mypy_cache/`, `target/`) ou nécessiter des écritures éphémères dans `/tmp`.

**Distinction ontologique :**
- L'apparition d'artefacts de cache temporaires (généralement ignorés par `.gitignore`) **ne modifie pas le code source** et ne transforme pas le Reviewer en implémenteur.
- Le Reviewer peut exécuter lui-même une vérification dynamique ciblée si son adaptateur le permet, tant qu'il ne touche à aucun fichier source versionné.

---

## 2. Le Modèle Minimal de Preuve Universelle

Une preuve est un ensemble auditable attestant de la conformité d'un état matériel du code. Pour éliminer toute bureaucratie tout en assurant une traçabilité parfaite, la preuve universelle se compose de **6 champs nécessaires et suffisants** :

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                       STRUCTURE D'UNE PREUVE MINIMALE                      │
├───────────────┬────────────────────────────────────────────────────────────┤
│ 1. ETAT       │ Empreinte Git déterministe (20 hex via empreinte-git.py)    │
│ 2. COMMANDE   │ Commande exacte ou procédure exécutée                      │
│ 3. PÉRIMÈTRE  │ Fichier, module, sous-système ou 'workspace' couvert       │
│ 4. RÉSULTAT   │ Code retour (RC), verdict normé et métrique brute concise  │
│ 5. PRODUCTEUR │ Entité ayant exécuté l'action (implémenteur, reviewer, CI) │
│ 6. CONTEXTE   │ Condition de déterminisme si pertinent (toolchain, flags)  │
└───────────────┴────────────────────────────────────────────────────────────┘
```

### Formats d'expression légers

#### Format compact (Transmission inter-agents et journaux d'outils)
```text
[PREUVE:TEST]
ETAT: 8630c96d1e7d107fb4ce
COMMANDE: pytest tests/unit/test_auth.py
PERIMETRE: auth/
RESULTAT: OK (RC=0, 18 passés en 0.35s)
PRODUCTEUR: ai-agent
CONTEXTE: python 3.12
```

#### Format en ligne (Opérationnel rapide)
`Validations: pytest tests/unit/test_auth.py OK (18/18, RC=0) @ 8630c96d1e7d107fb4ce`

---

## 3. Règles de Validité et d'Invalidation

### 3.1 À ETAT Git identique

1. **Preuve existante et suffisante : RÉUTILISATION OBLIGATOIRE.**
   - Il est **STRICTEMENT INTERDIT** de réexécuter une suite de tests, un linter ou une compilation qui a déjà été prouvée sur le même `ETAT` sans régression ni ambiguïté.
2. **Preuve existante mais insuffisante : COMPLÉTION PROPORTIONNELLE.**
   - Exécuter uniquement le delta manquant pour couvrir le périmètre requis, sans rejouer les preuves valides déjà disponibles.

### 3.2 Invalidation différentielle à ETAT modifié

Lorsqu'une mutation fait évoluer l'`ETAT`, l'invalidation n'est pas aveuglement globale. Elle s'évalue proportionnellement au périmètre modifié :

```text
Mutation de code
  │
  ├── Type 0 : Orthogonal (Doc, commentaires, markdown)
  │     └── Invalidation = NULLE pour tests et builds. Toutes les preuves restent valides.
  │
  ├── Type 1 : Ciblé / Local (Corps de fonction, module isolé)
  │     └── Invalidation = Tests du module touché + Build.
  │         Les preuves des modules indépendants RESTENT VALIDES.
  │
  ├── Type 2 : Transversal / Core (Types racines, interfaces publiques, middleware)
  │     └── Invalidation = LARGE (Composants dépendants + intégration).
  │
  └── Type 3 : Toolchain & Configuration (package.json, Cargo.toml, flags compilateur)
        └── Invalidation = TOTALE (Build complet et suites de tests à rejouer).
```

### 3.3 Fausses invalidations (Transitions Git)
Le Workflow pose la règle d'invariance :
> **INTERDIT** de considérer `implémentation → Review → commit → merge` comme une invalidation automatique.
- Le staging (`git add`) ou la création d'un commit (`git commit`) modifie l'empreinte Git de l'index ou de HEAD, mais si l'arbre de travail est inchangé, les preuves détaillées obtenues sur cet arbre demeurent pleinement valides.

---

## 4. L'Escalade de Review (Niveaux 0 à 4)

L'escalade de Review organise l'effort de vérification en entonnoir, ordonné par coût croissant. Le Reviewer commence toujours par le niveau le plus léger et ne monte au palier supérieur que si un fait technique observable l'exige.

```text
┌──────────────────────────────────────────────────────────────────┐
│ Niveau 0 : Analyse statique & sémantique                         │ (Coût zéro runtime)
│            Diff, code, architecture, conformité, risques         │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Suffisant (risque faible) ? ──► [STOP : VALIDÉ]
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ Niveau 1 : Réutilisation des preuves valides sur l'ETAT          │ (Coût zéro exécution)
│            Tests, builds et linters fournis par l'implémenteur   │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Suffisant (preuves cohérentes) ? ──► [STOP : VALIDÉ]
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ Niveau 2 : Validation dynamique ciblée par le Reviewer          │ (Coût local ciblé)
│            Vérification de syntaxe, test ciblé, reproduction     │
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Levée de doute OK ? ──► [STOP : VALIDÉ]
                                 │ Reviewer non outillé ou preuve lourde ?
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ Niveau 3 : Requête de preuve à un Exécuteur tiers                │ (Coût délégation)
│           Mandat de commande transmis à Principal/Implémenteur/CI│
└────────────────────────────────┬─────────────────────────────────┘
                                 │ Preuve retournée OK ? ──► [STOP : VALIDÉ]
                                 │ Défaut avéré (Bloquant/Important) ?
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ Niveau 4 : Constat de défaut -> Retour à l'implémenteur          │ (Cycle correction)
│            Verdict CORRECTIONS REQUISES -> nouvel ETAT           │
└──────────────────────────────────────────────────────────────────┘
```

### 4.1 Description des Niveaux

- **Niveau 0 (Analyse statique)** : Examen du `git diff`, cohérence avec le périmètre assigné, détection d'effets de bord, audit de logique et conventions.
  - *Critère d'arrêt :* Sur une tâche à risque faible (documentation, correction triviale, configuration isolée), si N0 est satisfaisant → **STOP immédiat** (`REVIEW VALIDÉE`).
- **Niveau 1 (Réutilisation de preuves)** : Contrôle des sorties de tests unitaires/intégration et builds fournis sur l'`ETAT` exact.
  - *Critère d'arrêt :* Sur une tâche standard, si N0 est propre et les preuves N1 couvrent le périmètre sans ambiguïté → **STOP immédiat** (`REVIEW VALIDÉE`).
- **Niveau 2 (Validation dynamique ciblée par le Reviewer)** : Le Reviewer exécute lui-même une commande non mutatrice (`bash -n`, `python3 -m py_compile`, test unitaire ciblé) pour lever une **incertitude concrète** non résolue par N0/N1.
  - *Critère d'arrêt :* Si la vérification confirme le comportement attendu → **STOP immédiat** (`REVIEW VALIDÉE`).
- **Niveau 3 (Délégation à un Exécuteur de preuve)** : Le Reviewer ne peut ou ne doit pas exécuter la preuve lui-même (sandbox fermée, dépendances lourdes, conteneur requis). Il formule une requête précise transmise à un tiers.
- **Niveau 4 (Constat de défaut)** : Dès qu'une anomalie (`Bloquant` ou `Important`) est avérée, le Reviewer émet le verdict `CORRECTIONS REQUISES` avec un diagnostic structuré. **Il ne modifie aucun fichier.**

### 4.2 Règle stricte de proportionnalité : Rejet de la réassurance psychologique
- **Interdiction formelle :** Il est expressément interdit de passer en Niveau 2 ou Niveau 3 uniquement « par acquit de conscience », « pour être plus sûr » ou « pour vérifier par moi-même ».
- **Déclencheurs légitimes d'une nouvelle preuve :**
  1. Incertitude concrète sur un cas limite critique non sollicité par les tests existants.
  2. Contradiction observable entre le diff et la preuve déclarée.
  3. `ETAT` Git invalidé par une modification matérielle.
  4. Suspicion étayée de non-déterminisme environnemental.

---

## 5. Séparation des Rôles et Exécuteur de Preuve

Le Workflow IA formalise quatre rôles opérationnels :

1. **Principal** : Pilote l'orchestration, veille à la cohérence d'ensemble, traite les tâches simples et arbitre.
2. **Implémenteur (`AI-Agent` / `self`)** : Implémente le code, compile, exécute ses auto-validations et produit les premières preuves.
3. **Reviewer (`AI-Reviewer` / `research`)** : Analyse de façon indépendante, diagnostique, audite les preuves et émet le verdict final.
4. **Exécuteur de preuve (*Proof Runner*)** : Fonction temporaire assurée par le Principal, un implémenteur dédié ou un environnement de CI, lorsque le Reviewer ne dispose pas des capacités d'exécution requises.

### Protocole de l'Exécuteur de preuve : Étanchéité de jugement
> **Règle d'or : L'Exécuteur de preuve exécute la commande demandée et transmet la trace brute sans jamais interpréter le résultat ni usurper le verdict de Review.**
>
> **Réciproquement, le Reviewer est le seul juge de la conformité de la preuve.**

```text
Reviewer (Contexte isolé)                     Exécuteur de preuve (Principal/Implémenteur)
        │                                                     │
        │ 1. Demande : commande exacte, ETAT attendu          │
        │────────────────────────────────────────────────────►│
        │                                                     │ 2. Exécution matérielle déterministe
        │                                                     │    sur l'ETAT vérifié
        │ 3. Restitution : code retour, stdout/stderr bruts   │
        │◄────────────────────────────────────────────────────│
        │                                                     │
        │ 4. Analyse critique et émission du verdict           │
        ▼                                                     ▼
```

---

## 6. Cycle après Correction et Review Différentielle

Lorsqu'une Review initiale aboutit à un rejet :
```text
ETAT A (Implémentation initiale)
  ↓
Review indépendante → Verdict : CORRECTIONS REQUISES (Finding F1 identifié)
  ↓
L'implémenteur applique la correction ciblée
  ↓
ETAT B (Nouvelle empreinte Git)
```

### Arbitrage : Review Ciblée vs Review Complète

#### La Review Ciblée SUFFIT si (Conditions cumulatives) :
1. **Périmètre strictement borné :** La correction touche uniquement les lignes ou la fonction incriminée par F1.
2. **Contrats préservés :** Aucune modification d'interface publique, de signature exportée ou de schéma de données.
3. **Absence d'effets de bord :** Aucun fichier de configuration ni dépendance n'a été touché.
4. **Validations techniques vertes :** Les tests ciblés du module corrigé passent avec succès.
5. **Adéquation exacte :** Aucun refactoring opportuniste n'a été mêlé au correctif.

*Processus :* Le Reviewer inspecte uniquement le diff différentiel `ETAT A..ETAT B` et valide la levée de F1 → `REVIEW VALIDÉE`.

#### La Review Complète est REQUISE si (Au moins une condition) :
1. Changement de signature publique ou de contrat partagé.
2. Propagation du correctif à plusieurs sous-systèmes.
3. Faille de sécurité critique ou bug de concurrence résolu.
4. Ajout ou modification d'une dépendance externe.

---

## 7. Contrat Universel de Capacités d'Adaptateur

Chaque adaptateur d'outil IA déclare ses capacités de Review selon une interface standardisée :

```json
{
  "$schema": "https://ai-workflow.invalid/schemas/adapter-capabilities-v1.json",
  "adaptateur": "nom-outil",
  "capacites_review": {
    "reviewer_independant": true,
    "reviewer_peut_lire": true,
    "reviewer_peut_executer_validation": true,
    "reviewer_peut_modifier_source": false,
    "chemin_execution_preuve_si_indisponible": "principal",
    "isolation_contextuelle": "subagent_ephemere",
    "support_ETAT": true,
    "support_review_ciblee": true
  }
}
```

### Matrice de référence par adaptateur

| Capacité | Claude Code (2.1.280) | Antigravity (1.2.6) | Codex (cli) | Grok (1.0.x) | Gemini CLI |
|---|---|---|---|---|---|
| **Mécanisme natif** | Agent personnalisé `ai-reviewer` (`Read`, `Bash`), non systématique | Subagent `research` | Binaire `review-native-codex` | Skill bundled `review` | Session CLI distincte |
| **`reviewer_independant`** | `true` (contexte neuf ; voir note) | `true` | `true` | `true` | `true` |
| **`isolation_contextuelle`** | `subagent_ephemere` | `subagent_ephemere` | `processus_isole` | `subagent_ephemere` | `processus_isole` |
| **`reviewer_peut_lire`** | `true` (`Read`, Git en lecture) | `true` (`view_file`, git) | `true` (inspection native) | `true` (lecture workspace) | `true` (lecture workspace) |
| **`reviewer_peut_executer_validation`** | `true` (Bash : tests, build, lint, sans écriture de source) | `true` (`run_command` qualifié) | `false` (sandbox read-only strict) | Variable selon profil | Variable selon invocation |
| **`reviewer_peut_modifier_source`** | `false` (structurel pour `Edit`/`Write` ; déclaratif pour Bash, vérifié par `ETAT` initial = final) | `false` (structurel : pas d'outil d'écriture) | `false` (structurel : sandbox read-only) | `false` (politique native Skill) | `false` (politique d'appel) |
| **Exécuteur de preuve requis ?** | Rare (validations exécutables via Bash) | Rare (uniquement si commande hors grants dev) | **OUI, OBLIGATOIRE** (Codex read-only) | Possible selon sandbox | Si outil d'exécution absent |
| **Chemin de repli preuve** | Principal | Principal | Principal / Implémenteur | Principal | Shell parent / Principal |
| **`support_ETAT`** | `true` (`empreinte-git.py`, initial et final) | `true` (`empreinte-git.py`) | `true` (via wrapper/shell) | `true` (`empreinte-git.py`) | `true` (terminal) |
| **`support_review_ciblee`** | `true` (mission bornée) | `true` (mission bornée) | `true` (flags `--commit/base`) | `true` (ciblage natif) | `true` (paramètres passés) |

**Note Claude Code.** Lorsque Claude est auteur, `ai-reviewer` n’est qu’une Review supplémentaire ou un diagnostic interne ; la Review finale est externe : Antigravity, ou Antigravity + Codex si le risque est élevé. Lorsque Codex ou Antigravity est auteur, `ai-reviewer` peut être désigné Reviewer indépendant.

Les URL de schéma en `.invalid` ci-dessus sont des exemples de structure, pas des schémas publiés ou téléchargeables.
