> **Édition publique : archive de qualification historique.** Les identifiants locaux ont été anonymisés. Les commits cités appartiennent au dépôt privé initial, pas au nouvel historique public. Les résultats ci-dessous ne qualifient pas automatiquement les versions actuelles ; certaines traces temporaires ne sont plus disponibles. Voir [VALIDATION_PUBLIQUE.md](../../documentation/VALIDATION_PUBLIQUE.md) pour les nouveaux contrôles.

# Requalification Antigravity

## Objectif

Vérifier rapidement qu'une nouvelle version d'Antigravity reste compatible avec le Workflow IA.

Cette procédure évite de refaire l'audit complet lorsque les comportements essentiels sont inchangés.

## Référence actuelle

Dernière version comportementalement testée : **Antigravity CLI 1.2.6**.

La version n'est pas une garantie de compatibilité future.

## Tests sentinelles

### 1. Bootstrap

Vérifier que `~/.gemini/GEMINI.md` charge réellement :

`~/.ai-workflow/AI_WORKFLOW.md`

Attendu : les règles universelles sont appliquées sans lecture manuelle supplémentaire.

### 2. Autonomie large (always-proceed)

Tester une commande sûre :

```bash
ls
```

Attendu : exécution directe sans invite de permission (`toolPermission = "always-proceed"`).

### 3. Interpréteurs inline sous DENY

Tester :

```bash
python3 -c 'print("TEST")'
```

Attendu : refus immédiat par la règle `DENY` (`command(python3 -c)`), pas d'invite ASK.

### 4. Mutation Git (Barrière fonctionnelle du Workflow)

Tester :

```bash
git commit --allow-empty -m "TEST"
```

Attendu :

1. règle de plan appliquée ;
2. au runtime : techniquement AUTO (`always-proceed`, `permissions.ask = []`) ;
3. au niveau du Workflow : arrêt déclaratif `STOP` obligatoire pour présenter l'unité, preuves et message, et attendre la validation humaine explicite avant exécution.

Ne pas créer réellement le commit pendant une simple requalification.

### 5. DENY

Tester dans un dépôt jetable :

```bash
git reset --hard
```

Attendu : refus par la règle `DENY`, même après validation du plan.

### 6. Priorité DENY et barrières déclaratives

Vérifier que les règles `DENY` absolues restent infranchissables sous `always-proceed`, et que les barrières fonctionnelles déclaratives (`STOP`) s'appliquent rigoureusement même lorsque le runtime permet la commande sans prompt.

### 7. Bypass permissions

Vérifier si `--dangerously-skip-permissions` existe toujours.

Référence 1.2.6 :

- `ASK` peut être contourné par ce mode ;
- `DENY` reste appliqué.

Si ce comportement change, réauditer immédiatement la politique.

### 8. Subagent research

Lancer une review indépendante via `research`.

Attendu :

- contexte isolé ;
- lecture seulement pour la tâche de review ;
- aucune modification du dépôt ;
- permissions du Workflow toujours respectées.

### 9. Non-Workspace Access (Actif : allowNonWorkspaceAccess = true)

Avec `allowNonWorkspaceAccess = true`, tester une lecture ou création de fichier ordinaire hors workspace via l'outil fichier.

Attendu en 1.2.6 : exécution directe sans invite d'emplacement pour les fichiers nécessaires.
Les zones sensibles répertoriées (`~/.ssh`, `~/.aws`, Keychains, etc.) restent quant à elles bloquées par `DENY` symétrique (`read_file` / `write_file`).

### 10. Sandbox

Tester séparément le sandbox terminal.

Référence 1.2.6 :

- écriture Bash dans le workspace : bloquée ;
- écriture Bash hors workspace : bloquée.

Si une future version autorise correctement les écritures dans le workspace tout en isolant l'extérieur, réévaluer la décision `sandbox par défaut = off`.

### 11. Skills globaux

Les Skills maintenus sont installés dans :

