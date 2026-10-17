> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Configuration Codex

## Politique active — 4 octobre 2026

Le [manifeste](../../adaptateurs/codex/configuration-workflow.json) porte :
Principal et Plan `gpt-6.1-sol` / `medium`, sous-agent normal `gpt-6.1-sol` /
`low`, escalade explicite `medium` puis `high` sur signal concret ; Reviewer
`gpt-6.1-sol` / `high`, effort imposé par le lanceur. Astra reste exceptionnel,
Terra historique uniquement. La taille seule ne justifie aucune escalade.

Le CLI observé est `codex-cli 0.160.0`, résolu en `/opt/homebrew/bin/codex` sur
cette machine. Le lanceur installable résout `codex` via le PATH ; ses contraintes
`read-only`, approbation `never`, effort `high` et interface fermée sont conservées.
L’état installé et les résultats différentiels figurent dans
[REQUALIFICATION.md](../../tests/codex/REQUALIFICATION.md).

## Requalification fonctionnelle — 23 septembre 2026

Le manifeste décrivait alors le Principal et la Review native en
`gpt-6-sol` / `high`. L'installation portait alors ces mêmes valeurs : une Review réelle a confirmé le modèle, l'effort,
le contexte distinct, `read-only` et `approval_policy="never"`. Le lanceur était
inchangé ; le manifeste n'est pas appliqué automatiquement. Un tour Plan a
également confirmé `gpt-6-sol` / `high`, et un sous-agent lancé avec override
explicite a effectivement utilisé `gpt-6-sol` / `high`. Le défaut Terra / High
était alors inchangé ; sa preuve de résolution reste historique. Ces sondes établissent
des mécanismes, pas la qualité relative ou la politique finale des modèles ;
détails et limites dans [REQUALIFICATION.md](../../tests/codex/REQUALIFICATION.md).

## Qualification du 19 septembre 2026 — historique

Les sous-sections suivantes retracent cette qualification initiale. Les constats
ultérieurs du 23 septembre y sont datés explicitement ; pour l'état installé
actuel, voir la politique active et les preuves différentielles.

### Installation

Binaire natif : `/Applications/ChatGPT.app/Contents/Resources/codex`.
Version mesurée : `codex-cli 0.155.0-alpha.9`.

Les valeurs maintenues appartiennent au
[manifeste](../../adaptateurs/codex/configuration-workflow.json).
Le 19 septembre, la configuration utilisateur a été modifiée uniquement pour passer
`approvals_reviewer` à `auto_review` et ajouter
`sandbox_workspace_write.network_access = true` ; `on-request` et
`workspace-write` étaient déjà configurés. Le 23 septembre, `review_model` a été
synchronisé séparément vers `gpt-6-sol`.

Une nouvelle session CLI a chargé les quatre valeurs cibles, confirmées par son
`turn_context`. Le profil effectif est `managed` / `restricted`, réseau `enabled`,
écritures workspace et temporaires ; `.git`, `.codex` et `.agents` du workspace
restent protégés en écriture. Cela n’atteste pas une migration de l’ancienne
session principale encore ouverte.

Sources installées : `AGENTS.md`, `rules/default.rules` et
`bin/review-native-codex`, selon [l’inventaire](../../adaptateurs/codex/INVENTAIRE.md).
Les hooks de notification, les deux skills et le lien PATH restent inchangés.
Aucun profil personnalisé, agent personnalisé ou nouvelle couche runtime ajouté.

### Agents : documentation et disponibilité observée

La documentation native décrit `default` (polyvalent), `worker` (implémentation
et correction) et `explorer` (exploration). Leur existence documentaire ne prouve
pas leur sélection dans chaque interface.

Sur la session CLI qualifiée et cette interface, le schéma exposé est :

```text
collaboration.spawn_agent(
  task_name, message, fork_turns?, model?, reasoning_effort?
)
```

