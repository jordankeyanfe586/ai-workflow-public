> **Portée historique — édition publique.** Les versions, chemins d’installation, sauvegardes et qualifications ci-dessous décrivent l’environnement historique de l’auteur. Ils ne prouvent ni une installation sur ta machine ni une qualification des versions actuelles. Voir documentation/VALIDATION_PUBLIQUE.md depuis la racine du dépôt.

# Adaptateur Antigravity

## Rôle

Cette documentation décrit uniquement l'intégration d'Antigravity au Workflow IA.

Les règles universelles restent dans `AI_WORKFLOW.md`.

## Architecture

```text
AI_WORKFLOW.md
    ↓ inclusion native
~/.gemini/GEMINI.md
    ↓
Antigravity

permissions.json (source portable)
    ↓ résolution des chemins '~' et fusion ciblée
~/.gemini/antigravity-cli/settings.json (runtime résolu)
```

L'adaptateur suit le principe **native first** et **capability first** :

1. utiliser les mécanismes natifs Antigravity ;
2. ajouter uniquement l'adaptation nécessaire ;
3. ne pas dupliquer les règles universelles ;
4. requalifier les comportements par capacité observée après une évolution du runtime.

## Bootstrap

Le fichier maintenu :

`adaptateurs/antigravity/fichiers-installation/.gemini/GEMINI.md`

contient :

```md
@[AI_WORKFLOW](~/.ai-workflow/AI_WORKFLOW.md)
```

Il est installé comme :

`~/.gemini/GEMINI.md`

L'inclusion native charge donc directement la source universelle du Workflow.

## Permissions et modèle de confiance

La source maintenue est :

`adaptateurs/antigravity/permissions.json`

Elle ne représente que la clé `permissions` sous forme portable (chemins basés sur `~`).

Elle ne doit jamais remplacer le fichier `settings.json` complet, qui contient des réglages locaux indispensables comme `trustedWorkspaces` et `statusLine`.

### Profil actif : AUTO LARGE ASSUMÉ

L'adaptateur Antigravity CLI 1.2.6 applique le profil **AUTO LARGE ASSUMÉ** articulé autour du triptyque :
1. **Autonomie large par défaut au runtime** (`toolPermission = "always-proceed"`, `allowNonWorkspaceAccess = true`, `agentMode = "accept-edits"`) ;
2. **DENY technique minimal et symétrique** (destructions irréversibles, Git destructif, élévation de privilèges, interpréteurs inline arbitraires, et protection symétrique `read_file` / `write_file` sur les zones sensibles répertoriées) ;
3. **Règles déclaratives fortes du Workflow** (Frontières sensibles non négociables).

#### Absence de listes intermédiaires
- **`permissions.allow` vide** : sous `always-proceed`, toute commande ou outil non intercepté par une règle `deny` s'exécute automatiquement sans prompt. Aucune micro-whitelist n'est requise.
- **`permissions.ask` vide** : suppression totale des invites répétitives de confirmation sur les actions ordinaires de dev (`git commit`, `git add`, `npm install`, `curl`, etc.).
- **`permissions.deny` minimal** : regroupe uniquement les classes réellement dangereuses et techniquement fiables.

### AUTO ≠ Autorisation fonctionnelle

Le mode AUTO / `always-proceed` signifie uniquement :
**absence de confirmation UI du runtime.**

Il ne confère en aucun cas à l'agent une autorisation fonctionnelle générale d'exécuter n'importe quelle opération. Toute action doit impérativement être :
- strictement nécessaire à la tâche demandée ;
- comprise dans le périmètre convenu ;
- cohérente avec le plan courant ;
- conforme aux règles universelles du Workflow.

**Exemples concrets** :
- `git push` est techniquement AUTO au niveau du runtime, mais ne doit jamais être exécuté si aucune publication vers le remote n'est expressément demandée.
- `brew install` ou `npm install` peuvent être techniquement AUTO, mais ne doivent pas être invoqués si aucune installation n'est requise pour la tâche.
- `curl` ou `ssh` peuvent être techniquement AUTO, mais ne doivent pas être utilisés hors nécessité fonctionnelle prouvée.