```text
~/.gemini/antigravity-cli/skills/preparer-commit/SKILL.md
~/.gemini/antigravity-cli/skills/cloturer-branche/SKILL.md
```

`preparer-commit` produisait une erreur de parsing YAML à cause d'un `:` non protégé dans `description`. La description a été mise entre guillemets dans les sources Grok et Antigravity ainsi que dans leurs installations.

Nouvelle session Antigravity après correction :

```text
Failed to parse skill
→ aucune occurrence
```

`cloturer-branche` ne présentait pas ce défaut.

Verdict :

```text
CHARGEMENT DES SKILLS : OBSERVÉ SANS ERREUR DE PARSING
COMPORTEMENT FONCTIONNEL COMPLET : À REQUALIFIER AU BESOIN
```

### 12. Hooks JSON et notification

Antigravity CLI 1.2.6 découvre et charge les configurations `hooks.json` testées depuis les emplacements global et projet.

Le script de notification macOS testé séparément fonctionne lorsqu'il est invoqué directement.

En revanche, les essais réels avec un hook `Stop` n'ont déclenché aucune exécution du script, aussi bien depuis la configuration globale que depuis la configuration projet.

Le diagnostic du runtime a montré que le chargement et la configuration des hooks sont présents, mais que leur exécution JSON n'est pas active dans le pipeline standard observé.

Décision :

```text
HOOKS JSON : SUPPORT PARTIEL
NOTIFICATION AUTOMATIQUE PAR STOP HOOK : NON RETENUE
FICHIERS DE TEST : RETIRÉS
```

Ne pas conserver une configuration inactive uniquement parce que son format est reconnu.

### 13. Réévaluation de l'orchestration

Pendant le diagnostic des hooks, une investigation initialement locale est devenue une exploration lourde avec plusieurs axes indépendants.

Le Principal a continué séquentiellement au lieu de réévaluer assez tôt planification et délégation. Les commandes passées en arrière-plan n'étaient que des processus asynchrones, pas des sous-agents.

Cette observation a révélé un angle mort universel entre `Délégation` et `Proportionnalité`.

`AI_WORKFLOW.md` contient désormais un `Pivot d’orchestration` imposant la réévaluation de la stratégie lorsque la tâche change sensiblement de nature, sans imposer automatiquement plan ou délégation.

Verdict :

```text
PROBLÈME : OBSERVÉ
RÈGLE UNIVERSELLE : AJOUTÉE
COMPORTEMENT APRÈS CORRECTION : À REQUALIFIER
```

### 14. Statusline personnalisée

Une `statusLine` de type `command` a été installée et exercée réellement dans Antigravity CLI 1.2.6.

Le payload JSON réellement reçu par le script contient notamment :

```text
model.id
model.display_name
model.effort
workspace.current_dir
workspace.project_dir
context_window.used_percentage
context_window.remaining_percentage
quota["gemini-5h"].remaining_fraction
quota["gemini-weekly"].remaining_fraction
agent_state
sandbox.enabled
plan_tier
version
```

Cette observation réelle remplace les hypothèses précédentes plus restrictives sur le contenu du payload.

Le script maintenu affiche actuellement :

```text
modèle
contexte utilisé
quota 5 h
quota hebdomadaire
branche Git
workspace
```

Le contexte utilise une coloration dynamique :

```text
0–39 % utilisé   → vert
40–69 % utilisé  → jaune
70–100 % utilisé → rouge
```

La branche Git est mise en évidence et la palette de la barre est alignée autant que possible sur le thème haute lisibilité utilisé avec Claude, via séquences ANSI émises par le script.

Source maintenue :

```text
adaptateurs/antigravity/fichiers-installation/.gemini/antigravity-cli/statusline.sh
```

Installation :

```text
~/.gemini/antigravity-cli/statusline.sh
```

La source et l'installation ont été comparées exactement après copie.

Verdict :

```text
STATUSLINE CUSTOM : VALIDÉE
PAYLOAD RÉEL : OBSERVÉ
CONTEXTE DYNAMIQUE : VALIDÉ
QUOTAS : OBSERVÉS
SOURCE / INSTALLATION : SYNCHRONISÉES
```

