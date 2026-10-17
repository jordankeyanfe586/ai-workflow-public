> **Édition publique : archive de qualification historique.** Les identifiants locaux ont été anonymisés. Les commits cités appartiennent au dépôt privé initial, pas au nouvel historique public. Les résultats ci-dessous ne qualifient pas automatiquement les versions actuelles ; certaines traces temporaires ne sont plus disponibles. Voir [VALIDATION_PUBLIQUE.md](../../documentation/VALIDATION_PUBLIQUE.md) pour les nouveaux contrôles.

# Migration différentielle GPT-6.1 Sol — 4 octobre 2026

Auteur : Codex. Review indépendante finale : Antigravity, effectuée avant staging.
Statut : **QUALIFICATION DIFFÉRENTIELLE OBTENUE — REVIEW FINALE ANTIGRAVITY VALIDÉE**.

## État et installation

Départ : `main`, HEAD `55ba592acf9b59485a586b06ca849596ae8f3853`,
ETAT `8454ef157efb65fcef2b` ; index et fichiers suivis propres.
PDF non suivi préexistant `modeles-projet/document-personnel-non-publie.pdf` préservé.
Branche créée : `migration/codex-gpt-6-1-sol`.
CLI réel : `/opt/homebrew/bin/codex`, `codex-cli 0.160.0`.
Le catalogue local de ce CLI expose `gpt-6.1-sol` et `low`, `medium`, `high`.

La configuration locale portait déjà Principal/Plan Sol 6.1 Medium, Review
Sol 6.1 et sous-agent Sol 6.1 Medium. Seul
`agents.default_subagent_reasoning_effort` a été modifié vers `low` ;
concurrence `3` et tous les autres paramètres ont été conservés.
Instructions installables et lanceur synchronisés par élévations natives approuvées.
Le lanceur pointait vers un binaire ChatGPT.app absent (RC=69, même pour `--help`).
Il résout maintenant une fois `codex` via le PATH, sans chemin Homebrew versionné.
Les contraintes read-only, approbation never et High imposé sont inchangées.

## Preuves runtime ciblées

Producteur : auteur Codex, sondes génériques distinctes sans outil ni édition.
Nouvelle session : `codex exec --strict-config --sandbox read-only --json`,
sans override modèle/effort ; RC=0, réponse `PRINCIPAL_OK`.
L’initialisation a nécessité une élévation native du processus parent après
`Operation not permitted` ; le sandbox de la session testée reste read-only.
Les identifiants ci-dessous renvoient aux traces locales `turn_context`.

| Rôle | Politique active | Preuve |
|---|---|---|
| Principal | GPT-6.1 Sol / Medium | Session `session-anonymisee-001`, tour `session-anonymisee-002` : modèle/effort confirmés |
| Plan | GPT-6.1 Sol / Medium | Nouvelle session CLI interactive `session-anonymisee-003`, `/plan`, tour `session-anonymisee-004` : mode plan, Medium, read-only ; plan d’une étape produit, sans exécution |
| Sous-agent défaut | GPT-6.1 Sol / Low | Enfant `session-anonymisee-005` de la nouvelle session, contexte neuf sans override : Low, read-only, `DEFAUT_OK` |
| Sous-agent escalade | GPT-6.1 Sol / Medium puis High | Spawn natif avec `fork_turns="none"`, `model="gpt-6.1-sol"`, `reasoning_effort="medium"` : enfant `session-anonymisee-006`, Medium, `MEDIUM_OK`. High supporté par le catalogue et le même champ d’override ; aucune sonde High redondante exécutée |
| Reviewer | GPT-6.1 Sol / High | `review-native-codex --uncommitted`, RC=0 ; session distincte `session-anonymisee-007`, tour `session-anonymisee-008` : `gpt-6.1-sol`, `high`, sandbox `read-only`, approbation `never` |
| Astra | exceptionnel | Preuves historiques conservées, non requalifié |
| Terra | historique uniquement | Anciennes preuves conservées intégralement |
| Luna | aucune politique | N/A |

