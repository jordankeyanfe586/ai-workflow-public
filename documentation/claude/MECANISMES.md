> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Mécanismes Claude Code

Le modèle fonctionnel appartient à [AI_WORKFLOW.md](../../AI_WORKFLOW.md) et à [architecture/AUTORISATIONS.md](../../architecture/AUTORISATIONS.md). Ce document explique uniquement leur mise en œuvre dans Claude Code 2.1.280. Les preuves et leur périmètre appartiennent à [REQUALIFICATION.md](../../tests/claude/REQUALIFICATION.md).

## Couches de protection

Ordre d’évaluation observé pour un appel d’outil :

```text
permissions.deny  →  permissions.ask / hook PreToolUse "ask"  →  classifieur du mode auto  →  sandbox (Bash)
```

| Couche | Rôle dans le Workflow | Limite |
|---|---|---|
| `permissions.deny` | Git destructif canonique (dont suppressions forcées `branch -D`, `--force --delete`, `-d -f`, `-df`), secrets connus (Read/Edit ; `cat .env` en Bash également refusé) | motifs de préfixe : ne couvre pas `git -C … reset --hard` ni `bash -c '…'` |
| `permissions.ask` | formes canoniques des classes STOP (`add`, `stage`, `commit`, `merge`, `rebase`, `pull`, `push`, `branch -d`/`--delete`), y compris chaînées (`&&`), préfixées (`env`, `VAR=`) | ne couvre pas `-C`, `-c`, `--no-pager`, chemin absolu, `bash -c` ; un push destructif hors motifs `deny` (`+refspec`, `--mirror`…) n’y est qu’un `ask` |
| `barriere-git.py` | classes Git après normalisation : STOP → `ask` ; push réécrivant ou supprimant des références distantes et suppression forcée de branche → `deny` ; jamais `allow` | frontière de couverture ci-dessous |
| Classifieur `auto` | destructions et contournements sémantiques (a refusé `git -C . reset --hard` et `bash -c 'git clean -fd'`) | autorise le push et n’applique aucune barrière Git ; non déterministe |
| Sandbox | confinement Seatbelt des commandes Bash ; échec fermé (`failIfUnavailable`) | ne couvre ni les outils Read/Edit ni les processus hors Bash |

Une permission technique n’est jamais une autorisation fonctionnelle : les STOP du Workflow restent déclaratifs dans `CLAUDE.md` ; l’invite native (`ask`) en est l’acte de validation technique.

## Mode auto

`permissions.defaultMode: "auto"` et `--permission-mode auto` activent le mode auto avec Opus 5.5 (qualifié en 2.1.280, où l’alias `sonnet` désignait alors Sonnet 5, également qualifié ; Sonnet 5.5 n’a pas été requalifié comme modèle de session en mode auto). Avec Haiku 4.5, la session retombe silencieusement en `default` : ne jamais choisir Haiku comme Principal.

Le classifieur ne remplace pas les barrières : ses règles par défaut jugent un push vers le dépôt « ordinaire ». Aucune règle `autoMode` personnalisée n’est ajoutée ; si elle l’était, elle devrait conserver `$defaults` et ne serait jamais la seule frontière d’un STOP.

## Barrière Git

La politique Git est gouvernée par des classes, pas par une énumération de syntaxes :

| Classe | Décision |
|---|---|
| lecture, inspection, `fetch` ; création et bascule de branche hors clôture | AUTO |
| staging / commit (`add`, `stage`, `commit`) | STOP |
| intégration (`merge`, `rebase`, et `pull`, qui les encapsule) | STOP |
| push normal | STOP |
| suppression normale de branche (`branch -d`) ; bascule vers la branche cible pendant une clôture | STOP |
| réécriture ou destruction locale/distante (reset/clean forcés, suppression forcée de branche : `-D` ou suppression avec `--force`/`-f`, push forcé, `+refspec`, `:refspec`, `--delete`, `--mirror`, `--prune`) | DENY |

Chemin autonome : jamais `git pull` ; `git fetch` (AUTO), puis `git merge` ou `git rebase` explicite (STOP). Le Principal exécute chaque opération STOP une par une en forme canonique après la présentation exigée par le Workflow.

