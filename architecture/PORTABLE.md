# Architecture portable du Workflow IA

> **Statut : provisoire**
>
> Ce document conserve les principes d'architecture actuellement retenus.
> Il sera réévalué lorsque les adaptateurs actuels ou futurs révèlent un nouvel angle mort réellement universel.
>
> L'objectif est de conserver notre réflexion actuelle sans figer prématurément une architecture définitive.

---

## 1. Objectif

Construire un Workflow de développement assisté par IA qui :

- ne dépend pas d'un fournisseur ;
- ne dépend pas d'un modèle précis ;
- ne dépend pas d'un mécanisme propriétaire précis ;
- reste compréhensible par l'humain ;
- puisse évoluer lorsque les outils IA changent ;
- limite les duplications entre outils ;
- préserve la fenêtre de contexte ;
- utilise les mécanismes natifs de chaque outil lorsqu'ils sont pertinents ;
- conserve Git comme source de vérité pour l'état du code ;
- conserve l'humain comme autorité finale pour les décisions importantes.

L'objectif n'est donc pas de construire un « Workflow Claude » ou un « Workflow Codex ».

L'objectif est de construire un **Workflow IA portable** auquel différents agents peuvent être raccordés.

---

## 2. Principe fondamental

L'architecture distingue cinq éléments :

1. ce qui doit arriver ;
2. ce qu'un agent doit connaître ;
3. comment une procédure doit être réalisée ;
4. ce qui est autorisé ou interdit ;
5. comment un outil particulier implémente ces règles.

En résumé :

> **Le Workflow définit ce qui doit arriver.**
>
> **Le contexte projet définit ce qu'il faut connaître.**
>
> **Les procédures définissent comment accomplir une tâche.**
>
> **Les politiques définissent ce qui est autorisé.**
>
> **Les adaptateurs traduisent ces principes dans les mécanismes propres à chaque outil.**

---

## 3. Sources de vérité principales

### 3.1 `AI_WORKFLOW.md`

`AI_WORKFLOW.md` décrit les règles universelles du développement.

Il contient notamment :

- le cycle de travail ;
- la pré-vérification Git ;
- la séparation des responsabilités ;
- les validations ;
- la Review ;
- les commits ;
- la clôture d'une branche ;
- les décisions humaines ;
- la continuité du contexte.

Il ne doit pas dépendre :

- de Claude ;
- de Codex ;
- de Gemini ;
- d'OpenCode ;
- d'un modèle précis ;
- d'un format de configuration propriétaire.

Conceptuellement :

```text
AI_WORKFLOW.md
      │
      └── Comment nous développons
```

---

### 3.2 `PROJECT_CONTEXT.md`

Chaque projet peut disposer d'un :

```text
PROJECT_CONTEXT.md
```

Ce fichier décrit uniquement ce qui est spécifique au projet.

Il peut contenir :

- l'objectif ;
- l'état du projet ;
- l'architecture ;
- la stack technique ;
- les commandes de lancement ;
- les tests ;
- le build ;
- les autres validations ;
- les conventions spécifiques ;
- les contraintes importantes.

Conceptuellement :

```text
PROJECT_CONTEXT.md
      │
      └── Sur quoi nous travaillons
```

`PROJECT_CONTEXT.md` doit rester indépendant du fournisseur et du modèle IA.

---

## 4. Modèles de projet

Les modèles sont stockés dans :

```text
modeles-projet/
├── PROJECT_CONTEXT_MODEL.md
├── INSTRUCTIONS_CHATGPT_MODEL.md
└── claude/CLAUDE.md
```

### Distinction conventionnelle
- `PROJECT_CONTEXT.md` : **instance réelle** propre à un projet, située à la racine de son dépôt.
- `PROJECT_CONTEXT_MODEL.md` : **modèle générique** à copier pour initialiser l'instance réelle d'un nouveau projet.
- `INSTRUCTIONS_CHATGPT_MODEL.md` : **modèle de texte** à copier dans les Instructions personnalisées d'un projet ChatGPT.

### Adoption dans un nouveau projet
Pour intégrer un nouveau dépôt au Workflow IA, la démarche est volontairement minimale :
1. Copier `modeles-projet/PROJECT_CONTEXT_MODEL.md` vers `PROJECT_CONTEXT.md` à la racine du nouveau projet.
2. Remplacer les champs du modèle par le contexte réel du projet (objectif, stack, commandes canoniques).
3. Optionnel : copier `modeles-projet/INSTRUCTIONS_CHATGPT_MODEL.md` dans les Instructions du projet ChatGPT correspondant si ce pont est utilisé.

Aucun générateur de code, script ou outil maison n'est exigé : une simple copie manuelle suffit.

Pour Codex, `PROJECT_CONTEXT.md` est configuré comme fichier fallback de documentation projet. La déclaration `**Workflow IA :** activé` dans ce fichier constitue l'activation explicite du Workflow pour Codex. Un `AGENTS.md` propre au projet n'est donc pas nécessaire par défaut.

---

## 5. Les rôles doivent être indépendants des modèles

Le Workflow ne doit pas être défini principalement avec des noms de modèles.

Il doit être défini avec des responsabilités.

Rôles possibles :

```text
Humain
│
├── Orchestrateur
├── Planificateur
├── Agent d'exécution
├── Explorateur
└── Reviewer
```

Architecture logique :

```text
Planificateur
      │
      ▼
Agent d'exécution
      │
      ▼
Validations
      │
      ▼
Reviewer
      │
      ▼
Humain
```

Chaque outil peut ensuite attribuer ces rôles à ses propres modèles ou mécanismes.

Exemple conceptuel :

```text
Claude Code
├── Planificateur → modèle adapté à la planification
├── Exécution     → modèle adapté au développement
└── Reviewer      → mécanisme retenu pour la Review

Codex
├── Planificateur → modèle principal
├── Worker        → modèle adapté à l'exécution
├── Explorateur   → modèle adapté à l'exploration
└── Reviewer      → Review native

Futur outil
├── Planificateur → ...
├── Exécution     → ...
└── Reviewer      → ...
```

Ainsi, remplacer un modèle ne nécessite normalement pas de modifier l'architecture générale.

---

## 6. Cycle de vie universel

Le cycle de développement doit rester indépendant de l'outil utilisé.

Schéma provisoire :

```text
Début
  │
  ▼
Pré-vérification Git
  │
  ▼
Compréhension de la demande
  │
  ▼
Exploration si nécessaire
  │
  ▼
Planification
  │
  ▼
Exécution
  │
  ▼
Tests / Build / Validations
  │
  ▼
Review
  │
  ├──── corrections nécessaires ────┐
  │                                  │
  └──────────────────────────────────┘
  │
  ▼
Préparation du commit
  │
  ▼
Décision humaine
  │
  ▼
Commit
  │
  ▼
Préparation de la clôture
  │
  ▼
Décision humaine
  │
  ▼
Merge / clôture
  │
  ▼
Vérification finale
```