Une sonde sans override lancée depuis la session auteur déjà ouverte a utilisé
Medium (enfant `session-anonymisee-009`). Elle établit la limite
de rechargement : le nouveau TOML ne migre pas rétroactivement une session ouverte.
Les événements JSONL de la sonde CLI ne suffisaient pas à établir le spawn ; la
trace enfant confirme néanmoins sa création, son parent et le défaut Low.

## Qualification Reviewer et validations

La première élévation pour `review-native-codex --uncommitted` avait été rejetée
avant exécution : la transmission du diff au service Codex n’était pas jugée
explicitement autorisée. L’humain a ensuite autorisé précisément cette commande
et cette transmission, uniquement pour la sonde de qualification du mécanisme.
Une élévation native a permis l’exécution du lanceur installé, sans contournement.

Commande exacte : `review-native-codex --uncommitted` ; producteur : auteur Codex.
Périmètre : diff non stagé courant de l’unité ; CLI `0.160.0`, résolu via PATH en
`/opt/homebrew/bin/codex`. Résultat : RC=0, stderr vide, sortie exploitable :

> Aucun défaut actionnable identifié dans les changements. Le verdict repose sur l’analyse statique et les preuves consignées ; la qualification runtime du nouveau lanceur de Review reste explicitement incomplète.

Cette dernière mention décrit le document reçu par la sonde avant ajout de sa
preuve ; elle ne contredit pas les observations de l’exécution maintenant terminée.
Le `turn_context` confirme le modèle `gpt-6.1-sol`, effort `high`, sandbox
`read-only` et `approval_policy="never"`. La session de Review native distincte
est identifiée dans le tableau ; aucune reprise du contexte auteur n’a été utilisée.
L’ETAT est resté `29e729a1e12fd244ef0f` avant et après la sonde : aucune mutation
du dépôt par le Reviewer observée. Sortie conservée dans `reviewer.txt` et
métadonnées dans `reviewer-observe.json`, sous `<repertoire-temporaire-historique>`.

Cette exécution établit uniquement la qualification technique du mécanisme.
Elle ne satisfait ni ne remplace la Review indépendante finale de l’unité :
Codex est l’auteur ; Antigravity conserve cette mission, dans un contexte neuf.
Aucune correction de source n’a été déduite de la sortie ; seul ce document
est actualisé pour consigner la preuve obtenue.

Contrôles réellement exécutés : JSON/TOML valides, tous les paramètres du manifeste
conformes au TOML, concurrence inchangée ; source/installation du lanceur et des
instructions identiques ; `sh -n` RC=0 ; `--help` RC=0 ; argument supplémentaire,
SHA invalide et absence de cible refusés avec RC=64 ; `git diff --check` RC=0.
Les sondes n’ont modifié aucun fichier suivi : ETAT `4616898b0f4b1373ed35`
après sondes, avant ajout de cette documentation de preuve.
Artefacts locaux : `<repertoire-temporaire-historique>` (JSONL Principal, réponse,
`modeles-observes.json`, `plan-observe.json`, schéma app-server 0.160.0).
Aucun benchmark, aucune comparaison Terra/Sol ou d’efforts, aucune requalification Astra.

---

# Requalification fonctionnelle ciblée — modèles Codex, 23 septembre 2026

Lors de ces sondes, le [manifeste versionné](../../adaptateurs/codex/configuration-workflow.json)
décrivait Principal et Reviewer natif `gpt-6-sol` / `high`, sous-agent par défaut
`gpt-5.6-terra` / `high`. Aucune comparaison de qualité ou de quota n'a été faite.
La décision ultérieure du 23 septembre plaçait Principal et Plan en `gpt-6-sol` /
`medium` ; ces preuves ne qualifiaient pas ce couple. Cette politique est désormais
historique ; la migration du 4 octobre est documentée séparément.

