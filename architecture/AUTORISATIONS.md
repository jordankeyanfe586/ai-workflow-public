# Architecture universelle : Périmètres d'Autorisation et Modèle de Confiance

Ce document constitue la référence architecturale détaillée du Workflow IA pour la définition des périmètres d'autorisation, les frontières de sécurité et le modèle de confiance, applicables de façon portable à tous les agents de développement (Antigravity, Claude Code, Grok, Codex, Gemini, etc.).

---

## 1. Principes Fondateurs et Modèle de Confiance

Le Workflow IA formalise une séparation claire entre le travail de développement ordinaire et les frontières de sécurité matérielles :

### 1.1 Le projet de confiance (*Workspace*)
Lorsqu'un utilisateur ouvre un dépôt comme espace de travail de développement, il accorde explicitement sa confiance à ce projet :
- L'utilisateur accepte que le code de ce dépôt soit lu, analysé, compilé, testé et exécuté par l'agent.
- L'agent doit pouvoir accomplir l'ensemble du cycle de développement normal de façon autonome, sans sollicitation humaine permanente pour des opérations ordinaires et qualifiées.

### 1.2 L'environnement externe protégé
Tout ce qui se situe hors du projet de confiance est réputé protégé par défaut :
- Les lectures externes utiles et non sensibles (SDK, compilateurs, bibliothèques système, documentation locale, configuration de développement) sont autonomes.
- Toute écriture, modification de fichier ou altération d'état hors du workspace relève impérativement d'une décision humaine explicite, sauf dans les cas expressément nécessaires à la tâche et circonscrits à son périmètre fonctionnel convenu (ex. synchronisation de configuration d'adaptateur déclarée). L'autonomie technique d'accès au système de fichiers ne constitue jamais une autorisation d'étendre arbitrairement les écritures externes.

### 1.3 Les secrets et identifiants
Les clés privées, jetons d'accès, mots de passe et fichiers d'identifiants (`~/.ssh`, `~/.aws`, jetons de cloud, etc.) sont strictement hors du périmètre automatique :
- Ils sont bloqués autant que les capacités du runtime de l'outil le permettent.
- L'agent ne doit jamais tenter d'y accéder de sa propre initiative.

### 1.4 La limite matérielle de l'exécution transitive
Tout système d'autorisation applicatif (qu'il s'agisse de filtrage d'outils, d'interception d'appels ou de listes blanches/noires) présente une limite universelle :
- Les règles d'autorisation interceptent les **actions directes** de l'agent (appels d'outils natifs, commandes explicites soumises au terminal).
- Elles ne constituent pas une sandbox physique étanche des **sous-processus descendants** : une commande autorisée (ex. suite de tests de tests exécutant un script projet, compilation lançant un binaire tiers) peut exécuter des sous-processus qui ne repassent pas par le moteur de permissions de l'agent.
- Par conséquent, la sécurité repose fondamentalement sur la **confiance accordée au projet ouvert**. Les restrictions d'accès réduisent l'exposition directe de l'agent mais ne doivent jamais être présentées comme une étanchéité absolue face à un code hostile exécuté dans le workspace.

---

## 2. Les Trois Niveaux de Frontière Universelle

L'architecture organise les opérations logiques en trois niveaux de décision immuables :

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    NIVEAUX DE PÉRIMÈTRE D'AUTORISATION                     │
├───────────────────┬────────────────────────────────────────────────────────┤
│ 1. AUTONOME       │ Opérations régulières et déterministes du cycle de dev │
│                   │ -> Exécution directe sans interruption humaine         │
├───────────────────┼────────────────────────────────────────────────────────┤
│ 2. DÉCISION       │ Actions sensibles, modifications d'état externe ou     │
│    HUMAINE        │ mutations durables -> Accord explicite préalable       │
├───────────────────┼────────────────────────────────────────────────────────┤
│ 3. BLOQUÉ         │ Opérations destructrices, perte irrémédiable de        │
│                   │ données, accès aux secrets ou contournement de règles  │
└───────────────────┴────────────────────────────────────────────────────────┘
```

### 2.1 Périmètres autonomes (Sans interruption)
Les opérations suivantes sont autonomes dès lors qu'elles sont nécessaires à la tâche et comprises dans le périmètre convenu :

1. **Cycle de développement normal :**
   - Lecture, navigation et recherche de fichiers du workspace.
   - Édition normale de code source et de fichiers du projet.
   - Compilation et construction du projet (*build*).
   - Exécution des tests unitaires et d'intégration ciblés.
   - Analyse statique, linter, vérification de types (*type-check*) et validation de syntaxe.
   - Reproduction contrôlée de bogues et diagnostics locaux.
   - Exécution des scripts de validation internes au projet.
   - Génération normale d'artefacts de build et caches éphémères.
2. **Gestion des dépendances nécessaires :**
   - Installation, ajout, mise à niveau ou suppression de paquets et dépendances nécessaires à l'objectif courant dans le périmètre du projet.
3. **Réseau de travail nécessaire :**
   - Téléchargements de dépendances, paquets ou outils utiles à la tâche.
   - Opérations Git distantes en lecture (`fetch`, `clone`).
   - Requêtes HTTP d'observation ou de consultation d'API publiques requises pour le développement.
4. **Écritures externes convenues :**
   - Création ou modification de fichiers hors workspace déjà expressément comprises dans le périmètre fonctionnel convenu de l'unité (ex. synchronisation déclarée de fichiers d'adaptateur ou de configuration d'environnement).
5. **Consultation de l'environnement local :**
   - Lectures externes non sensibles : SDK, runtimes (Python, Node, Rust, JDK, Go), manuels, configuration d'outils de développement (`~/.gitconfig`, `~/.cargo/config.toml`, configuration du Workflow sous `~/.ai-workflow`).
6. **Recherche et consultation Web publiques :**
   - Recherche d'informations techniques sur des moteurs publics (documentation officielle, RFC, issues, API).
   - Lecture de ressources Web publiques par requêtes HTTP en lecture seule.
7. **Inspection Git et branches de travail :**
   - Commandes d'observation (`git status`, `git diff`, `git log`, empreinte Git matérielle).
   - Création ou bascule sur une branche de travail locale, hors procédure spécifique de clôture.

### 2.2 Périmètres soumis à décision humaine (Validation explicite)
Les opérations suivantes exigent une validation humaine explicite préalable (mise en œuvre selon les capacités de l'outil par un point d'arrêt déclaratif `STOP` dans le dialogue ou par une invite native interactive `ASK` lorsque le runtime la gère) :

1. **Barrières Git fonctionnelles du Workflow :**
   - **Staging (`git add`) :** Présentation du périmètre précis à stager.
   - **Commit (`git commit`) :** Présentation de l'unité stagée, preuves rattachées, verdict de Review et message proposé.
   - **Publication (`git push`) :** Présentation de la branche, révision et remote cible si une publication est envisagée.
2. **Opérations de clôture de branche :**
   - Fusion (`merge`), rebasage (`rebase`), bascule vers la branche cible post-merge, et suppression de branche locale (`git branch -d`).
3. **Extension réelle de périmètre hors workspace :**
   - Écritures ou altérations hors workspace non convenues initialement dans le plan validé, nécessitant un plan révisé et un accord explicite.
4. **Publication et déploiement externe :**
   - Déploiements cloud, publication de paquets ou d'artefacts vers des registres externes, transmission de données vers un service externe.

### 2.3 Périmètres interdits ou bloqués (Interdiction stricte)
Les opérations suivantes sont formellement interdites universellement et bloquées par le runtime lorsque ses capacités le permettent :

1. **Secrets et identifiants :**
   - Recherche opportuniste, lecture, affichage, modification ou transmission de clés privées, jetons de production, répertoires d'identifiants (`~/.ssh`, `~/.aws`, `~/.gnupg`, Keychains) ou fichiers d'environnement sensibles, sans instruction humaine explicite ou nécessité expressément autorisée par la tâche.
   - Exfiltration de données privées (interdiction absolue).
2. **Opérations destructrices :**
   - Suppression irréversible de l'historique Git (`git reset --hard`, suppression forcée de branche non mergée `git branch -D`).
   - Commandes destructives récursives non bornées sur le système (`rm -rf /`, `rm -rf ~`, suppressions récursives hors périmètre).
3. **Contournement et Bypass :**
   - Utilisation d'interpréteurs inline pour contourner les règles (`python3 -c "..."`, `bash -c "..."` non qualifiés, encodage base64 pour masquer des commandes).
   - Utilisation de drapeaux ou mécanismes désactivant, contournant ou neutralisant les protections du runtime ou du Workflow (interdiction universelle stricte ; l'adaptateur applique un verrouillage technique `DENY` si son runtime le permet, ou documente de façon transparente l'absence de verrouillage matériel sans prétention de garantie technique inexistante).

### 2.4 Minimalité d'exécution et conservation des frontières

Pour préserver la fluidité opérationnelle du développement sans dégrader les contrôles de sécurité :

1. **Mécanismes directs et proportionnés :** Pour toute opération intrinsèquement autonome (lecture, inspection, validation, test, build, lint, édition normale), l'agent privilégie le mécanisme direct, natif ou atomique minimal suffisant.
2. **Élimination de la complexité évitable :** Les compositions shell avancées (pipelines `|`, substitutions de commande `$()`, `awk`, `sed`, `xargs` ou interpréteurs) sont évitées lorsqu'un mécanisme direct ou une option native de l'outil suffit à l'objectif. Ces outils ne font pas l'objet d'une interdiction dogmatique : ils demeurent légitimes lorsqu'ils sont réellement nécessaires à la tâche, mais sont proscrits lorsqu'ils introduisent une complexité inutile.
3. **Règle de minimalité face aux blocages ou invites évitables :** Si une opération dont la nature est autonome déclenche une invite ou un blocage technique uniquement en raison d'une construction technique ou d'un outil intermédiaire évitable, l'agent revient immédiatement à la forme atomique qualifiée.
4. **Conservation absolue des frontières :** Cette simplification est réservée aux opérations de nature autonome. Il est **STRICTEMENT INTERDIT** de chercher une reformulation technique, un alias ou un découpage dans le but d'éviter une validation humaine obligatoire sur les barrières Git fonctionnelles (staging `git add`, `commit`, `push` conditionnel), les mutations de clôture de branche (`merge`, `rebase`, `branch -d`), l'extension réelle de périmètre, ou de contourner une règle `DENY`. Une permission technique AUTO ne lève jamais une barrière fonctionnelle.

---

## 3. Contrat Universel de Capacités d'Adaptateur

Chaque adaptateur d'outil IA formalise sa prise en charge des garanties universelles via un contrat déclaratif de capacités :

```json
{
  "$schema": "https://ai-workflow.invalid/schemas/adapter-authorizations-v1.json",
  "adaptateur": "nom-outil",
  "contrat_capacites_autorisations": {
    "projet_confiance_supporte": true,
    "lecture_locale_autonome": true,
    "lecture_externe_non_sensible_autonome": true,
    "recherche_web_autonome": true,
    "lecture_web_autonome": true,
    "dev_local_autonome": true,
    "tests_autonomes": true,
    "build_autonome": true,
    "git_lecture_autonome": true,
    "git_mutation_controlee": true,
    "dependances_controlees": true,
    "reseau_externe_controle": true,
    "ecriture_externe_controlee": true,
    "secrets_proteges": true,
    "destruction_bloquee": true,
    "bypass_bloque": true,
    "permissions_heritees_par_subagents": true,
    "limites_connues": {
      "execution_transitive_hors_moteur": true,
      "portee_bac_a_sable": "description_du_confinement_disponible"
    }
  }
}
```

Ce contrat décrit des **capacités fonctionnelles**, sans jamais imposer la syntaxe technique propre à un outil particulier.

---

## 4. Convention pour les Futures Adaptations

Pour intégrer ou mettre à jour un outil IA (Grok, Codex, Claude Code, Gemini, futur agent), la méthode de qualification suit un protocole normé en 5 étapes :

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                    PROTOCOLE DE QUALIFICATION D'OUTIL                      │
├────────────────────────────────────────────────────────────────────────────┤
│ 1. LECTURE DES GARANTIES      architecture/AUTORISATIONS.md                │
│                               -> Assimilation des périmètres requis        │
├────────────────────────────────────────────────────────────────────────────┤
│ 2. INVENTAIRE NATIF           Analyse des capacités natives actuelles de   │
│                               l'outil (moteur de règles, sandbox, etc.)    │
├────────────────────────────────────────────────────────────────────────────┤
│ 3. TESTS SENTINELLES          Exécution d'un jeu d'épreuves minimal        │
│                               (dev autonome, blocage secret, ask mutation) │
├────────────────────────────────────────────────────────────────────────────┤
│ 4. MAPPING DÉCLARATIF         Documenter chaque capacité du contrat :      │
│                               SATISFAIT | PARTIEL | NON SUPPORTE | ALTERNATIF│
├────────────────────────────────────────────────────────────────────────────┤
│ 5. OPTIMISATION NATIVE        Déployer l'approche native la plus sobre     │
│                               sans artifice shell superflu                 │
└────────────────────────────────────────────────────────────────────────────┘
```

Grâce à ce protocole, une mise à jour d'un outil n'exige jamais de réécrire la politique de sécurité : il suffit de réévaluer son mapping face aux garanties universelles immuables.

Les URL de schéma en `.invalid` ci-dessus sont des exemples de structure, pas des schémas publiés ou téléchargeables.
