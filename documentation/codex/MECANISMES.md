> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Mécanismes Codex

## Frontières

Le modèle fonctionnel appartient à [AI_WORKFLOW.md](../../AI_WORKFLOW.md) et à
[architecture/AUTORISATIONS.md](../../architecture/AUTORISATIONS.md).
Les instructions courtes sont dans l’adaptateur `AGENTS.md` ; ce document explique
uniquement leur mise en œuvre Codex.

`workspace-write` confine les écritures. Le réseau de travail est autorisé par
`sandbox_workspace_write.network_access`. Les commandes nécessaires emploient
la forme native, directe et atomique suffisante ; aucune micro-whitelist ne
remplace les anciens prompts Git.

`on-request` permet de demander une élévation lorsqu’une frontière technique
l’exige. `auto_review` examine les demandes admissibles avec le mécanisme natif ;
il ne remplace ni les STOP humains du Workflow ni le Reviewer indépendant du code.
Un refus reste un refus : aucun changement de syntaxe, wrapper ou interpréteur
ne doit servir à le contourner. Une intervention humaine reste possible lorsque
le runtime l’exige réellement.

Les écritures externes sont limitées au périmètre convenu ; aucun accès global
en écriture au dossier personnel n’est ajouté. Les caches et outils nécessaires
peuvent requérir une élévation native. Une autorisation runtime ne constitue
jamais une extension fonctionnelle du périmètre.

## Règles natives

`default.rules` ne contient que les quatre protections destructives conservées.
Les commandes et variantes effectivement couvertes sont consignées dans
[la requalification](../../tests/codex/REQUALIFICATION.md).
Une absence de correspondance signifie seulement qu’aucune de ces règles ne
s’applique : elle ne vaut ni autorisation fonctionnelle ni garantie d’exécution.

Les STOP de staging, commit, push conditionnel et clôture restent déclaratifs,
avant tout appel d’outil, même si la commande serait techniquement acceptée.
Les règles globales ne tentent pas de reconnaître toutes les variantes Git,
les chemins absolus, alias, scripts ou sous-processus.

## Limites techniques

Le confinement du système d’exploitation et le filtrage de préfixes sont deux
mécanismes distincts. Un sous-processus exécuté dans le sandbox reste soumis à
ce confinement ; cela ne prouve pas que chaque commande descendante soit
réévaluée par ExecPolicy. Une élévation approuvée peut exécuter la commande hors
sandbox : son périmètre doit donc rester borné.

Aucun DENY général sur toutes les lectures de secrets n’est établi pour ce
profil. La lecture externe est largement permise. L’interdiction fonctionnelle
universelle demeure, sauf nécessité expressément autorisée ; aucun secret réel
n’est utilisé pour les tests. Le réseau autorisé ne fournit pas une barrière
matérielle générale contre l’exfiltration ou la publication non demandée.

Le nom d’un sous-agent ne garantit pas sa lecture seule. Types exposés,
permissions annoncées et observations appartiennent à `CONFIGURATION.md`.
Les permissions des connecteurs et de l’utilisation de l’ordinateur restent
propres à leurs outils ; les règles shell ne les couvrent pas.

## Review de code

Le Reviewer explicitement désigné pour l’unité prime sur le choix par défaut.
Le Reviewer indépendant désigné pour une unité reste une décision distincte de
la sonde fonctionnelle du lanceur Codex.

Lorsqu’une Review Codex est retenue, le lanceur existant accepte uniquement
`--uncommitted`, `--base <branche>`, `--commit <sha>` ou `--help`.
Il conserve la configuration utilisateur et les règles, impose `read-only`,
`approval_policy="never"` et l’effort `high`. Cette politique propre à la Review
évite d’hériter des élévations automatiques du Principal. Une validation exigeant
une écriture est confiée à un Exécuteur de preuve ; le Reviewer conserve son verdict.
Le lanceur ne reprend pas la conversation de l’implémenteur.
Son modèle provient de `review_model` dans la configuration utilisateur : la cible
active est `gpt-6.1-sol`. Le lanceur résout une fois le CLI via `command -v codex`
et vérifie qu’il est exécutable ; aucun chemin fournisseur n’est imposé. Le PATH
doit désigner le CLI attendu. La preuve `gpt-6-sol` / `high` du 23 septembre 2026
reste historique ; les preuves différentielles sont dans `REQUALIFICATION.md`.

## Maintenance et diagnostic

Ne modifier que les clés appartenant au manifeste ; conserver les autres
réglages utilisateur. Les fichiers installables se maintiennent dans le dépôt,
puis se synchronisent selon `INVENTAIRE.md`. Un nouveau processus permet de
vérifier les paramètres chargés ; éditer le fichier n’atteste pas une migration
de la session déjà ouverte.

Une commande bloquée appelle d’abord le diagnostic de la frontière effective
(règle, sandbox, réseau, approbation). Aucun nouveau parser, wrapper, daemon ou
système de permissions parallèle n’est nécessaire.