| Rôle | Preuve du mécanisme |
|---|---|
| Principal | Trace réutilisée `session-anonymisee-010` : `turn_context` `gpt-6-sol` / `high`. Aucun nouveau test Principal. |
| Plan | Unique tour `session-anonymisee-011` de la session CLI `session-anonymisee-012` : `collaboration_mode.mode=plan`, `model=gpt-6-sol`, `effort=high` ; dépôt read-only. Conforme à la sélection du Principal et à `plan_mode_reasoning_effort=high` dans cette configuration, sans tester une autre sélection. |
| Sous-agent par défaut | Preuve historique réutilisée du 19 septembre : enfant `session-anonymisee-013` sans override, `gpt-5.6-terra` / `high`. Défauts installés alors inchangés ; cette preuve ne compare pas les modèles actuels. |
| Sous-agent explicite | Un seul enfant avec `fork_turns="none"`, `model="gpt-6-sol"`, `reasoning_effort="high"` : trace `session-anonymisee-014`, `turn_context` `gpt-6-sol` / `high`. Lecture correcte des lignes 9–10 du manifeste, aucune édition. |
| Reviewer natif | Une seule exécution `review-native-codex --uncommitted`, RC=0. Session distincte `session-anonymisee-015`, tour `session-anonymisee-016` : `gpt-6-sol` / `high`, sandbox `read-only`, approbation `never`. Le verdict exploitable a pointé un état de synchronisation périmé dans `CONFIGURATION.md` et ce fichier (P2), corrigé ensuite sans relancer la Review. |

Avant la sonde Plan, `~/.codex/config.toml` portait encore
`review_model="gpt-5.6-sol"` (SHA-256 `5dbcf69a7d3ad87c54a3087e7467f3a661c8283a7a90fce325b1bbadd85e9a0f`).
Une édition ciblée l'a passé à `gpt-6-sol` ; TOML valide, Principal/Plan High,
Terra/High et valeurs d'approbation/sandbox contrôlés inchangés. SHA-256 après
édition et Review : `8153fdef2581560be8d48f0064b74fb71c51fba5b00b88104d3fdc769e59d5cd`.
La première empreinte précédait la session Plan : après restauration virtuelle de
la seule ligne `review_model`, les empreintes de fichier entier ne coïncident
pas. Une variation intermédiaire du fichier ne peut donc être exclue ; seule
l'édition ciblée et la préservation des valeurs contrôlées sont établies.

Le Reviewer a lu le diff non commité des quatre fichiers candidats et produit
son finding P2. L'ETAT Git est resté `f42dff37937d17bbc008` avant et après
chaque sonde runtime, y compris la Review ; aucune écriture du dépôt par ces
sondes n'a été observée. Une sortie exploitable ne prouve pas la supériorité de
GPT-6 Sol comme Reviewer. Les qualifications ci-dessous restent historiques.

---

# Requalification ciblée — modèles et concurrence

Micro-unité du 19 septembre 2026 ; référence `7a20ba85d72dbb5a75535142325c3243cb15c387`,
ETAT initial `cddd5815dfe8097b7d70`, `main` propre. Implémenteur : Codex ;
Review indépendante de ce delta à effectuer par Antigravity.

## Preuve native minimale

Version inchangée : `codex-cli 0.155.0-alpha.9`.
Nouvelle session `codex exec --strict-config`, sans override de modèle/effort,
terminée avec RC=0 ; un seul sous-agent avec `fork_turns="none"`, sans override,
réponse `TEMOIN_OK`. Aucune commande de travail ni mutation exécutée par ces agents.

| Observation native | Résultat |
|---|---|
| Principal, `turn_context` | `gpt-5.6-sol`, effort `high` |
| Enfant, `turn_context` | `gpt-5.6-terra`, effort `high` |
| Concurrence, contexte injecté | 3 places, Principal inclus : 2 enfants |
| Configuration | JSON/TOML valides ; clés maintenues conformes au runtime |
| Instructions | source et copie runtime strictement identiques |

Le générateur natif `codex debug prompt-input` confirmait déjà ce plafond avant
installation. Pas de test de saturation : aucun agent supplémentaire lancé pour
le provoquer. La sélection des paliers supérieurs repose sur les mécanismes natifs
et la règle d’orchestration ; aucun benchmark ou succès Astra n’est revendiqué.

Preuves locales conservées : `<repertoire-temporaire-historique>`
(`mission.txt`, `evenements.jsonl`, `resultat.txt`, `modeles-observes.json`).
Principal : `session-anonymisee-017`.
Enfant : `session-anonymisee-013`.