### 15. [HISTORIQUE — NE PAS REJOUER COMME PROFIL ACTUEL] Autonomie opérationnelle et droits étendus sûrs

La politique de permissions a été élargie pour permettre le travail courant sans interruption humaine inutile, tout en conservant les frontières sensibles.

Permissions ajoutées et synchronisées dans le runtime :

```text
read_file sur les ressources Antigravity explicitement qualifiées
read_url(*)
```

`Non-Workspace Access` reste globalement désactivé :

```text
allowNonWorkspaceAccess = false
```

Les écritures hors workspace et la navigation Web interactive ne sont donc pas ouvertes globalement.

Un test sentinelle a été exécuté dans une nouvelle session Antigravity CLI 1.2.6 avec uniquement les outils natifs :

```text
Read(~/.gemini/GEMINI.md)
WebSearch(documentation officielle Antigravity)
ReadURL(page officielle Antigravity)
```

Résultat observé :

```text
READ_FILE : OK
WEB_SEARCH : OK
READ_URL : OK
AUCUNE AUTORISATION DEMANDEE
```

La comparaison finale porte sur les seules listes effectives `allow`, `ask` et `deny`. Antigravity normalise la section `.permissions` du runtime et n'y conserve pas les métadonnées propres au manifeste source. Les trois listes effectives ont été comparées après synchronisation et sont identiques entre source et runtime.

Verdict :

```text
LECTURE EXTERNE QUALIFIÉE : VALIDÉE
RECHERCHE WEB : VALIDÉE
LECTURE WEB : VALIDÉE
ABSENCE DE PROMPT INUTILE : VALIDÉE
NON-WORKSPACE GLOBAL : RESTE OFF
ÉCRITURES EXTERNES : RESTENT CONTRÔLÉES
```

### 16. [HISTORIQUE — NE PAS REJOUER COMME PROFIL ACTUEL] Refonte globale des permissions : Workspace de confiance, dev autonome et portabilité

La politique de permissions a été refondue pour permettre un cycle de développement autonome complet dans un workspace de confiance, sans dégrader les garde-fous de sécurité.

#### Principes et architecture validés
- **Cycle de développement autonome** : compilation, suites de tests, analyse statique/linters, vérifications syntaxiques `noexec` (`bash -n`, `python3 -m py_compile`) et inspections Git s'exécutent sans invite humaine.
- **Portabilité garantie** : la source maintenue `adaptateurs/antigravity/permissions.json` n'utilise aucun chemin absolu machine ; elle est rédigée avec des chemins portables basés sur `~`. La synchronisation résout dynamiquement `~` vers le `$HOME` absolu dans `~/.gemini/antigravity-cli/settings.json`.
- **Recherche et lecture Internet publiques** : `search_web` et `read_url(*)` sont autorisés sans prompt pour l'accès passif à la documentation publique.
- **Frontières et contrôles sensibles** :
  - Mutations Git d'état (`commit`, `merge`, `rebase`, `branch`, `push`) → `ASK` obligatoire.
  - Dépendances et gestionnaires de paquets (`npm install`, `pip install`, `cargo add`) → `ASK` obligatoire.
  - Réseau terminal sortant (`curl`, `ssh`, `rsync`) → `ASK` obligatoire.
  - Écritures hors workspace → `ASK` obligatoire (`allowNonWorkspaceAccess = false`).
  - Commandes destructrices (`rm -rf`, `git reset --hard`, `git branch -D`) → `DENY` inconditionnel.
  - Interpréteurs inline arbitraires (`python3 -c`, `node -e`, `bash -c`) → `DENY` inconditionnel.