Claude, Codex ou un autre outil peuvent implémenter ces étapes différemment.

Le cycle logique reste commun.

---

## 7. Procédures universelles

Certaines Skills actuellement propres aux outils représentent en réalité des procédures générales.

Exemples :

```text
Préparer un commit
Clôturer une branche
```

La logique générale de ces procédures pourrait à terme être centralisée.

Exemple :

```text
PRÉPARER UN COMMIT

1. vérifier Git ;
2. examiner les modifications ;
3. déterminer le périmètre logique ;
4. vérifier les validations ;
5. préparer le staging ;
6. préparer le message ;
7. demander la décision humaine ;
8. exécuter seulement après autorisation.
```

Cette logique ne dépend ni de Claude ni de Codex.

Une organisation future pourrait être :

```text
procedures/
├── PREPARER_COMMIT.md
└── CLOTURER_BRANCHE.md
```

Les Skills propres aux outils pourraient alors devenir des adaptateurs de ces procédures.

Cette évolution reste provisoire et devra être validée après l'étude de plusieurs outils.

---

## 8. Politiques universelles

Les mécanismes techniques de sécurité diffèrent selon les outils.

Exemples :

```text
Claude Code
├── permissions
├── Hooks
└── PreToolUse

Codex
├── ExecPolicy
├── Hooks
└── Hook Stop de notification

Gemini
└── à étudier

OpenCode
└── à étudier
```

L'intention de sécurité peut cependant rester commune.

Exemple de politique Git :

```text
Opération                         Politique

git status                        autorisé
git diff                          autorisé
git log                           autorisé
git branch --show-current         autorisé

git add                           décision humaine
git commit                        décision humaine
git merge                         décision humaine
git push                          décision humaine
git rebase                        décision humaine

git push --force                  interdit chez Claude ; STOP déclaratif chez les autres adaptateurs distribués
git reset --hard                  interdit
git clean forcé                   interdit
git branch -D                     interdit
```

Chaque adaptateur doit essayer d'implémenter cette politique avec les mécanismes natifs disponibles.

L'objectif n'est donc pas :

```text
settings.json == config.toml
```

L'objectif est plutôt :

```text
Politique Claude
       ≈
Politique Codex
       ≈
Politique Gemini
       ≈
Politique OpenCode
```

même lorsque leurs implémentations techniques sont différentes.

---

## 9. Gestion portable du contexte

La fenêtre de contexte est une ressource.

Une grande fenêtre de contexte ne justifie pas de charger des informations inutiles.

Principe :

> **Charger au démarrage uniquement les informations susceptibles d'influencer régulièrement les décisions de l'agent.**

Organisation conceptuelle :

```text
NIVEAU 1 — toujours disponible
│
├── règles essentielles du Workflow
├── contexte essentiel du projet
└── adaptateur minimal de l'outil
│
▼
Chargé au début de la session


NIVEAU 2 — chargé lorsque nécessaire
│
├── procédures
├── Skills
├── règles spécialisées
└── documentation d'architecture détaillée
│
▼
Chargé à la demande


NIVEAU 3 — chargé ponctuellement
│
├── historique
├── anciens plans
├── rapports
├── logs
└── documentation rarement nécessaire
│
▼
Chargé uniquement lorsqu'une tâche le nécessite
```

Objectifs :

- préserver la fenêtre de contexte ;
- réduire les tokens inutiles ;
- réduire le bruit ;
- améliorer l'attention de l'agent ;
- limiter les instructions contradictoires ;
- charger les informations spécialisées seulement lorsqu'elles deviennent pertinentes.

Le Workflow doit donc optimiser **la pertinence du contexte**, pas simplement rechercher la plus grande fenêtre possible.

### 9.1 Ponts de contexte portables et étanchéité des sources

Le Workflow IA formalise deux fichiers de contexte portables et informatifs :

1. `CAP_WORKFLOW_IA.md` : résumé portable de **COMMENT** fonctionne le Workflow IA (méthode, écosystème actif, gouvernance, cap immédiat).
2. `PROJECT_CONTEXT.md` : résumé portable de **SUR QUOI** porte le projet courant (objectif, architecture, stack, commandes canoniques, point de reprise).

Ces deux fichiers sont conçus pour être importés manuellement comme « Sources » dans des projets ChatGPT ou d'autres environnements externes.

> **Principe fondamental d'étanchéité :**
> - **Source de vérité matérielle** : les fichiers techniques et normatifs du dépôt Git (`AI_WORKFLOW.md`, `architecture/PORTABLE.md`, code source, suites de tests, configurations).
> - **Ponts de contexte informatifs** : `CAP_WORKFLOW_IA.md` et `PROJECT_CONTEXT.md` ne sont JAMAIS des sources normatives bis. Ils renvoient aux sources du dépôt dès qu'un détail d'implémentation ou de preuve est requis.

### 9.2 Métadonnées de versionnement (`Context-Version`)

Pour permettre à l'humain et aux environnements externes d'identifier immédiatement la fraîcheur d'un contexte sans recourir à un système complexe de versionnage ou à l'empreinte Git, chaque fichier de contexte portable comporte un en-tête léger :

```markdown
<!-- CONTEXT_METADATA
Context-Version: YYYY-MM-DD.N
Updated: YYYY-MM-DD
Scope: [AI-Workflow | Nom du projet]
-->
```

- **Format :** `YYYY-MM-DD.N` (ex. `2026-09-19.1`).
- **Lisibilité :** directement comparable et lisible à l'œil nu.
- **Découplage :** strictement indépendant du hash SHA du commit Git.
- **Minimalité :** aucun compteur automatisé, aucune base d'état ni outillage maison.

### 9.3 Règles matérielles de mise à jour

Pour éviter le bruit et préserver la stabilité du contexte :

#### Quand mettre à jour `CAP_WORKFLOW_IA.md`
Mettre à jour le CAP **uniquement lors d'un changement durable ou structurel du Workflow IA** :
- Évolution de l'architecture générale ou des principes directeurs ;
- Évolution du trio actif d'outils/fournisseurs (ex. intégration d'Antigravity, réintégration de Claude Code, retrait de Grok) ;
- Changement durable des modèles de référence ou de la politique de raisonnement ;
- Modification de la politique de dispatch multi-fournisseurs ou des garanties de Review ;
- Évolution significative des frontières universelles d'autorisations ;
- Clôture d'une grande étape majeure et bascule vers un nouvel objectif structurant.
*INTERDIT de le modifier pour un commit ordinaire, une correction de coquille, un bug local ou une retouche mineure.*