L’écriture du TOML a été contrôlée : seules les cinq valeurs de cette micro-unité
ont changé lors de l’installation. Les valeurs d’autorisation restent conformes
au profil qualifié ; `default.rules`, le lanceur, le socle universel et les autres
adaptateurs restent inchangés. Contrôle final : `git diff --check` et empreinte Git.
Les résultats ci-dessous appartiennent à l’unité d’autorisations précédente et
ne sont pas rejoués par cette micro-unité.

---

# Requalification Codex — modèle universel d’autorisations

Date : 19 septembre 2026. Version : `codex-cli 0.155.0-alpha.9`.
Implémenteur : Codex. Review indépendante finale : Antigravity, encore à effectuer.
Statut : **PRÊT POUR REVIEW ANTIGRAVITY**, sans verdict indépendant par Codex.

## Périmètre et état de départ

`main` ; HEAD `712603cef977` ; ETAT `6767465647b2395212e0` ; worktree propre.
Huit fichiers de l’adaptateur, de sa documentation et de cette requalification.
Aucun staging, commit, push, merge, rebase ou suppression de branche exécuté.
Aucune branche créée. Socle universel, autres adaptateurs et anciens laboratoires
inchangés. L’empreinte finale est remise dans le compte rendu pour éviter une
empreinte autoréférente dans le contenu qu’elle mesure.

## Configuration réellement chargée

Après synchronisation, nouvelle session native `codex exec` dans un workspace
temporaire, avec configuration utilisateur et règles conservées. Son
`turn_context` confirme : `approval_policy=on-request`,
`approvals_reviewer=auto_review`, `sandbox_policy.type=workspace-write`,
`network_access=true`. Profil effectif `managed` / `restricted`, réseau `enabled` ;
écritures limitées au workspace et aux temporaires, métadonnées protégées.
L’ancienne session principale n’est pas déclarée migrée par ce seul changement.

## ExecPolicy : évaluation native, sans mutation

Invocation : `codex execpolicy check --rules <default.rules versionné> -- <argv>`.
Les **17 cas** suivants ont tous rendu le résultat attendu (code retour 0) :

| Commande évaluée | Résultat |
|---|---|
| `git reset --hard HEAD` | `forbidden` |
| `git reset --soft HEAD` | aucune règle correspondante |
| `git clean -f`, `-fd`, `-df`, `-fx`, `-fdx` (5 cas) | `forbidden` |
| `git clean -n` | aucune règle correspondante |
| `git branch -D temoin` | `forbidden` |
| `git branch -d temoin` | aucune règle correspondante |
| `git worktree remove -f temoin`, `--force temoin` (2 cas) | `forbidden` |
| `git worktree remove temoin` | aucune règle correspondante |
| `git status --short` | aucune règle correspondante |
| `git add temoin` | aucune règle correspondante |
| `git commit -m temoin` | aucune règle correspondante |
| `git push origin main` | aucune règle correspondante |

Seul l’évaluateur a reçu ces argv : aucune des mutations listées n’a été exécutée.
L’absence de règle n’autorise pas fonctionnellement les opérations soumises à STOP.
Aucune couverture des formes non testées n’est revendiquée.
Le fichier contient uniquement quatre règles `forbidden`, sans `prompt` ni `allow`.

## Autonomie observée et sous-agent

Dans la nouvelle session : `cat temoin.json`, édition par `apply_patch`
(`initiale` → `validee`), `python3 -m json.tool temoin.json` et
`curl -I --max-time 20 https://developers.openai.com` réussis ; HTTP/2 200,
aucune élévation demandée. La requête publique suffit au test réseau : aucune
installation de dépendance ni opération Git distante inutile ajoutée.
Git read-only et `git diff --check` exécutés dans la session principale.
Aucun test de création de branche nécessaire pour ce delta.

