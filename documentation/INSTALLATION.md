# Installation contrôlée — édition publique

## Prérequis et portée
macOS est la plateforme examinée. Command Line Tools avec /usr/bin/git et /usr/bin/python3 fonctionnels, Python 3.12.14 ou 3.13 pour les autres suites, shell POSIX et jq sont nécessaires aux composants concernés. osascript assure les notifications macOS. Les fournisseurs s'installent et s'authentifient séparément selon leur documentation ; leur accès et leurs quotas ne sont pas fournis par le dépôt. Ne pas revendiquer la compatibilité complète Linux/Windows.

## Structure
`AI_WORKFLOW.md` et `architecture/` contiennent les règles ; `adaptateurs/` les fichiers installables et manifestes ; `procedures/` les opérations ; `tests/` les bancs et archives ; `outils/` l'empreinte Git. Les instructions restent intentionnellement en français.

## Avant toute installation
Lire README et mécanismes de l'adaptateur choisi. Exécuter les tests hors ligne indiqués dans le README. Inspecter `~/.ai-workflow` : s'il existe, ne pas l'écraser, le déplacer ou le remplacer. Sur une machine utilisant déjà un workflow privé, faire les essais dans un compte séparé. Cette préparation publique ne modifie aucun lien global.

## Sauvegarde et comparaison
Établir une liste des fichiers et clés à installer d'après l'INVENTAIRE de l'adaptateur. Sauvegarder uniquement les cibles concernées dans un dossier privé hors dépôt, en conservant leurs permissions. Noter les fichiers absents initialement. Comparer chaque fichier source/cible ; ne jamais copier récursivement `.claude`, `.codex` ou `.gemini` depuis un environnement personnel.

## Racine stable et fichiers statiques
Dans un compte vierge, choisir une racine stable pour ce dépôt et créer `~/.ai-workflow` vers cette racine seulement si la destination n'existe pas. Copier chaque fichier statique déclaré par l'inventaire, après validation de son diff. Pour Codex, préserver le lien relatif `.local/bin/review-native-codex` vers `.codex/bin/review-native-codex` et les permissions exécutables du lanceur. Ne pas modifier les noms des composants pour traduire leur langue.

## Réglages des adaptateurs
- Claude : `configuration-workflow.json` contient un `fragment_settings`, pas un settings.json complet. Examiner puis fusionner manuellement les seules clés choisies ; les listes de permissions et les hooks exigent une comparaison attentive. Ne jamais remplacer les réglages existants, leur authentification, leurs connexions MCP ou leurs plugins.
- Codex : appliquer manuellement les paramètres choisis du manifeste dans config.toml ; les noms pointés décrivent des clés imbriquées. Ne pas copier le JSON comme TOML et ne pas effacer les autres tables.
- Antigravity : profil large documenté dans son manifeste et guide. L'accès hors workspace et always-proceed sont des décisions à accepter explicitement lors de l'installation ; ils ne constituent pas un sandbox strict. Ne pas l'installer par défaut simplement parce qu'il figure dans le dépôt.

## Validation progressive
Parser JSON/TOML, contrôler les différences et redémarrer une session neuve. Dans un dépôt jetable contenant uniquement des données fictives, contrôler la racine chargée, les outils, les permissions effectives et les points d'arrêt humains. Les sessions fournisseurs peuvent transmettre du code et consommer un abonnement/quota. Exiger une décision explicite avant ces essais. Les simulations publiques vérifient des mécanismes locaux ; elles ne valident pas la fusion de tous les réglages réels ni le comportement des fournisseurs.

## Retour à l'état initial
Arrêter les sessions concernées. Comparer l'état actuel avec l'état sauvegardé : si des modifications utilisateur sont intervenues, restaurer seulement les clés/fichiers de cette installation. Restaurer les sauvegardes approuvées et retirer seulement les nouveaux fichiers consignés comme créés par l'installation. Aucun nettoyage récursif de configuration globale. Ne retirer le lien de racine que si sa création fait partie de cette installation et qu'il vise toujours cette édition.

## Limites des preuves
Voir VALIDATION_PUBLIQUE.md : copies de fichiers et conservation de clés étrangères simulées dans un répertoire temporaire ; aucune installation réelle dans les réglages de l'auteur. Les versions anciennes restent des références historiques, pas des garanties sur une version nouvelle.

## Prérequis exacts et contrôle du hook
Les hooks distribués appellent `/usr/bin/python3` ; l’empreinte appelle `/usr/bin/git`. Installer les Command Line Tools et vérifier que ces exécutables fonctionnent réellement :
```sh
/usr/bin/python3 --version
/usr/bin/git --version
```
Après copie contrôlée du hook, lui transmettre uniquement du JSON synthétique (la chaîne Git n’est pas exécutée) :
```sh
printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"git add x"}}' | /usr/bin/python3 -B ~/.claude/hooks/barriere-git.py
```
La réponse JSON attendue contient `"hookSpecificOutput": {"permissionDecision": "ask", ...}` (d’autres champs sont possibles). Ce contrôle vérifie l’interpréteur et le script copié, pas son branchement dans settings.json ; le déclenchement dans une session fournisseur relève de la validation progressive distincte. Une absence, une erreur ou une sortie différente interdit de considérer le hook comme opérationnel : arrêter l’installation et diagnostiquer. Ne pas supposer qu’une erreur d’interpréteur bloque les actions de l’agent. La suite du hook peut également être rejouée avec `/usr/bin/python3 -B tests/claude/outils/test_barriere_git.py`.

Pour fusionner les listes de permissions/hooks, préserver les éléments utilisateur existants et ajouter seulement les éléments revus, en évitant les doublons ; ne pas remplacer une liste entière. La simulation publique ne prouve pas cette fusion manuelle complète. Contrôles syntaxiques après sauvegarde, en adaptant la cible :
```sh
python3 -m json.tool ~/.claude/settings.json >/dev/null
python3 -c 'import tomllib, pathlib; tomllib.loads((pathlib.Path.home()/".codex/config.toml").read_text())'
```
Le second exemple requiert Python 3.11 ou supérieur ; ne pas utiliser le Python système 3.9 pour tomllib. Les contrôles syntaxiques ne vérifient pas la sémantique des réglages.