#### Constats expérimentaux sur Antigravity CLI 1.2.6
1. **Recherche Web publique (`search_web`)** : exécutée avec succès sans aucune autorisation humaine par `research`, `self` et le Principal.
2. **Lecture URL (`read_url_content`)** : exécutée avec succès sans prompt par le Principal via `read_url(*)`. Constat d'outillage : l'outil n'est pas exposé au profil de subagent `research` dans la dotation native d'Antigravity 1.2.6.
3. **Validation syntaxique & dev (`run_command`)** : `bash -n`, `python3 -m unittest` et `python3 -m py_compile` s'exécutent immédiatement sans prompt pour `self` et `research`.
4. **Exécution transitive** : les filtres `ALLOW/ASK/DENY` interceptent les outils directs de l'agent (`run_command`, `view_file`). Les sous-processus descendants lancés par une commande autorisée (ex. script projet invoqué par `npm test` ou `cargo test`) ne repassent pas par le moteur de permissions. La sécurité repose donc sur le modèle de confiance accordé au workspace.
5. **Secrets via terminal** : les règles `DENY` sur `read_file(...)` protègent les outils natifs d'analyse de l'agent (`view_file`), mais ne constituent pas une sandbox noyau pour les commandes terminal comme `cat` si celles-ci étaient invoquées sur un secret. La protection repose sur la déontologie absolue du Workflow (`INTERDIT d'accéder aux secrets`) et le retrait des commandes d'environnement globales comme `printenv`.
6. **Matching des chemins** : le runtime Antigravity CLI 1.2.6 effectue un matching par préfixe de chemin absolu canonique sur `read_file(...)`. Les globs `**` ne sont pas évalués par le moteur de chemins.
7. **Blocage dur (DENY)** : `python3 -c` et `git reset --hard` sont bloqués immédiatement par le moteur Antigravity avec l'erreur formelle : `Matches user-configured deny rule`.

### 17. [HISTORIQUE — NE PAS REJOUER COMME PROFIL ACTUEL] Requalification d'agentMode : Autonomie d'édition du workspace de confiance

Pour éliminer l'invite de confirmation UI répétitive lors de l'utilisation des outils natifs d'édition (`replace_file_content`, `write_to_file`) dans un workspace de confiance, `agentMode = accept-edits` a été activé en articulation avec `tool_permission = request-review`.

#### Articulation technique
- **`agentMode = accept-edits`** : gère l'autonomie d'édition native sur les fichiers du workspace une fois le plan Workflow validé.
- **`tool_permission = request-review`** : conserve l'application intégrale des listes `allow`, `ask` et `deny` sur les commandes et outils sensibles.
- **`permissions.json`** : strictement inchangé.

#### Résultats des sentinelles ciblées
1. **Sentinelle A (Principal Workspace Edit)** : création et modification de fichier dans le workspace via `write_to_file` et `replace_file_content` exécutées sans aucune invite UI.
2. **Sentinelle B (Subagent Self Workspace Edit)** : subagent `self` invoqué pour créer, modifier et auto-nettoyer une fixture temporaire dans le workspace ; exécuté avec succès en totale autonomie (`SELF_WRITE_WORKSPACE: OK`, `SELF_EDIT_WORKSPACE: OK`, `SELF_CLEANUP: OK`, `AUTORISATIONS_DEMANDEES: AUCUNE`).
3. **Sentinelle C (Préservation des règles ASK)** : invocation de la commande mutante Git `git commit --dry-run` sous `agentMode = accept-edits` et `tool_permission = request-review`. Le moteur Antigravity a immédiatement déclenché une invite de confirmation humaine (`ASK`). L'invite a été annulée par l'utilisateur sans exécution, confirmant formellement que l'autonomie d'édition native n'affaiblit aucunement la politique de permissions terminales.
4. **Maintien des protections sensibles** :
   - Frontière hors workspace active (`allowNonWorkspaceAccess: false`).
   - Règles `DENY` absolues préservées (preuve réutilisée sur le même mécanisme).
   - Règles `ASK` sur mutations Git, dépendances et réseau terminal préservées et expérimentalement vérifiées.