Un seul sous-agent générique lancé avec `fork_turns="none"`, sans override :
lecture du témoin et `pwd` réussis, aucun fichier modifié. Son fil distinct,
son lien parent et `agent_role: null` sont attestés par les métadonnées natives.
Son `turn_context` confirme les mêmes approbations/sandbox/réseau ; modèle
`gpt-5.6-sol`, effort `high`. Les outils d’écriture sont annoncés, leur utilisation
n’a pas été provoquée. L’inventaire et la limite de sélection des types intégrés
sont documentés dans [CONFIGURATION.md](../../documentation/codex/CONFIGURATION.md).
Aucun agent personnalisé créé ; aucun lancement fictif des trois types documentés.

## Lanceur, STOP et installation

`sh -n` réussi ; `--help` réussi ; absence d’argument, override sandbox,
SHA invalide et argument supplémentaire à `--help` rejetés avec RC=64.
Le lanceur conserve les règles, `read-only` et l’effort `high`, avec
`approval_policy="never"` pour sa propre exécution. Aucun nouveau bypass.
Pas de Review Codex réelle rejouée ni de verdict indépendant émis pour cette unité.

Les instructions portent explicitement les STOP avant staging, commit, push
conditionnel et clôture, et renvoient au Workflow pour leurs éléments requis.
Ces barrières ont été vérifiées statiquement, sans exécuter ces opérations.

JSON et TOML parsés ; toutes les clés du manifeste comparées au runtime.
Comparaison stricte des trois fichiers installés concernés : instructions,
règles et lanceur. Les autres réglages utilisateur sont préservés.
`git diff --check` fait partie du contrôle final.

## Preuves locales et limites

Workspace témoin conservé : `<repertoire-temporaire-historique>`.
`mission.txt`, `evenements.jsonl`, `resultat.txt`, `stderr.txt`, `temoin.json`.
Session parent : `session-anonymisee-018`.
Sous-agent : `session-anonymisee-019`.
Les `turn_context` natifs de ces deux sessions étayent les valeurs effectives.

Le contrôle technique d’une élévation par `auto_review` n’a pas été provoqué
artificiellement. Aucun DENY général des secrets, aucune couverture exhaustive
d’ExecPolicy et aucune garantie d’absence de prompts pour toute opération future
ne sont revendiqués. Les limites appartiennent à
[MECANISMES.md](../../documentation/codex/MECANISMES.md).

## Historique conservé — Round 5

Les résultats ci-dessous décrivent uniquement l’ancienne version et son ancien
profil. Les mentions de validation, de prompts Git et de bypass ne constituent
ni une validation du profil actuel ni une autorisation de les réutiliser.

<details>
<summary>Preuves historiques Round 5, conservées sans suppression</summary>

# Requalification Codex — Round 5

Ce document conserve les preuves encore pertinentes pour l’architecture Codex actuelle.

Les preuves concernant les mécanismes supprimés restent accessibles dans l’historique Git mais ne décrivent plus l’état actif.

## 1. Statut

    Adaptateur Round 5             VALIDÉ fonctionnellement
    Source canonique               VALIDÉE
    Installation réelle            VALIDÉE
    Review native réelle           VALIDÉE
    Exécution Codex générale      VALIDÉE DANS LE SCÉNARIO TESTÉ
    Documentation Round 5          EN COURS
    Audit Git / Review finale      À FAIRE

Version observée :

    codex-cli 0.154.0-alpha.6.2

Environnement principal :

    macOS
    Codex fourni par ChatGPT.app
    Git local
    zsh

Une preuve obtenue ici n’est pas automatiquement transférée à une autre version de Codex ou à un autre système.

## 2. Objectif du Round 5

Le Round 5 répond à un problème réel.

L’ancienne architecture ajoutait globalement :

    scanner d’environnement
    registre de fichiers
    référence persistante
    wrapper codex
    routeur shell
    reprise personnalisée
    checkpoints
    PermissionRequest personnalisé

Une Review réelle a été bloquée par ce système alors que le changement à Review était sans rapport avec sa maintenance.

L’utilisateur avait également observé que CoWork pouvait être bloqué par la configuration globale.

Décision :

    supprimer les mécanismes globaux non nécessaires
    → revenir au Codex natif
    → conserver uniquement les garde-fous ciblés
    → ne recréer un mécanisme qu’après problème réel reproductible

## 3. Validation statique du candidat