#### Quand mettre à jour `PROJECT_CONTEXT.md`
Mettre à jour le contexte projet **uniquement lors d'un changement significatif de la réalité du projet** :
- Modification de l'architecture logicielle ou de l'arborescence des modules ;
- Évolution de la stack technique (nouveau framework, outil de build, version majeure de runtime) ;
- Modification des commandes canoniques de validation (tests, build, exécution, linters) ;
- Clôture d'une fonctionnalité majeure ou bascule d'état (ex. de Prototype à Développement) ;
- Nouvelle convention durable ou contrainte structurante ;
- Changement de la prochaine grande étape de reprise.
*INTERDIT d'en faire un journal de développement ou de le modifier à chaque commit.*

### 9.4 Protocole de synchronisation externe (`CHATGPT_SYNC`)

Lorsqu'un agent modifie matériellement un fichier de contexte portable (`CAP_WORKFLOW_IA.md` ou `PROJECT_CONTEXT.md`), il applique rigoureusement le protocole déclaratif `CHATGPT_SYNC` articulé en deux temps :

#### A. Avant commit (Handoff / Présentation pour Review ou Staging)
Pendant la phase de travail, le contexte peut encore évoluer au fil des revues et des corrections. L'agent émet un signal de mise en attente :

```text
CHATGPT_SYNC :
STATUT : EN_ATTENTE_COMMIT

FICHIER :
[CAP_WORKFLOW_IA.md | PROJECT_CONTEXT.md]

ANCIENNE_VERSION :
[ancienne Context-Version]

VERSION_CANDIDATE :
[nouvelle Context-Version]

RAISON :
[explication concise du changement structurel]

ACTION_UTILISATEUR :
AUCUNE POUR L'INSTANT
```

#### B. Après validation du commit (Commit terminé)
Dès lors que le commit est validé et scellé dans Git, l'agent avertit explicitement l'humain que le fichier de contexte a divergé de la Source présente dans ChatGPT :

```text
CHATGPT_SYNC :
REQUISE : OUI

FICHIER :
[CAP_WORKFLOW_IA.md | PROJECT_CONTEXT.md]

ANCIENNE_VERSION :
[ancienne Context-Version]

NOUVELLE_VERSION :
[nouvelle Context-Version commitée]

RAISON :
[explication concise du changement structurel]

ACTION_UTILISATEUR :
Remplacer manuellement l’ancienne Source ChatGPT par cette version commitée.
```

- **Pour `CAP_WORKFLOW_IA.md` :** remplacer la Source dans chaque projet ChatGPT actif utilisant ce résumé (ex. projet AI-Workflow, projet gestion-personnes, etc.).
- **Pour `PROJECT_CONTEXT.md` :** remplacer la Source uniquement dans le projet ChatGPT correspondant.

#### Règle d'or : Absence de faux état interne
> **INTERDIT** de stocker un état du type `CHATGPT_SYNCED=true` dans le dépôt Git.
> Le dépôt ne peut ni ne doit présumer des actions réelles de l'utilisateur dans une interface externe tierce. Le dépôt sait uniquement : *contexte modifié et commité → synchronisation externe requise par l'humain*.

#### Remplacement humain sans plomberie
Aucun daemon, watcher, script réseau ou appel API OpenAI n'est toléré. L'action consiste en un remplacement manuel par l'humain dans les paramètres de son projet ChatGPT.

---

## 10. Adaptateurs spécifiques aux outils

Certains éléments doivent rester spécifiques aux outils.

Exemples :

```text
CLAUDE.md
AGENTS.md
GEMINI.md
settings.json
config.toml
hooks.json
ExecPolicy
Hooks propriétaires
Skills natives
Subagents
commandes natives de Review
permissions
syntaxe de configuration
noms des modèles
niveaux d'effort
```

Ces éléments sont considérés comme des **adaptateurs**.

Ils peuvent évoluer rapidement.

Le cœur universel du Workflow ne doit pas dépendre directement de leur forme actuelle.

---

## 11. Tests de conformité portables

Le protocole universel existe dans `tests/TESTS_UNIVERSELS.md`. Ce document d’architecture n’en recopie pas la matrice ni les verdicts.

~~~text
tests/TESTS_UNIVERSELS.md
        ↓
protocole commun
        ↓
adaptateur testé
        ↓
tests/<outil>/REQUALIFICATION.md
        ↓
verdicts et preuves propres à l’outil
~~~

Les tests universels vérifient les garanties communes. Les tests techniques spécifiques vérifient leur implémentation par chaque adaptateur.

Un nouvel outil réutilise donc le protocole commun, puis conserve ses résultats dans son propre fichier de requalification.

## 12. Architecture provisoire globale

```text
                         HUMAIN
                           │
                           ▼
                    AI_WORKFLOW.md
              règles universelles du travail
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
 PROJECT_CONTEXT.md                 Politiques / procédures
 contexte du projet                    universelles
          │                                 │
          └────────────────┬────────────────┘
                           │
                           ▼
                      ADAPTATEURS
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   Claude Code            Codex          Futurs outils
        │                  │          Gemini / OpenCode / ...
        ▼                  ▼                  ▼
 mécanismes Claude    mécanismes Codex   mécanismes natifs
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                Même cycle de développement
```

---

## 13. Architecture possible du dépôt à terme

Cette organisation est une direction de réflexion, pas encore une structure définitive :

```text
AI-Workflow/
│
├── AI_WORKFLOW.md
├── PLAN_MAITRE.md
├── architecture/PORTABLE.md
│
├── modeles-projet/
│   ├── PROJECT_CONTEXT.md
│   └── claude/CLAUDE.md
│
├── procedures/
│   ├── PREPARER_COMMIT.md
│   └── CLOTURER_BRANCHE.md
│
├── politiques/
│   ├── GIT.md
│   ├── CONTEXTE.md
│   └── REVIEW.md
│
├── adaptateurs/
│   ├── claude/
│   ├── codex/
│   ├── gemini/
│   └── opencode/
│
└── tests/
    ├── TESTS_UNIVERSELS.md
    ├── claude/
    ├── codex/
    ├── gemini/
    └── opencode/
```

Cette structure ne doit pas être créée intégralement tant que les mécanismes de plusieurs outils n'ont pas été testés.

Le risque serait de construire trop tôt une abstraction qui ne correspondrait pas aux besoins réels.

---

## 14. Méthode d'intégration d'un nouvel outil

Pour chaque nouvel outil ou nouvelle génération de modèles :