`barriere-git.py` applique ces classes après une normalisation bornée : options globales de Git, chemin absolu, quelques wrappers (`env`, dont la chaîne de `env -S`/`--split-string` est réanalysée, `command`, `exec`, `nice`, `nohup`, `time`, `sudo`, `xargs`, `eval`), `sh|bash|zsh -c`, chaînage, substitution `$(…)`/backticks, mots réservés (`if`, `while`, `{ }`…). Seul le corps d’un heredoc réellement actif est ignoré : un `<<` situé dans une chaîne citée reste du texte et ne masque jamais la commande suivante. La classe d’un push est déterminée par son sens (réécriture ou suppression de références distantes), et celle d’une suppression de branche par son caractère forcé (`-D`, ou suppression accompagnée de `--force`/`-f`), non par une liste de motifs ; la décision la plus forte l’emporte sur la commande entière. Repli borné : un exécuteur non reconnu (`timeout`, `find -exec`…) ne produit une décision que si ses arguments contiennent réellement `git <opération>` ; les commandes qui n’exécutent pas leurs arguments (`echo`, `grep`, `rg`…) en sont exclues ; une syntaxe non analysable produit `ask` si une barrière y figure.

**Frontière de couverture assumée.** Le hook n’est pas un interpréteur Bash et ne prétend couvrir aucune syntaxe exhaustivement. Non couverts : variables et indirections (`$GIT add`, `g=git; $g add`), alias Git, fonctions et scripts, entrée standard d’un shell (`bash <<< …`, `sh <<'EOF' … EOF`), corps de tout heredoc actif (cité ou non) interprété comme programme ou contenant des substitutions non citées, sous-processus d’une commande autorisée, configuration qui change le sens d’un push (`remote.*.mirror`, refspecs forcées configurées). Ces cas relèvent de la forme canonique obligatoire (`CLAUDE.md`), du classifieur `auto` (`Git Destructive`) et de la décision humaine. Une nouvelle syntaxe appartenant à une classe déjà protégée n’appelle pas de nouvelle règle. Faux positif connu, non bloquant (backlog) : une substitution littérale entre apostrophes (`echo '$(git push)'`) produit `ask`.

**Portée des preuves.** La décision exacte du hook (`ask`, `deny`, aucune) est prouvée hors ligne par `test_barriere_git.py`. Le banc en session réelle prouve l’exécution, la non-exécution, l’erreur ou la trace incomplète : avec `--permission-prompts none`, un `DENY` et un `ASK` sans surface d’approbation donnent tous deux une non-exécution. Claude Code n’expose pas la cause du refus comme donnée structurée (`permission_denials` ne contient que l’outil et son entrée) ; les messages textuels diffèrent mais ne sont pas utilisés comme preuve. La distinction runtime `DENY`/`ASK` est donc **NON EXPOSÉE**.

## Sandbox et réseau

Le sandbox limite les écritures Bash au workspace et aux temporaires ; le réseau passe par un proxy filtrant, dont les domaines supplémentaires sont examinés par le classifieur en mode auto. `allowUnsandboxedCommands: false` désactive `dangerouslyDisableSandbox`. Les écritures de caches de build hors workspace (`~/.m2`, `~/.npm`, …) ne sont autorisées qu’après une friction réellement observée.

## Sous-agents

Les sous-agents natifs héritent des permissions et des hooks du Principal (un `general-purpose` a vu `git -C . add` refusé et ne l’a pas contourné). Le paramètre `model` de l’outil Agent (`sonnet`, `opus`, `haiku`, `fable`) choisit le modèle par mission et prime sur le frontmatter ; sans lui, `Explore` et `Plan` héritent du Principal (observé : `claude-opus-5-5`, effort `medium`). L’outil Agent n’expose aucun paramètre d’effort : les sous-agents héritent de l’effort de la session. La clé `effort:` en frontmatter d’agent ou de skill est documentée mais non qualifiée en 2.1.280 et n’est pas utilisée. Claude ne peut pas changer lui-même l’effort (seuls `/effort`, `Option+T`, `/model`, `--effort`, `CLAUDE_CODE_EFFORT_LEVEL` ou les settings le font) ; `ultrathink` ajoute une consigne sans changer l’effort envoyé à l’API. L’escalade automatique vers `high` (Principal, `Plan`, `ai-reviewer`) est donc indisponible ; l’escalade de modèle `sonnet` → `opus` l’est. Aucune limite native de concurrence n’a été atteinte à 6 agents. Le Workflow n’impose aucun plafond fixe : la concurrence est proportionnée à la tâche et le Principal choisit le nombre minimal suffisant de sous-agents selon les axes réellement indépendants, dans les limites natives, de quota et de contexte.