Candidat de travail :

    <repertoire-temporaire-historique>/codex-round5-simplification/candidat

Fichiers principaux contrôlés :

    AI_WORKFLOW.md
    .codex/AGENTS.md
    .codex/hooks.json
    .codex/hooks/notification.py
    .codex/rules/default.rules
    .codex/bin/review-native-codex
    .codex/skills/preparer-commit/SKILL.md
    .codex/skills/cloturer-branche/SKILL.md
    outils/empreinte-git.py
    configuration-workflow.json

Résultats observés :

    AI_WORKFLOW.md               54 lignes
    AGENTS.md                    21 lignes
    preparer-commit              12 lignes
    cloturer-branche             12 lignes

    AI_WORKFLOW universel        OK
    ancien système candidat      absent
    Python                       OK
    review-native-codex shell    OK
    JSON                         OK
    lien Review                  OK

La recherche de termes propres à Codex ou Claude dans `AI_WORKFLOW.md` n’a trouvé aucun terme spécifique interdit.

## 4. AI_WORKFLOW universel

Principe retenu :

    une règle universelle
    → une source unique

L’adaptateur ne doit pas recopier cette règle.

Ajout central Round 5 :

    Ne jamais se répéter.

Le Workflow universel ne contient plus de mécanisme Codex spécifique.

## 5. AGENTS.md Codex

Le nouvel adaptateur global est volontairement court.

Responsabilités :

    activer le Workflow uniquement dans son périmètre
    empêcher les relectures inutiles
    mapper Principal / Worker / Explorer
    utiliser les Skills lorsque nécessaire
    imposer la route de Review native contrôlée
    conserver la communication spécifique Codex

Validation statique :

    21 lignes
    aucune copie complète des règles universelles

## 6. PreToolUse — retiré du Round 5

Une première simplification de `PreToolUse` a été testée avec plusieurs matrices de commandes.

Ces tests ont révélé deux tendances opposées :

- des faux négatifs sur certaines variantes shell et certains wrappers ;
- des faux positifs sur des commandes Git de lecture ou de simulation.

Un audit approfondi a confirmé que poursuivre cette approche revenait progressivement à reconstruire un parser shell spécifique au Workflow.

Décision finale du Round 5 :

    PreToolUse personnalisé
    → RETIRÉ

Le Workflow s'appuie désormais sur :

    AI_WORKFLOW.md
    + ExecPolicy native
    + sandbox Codex
    + décision humaine

Cette architecture n'affirme pas qu'ExecPolicy détecte toutes les reformulations syntaxiques possibles. L'interdiction de contourner une autorisation ou un refus reste un invariant comportemental universel.

## 7. ExecPolicy

Tests statiques observés :

    git status
    → prompt

    git reset --hard HEAD
    → forbidden

    review-native-codex --help
    → allow

Un test statique de :

    git push --force origin main

a produit `prompt` au niveau ExecPolicy.

Dans la forme canonique testée, le push forcé produit `prompt` : il nécessite donc une décision humaine ; il n'est pas `forbidden` par ExecPolicy native.

Cette séparation est volontaire : Round 5 évite de dupliquer toute la logique dans plusieurs couches.

## 8. Hooks

Configuration actuelle :

    ExecPolicy native
    → default.rules

    Stop
    → notification.py

`permission_request.py` a été supprimé.

Le Hook Stop a été observé fonctionnel pendant le test Codex général :

    hook: Stop
    hook: Stop Completed

## 9. Review native — interface

Interface actuelle :

    review-native-codex --uncommitted
    review-native-codex --base <branche>
    review-native-codex --commit <sha>
    review-native-codex --help

Le lanceur utilise le Codex natif fourni par ChatGPT.app.

Il impose :

    sandbox read-only
    model_reasoning_effort = high

Une matrice isolée antérieure avait validé :

    syntaxe shell
    --uncommitted
    --base
    --commit
    absence d’argument
    refus d’arguments arbitraires
    refus d’override sandbox
    propagation des codes d’échec
    stdout vide → erreur
    argv contrôlé

Cette matrice complète a été exécutée avant l’ajout du forçage :

    model_reasoning_effort = high

Après cette modification :

    sh -n
    → OK