```text
1. comprendre ses mécanismes natifs ;
2. identifier ce qu'il sait faire ;
3. identifier ses limites ;
4. tester réellement ses mécanismes ;
5. comparer son comportement aux principes universels ;
6. créer l'adaptateur minimal nécessaire ;
7. éviter de modifier le cœur si un adaptateur suffit ;
8. modifier l'architecture universelle seulement lorsqu'un enseignement est réellement général.
```

On ne cherche donc pas à forcer tous les outils à fonctionner exactement de la même manière.

On cherche à obtenir **les mêmes garanties et le même cycle logique** avec les meilleurs mécanismes disponibles dans chaque outil.

---

## 15. Principe de portabilité

Une bonne architecture doit permettre :

```text
Claude aujourd'hui
       │
       ▼
Codex demain
       │
       ▼
Gemini plus tard
       │
       ▼
Autre système futur
```

sans devoir reconstruire les éléments fondamentaux :

```text
AI_WORKFLOW.md
PROJECT_CONTEXT.md
cycle Git
politique de sécurité
responsabilités
principes de Review
validation
décision humaine
```

Les modèles sont remplaçables.

Les mécanismes natifs évoluent.

Les adaptateurs évoluent.

Les principes du Workflow doivent rester aussi stables que possible.

---

## 16. Règle d'évolution de l'architecture

Nous devons éviter deux extrêmes :

### Trop spécifique

```text
Workflow
└── dépend complètement de Claude/Codex
```

Conséquence : chaque changement d'outil impose une reconstruction.

### Trop abstrait

```text
Workflow
└── abstractions construites avant de connaître les outils réels
```

Conséquence : complexité inutile et architecture théorique difficile à maintenir.

### Direction retenue

```text
Mécanisme réel
      │
      ▼
Test
      │
      ▼
Compréhension
      │
      ▼
Détection d'un principe général
      │
      ▼
Intégration éventuelle au cœur portable
```

Nous généralisons donc **après observation**, et non avant.

---

## 17. Planification automatique par rôle

> **Statut : hypothèse architecturale à tester**

La planification ne devrait pas nécessairement dépendre du « mode Plan » propre à un outil.

L'architecture portable peut plutôt définir un rôle logique :

    Planificateur

L'orchestrateur décide, selon la complexité de la demande, si une phase de planification spécialisée est nécessaire.

Schéma provisoire :

    Demande utilisateur
            │
            ▼
       Orchestrateur
        │        │
        │        └── tâche simple ───────► Exécution
        │
        └── planification nécessaire
                    │
                    ▼
               Planificateur
                    │
                    ▼
                  Plan
                    │
                    ▼
               Orchestrateur
                    │
                    ▼
                 Exécution
                    │
                    ▼
                Validations
                    │
                    ▼
                  Review

Le rôle `Planificateur` peut utiliser un modèle, un niveau d'effort ou un agent différent de celui utilisé pour l'exécution.

L'objectif est de permettre par exemple :

    Planification
    → modèle plus puissant / effort supérieur

    Exécution
    → modèle adapté au développement courant

    Exploration
    → modèle rapide ou économique

    Review
    → Reviewer indépendant ou mécanisme natif

Le choix de déclencher la planification doit rester principalement sémantique : l'orchestrateur évalue si la tâche nécessite réellement un plan.

On évite donc une règle déterministe du type :

    chaque demande → mode Plan

Le comportement recherché est plutôt :

    tâche simple
    → pas de planification spécialisée

    tâche complexe, ambiguë ou structurante
    → délégation automatique au Planificateur

Cette abstraction présente plusieurs avantages :

- elle ne dépend pas du bouton ou du mode Plan d'un outil particulier ;
- elle permet d'utiliser des modèles différents selon les rôles ;
- elle évite de consommer inutilement un modèle puissant pour les tâches simples ;
- elle peut être adaptée aux mécanismes natifs de Claude Code, Codex, Gemini, OpenCode ou d'autres outils ;
- elle reste compatible avec une activation manuelle du mode Plan lorsqu'elle est utile.

### Points à tester

Avant de considérer cette architecture comme validée, il faudra vérifier :

1. si l'orchestrateur reconnaît correctement une tâche nécessitant une planification ;
2. s'il peut déléguer automatiquement au Planificateur ;
3. si le Planificateur peut utiliser un modèle ou un effort différent ;
4. si le plan revient correctement à l'orchestrateur ;
5. si l'exécution reprend ensuite avec le rôle d'exécution normal ;
6. si le Reviewer reste indépendant de la phase de planification ;
7. si les tâches simples évitent correctement cette délégation ;
8. si cette architecture fonctionne de manière comparable sur plusieurs outils.

Cette possibilité devra être testée séparément sur chaque adaptateur avant d'être intégrée définitivement au Workflow universel.

---

## 18. Unités de travail et demandes indépendantes

Une session de développement reste liée à une unité de travail cohérente. La règle universelle appartient à `AI_WORKFLOW.md` ; ce document décrit seulement son architecture portable.

~~~text
nouveau prompt
├── lié à l’unité courante       → continuer normalement
└── clairement indépendant       → signaler la sortie d’unité
                                   → recommander une nouvelle session
                                   → STOP
~~~

La détection reste sémantique : ni mots-clés ni Hook ne remplacent la compréhension du contexte. Les petites digressions ne justifient pas automatiquement une nouvelle unité.

Le protocole de test est `J1` dans `tests/TESTS_UNIVERSELS.md`. Le verdict d’un adaptateur appartient uniquement à `tests/<outil>/REQUALIFICATION.md` ; `PORTABLE.md` ne conserve aucun verdict propre à Codex, Claude Code ou un autre outil.

---

## 19. État de l’architecture portable

Cette architecture définit les responsabilités communes et les points d’adaptation, mais ne possède pas l’état d’avancement des outils.

~~~text
règles universelles        → AI_WORKFLOW.md
protocole de test          → tests/TESTS_UNIVERSELS.md
preuves par adaptateur     → tests/<outil>/REQUALIFICATION.md
état général du projet     → PLAN_MAITRE.md
~~~

Un adaptateur futur peut encore révéler un angle mort. Dans ce cas : vérifier qu’il est réellement universel, modifier le propriétaire approprié, puis requalifier seulement les mécanismes et preuves invalidés.

---

## Noyau d’orchestration portable — direction à consolider

Cette section décrit une architecture cible issue des observations de requalification. Elle ne remplace pas encore les règles universelles tant que les tests restants ne sont pas terminés.

### Arbre de travail compact

~~~text
demande
  ↓
Orchestrateur
  ├── tâche simple / délégation sans gain net
  │      └── traitement direct
  │
  ├── exploration volumineuse
  │      └── Explorateur
  │
  ├── implémentation ou correction non triviale
  │      └── Exécuteur / Worker
  │
  └── Review indépendante requise
         └── Reviewer
~~~