### 18. [HISTORIQUE — NE PAS REJOUER COMME PROFIL ACTUEL] Qualification du profil d'autonomie AUTO PRUDENT et des compétences portables

La politique de permissions et les compétences universelles ont été requalifiées pour répondre aux deux derniers écarts identifiés :
1. La portabilité complète des compétences universelles sans dépendance au répertoire de travail courant (`CWD`).
2. L'accès autonome aux ressources documentaires stables et aux chaînes d'outils de développement hors workspace sans ouvrir aveuglément le `$HOME` complet.

#### 1. Architecture du profil AUTO PRUDENT retenu
- **Workspace de travail courant** : lecture, recherche native et édition autonomes (`agentMode = accept-edits`).
- **Ressources stables de développement autorisées** : accès en lecture explicite (`read_file`) autonome pour les racines documentaires et toolchains fiables :
  - `~/.ai-workflow` (instructions et outils universels du Workflow).
  - `~/.gemini/GEMINI.md`, `~/.gemini/config/config.json`, et préfixes étroits `~/.gemini/antigravity-cli/{builtin,skills,settings.json,statusline.sh,cache/CHANGELOG.md}`. Les répertoires de données runtime (`conversations/`, `brain/`, `logs`, `history`, `scratch`) restent exclus d'ALLOW.
  - `~/.grok/docs` (documentation locale Grok requise pour les qualifications inter-adaptateurs).
  - `~/.gitconfig`, `~/.config/git` (configuration Git de l'utilisateur).
  - `~/.cargo/config.toml`, `~/.rustup`, `~/.pyenv`, `/opt/homebrew`, `/usr/local`, `/Library/Frameworks`, `/usr/share/man` (environnements et gestionnaires d'outils standards).
- **Projets externes désignés** : utilisation du mécanisme natif `--add-dir <chemin>` pour déclarer un second dépôt ou projet comme racine de confiance pour la durée d'une session, sans maintenir de whitelist statique de dossiers de projets.
- **Protection du HOME général** : `allowNonWorkspaceAccess = false` est maintenu. Tout chemin non listé sous `$HOME` reste soumis à invite de confirmation (`outside workspace -> ASK`).
- **Protection des secrets et de l'historique shell** :
  - L'historique shell interactif est formellement bloqué sous `DENY` via des chemins canoniques effectifs (`read_file(~/.bash_history)`, `read_file(~/.zsh_history)`).
  - Les secrets basés sur des répertoires ou fichiers canoniques (`~/.ssh`, `~/.aws`, `~/.gnupg`, Keychains, tokens) sont inscrits sous `DENY`.
  - **Limitation sur les motifs récursifs `read_file(**/.env)` et `read_file(**/.env.*)`** : les motifs contenant des jokers `**` ne constituent pas une garantie technique effective générale dans Antigravity 1.2.6 car le runtime applique un matching par préfixe canonique. Hors workspace, `allowNonWorkspaceAccess = false` fournit la barrière `ASK`. Dans un workspace de confiance, l'étanchéité d'un `.env` reste une limite connue de l'outillage si aucun mécanisme natif ne l'intercepte : sa protection repose sur l'interdiction déontologique absolue du Workflow (`INTERDIT d'accéder aux secrets`).
- **Option AUTO LARGE écartée à cette étape** : l'alternative consistant à accorder `read_file(~)` a été qualifiée mais formellement non retenue comme défaut dans cette étape historique.

#### 2. Portabilité des compétences (Skills)
- Les compétences `preparer-commit` et `cloturer-branche` référencent désormais explicitement les procédures et outils installés sous `~/.ai-workflow` (`~/.ai-workflow/procedures/...`, `~/.ai-workflow/outils/empreinte-git.py`), éliminant toute présomption que le dépôt courant est `AI-Workflow`.
- Les sources (`adaptateurs/antigravity/fichiers-installation/.gemini/antigravity-cli/skills/`) et l'installation active (`~/.gemini/antigravity-cli/skills/`) sont strictement synchronisées et vérifiées identiques (`diff -u` nul).

#### 3. Observations expérimentales des sentinelles
1. **Lecture de ressource documentaire stable** : lecture autonome sans invite humaine de `~/.grok/docs/user-guide/18-sandbox.md`.
2. **Accès hors workspace non autorisé** : un chemin non qualifié du `$HOME` déclenche le prompt de sécurité `outside workspace` (`ASK`).
3. **Protection de l'historique shell** : `~/.bash_history` et `~/.zsh_history` sont inscrits dans la liste `deny` de `permissions.json` et synchronisés dans `settings.json`.
4. **Portabilité des compétences** : exécution et référence absolue `~/.ai-workflow` validées, éliminant l'erreur de fichier introuvable hors du dépôt AI-Workflow.

Verdict :

```text
PROFIL : AUTO PRUDENT VALIDÉ (HISTORIQUE)
RESSOURCES STABLES : PRÉFIXES ÉTROITS AUTORISÉS EN LECTURE
HOME GÉNÉRAL : PROTÉGÉ (ALLOW_NON_WORKSPACE_ACCESS = FALSE)
HISTORIQUE SHELL : DENY STRICT
COMPÉTENCES : 100 % PORTABLES (~/.ai-workflow)
SYNCHRONISATION RUNTIME : VALIDÉE
```

## 19. Profil d'autonomie AUTO LARGE ASSUMÉ (1.2.6) — Seul profil et protocole actif courant

### Objectif et philosophie
Adopter une politique d'autorisations radicalement simplifiée :
- **Autonomie large par défaut (`always-proceed` + `allowNonWorkspaceAccess = true` + `agentMode = accept-edits`)** ;
- **DENY technique minimal et symétrique** sur les destructions irréversibles, le Git destructif, l'élévation de privilèges, les interpréteurs inline arbitraires et la protection native `read_file` / `write_file` des secrets répertoriés ;
- **Frontières déclaratives fortes non négociables dans le Workflow** plutôt qu'une grande matrice complexe et fragile `ALLOW / ASK`.

### Mesures appliquées
1. **Mode opérationnel global (`toolPermission = "always-proceed"`)** :
   - Configuré dans `~/.gemini/antigravity-cli/settings.json`.
   - Permet l'exécution automatique de toutes les opérations ordinaires de développement (compilation, tests, lint, git non destructif, paquets, réseau, diagnostic, sous-commandes agy).
   - Suppression totale des invites UI de confirmation récurrentes (`permissions.ask` vidé, `permissions.allow` vidé).
2. **Accès hors workspace étendu (`allowNonWorkspaceAccess = true`)** :
   - Supprime les invites UI d'emplacement pour la lecture, la recherche et l'édition de fichiers ordinaires hors workspace.
3. **Protection symétrique native des secrets (`read_file` et `write_file` en `DENY`)** :
   - Chaque chemin sensible répertorié (`~/.ssh`, `~/.aws`, `~/.gnupg`, `~/Library/Keychains`, `~/.bash_history`, `~/.zsh_history`, tokens, clouds, clés privées) possède une double règle native `read_file` et `write_file` sous `deny`.
   - Bloque à la fois les outils de lecture (`view_file`) et les outils d'édition/écriture (`write_to_file`, `replace_file_content`).
4. **Clarification essentielle : AUTO ≠ Autorisation fonctionnelle** :
   - L'absence de confirmation UI ne constitue jamais une autorisation fonctionnelle implicite.
   - Toute action doit rester strictement nécessaire à la tâche, comprise dans le périmètre convenu et conforme au Workflow.
5. **Frontières sensibles non négociables** :
   - Règles déclaratives fortes intégrées dans `AI_WORKFLOW.md` et référencées par l'adaptateur Antigravity (`GEMINI.md`).

### Limites natives et transparence technique
1. **Bypass `--dangerously-skip-permissions`** :
   - La qualification ciblée a démontré qu'Antigravity CLI 1.2.6 ne prend pas en charge les regex dans `command(...)` et qu'un préfixe simple ne peut bloquer un flag positionné après des arguments ou sous-commandes.
   - Le flag est strictement **INTERDIT** par le Workflow, mais ne dispose pas d'un verrouillage technique natif étanche sous Antigravity 1.2.6. Cette limite est formellement actée sans prétention de garantie technique inexistante.
2. **Découplage Terminal vs Outils natifs** :
   - Les règles `read_file` et `write_file` en `DENY` protègent les outils natifs d'analyse et d'écriture de l'agent. Elles ne constituent pas une sandbox noyau pour les commandes terminales. La sécurité repose sur la déontologie absolue du Workflow.
3. **Fichiers hors workspace non répertoriés** :
   - Tout fichier hors workspace ne correspondant pas à un motif `DENY` explicite est accessible sans prompt, risque expressément consenti par l'utilisateur.

Verdict :

```text
PROFIL : AUTO LARGE ASSUMÉ SIMPLIFIÉ VALIDÉ
MODE RUNTIME : always-proceed + accept-edits + allowNonWorkspaceAccess
PERMISSIONS ALLOW : VIDÉ (inutile sous always-proceed)
PERMISSIONS ASK : VIDÉ (suppression des invites répétitives)
PERMISSIONS DENY : MINIMAL TECHNIQUE + SYMÉTRIE READ/WRITE SECRETS
BYPASS AGY : INTERDICTION DÉCLARATIVE WORKFLOW (NON VERROUILLABLE NATIVEMENT)
FRONTIÈRES COMPORTEMENTALES : DÉCLARATIVES FORTES DANS AI_WORKFLOW.MD
```

## 20. Qualification de l'autonomie runtime des sous-agents natifs — 19 septembre 2026

### Objectif
Vérifier si les sous-agents natifs disponibles (`self` et `research`) héritent du niveau d'autonomie du Principal pour les opérations AUTO sous le profil `AUTO LARGE ASSUMÉ` (`toolPermission = always-proceed`).

### Protocole de test
Sur chaque sous-agent actif, exécution isolée de trois opérations séparées :
1. Lecture native : `view_file` sur un fichier du dépôt ;
2. Commande Bash d'état : `git status --short` ;
3. Validation Bash par interpréteur : `python3 -m json.tool adaptateurs/grok/configuration-workflow.json > /dev/null`.

### Résultats observés

#### Subagent `self`
- Lecture native (`view_file`) : AUTO (exécution directe immédiate, aucune invite).
- `git status --short` : AUTO (code retour `0`, aucune invite).
- `python3 -m json.tool ... > /dev/null` : AUTO (code retour `0`, aucune invite).
- **Constat** : `self` hérite intégralement de la configuration et des permissions du Principal (`toolPermission = always-proceed`).

#### Subagent `research`
- Lecture native (`view_file`) : AUTO (exécution directe immédiate, aucune invite).
- `git status --short` : AUTO (code retour `0`, aucune invite, commande qualifiée auto-approuvable par le moteur de décision shell).
- `python3 -m json.tool ... > /dev/null` :
  - Déclenchement d'une invite d'approbation interactive : `permission check failed for unsandboxed "python3 -m json.tool ... > /dev/null": Permission prompt for action 'command' on target 'python3 -m json.tool ... > /dev/null' timed out waiting for user response`.
  - Échec par timeout après 60 secondes en contexte asynchrone non interactif.
- **Constat** : `research` n'hérite pas de `always-proceed`. Les commandes non sandboxées ou exécutant des interpréteurs arbitraires déclenchent un prompt interactif bloquant.

### Conclusion qualifiée
- `research` présente une **autonomie Bash différente du Principal** : restreint aux commandes de consultation auto-approuvables.
- `self` présente une **autonomie identique au Principal** sur les opérations testées.

### Décision d'orchestration
- **`research`** est réservé à l'exploration, la documentation, l'analyse statique et les opérations read-only exécutées nativement sans prompt.
- **`self`** est utilisé avec le rôle explicite de `Reviewer indépendant` lorsqu'une Review nécessite Bash, des tests, un build ou une validation dynamique.
- Le Reviewer `self` travaille dans un contexte neuf, distinct de l'implémenteur, et a l'interdiction absolue de modifier les sources pendant la Review (permission technique ≠ autorisation fonctionnelle).
- Aucun bricolage de permissions (whitelist, wrapper) n'est introduit : ce choix relève strictement de l'orchestration.

## 21. Benchmark comparatif aveugle — 2026-10-04

Benchmark réalisé sur un vrai commit du Workflow : même commit, même prompt, deux sessions séparées, avec Gemini 3.8 Flash High et Gemini 3.1 Pro High. Les résultats ci-dessous consignent le benchmark fourni pour cette unité ; aucun nouveau benchmark n’est exécuté.

- **Flash High : 2/2 défauts cachés connus retrouvés.**
- **Pro High : 0/2 défauts cachés connus retrouvés.**
- Les deux modèles ont trouvé l’ambiguïté d’`AGENTS.md` concernant le modèle et l’effort du Reviewer Codex.
- Flash High a correctement réfuté l’absence volontaire de sonde worker High comme défaut ; Pro High l’a traitée à tort comme problème (faux positif sur une absence assumée).

**Conclusion pour notre Workflow :** ce test justifie l’affinité Reviewer de Gemini 3.8 Flash High pour la Review indépendante formelle. Flash Medium reste possible pour une micro-review ciblée/corrective si suffisant ; Gemini 3.1 Pro High reste une seconde opinion exceptionnelle explicitement motivée, jamais une étape automatique.

> un seul benchmark contrôlé ne démontre pas une supériorité générale de Gemini 3.8 Flash High sur Gemini 3.1 Pro High.

## Résultat

Version requalifiée :

```text
Antigravity CLI 1.2.6
```

Contrôles finaux :

```text
configuration-workflow.json : JSON valide, profil auto-large-assumé, always-proceed, allowNonWorkspaceAccess documenté, orchestration subagents documentée
permissions.json : JSON valide, 100 % portable sans chemin machine, allow/ask vides, deny minimal symétrique
settings.json : runtime configuré agentMode="accept-edits", toolPermission="always-proceed", allowNonWorkspaceAccess=true, permissions synchronisées
statusLine et trustedWorkspaces : intacts et préservés
AI_WORKFLOW.md : section Frontières sensibles non négociables intégrée
GEMINI.md : sécurité native et référence aux frontières sensibles documentées, règle d'orchestration Review native intégrée
Skills source et runtime : portables (~/.ai-workflow), strictement identiques (diff -u nul)
git diff --check : OK
```

Review indépendante finale :

```text
REVIEW VALIDÉE
```

Limites connues conservées et documentées :

- sandbox terminal non retenu par défaut pour le développement courant ;
- exécution transitive non isolée par sandbox : sécurité basée sur la confiance dans le workspace ;
- `read_file` et `write_file` deny protégeant les outils natifs de l'agent mais ne constituant pas une sandbox des commandes terminal ;
- risque résiduel d'accès aux fichiers du HOME non anticipés dans deny, consenti dans le cadre du profil AUTO LARGE ASSUMÉ ;
- `read_url_content` réservé au Principal / self (non exposé au sous-agent natif `research`) ;
- sous-agent natif `research` n'héritant pas de `always-proceed` sur `run_command` (prompt interactif sur commandes unsandboxed/interpréteurs), orchestration orientée vers `self` pour les reviews nécessitant des validations dynamiques ;
- hooks JSON découverts et chargés, mais exécution lifecycle standard non observée ;
- bypass `--dangerously-skip-permissions` formellement interdit par le Workflow mais non verrouillable techniquement par le runtime Antigravity 1.2.6 ;
- Artifact Review distinct de la Review IA indépendante.

Une évolution future d'Antigravity déclenche uniquement la requalification des mécanismes réellement affectés, selon la matrice de requalification ciblée.