Il ne contient aucun sélecteur `agent_type` ni argument de permissions.
Aucun lancement distinct des trois types intégrés n’est donc revendiqué.
Il serait incorrect de les simuler en changeant seulement `task_name`.

| Capacité | Disponibilité observée | Contexte et permissions | Usage |
|---|---|---|---|
| Principal | Actif pendant la qualification | Profil effectif ci-dessus ; édition du témoin observée | Orchestration / implémentation |
| Sous-agent générique | Un lancement réussi, terminé | Contexte neuf (`fork_turns="none"`), même sandbox/réseau/approbations ; outils d’écriture annoncés, aucune écriture effectuée | Lecture et commande read-only qualifiées ; rôle transmis par mission |
| `default` | Documenté ; pas de sélection distincte exposée | Non qualifié séparément ; aucune assimilation implicite au générique | Polyvalence documentée |
| `worker` | Documenté ; pas de sélection distincte exposée | Non qualifié séparément | Implémentation documentée |
| `explorer` | Documenté ; pas de sélection distincte exposée | Non qualifié séparément ; aucune garantie read-only tirée du nom | Exploration documentée |
| Réviseur `auto_review` | Activé dans la nouvelle session | Contrôle technique des élévations ; aucune élévation provoquée pour ce test | Aucun verdict de Review de code |
| Reviewer Codex | Lanceur installé, interface/syntaxe vérifiées ; Review réelle confirmée le 23 septembre 2026 | Nouveau contexte `gpt-6-sol` / `high`, `read-only`, `approval_policy="never"` | Sonde fonctionnelle, sans preuve de supériorité qualitative |

Lors de la qualification des autorisations au commit `7a20ba85d72d`, le
sous-agent utilisait `gpt-5.6-sol`, effort `high`, sans override au lancement.
Cette observation historique ne définit pas le nouveau défaut décrit ci-dessous. Les métadonnées de son fil indiquent `agent_role: null` et le parent
correct. Ce résultat ne démontre pas le comportement de toutes les interfaces,
d’un agent personnalisé ou d’un futur changement de version.

### Modèles et concurrence — micro-unité du 19 septembre 2026

À cette date, les clés persistantes étaient définies dans le manifeste : Principal
Sol High, mode Plan High, Review interne Sol (effort High déjà imposé par le
lanceur inchangé), sous-agent par défaut Terra High et jusqu’à trois enfants simultanés.
Les identifiants natifs qualifiés alors étaient `gpt-5.6-sol`,
`gpt-5.6-terra` et `gpt-6-astra` ; cette liste n'est pas la politique actuelle.

Le catalogue local annonce les niveaux demandés pour ces trois modèles.
`codex debug prompt-input` avec la limite native à `3` annonce quatre places au
total, Principal inclus. Les sessions de qualification confirment les valeurs
chargées ; résultats dans [REQUALIFICATION.md](../../tests/codex/REQUALIFICATION.md).

La matrice des missions, l’ordre d’escalade et le renouvellement raisonnable des
sessions appartiennent à l’`AGENTS.md` versionné puis installé. Les modalités
natives de changement de modèle, de fork et d’override au-delà de trois enfants sont
expliquées dans [MECANISMES.md](MECANISMES.md#modèles-reasoning-et-escalade).
Aucun agent personnalisé, profil supplémentaire ou script d’escalade ajouté.

## Chargement et procédures

Le Workflow s’active par la déclaration de `PROJECT_CONTEXT.md` ; l’adaptateur
injecté reste court. Aucune relecture automatique de `~/.codex/AGENTS.md`.
Les skills de préparation de commit et clôture demeurent disponibles et
s’utilisent uniquement lorsque leur procédure est pertinente dans ce périmètre.
Leur présence ne constitue aucune autorisation Git.

Les explications des protections et limites appartiennent à
[MECANISMES.md](MECANISMES.md) ; les preuves détaillées et leur périmètre à
[REQUALIFICATION.md](../../tests/codex/REQUALIFICATION.md).