## Modèle, effort et contexte

`opus` désigne Opus 5.5 et `sonnet` désigne Sonnet 5.5 (alias dynamiques résolus par Claude Code ; observé en 2.1.289 : `claude-opus-5-5` et `claude-sonnet-5-5` ; en 2.1.280, `sonnet` résolvait Sonnet 5). Aucun identifiant de modèle n’est figé dans l’adaptateur. En 2.1.280, `opus`, `claude-opus-5-5` et `opus[1m]` annoncent tous une fenêtre de 1 000 000 tokens : le suffixe `[1m]` ne borne plus la fenêtre. Décision : le comportement natif est conservé ; aucun réglage d’autocompaction (`autoCompactWindow`, `--autocompact`) n’est ajouté. Il ne sera réévalué que si un retour réel justifie de borner ou de compacter différemment le contexte. `/model`, `/effort` et `--effort` sont des mécanismes manuels à la disposition de l’humain ; ils ne constituent pas l’escalade automatique en cours de tâche. Lorsque `high` serait justifié mais non automatisable, le Principal fait seulement le signalement non bloquant prévu par l’adaptateur et poursuit en `medium`.

## Plan mode

`--permission-mode plan` empêche toute modification des sources ; le plan est présenté pour validation. L’approbation du plan ne vaut jamais autorisation Git.

## Reviewer dédié `ai-reviewer`

Agent personnalisé conservé parce qu’aucun type natif n’offre à la fois un rôle de Reviewer, un contexte neuf et l’absence structurelle d’outils d’écriture (`Explore` est un outil de recherche, pas d’audit). Le frontmatter limite ses outils à `Read` et `Bash` : `Edit`, `Write` et `NotebookEdit` sont absents. En 2.1.280, `Grep` et `Glob` ne sont plus des outils natifs ; la recherche passe par Bash.

La non-modification est donc structurelle pour les outils d’édition et déclarative pour Bash ; elle est vérifiée à chaque Review par `ETAT` initial = `ETAT` final sur le périmètre pertinent. Lecture seule ne signifie pas absence de toute écriture physique : tests et builds peuvent produire des artefacts générés (`target/`, `build/`, `__pycache__/`, caches) ; si l’`ETAT` change, le Reviewer liste les chemins et seule une modification de source invalide la Review. Les barrières Git (`ask` + `barriere-git.py`), les `deny` et le sandbox s’appliquent au sous-agent comme au Principal.

Son usage n’est jamais systématique : Review isolée supplémentaire ou diagnostic lorsque Claude est auteur ; Reviewer indépendant externe possible lorsque Codex ou Antigravity est auteur.

## Review externe

Quand Claude est auteur, la Review finale est externe : il ne lance ni Codex ni Antigravity, produit une `MISSION DE REVIEW` relayée par l’humain, gèle le périmètre pendant la Review et vérifie l’`ETAT` au retour.

## Maintenance

Ne modifier que les clés de `fragment_settings` ; conserver les autres réglages utilisateur. Les fichiers statiques se maintiennent dans le dépôt puis s’installent par copie selon l’inventaire. Un nouveau processus permet de vérifier les valeurs chargées : éditer `settings.json` n’atteste pas la migration d’une session ouverte.

Couplage externe connu : Grok lit encore `~/.claude/settings.json` comme source de permissions (rapport privé non distribué). Grok étant sorti de l’écosystème actif, son adaptateur est exclu de cette édition ; ce couplage est seulement historique.

## Limites explicites de l'édition publique
Le hook retire les corps de heredocs avant analyse, y compris les non cités qui peuvent contenir des substitutions exécutables par le shell. Les tests publics constatent cette limite sans exécuter les commandes synthétiques. Les protections natives ou le classifieur peuvent ajouter d'autres barrières, mais aucun blocage universel n'est garanti. Le Reviewer n'a pas Edit/Write mais dispose de Bash ; sa non-modification dépend aussi des instructions et d'un contrôle d'état. Aucun comportement du hook ni des permissions n'a été changé dans cette édition.

Un heredoc cité ne garantit pas une entrée inerte : `sh` ou un autre interpréteur peut exécuter son corps. Tous les corps de heredocs actifs sont retirés de l’analyse ; le risque couvre cette interprétation ainsi que les substitutions dans les corps non cités. Aucun comportement du hook n’a été modifié pour corriger cette limite.