Références natives : [approbation automatique](https://developers.openai.com/fr-FR/docs/sandboxing/auto-review),
[règles](https://developers.openai.com/fr-FR/docs/agent-configuration/rules),
[configuration](https://developers.openai.com/fr-FR/docs/config-file/config-reference).

## Modèles, reasoning et escalade

La politique opérationnelle appartient à l’`AGENTS.md` installé ; les valeurs
persistantes au manifeste. Les réglages natifs sont `model`,
`model_reasoning_effort`, `plan_mode_reasoning_effort`, `review_model`,
`agents.default_subagent_model`, `agents.default_subagent_reasoning_effort` et
`agents.max_concurrent_threads_per_session`. Politique du 4 octobre 2026 :
Principal et Plan en `gpt-6.1-sol` / `medium`, sous-agent par défaut en
`gpt-6.1-sol` / `low`, Reviewer en `gpt-6.1-sol` / `high` (effort imposé
par le lanceur, aucune clé dédiée inventée). Le mode Plan utilise explicitement
`plan_mode_reasoning_effort="medium"`. Les anciennes observations GPT-6 Sol et
Terra restent des preuves historiques, sans qualification implicite du nouveau couple.

### Choisir et changer de modèle

La CLI interactive expose `/model` pour choisir modèle et effort. Au lancement,
les options natives `--model` / `-m` et `-c model_reasoning_effort=...` permettent
une sélection ponctuelle sans remplacer le défaut persistant. Exemple de recours
exceptionnel explicite à Astra, uniquement après un motif concret, sans palier automatique :

```sh
codex --model gpt-6-astra -c 'model_reasoning_effort="low"'
```

Ce lancement crée une autre session ; il ne transforme pas rétroactivement la
session courante. Dans l’interface d’application, utiliser le sélecteur natif
modèle/effort lorsqu’il est proposé. Aucun outil de cette session ne permet au
Principal de modifier directement son propre modèle en cours de réponse : il
signale le besoin et le réglage natif à appliquer, ou délègue un diagnostic borné
au modèle approprié. Une délégation ne devient pas une escalade du Principal.

Le passage de palier dépend du problème observé et du résultat du palier
précédent ; il n’existe pas de règle de configuration installée qui détecte
l’ambiguïté et escalade automatiquement. Le sous-agent normal utilise Sol Low ; une difficulté concrète justifie un
override Medium, puis High si nécessaire. La taille seule ne suffit pas. Terra
est historique uniquement ; Astra reste exceptionnel, sans étape automatique. Revenir au défaut pour la prochaine mission ne nécessitant pas
l’escalade.

### Overrides des sous-agents

Le schéma exposé de `collaboration.spawn_agent` accepte `model` et
`reasoning_effort`. Sans ces overrides, un contexte neuf (`fork_turns="none"`)
utilise les valeurs par défaut des sous-agents. Transmettre la mission et les
éléments utiles, sans recopier toute la conversation.
Une sonde read-only du 23 septembre 2026 a confirmé `gpt-6-sol` / `high` dans
le `turn_context` d'un enfant lancé avec ces deux overrides explicites.

Dans cette interface, `fork_turns="all"` hérite du modèle et de l’effort du parent
et n’accepte pas ces overrides. Pour choisir explicitement Sol Medium, Sol High ou exceptionnellement
Astra, utiliser `fork_turns="none"` ou un nombre positif de tours avec `model` et
`reasoning_effort`. Ne pas créer d’agents personnalisés pour matérialiser la
matrice des missions. Exemple d’escalade explicite après justification :
`collaboration.spawn_agent(task_name="diagnostic", message="mission bornée",
fork_turns="none", model="gpt-6.1-sol", reasoning_effort="medium")` ;
remplacer l’effort par `high` uniquement si nécessaire. Sans override et avec un
contexte neuf dans une session ouverte après installation, le défaut persistant
Low s’applique. Une session déjà ouverte peut conserver son ancien défaut ;
modifier le TOML ne recharge pas ses valeurs. Un fork intégral peut hériter
de Medium du Principal et ne qualifie donc pas le défaut Low.
Les exceptions sont décidées au lancement ;
leur simple disponibilité ne justifie pas de les employer.

### Concurrence

`agents.max_concurrent_threads_per_session = 3` limite les fils enfants ouverts
simultanément, hors Principal. Le contexte natif annonce alors quatre places au
total. Ce plafond constitue une capacité normale disponible et non un objectif
de consommation ni un fan-out automatique : le Principal adapte le nombre d’agents
aux axes indépendants réels (0, 1, 2 ou jusqu’à 3).

Si plus de trois sous-agents sont exceptionnellement nécessaires, expliciter le
besoin (indépendance, gain, coût/quota raisonnable, absence de conflit d’écriture) et
appliquer ponctuellement la clé avec une valeur supérieure par override natif au lancement
de la session concernée (ex. `-c agents.max_concurrent_threads_per_session=4`).
Le défaut persistant reste `3`. Un outil de spawn ne relève pas ce plafond à lui
seul ; aucune modification à chaud n’est revendiquée ici.

Références : [modèles et changement interactif](https://developers.openai.com/fr-FR/docs/models),
[sous-agents](https://developers.openai.com/fr-FR/docs/agent-configuration/subagents),
[clés de configuration](https://developers.openai.com/fr-FR/docs/config-file/config-reference).

## Limites explicites de l'édition publique
Les quatre règles natives sont des protections de préfixes qualifiés, pas une analyse exhaustive du shell. Les STOP avant staging, commit et publication sont aussi des obligations comportementales ; ils ne sont pas tous des invites techniques natives. Le lanceur de Review impose read-only et ne permet pas d'override libre, mais une session fournisseur peut transmettre les sources lues et les diff au service externe. Ne jamais reviewer de données confidentielles sans autorisation de transmission. Les qualifications historiques ne certifient pas les versions nouvelles.