puis une Review réelle a réussi.

La matrice complète n’a pas été rejouée après cette modification unique.

Ne pas prétendre le contraire.

## 10. Review native — test réel Round 5

Dépôt jetable :

    <repertoire-temporaire-historique>/codex-round5-simplification/validations/review-reel-round5

Fichier initial :

    def addition(a, b):
        return a + b

Modification non commitée :

    def division(a, b):
        return a / b

Avant Review :

    SHA-256
    5f1aabd125179fa5ef776d350dd007f0d9b45a2a7eeec7eb1f25a4fa55ec95bf

    git status
     M calcul.py

Commande :

    review-native-codex --uncommitted

Résultat :

    Review exécutée
    RC=0

Après Review :

    SHA-256 identique
    git status identique

Conclusion :

    Review native réellement exécutée       OK
    aucune mutation du fichier              OK
    Working tree inchangé                   OK
    ancien scanner non déclenché            OK
    code retour                             0

Cette preuve ferme le problème principal qui avait motivé Round 5.

## 11. Empreinte Git

Outil :

    outils/empreinte-git.py

Durcissements Round 5 :

    /usr/bin/git
    PATH minimal
    LC_ALL=C
    GIT_OPTIONAL_LOCKS=0
    GIT_TERMINAL_PROMPT=0
    GIT_PAGER=cat
    pas de shell
    options de diff déterministes

Test réel observé :

    DEPOT=AI-Workflow
    BRANCHE=main
    HEAD=0067d148c97d
    ETAT=e29c1f1b65e9ccd07f92
    WORKTREE=PROPRE

Contrôle :

    WORKTREE INCHANGE=OK
    INDEX INCHANGE=OK

`py_compile` a également réussi.

Une campagne automatique plus longue avait expiré pendant un scénario detached HEAD.

Elle ne doit donc pas être présentée comme entièrement réussie.

La preuve retenue est le test réel sur la machine plus la validation Python.

## 12. Promotion vers la source canonique

Après validation du candidat, les fichiers Round 5 ont été promus dans le dépôt.

Comparaisons observées :

    AI_WORKFLOW               OK
    AGENTS                    OK
    hooks.json                OK
    review-native-codex       OK
    preparer-commit           OK
    cloturer-branche          OK
    empreinte-git             OK
    configuration             OK

Éléments supprimés de la source :

    .codex/bin/reprendre-codex
    .codex/hooks/permission_request.py
    .local/bin/codex
    outils/empreinte-environnement-codex.py
    outils/environnement-codex.json
    outils/routage-codex.zsh

## 13. Installation réelle

Après synchronisation de l’installation :

    AGENTS                    OK
    hooks.json                OK
    notification              OK
    default.rules             OK
    review-native-codex       OK
    preparer-commit           OK
    cloturer-branche          OK

Résolution observée :

    codex is /Applications/ChatGPT.app/Contents/Resources/codex

Version :

    codex-cli 0.154.0-alpha.6.2

L’ancien routage Zsh était absent.

Un contrôle avait encore observé uniquement :

    ~/.local/state/ai-workflow/.DS_Store

Le nettoyage de ce résidu a ensuite été proposé séparément.

Aucune preuve ultérieure dans cette campagne ne dépend de ce fichier.

## 14. Configuration effective

Valeurs observées dans `~/.codex/config.toml` :

    model = "gpt-6-astra"
    model_reasoning_effort = "high"
    personality = "pragmatic"
    plan_mode_reasoning_effort = "xhigh"
    review_model = "gpt-6-astra"
    project_doc_fallback_filenames = ["PROJECT_CONTEXT.md"]
    approvals_reviewer = "user"
    approval_policy = "on-request"
    sandbox_mode = "workspace-write"

    [agents]
    default_subagent_model = "gpt-5.6-sol"
    default_subagent_reasoning_effort = "high"

Le manifeste :

    adaptateurs/codex/configuration-workflow.json

reste une référence des choix du Workflow et non une copie de `config.toml`.

## 15. Exécution Codex générale

Objectif :

vérifier que la configuration globale Round 5 n’impose plus l’ancien Workflow spécialisé dans un usage général.