La délégation n’est jamais automatique du seul fait qu’un fichier doit être modifié. Elle est utilisée lorsque l’isolation, la spécialisation ou l’économie de contexte apporte plus de valeur que son coût.

Le Principal conserve l’orchestration, les décisions et les preuves ; il ne reproduit pas le travail déjà correctement délégué.

### Chargement progressif du contexte

Le principal conserve seulement le noyau d’orchestration et l’état utile de l’unité en cours.

Les détails sont chargés à la demande :

~~~text
besoin de préparer un commit
→ charger la procédure/Skill de préparation du commit

besoin de clôturer
→ charger la procédure/Skill de clôture

besoin d’une règle spécialisée
→ charger seulement la règle concernée

aucun besoin
→ ne pas charger le détail
~~~

Les sous-agents ne reçoivent pas l’historique complet par défaut.

Ils reçoivent une mission minimale suffisante :

- objectif ;
- périmètre ;
- état de référence ;
- contraintes utiles ;
- validations attendues ;
- forme du retour.

### Registre d’état et de preuves

L’orchestrateur maintient un résumé compact de l’état connu.

Exemple conceptuel :

~~~text
ÉTAT
HEAD              = <hash Git>
diff-stagé        = <empreinte>
diff-working-tree = <empreinte>
dépendances       = <empreinte si pertinente>

PREUVES
tests ciblés      = OK @ <état>
build             = OK @ <état>
Review            = PRÊTE @ <état>
diff-check        = OK @ <état>
~~~

Principe :

**une preuve reste réutilisable tant que l’état et les dépendances pertinentes sur lesquels elle repose n’ont pas changé.**

Si l’état change, invalider seulement les preuves réellement affectées et revalider de manière différentielle.

Un hash ou une empreinte ne remplace pas le contenu d’une preuve ; il sert à rattacher cette preuve à un état précis.

### Corrections ciblées

Lorsqu’un reviewer identifie un problème, le handoff vers le worker doit être ciblé :

~~~text
finding
→ fichier / zone / nature du problème
→ correction ciblée
→ validation affectée
→ recontrôle du finding et de son impact
~~~

Éviter de relancer une exploration, une implémentation ou une Review complète si le changement ne le justifie pas.

### Traces détaillées et retour compact

Les traces détaillées restent consultables dans le thread de l’agent concerné lorsqu’elles apportent de l’auditabilité.

Le retour vers le principal doit rester compact, par exemple :

~~~text
Résultat          : terminé
Fichiers          : A, B, C
Validation        : 17 tests OK
État              : <empreinte>
Problème ouvert   : aucun
Décision requise  : aucune
~~~

Le but est de conserver la transparence sans recopier inutilement dans le contexte principal les lectures, logs, diffs et sorties déjà disponibles ailleurs.

### Directive de continuation

Formulation portable candidate :

> Continue le cycle normal de l’unité de travail en cours jusqu’au prochain point nécessitant une décision ou une autorisation humaine.

Cette directive autorise la progression normale du Workflow, mais ne constitue jamais une autorisation implicite pour une mutation sensible.

### Agents spécialisés

Le noyau actuel visé reste :

~~~text
Principal / Orchestrateur
├── Explorer
├── Worker / Exécuteur
└── Reviewer indépendant
~~~

Codex dispose nativement de `worker` et `explorer`.
Claude Code et Antigravity couvrent ces rôles via leurs mécanismes de sous-agents ou d'outils dédiés (`Explore`, `Plan`, `general-purpose`, `ai-reviewer` ; `research`, `self`).

D’autres agents spécialisés ne doivent être ajoutés qu’après observation d’un besoin concret.

### Architecture universelle de Review et de Preuves

Le modèle détaillé de Review indépendante et de gestion des preuves est porté par :

```text
architecture/REVIEW_ET_PREUVES.md
```

Il formalise les garanties portables communes à tous les adaptateurs :
1. **Séparation Rôle vs Capacité :** L'`AI-Reviewer` est strictement non-implémenteur (interdiction de modifier le code reviewé). Il peut néanmoins exécuter des validations dynamiques ciblées si son runtime le permet, les caches éphémères (`.pytest_cache`, `target/`, etc.) ne constituant pas une mutation de code source.
2. **Modèle universel de preuve :** Tuple auditable à 6 champs (`ETAT`, `COMMANDE`, `PERIMETRE`, `RESULTAT`, `PRODUCTEUR`, `CONTEXTE`).
3. **Escalade proportionnée (N0 à N4) :** De l'analyse statique zéro-runtime (N0) à la réutilisation stricte des preuves sur l'`ETAT` (N1), puis validation ciblée (N2), délégation de preuve (N3) et constat de défaut (N4).
4. **Fonction d'Exécuteur de preuve :** Lorsque le Reviewer opère dans une sandbox fermée sans terminal d'exécution, un exécuteur tiers (Principal ou implémenteur) produit la preuve brute sans jamais usurper le verdict de Review.
5. **Contrat universel d'adaptateur :** Déclaration neutre des capacités (`reviewer_independant`, `reviewer_peut_executer_validation`, `reviewer_peut_modifier_source`, etc.) permettant à chaque adaptateur d'implémenter nativement les invariants du Workflow.

### Architecture universelle des autorisations et modèle de confiance

Le contrat universel des périmètres d'autorisation est porté par :

```text
architecture/AUTORISATIONS.md
```

Il formalise le principe portable fondamental :
- **Mêmes garanties de permissions ≠ même configuration technique.**
- Chaque adaptateur préserve les mêmes frontières universelles via ses mécanismes natifs propres : autonomie fonctionnelle (travail nécessaire dans le périmètre convenu, dépendances requises, réseau de travail, écritures convenues), décision humaine explicite (barrières Git du Workflow, clôture de branche, extension réelle de périmètre, publication/déploiement) et interdictions strictes (secrets sans instruction/nécessité autorisée, destruction, bypass).

---

## Politique souple de dispatch multi-fournisseurs

Cette section constitue la **source principale** formalisant l'articulation et les critères de choix entre les fournisseurs de l'écosystème cible actif : **Claude Code**, **Codex** et **Antigravity**. Grok est sorti de l'écosystème actif ; son adaptateur et son historique sont conservés.

Elle prolonge les rôles universels et le noyau d'orchestration portable en définissant des affinités par défaut souples, sans enfermer aucun outil dans un rôle exclusif ni introduire de routeur ou de complexité automatique.

### 1. Affinités naturelles des fournisseurs

Les affinités ci-dessous représentent des prédispositions techniques et fonctionnelles observées, et non des frontières rigides.

> **Règle fondamentale : AFFINITÉ ≠ RÔLE OBLIGATOIRE.**
> Aucun fournisseur n’est enfermé dans une fonction unique.