### Frontières déclaratives non négociables

L'agent Antigravity est directement assujetti aux **Frontières sensibles non négociables** inscrites dans `AI_WORKFLOW.md` :

Sans instruction humaine explicite, l'agent ne doit jamais :
1. Utiliser `--dangerously-skip-permissions` ou un bypass équivalent ;
2. Contourner une règle `DENY` par shell, sous-processus, script, alias, symlink ou autre mécanisme indirect ;
3. Rechercher, lire, afficher, modifier ou transmettre volontairement des secrets ou identifiants ;
4. Publier, déployer ou transmettre vers un service externe si cela ne fait pas explicitement partie de la tâche ;
5. Supprimer ou écraser volontairement des données importantes hors du périmètre convenu ;
6. Exfiltrer des informations privées.

*Une permission technique n'est pas une autorisation fonctionnelle implicite.*

### Risques résiduels acceptés et limites transparentes

- **Bypass Antigravity (`--dangerously-skip-permissions`)** : Antigravity CLI 1.2.6 ne permet pas de garantir techniquement le blocage étanche de ce drapeau via une règle de permissions quand une autonomie large est en place. Le flag reste formellement **INTERDIT** par le Workflow ; son interdiction repose sur la règle déclarative absolue, sans prétention de verrouillage natif inexistant.
- **Exposition hors workspace** : Avec `allowNonWorkspaceAccess = true`, les fichiers ordinaires hors workspace sont accessibles en lecture et en écriture sans invite d'emplacement. Seules les racines canoniques explicites listées bénéficient du refus natif par préfixe. Les globs `**` ne sont pas évalués selon la qualification 1.2.6 ; les `.env` et clés du workspace ne sont donc pas protégés par ces motifs. Aucun blocage terminal général n’est établi. Les fichiers hors workspace non anticipés dans la deny-list restent accessibles ; ce risque est expressément consenti par l'utilisateur pour fluidifier le travail.
- **Terminal non sandboxé** : Les règles `read_file` et `write_file` protègent les outils natifs de l'agent (`view_file`, `write_to_file`, `replace_file_content`). Elles ne constituent pas une sandbox au niveau du noyau pour les commandes shell autorisées. La non-agression des secrets via terminal repose sur la règle comportementale stricte du Workflow.

## Plan

Le mode Plan natif et les règles du Workflow sont deux couches différentes.

Une mutation doit d'abord satisfaire les règles de plan du Workflow : **objectif · périmètre · étapes · validation · fin attendue**, puis attendre sa validation explicite.

L'approbation du plan ne remplace pas la permission d'outil, et le mode `always-proceed` n'exempte aucunement de l'obligation de plan avant modification.

## Modes d'exécution et autonomie d'édition

Antigravity CLI 1.2.6 articule trois réglages complémentaires :
- **`agentMode = "accept-edits"`** : confère l'autonomie d'édition native (`write_to_file`, `replace_file_content`) sans invite UI répétitive.
- **`toolPermission = "always-proceed"`** : élimine les invites UI sur les commandes et outils réguliers, maintenant uniquement l'interception inconditionnelle des règles `DENY`.
- **`allowNonWorkspaceAccess = true`** : élimine les invites d'emplacement hors workspace pour les opérations ordinaires.

## Modèles, reasoning et escalade

### Principal Antigravity
Le fonctionnement normal est configuré nativement sur **Gemini 3.8 Flash Medium** via la clé `"model": "Gemini 3.8 Flash (Medium)"` dans `~/.gemini/antigravity-cli/settings.json` (ou via les drapeaux CLI `--model` / `--effort`).

Politique d'effort :
- **Normal** → Gemini 3.8 Flash Medium (défaut durable).
- **Difficulté concrète motivée ou Review indépendante formelle** → Gemini 3.8 Flash High. Les difficultés concrètes comprennent : ambiguïté technique persistante, architecture délicate, diagnostic complexe, échecs répétés ou décision nécessitant davantage de raisonnement.
- **Exceptionnel** → escalade supérieure motivée seulement lorsqu'un niveau inférieur est réellement insuffisant.