Dossier jetable :

    <repertoire-temporaire-historique>/codex-round5-simplification/validations/codex-general-round5

Exécution réelle observée :

    OpenAI Codex v0.154.0-alpha.6.2
    model: gpt-6-astra
    sandbox: read-only
    reasoning effort: high

Prompt :

    Réponds uniquement par GENERAL_OK.
    Ne lis aucun fichier qui n’est pas nécessaire.

Réponse :

    GENERAL_OK

Code :

    RC=0

Aucun message concernant :

    scanner
    REFERENCE
    A_CLASSER
    reprendre-codex
    checkpoint Workflow

n’est apparu.

Verdict :

    invocation Codex générale
    → OK dans le scénario testé

Ce test utilisait `--ignore-rules`.

Il montre que le CLI natif s'exécute et que l'ancien scanner ne bloque pas ce chemin. À lui seul, il ne valide pas complètement l'isolation du périmètre normal des Rules.

Il ne constitue pas un test exhaustif de toutes les interfaces Codex ou CoWork.

## 16. Skills

Skills actuels :

    preparer-commit
    cloturer-branche

Les deux avaient déjà été déclenchés dans des tests réels antérieurs.

Round 5 a surtout supprimé leurs duplications documentaires et leur couplage à des noms de sections obsolètes.

Aucune nouvelle campagne runtime complète des Skills n’a été exécutée spécifiquement après cette simplification.

## 17. Ancien système — statut

Ne font plus partie de l’architecture active :

    scanner d’environnement
    manifestes de catégories
    référence persistante acceptée
    codex --etat
    codex --accepter-reference
    wrapper ~/.local/bin/codex
    routage-codex.zsh
    reprendre-codex
    checkpoints de reprise
    PermissionRequest personnalisé

Les anciennes preuves associées restent historiques.

Elles ne doivent plus être utilisées pour décrire le fonctionnement actuel.

## 18. Preuves historiques encore réutilisables

Le cycle réel :

    feature/recherche-age

reste pertinent pour les principes qui n’ont pas été supprimés :

    pré-vérification Git
    changements préexistants
    délégation
    tests / build
    préparation du commit
    Review indépendante
    décisions Git séparées
    intégration
    réutilisation des preuves lorsque le contenu est inchangé

Il ne valide plus :

    scanner
    référence persistante
    wrapper
    routeur shell
    reprise externe personnalisée

car ces mécanismes n’existent plus.

## 19. Quand rejouer une preuve ?

    AI_WORKFLOW.md / AGENTS.md
    → activation et isolation du Workflow

    default.rules
    → garde-fous concernés

    review-native-codex
    → syntaxe + interface concernée + Review réelle

    configuration-workflow.json / config.toml
    → valeurs effectives + démarrage Codex

    Skill
    → comportement du Skill concerné

    empreinte-git.py
    → état Git et absence de mutation

    mise à jour significative de Codex
    → capacités réellement utilisées par l’adaptateur

Principe :

    identifier l’invalidation concrète
    avant de rejouer une preuve

## 20. Critère de maintenance

Pour un fichier statique :

    source du dépôt
    → modification
    → validation
    → installation
    → comparaison source / installation
    → requalification ciblée

Pour `config.toml` :

    configuration-workflow.json
    → choix du Workflow

    config.toml
    → fichier réel Codex/OpenAI

Le fichier complet n’est jamais remplacé automatiquement.

Pour un composant critique, un candidat isolé peut être utilisé si cela réduit réellement le risque.

L’isolation n’est pas exigée mécaniquement pour une modification triviale ou documentaire.

## 21. Clôture Round 5 restante

    1. terminer la documentation Round 5
    2. rechercher les références obsolètes restantes
    3. vérifier le diff complet
    4. effectuer l’audit Git final
    5. effectuer la Review finale
    6. corriger uniquement les problèmes réellement observés
    7. préparer le commit
    8. commit après décision humaine
    9. push après décision humaine
    10. supprimer les laboratoires temporaires ensemble après réussite complète

Tant que ces étapes ne sont pas terminées, les laboratoires de requalification sont conservés.

</details>