#### Claude Code
- **Affinités naturelles :**
  - Principal / orchestrateur naturel ;
  - travail transversal ;
  - planification et coordination multi-axes ;
  - délégation proportionnée à ses sous-agents natifs.
- **Souplesse opérationnelle :**
  - peut également implémenter ;
  - peut reviewer le travail d'un autre fournisseur (Reviewer dédié `ai-reviewer`) ;
  - peut exécuter d’autres rôles si la tâche le justifie.

#### Codex
- **Affinités naturelles :**
  - implémentation technique substantielle ;
  - résolution de bugs ;
  - refactorings ;
  - écriture et exécution de tests ;
  - modifications multi-fichiers bien bornées ;
  - audits techniques du code ;
  - plans techniques et exécution disciplinée d’un plan compris et validé.
- **Souplesse opérationnelle :**
  - peut reviewer (notamment via son lanceur en sandbox de lecture seule) ;
  - peut explorer ;
  - peut orchestrer lorsque cela est pertinent.

#### Antigravity
- **Affinités naturelles :**
  - Review indépendante et challenge (second regard critique, audit contradictoire, recherche de régressions) ;
  - recherche et exploration ;
  - intégration globale de l'environnement de développement ;
  - synchronisation source/runtime.
- **Souplesse opérationnelle :**
  - peut également implémenter ;
  - peut orchestrer lorsque cela est pertinent ;
  - peut exécuter d’autres rôles si la tâche le justifie.

---

### 2. Critères de choix

Le choix d'un fournisseur pour une unité de travail doit rester proportionné, souple et pragmatique. Il prend en compte conjointement :

1. **Nature de la tâche :** conception d'ensemble, refactoring de code, audit contradictoire, implémentation bornée, etc.
2. **Capacités nécessaires :** exécution dynamique terminal, sandbox fermée, recherche web, analyse multi-fichiers.
3. **Mécanismes natifs utiles :** subagents éphémères, profil de lecture seule, modes de planification intégrés.
4. **Périmètre :** localisé, transverse, mono-composant ou modifiant l'architecture.
5. **Complexité :** niveau d'abstraction requis, risque technique, ambiguïté des interfaces.
6. **Besoin d’indépendance :** degré de séparation requis pour le contrôle et la Review.
7. **État du quota disponible :** facteur d'ajustement supplémentaire.

> **Le quota ne décide jamais seul.** Il ne constitue jamais un critère d'arbitrage unique ni un motif de bascule automatique.

---

### 3. Review croisée et degrés d'indépendance

Le Workflow préserve en toute circonstance son invariant universel :