*Règle d'or :* Medium est le fonctionnement normal ; Flash High est retenu sur difficulté concrète et pour la Review indépendante formelle. La taille seule ne suffit pas à justifier une escalade ; ni le confort ni « pour être sûr » ne la justifient.

### Review et seconde opinion
- **Review indépendante formelle** : Gemini 3.8 Flash High, affinité pour le contrôle indépendant de l’unité et son verdict.
- **Micro-review ciblée/corrective** : Flash Medium possible si suffisant pour contrôler les points bornés concernés.
- **Seconde opinion exceptionnelle** : Gemini 3.1 Pro High pour un besoin explicitement motivé de regard supplémentaire. Pro High n’est jamais le Reviewer par défaut ni une étape automatique après Flash High.

**AFFINITÉ ≠ RÔLE OBLIGATOIRE.** L’escalade reste motivée par un besoin concret ; elle ne signifie pas un passage automatique à Pro et ne forme aucune chaîne obligatoire de modèles.

### Sous-agents (`research` et `self`)
Antigravity CLI 1.2.6 ne fournit pas de clé native de configuration d'effort individuel par sous-agent (la directive `Model: inherit` de l'outil `invoke_subagent` hérite du modèle courant). La politique s'applique donc comme **règle déclarative d'orchestration** :
- **`research`** (recherche, exploration, documentation, analyse statique, collecte de faits) :
  - Normal : Medium ;
  - Complexe : High ;
  - Exceptionnel : escalade supérieure motivée.
- **`self` — implémentation** :
  - Plan clair et implémentation bornée : Medium ;
  - Implémentation complexe ou ambiguë : High ;
  - Exceptionnel : escalade supérieure motivée.
  - La simple délégation à `self` ne justifie jamais à elle seule le niveau High.
- **`self` — Review indépendante** :
  - Review indépendante formelle : Gemini 3.8 Flash High ;
  - Micro-review ciblée/corrective : Flash Medium possible si suffisant ;
  - Difficulté concrète : Flash High ;
  - Seconde opinion exceptionnelle : Gemini 3.1 Pro High, explicitement motivée et jamais automatique.
  - Le Reviewer reste indépendant de l'implémenteur, non-implémenteur pendant toute la Review, et propriétaire unique du verdict.

## Concurrence et fan-out

La capacité normale disponible pour Antigravity est fixée à **jusqu'à 3 sous-agents simultanés**.

Principes d'orchestration :
- **0 axe indépendant** → 0 sous-agent (traitement direct par le Principal) ;
- **1 axe indépendant** → jusqu'à 1 sous-agent ;
- **2 axes indépendants** → jusqu'à 2 sous-agents ;
- **3 axes indépendants** → jusqu'à 3 sous-agents.

La valeur « 3 » représente une **capacité normale disponible**, pas un objectif de fan-out systématique.

**Dépassement ponctuel au-delà de 3 :** possible uniquement si le Principal justifie préalablement l'indépendance réelle des tâches, un gain concret de parallélisme, un quota raisonnable et l'absence de conflit d'écriture.

**Absence de plafond dur technique :** Antigravity n'exposant pas de mécanisme natif associant un défaut à 3 et un override temporaire propre, aucun plafond technique rigide n'est imposé dans `settings.json` ni via un wrapper maison. La limitation repose sur la règle d'orchestration déclarative.

## Sessions, contexte et économie

### Règle de session
**1 grosse unité cohérente → 1 session.**
Une session typique couvre le cycle : analyse → plan → implémentation → validation → Review → commit. Une nouvelle grosse unité indépendante ne doit pas être empilée dans une session déjà chargée.

### Contexte long et compaction
Lorsque le contexte s'allonge :
1. Privilégier la **compaction native** si elle permet de poursuivre proprement la tâche courante ;
2. Si le contexte reste saturé ou si l'unité est achevée, ouvrir une **nouvelle session**.
Aucun seuil numérique arbitraire n'est imposé : la décision relève de la proportionnalité.