> **AUTEUR ≠ REVIEWER** (le reviewer ne modifie jamais le code source reviewé et opère dans un contexte d'exécution isolé).

#### Paires naturelles indicatives

Les associations ci-dessous représentent des paires naturelles courantes, sans former une matrice rigide obligatoire :

- **Claude Code implémente** → Antigravity ou Codex peuvent reviewer.
- **Codex implémente** → Antigravity ou Claude Code peuvent reviewer.
- **Antigravity implémente** → Codex ou Claude Code peuvent reviewer.

#### Degrés d'indépendance

L'indépendance d'un Reviewer s'articule selon trois degrés croissants :

- **NIVEAU 1 — Contexte frais / agent distinct dans le même système :**
  - Contexte d'exécution neuf (ex. subagent éphémère `research` ou session propre sans reprise de contexte).
  - Suffisant pour les unités locales, les petites modifications et les retouches de documentation.
- **NIVEAU 2 — Session ou processus distinct :**
  - Processus ou conteneur isolé assurant une séparation d'environnement et de mémoire (ex. lanceur autonome en sandbox read-only).
  - Adapté aux unités standards et aux refactorings de composants délimités.
- **NIVEAU 3 — Fournisseur différent (cross-provider) :**
  - Indépendance renforcée grâce à la diversité de modèle, d'heuristiques, de harness et de fournisseur.
  - Particulièrement adapté aux changements architecturaux sensibles, aux audits contradictoires d'hypothèses et aux diagnostics complexes.
  - **Non obligatoire pour chaque petite unité :** le cross-provider apporte une garantie forte mais ne doit pas être imposé systématiquement pour toute modification triviale.

---

### 4. Gestion qualitative du quota

La gestion du quota repose exclusivement sur une appréciation qualitative humaine, sans seuil chiffré ni automatisation de routage :

- **CONFORTABLE :**
  - Utilisation normale selon les affinités naturelles.
- **CONTRAINT :**
  - Limiter les explorations ou délégations secondaires coûteuses en contexte ;
  - Réserver le fournisseur aux tâches où sa valeur technique est réelle.
- **TRÈS CONTRAINT :**
  - Considérer un fournisseur alternatif techniquement adapté pour l'unité, sous réserve que la qualité technique reste suffisante.

> **Aucun seuil numérique.** Aucun fallback automatique. Aucun routeur maison. Aucune surveillance automatique.

---

### 5. Principes d'anti-rigidité

Le Workflow exclut formellement les rigidités et automatismes suivants :

- **Pas d'enfermement dogmatique :** interdiction de figer les rôles (« Codex = toujours coding », « Antigravity = toujours Review », « Claude Code = toujours Principal »).
- **Pas de choix par benchmark brut :** interdiction de décider uniquement sur un score de benchmark abstrait.
- **Pas de bascule automatique selon quota :** aucun basculement implicite ou non sollicité.
- **Pas de duplication inutile :** interdiction d'envoyer la même tâche à plusieurs fournisseurs sans justification technique concrète.
- **Pas de vote artificiel entre modèles :** la fiabilité découle de preuves matérielles vérifiées sur l'`ETAT` Git et du contrôle humain, jamais d'un consensus statistique ou d'un vote majoritaire de LLM.

Le chemin retenu doit être le **chemin minimal suffisant**.

---

### 6. Rôle central et pilotage humain

La décision finale demeure strictement humaine.

Principe personnel fondamental préservé :

> **« Je ne délègue jamais à une IA une tâche ou une décision technique que je ne comprends pas. »**

- **Le Workflow peut :** proposer, exécuter, reviewer, apporter des preuves vérifiables.
- **L’humain conserve exclusivement :**
  - la compréhension technique des choix et du code ;
  - l’arbitrage de conception et de méthode ;
  - la validation du plan court avant toute modification lorsque requise ;
  - les décisions et autorisations sur les mutations Git sensibles (`git add`, `git commit`, `git push`, clôture `merge/rebase`) ;
  - l'arbitrage final sur les constats de Review (*findings*).

L'architecture portable ne rend ChatGPT ou aucun autre assistant externe obligatoire : elle reste pleinement autonome et portable.

---

## Progression, blocage et escalade des agents — direction à consolider

### Suivi compact des sous-agents

L’orchestrateur ne doit pas relire les fichiers, les diffs ou les tests uniquement pour savoir où en est un sous-agent.

Il demande d’abord directement son état.

Format conceptuel :

~~~text
STATUT : WORKING | BLOCKED | DONE
Terminé :
En cours :
Blocage :
Prochaine étape :
État / empreinte :
~~~

Pendant qu’un `worker` ou un `explorer` travaille, le principal évite de reproduire son travail ou de surveiller sa progression en relisant le projet.

Une inspection directe par le principal reste possible lorsqu’une vérification ciblée est réellement nécessaire.

### Protocole `BLOCKED`

Un agent peut :

- retenter une erreur transitoire ;
- essayer plusieurs approches réellement différentes ;
- effectuer les diagnostics nécessaires à sa tâche.

Il ne doit cependant pas boucler indéfiniment sur un problème sans progrès.

Après plusieurs tentatives substantielles infructueuses, il rend la main avec un état compact :

~~~text
STATUT : BLOCKED

Objectif :
Travail déjà réalisé :
Blocage précis :
Tentatives effectuées :
Preuves / erreurs :
Besoin recommandé :
~~~

L’orchestrateur décide ensuite de la suite.

Options possibles :

~~~text
BLOCKED
├── nouvelle piste ciblée avec le même agent
├── Explorer pour contexte manquant
├── Reviewer pour diagnostic indépendant
├── décision humaine
└── escalade ponctuelle de modèle
~~~

### Reviewer comme diagnosticien

Le reviewer peut ponctuellement inspecter un travail bloqué sans devenir l’exécuteur.

Son diagnostic cible uniquement :

- ce qui est déjà correct ;
- la cause probable du blocage ;
- les hypothèses erronées éventuelles ;
- le périmètre réellement concerné ;
- la correction ou l’investigation recommandée ;
- les validations à refaire.

Il ne relance pas automatiquement une Review complète du projet.

Après diagnostic :

~~~text
Reviewer
→ Orchestrateur
→ décision
→ Worker ou agent adapté
~~~

### Escalade ponctuelle de modèle

Une montée de modèle est une exception.

Elle ne devient jamais automatiquement le nouveau niveau normal de la session.

Politique candidate :

~~~text
modèle normal
→ blocage ou complexité démontrée
→ proposition d’escalade
→ raison + périmètre + modèle visé
→ autorisation humaine par défaut
→ utilisation ponctuelle
→ retour compact
→ retour automatique au modèle normal
~~~

Tant qu’une catégorie d’escalade automatique n’a pas été testée réellement et explicitement autorisée, elle nécessite une décision humaine.

Même une première montée doit demander une autorisation lorsque son périmètre est :

- large ;
- ambigu ;
- potentiellement coûteux ;
- susceptible d’impliquer plusieurs agents ou une partie importante du projet.

Une éventuelle automatisation future devra rester limitée à des catégories très précises et préalablement validées.

Une catégorie devient exécutable automatiquement, dans les bornes de son autorisation, seulement lorsqu’elle est à la fois :

1. techniquement qualifiée pour le mécanisme utilisé (preuve runtime consignée dans la requalification de l’outil) ;
2. explicitement autorisée par l’humain.

Cette autorisation ne s’étend jamais implicitement à un autre fournisseur, modèle, niveau d’effort ou catégorie. Elle conserve les propriétés ci-dessous (signal concret, périmètre borné, retour au niveau normal, aucune escalade par confort, pour la seule longueur ou le seul nombre de fichiers) et n’affaiblit aucune barrière Git ni aucune autre décision humaine matérielle. Chaque adaptateur définit ses catégories autorisées ; exemple : adaptateur Claude, sous-agent natif `sonnet` → `opus` décidé par le Principal sur signal concret.

### Propriétés obligatoires d’une escalade

Toute escalade doit être :

- exceptionnelle ;
- justifiée ;
- limitée à un problème précis ;
- temporaire ;
- suivie d’un retour au modèle normal ;
- journalisée ;
- auditable.

Le modèle supérieur reçoit un handoff ciblé :

~~~text
objectif
état / empreinte
blocage
tentatives déjà effectuées
erreur ou finding précis
fichiers concernés
preuves disponibles
résultat attendu
~~~

Il ne recommence pas toute l’exploration ou l’implémentation sans justification.

### Journal des escalades

Chaque montée de modèle doit laisser une trace exploitable pour un audit périodique.

Format conceptuel :

~~~text
Date       : <horodatage>
Outil      : <Codex / Claude Code / ...>
Agent      : <principal / worker / explorer / ...>
De         : <modèle normal>
Vers       : <modèle supérieur>
Motif      : <raison précise>
Périmètre  : <finding / fichiers / étape>
Autorisé   : <humain / politique automatique validée>
Résultat   : <résolu / partiel / échec>
Retour     : <modèle normal>
~~~

L’objectif est de pouvoir auditer sur plusieurs semaines ou plusieurs mois :

- le nombre de montées ;
- leur fréquence ;
- les modèles utilisés ;
- les agents qui les demandent ;
- les motifs ;
- leur utilité réelle ;
- les escalades inutiles ou excessives.

### Planification avec modèle supérieur

L’escalade destinée à résoudre un blocage et la planification avec un modèle supérieur sont deux mécanismes distincts.

L’architecture future conserve l’hypothèse :

~~~text
tâche réellement complexe
→ modèle supérieur en Plan mode
→ construction du plan
→ retour au modèle normal
→ exécution par les agents adaptés
~~~

Cette stratégie n’est actuellement ni considérée comme implémentée ni comme validée.

Elle devra faire l’objet de tests dédiés afin de vérifier :

- qu’une tâche simple ne provoque pas de montée inutile ;
- qu’une tâche complexe justifie réellement le Plan supérieur ;
- que la descente de modèle a effectivement lieu après le plan ;
- que l’exécution reste sur les modèles normaux lorsqu’ils suffisent ;
- que l’orchestrateur n’abuse pas progressivement du modèle supérieur ;
- que toute automatisation respecte la politique de quota et de journalisation.

## Sources maintenues et fichiers installés

Les fichiers statiques créés et contrôlés par le Workflow mais exécutés hors du dépôt doivent avoir une source maintenue dans `AI-Workflow`.

La distinction fondamentale est :

~~~text
source maintenue
→ fichier conservé et modifié dans AI-Workflow

fichier installé
→ copie réellement utilisée par l’adaptateur sur la machine
~~~

La version installée n’est pas la source de maintenance.

Pour un adaptateur donné, le cycle normal devient :

~~~text
1. modifier la source dans le dépôt
2. valider la source
3. tester le mécanisme concerné
4. installer ou remplacer la copie hors du dépôt
5. vérifier que source et installation correspondent
6. requalifier les mécanismes concernés si nécessaire
7. exécuter les contrôles d’environnement
8. accepter un nouvel état de référence uniquement si cela est justifié
~~~

Cette règle évite qu’un fichier installé soit modifié localement puis oublié lors de la maintenance du dépôt.

Elle permet également d’utiliser Git comme historique réel des fichiers qui constituent les adaptateurs.

### Fichiers possédés conjointement

Certains fichiers ne sont pas entièrement contrôlés par le Workflow.

Exemples :

~~~text
config.toml
.zshrc
fichiers de configuration ou d’état maintenus par l’outil externe
~~~

Ces fichiers ne doivent pas être remplacés par une copie complète du dépôt.

Le dépôt conserve seulement :

- les paramètres appartenant réellement au Workflow ;
- les invariants que l’installation doit respecter ;
- les instructions nécessaires pour les appliquer ou les vérifier.

Le fichier réel reste sous le contrôle conjoint de l’outil externe, de la machine et du Workflow.

### États et données exclus

Les éléments dynamiques ne deviennent jamais des sources maintenues :

~~~text
secrets
authentification
sessions
caches
mémoires dynamiques
état interne
plugins ou capacités fournis par l’éditeur
données temporaires
~~~

L’objectif n’est pas de figer l’environnement complet de l’outil.

L’objectif est de rendre reproductible et maintenable uniquement la partie appartenant réellement au Workflow.

### Budget de contexte runtime

Les éléments chargés systématiquement au démarrage doivent rester nettement plus courts que la documentation complète de l’adaptateur.

Pour le bootstrap principal d’un adaptateur, l’heuristique de maintenance est :

~~~text
règles globales de l’adaptateur
+ Workflow universel acquis au démarrage
≤ environ 150 lignes de runtime permanent
~~~

Ce seuil de `150 lignes` est une **heuristique de maîtrise du contexte**, pas un garde-fou de sécurité ni une condition bloquante du Workflow.

S’il est dépassé durablement, la première réponse doit être de déplacer les explications, exemples, preuves et procédures détaillées vers la documentation chargée à la demande.

Les règles indispensables au comportement correct restent dans le runtime ; la documentation explicative n’y est pas ajoutée uniquement pour éviter une lecture ultérieure.

### Audit de maintenabilité par le modèle

La portabilité ne suffit pas : un adaptateur doit également rester compréhensible et maintenable par un futur modèle travaillant à partir du dépôt.

L’audit doit donc vérifier périodiquement qu’un modèle peut retrouver la méthode de maintenance correcte à partir de l’architecture et de la documentation actuelles.

Le contrôle porte sur les **invariants de maintenance**, pas sur une suite figée de commandes.

Pour un fichier statique contrôlé par le Workflow, le modèle doit notamment reconnaître que :

~~~text
le dépôt contient la source maintenue
la copie hors dépôt est l’installation exécutée

évolution
→ modifier la source
→ valider et tester
→ installer
→ vérifier la synchronisation
→ requalifier ce qui est réellement affecté
→ vérifier l’état final réel
~~~

Pour un fichier possédé conjointement avec l’outil externe, le modèle doit reconnaître l’exception correspondante.

Exemple :

~~~text
configuration-workflow.json
→ paramètres appartenant au Workflow

config.toml
→ fichier réel possédé conjointement
→ modification minimale
→ jamais remplacé intégralement par le manifeste
~~~

La méthode exacte peut évoluer avec le Workflow.

Un audit futur ne doit donc pas rejeter une meilleure méthode uniquement parce qu’elle diffère historiquement de celle utilisée lors de la création de l’adaptateur.

Le verdict doit répondre à la question :

> La stratégie proposée respecte-t-elle les sources de vérité, les responsabilités des fichiers, les garde-fous et le cycle de validation actuellement définis par le dépôt ?

### Candidat temporaire pour une évolution critique

Pour un composant dont une erreur peut casser, contourner ou affaiblir le Workflow, la modification ne commence pas directement dans la source maintenue.

Exemples typiques :

~~~text
garde-fou de commandes
règles d’autorisation
lanceur de Review
script d’installation critique
~~~

Avant toute expérimentation, vérifier d’abord que la source maintenue et l’installation correspondent.

~~~text
source != installation
→ STOP
→ comprendre et réconcilier la divergence

source == installation
→ création possible d’un candidat temporaire
~~~

Le candidat temporaire est créé **à partir de la source maintenue du dépôt**, jamais à partir de la copie installée.

Le cycle recommandé devient :

~~~text
source maintenue
        ↓
copie temporaire isolée
        ↓
modification du candidat
        ↓
tests du candidat
        ↓
candidat suffisamment validé
        ↓
report de la modification dans la source maintenue
        ↓
validation de la source
        ↓
installation
        ↓
validation intégrée
        ↓
requalification affectée
        ↓
contrôle final de l’état réel
~~~

Le candidat temporaire permet d’expérimenter sans transformer immédiatement la source de vérité en zone de travail instable.

Il ne devient jamais une troisième source canonique.

### Validation en trois niveaux

Pour un composant critique, distinguer trois niveaux :

~~~text
1. candidat temporaire
   → la modification envisagée fonctionne isolément

2. source du dépôt
   → la modification intégrée dans la source canonique est valide

3. installation
   → la version réellement exécutée fonctionne dans son environnement réel
~~~

Une réussite du candidat ne dispense donc jamais de revalider la source après intégration, puis l’installation après déploiement.

### Nettoyage du candidat

Le candidat et son dossier temporaire sont transitoires.

Ils sont supprimés uniquement lorsque le cycle de maintenance est entièrement terminé avec succès, notamment lorsque les contrôles pertinents établissent :

~~~text
source validée
installation synchronisée
tests concernés réussis
requalification concernée validée
documentation mise à jour si nécessaire
contrôles finaux sans anomalie
~~~

À ce moment :

~~~text
candidat temporaire
→ devenu inutile
→ suppression
~~~

Si le cycle échoue ou reste incomplet, le candidat peut être conservé temporairement pour le diagnostic.

Sa présence ne change jamais la source de vérité : la source maintenue reste celle du dépôt.

Le nettoyage doit viser uniquement le dossier temporaire créé pour cette unité de maintenance et ne doit jamais utiliser une suppression large ou ambiguë.

### Proportionnalité

Le candidat temporaire n’est pas obligatoire pour toute modification.

Pour un changement documentaire ou un composant à faible risque, modifier directement la source maintenue puis la valider peut être plus proportionné.

Le modèle doit donc évaluer le risque du composant et du changement avant de choisir la stratégie.