### Économie de contexte
- Réutiliser systématiquement les preuves valides sur l'`ETAT` Git courant ;
- Éviter les lectures massives répétitives de fichiers inchangés ;
- Éviter les commandes répétées qui réinjectent les mêmes sorties dans le contexte ;
- Approfondir uniquement en cas d'incertitude concrète, d'échec observable ou de changement d'état pertinent.

## Sandbox

Le sandbox terminal est disponible mais reste **désactivé par défaut**.

Comportement observé avec Antigravity CLI 1.2.6 :
- lecture terminal dans le workspace : possible ;
- écriture terminal dans le workspace : bloquée ;
- écriture terminal hors workspace : bloquée.

Il est donc surtout adapté aux audits et sessions volontairement non mutantes.

## Skills du Workflow

Deux Skills globaux sont maintenus par le Workflow :

```text
~/.gemini/antigravity-cli/skills/preparer-commit/SKILL.md
~/.gemini/antigravity-cli/skills/cloturer-branche/SKILL.md
```

Leurs sources appartiennent à l'adaptateur sous `fichiers-installation/`.

Ils restent courts et indépendants d'Antigravity : ils chargent seulement la procédure utile au moment où elle est nécessaire.

## Statusline

Une statusline personnalisée est maintenue dans :

```text
adaptateurs/antigravity/fichiers-installation/.gemini/antigravity-cli/statusline.sh
```

et installée dans :

```text
~/.gemini/antigravity-cli/statusline.sh
```

Elle utilise le payload natif fourni par Antigravity pour afficher de manière compacte :

```text
modèle
contexte utilisé
quota 5 h
quota hebdomadaire
branche Git
workspace
```

Le contexte est coloré dynamiquement :

```text
0–39 % utilisé   → vert
40–69 % utilisé  → jaune
70–100 % utilisé → rouge
```

## Autonomie opérationnelle et proportionnalité

Les règles universelles demandent d'utiliser directement les mécanismes courants, déterministes et déjà qualifiés.

L'agent n'inspecte pas préventivement les permissions pour prédire un éventuel blocage :
- un mécanisme déjà qualifié est utilisé directement sous l'autonomie large du runtime (`always-proceed`) ;
- une décision humaine est sollicitée via un point d'arrêt déclaratif `STOP` dès lors qu'une garantie fonctionnelle du Workflow l'exige (barrières Git pour `git add`, `git commit`, `git push`, clôture de branche, publication), ou lorsqu'une invite du runtime intervient ;
- le Reviewer réutilise en priorité les preuves valides sur l'`ETAT` Git courant et ne relance pas de validation uniquement "pour être plus sûr".

## Évolution d'Antigravity

Les mécanismes observés sont requalifiés selon une approche **capability-first** :
1. La politique de développement autonome, de non-mutation non validée et de protection des secrets est **durable** et indépendante des versions.
2. Les syntaxes, outils et réglages spécifiques restent **versionnés** dans l'adaptateur.
3. Lors d'une mise à jour d'Antigravity, seule la sous-partie affectée (permissions, subagents, Web ou statusline) fait l'objet d'une requalification ciblée, consignée dans `tests/antigravity/REQUALIFICATION.md`.

## Limites de l'édition publique
Le profil documenté always-proceed avec accès hors workspace n'est pas un confinement strict. Le sandbox terminal optionnel ne remplace pas les contrôles Read/Edit/Write et n'est pas activé par défaut dans le profil historique décrit. Les STOP humains et certaines interdictions restent déclaratifs. Aucun changement de permission ni nouvelle qualification runtime n'est effectué par cette préparation.

## Rectification de portée de la protection des secrets
Le contrat documentaire `secrets_proteges` est qualifié de partiel dans cette édition. Les affirmations générales du profil historique doivent être lues avec cette restriction. Les règles opérationnelles sont conservées ; ce changement de métadonnées ne renforce pas les permissions. Sous always-proceed, une lecture terminal telle que `cat .env` ne bénéficie pas des refus des outils natifs. Ne pas installer ce profil avec des données sensibles en supposant une protection générale.
