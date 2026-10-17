# Validation de l'édition publique — 17 octobre 2026

## Contrôles nouveaux réellement exécutés
Environnement macOS, Python 3.12.14 et 3.13, Git et shells système. Aucun fournisseur appelé pour les tests hors ligne.

| Contrôle | Résultat | Portée |
|---|---|---|
| Matrice historique du hook rejouée sur la copie | 118/118, aucun écart | JSON synthétique transmis au hook ; aucune commande Git des chaînes exécutée |
| Auto-tests des bancs rejoués | 28/28 | Analyse de traces fictives et détection de bancs défaillants ; fichiers temporaires |
| Suite publique | 13 tests réussis : 12 contrôles et 1 constat de limite | Lanceur avec faux codex, erreurs/arguments/cleanup, empreinte d'un dépôt jetable sans commit, simulation de copies/fusion/retour arrière, entrées hook |
| Heredoc non cité | Limite CONFIRMÉE hors ligne | Le hook ne demande aucune décision pour une substitution Git présente dans le corps ; aucune substitution exécutée. Ce constat n'est PAS une protection validée |
| Syntaxes Python/JSON/shell | Aucune erreur dans les fichiers sélectionnés | Analyse statique seulement ; aucun TOML dans les sources distribuées après exclusion de l'adaptateur historique Grok |
| Confidentialité initiale | Aucun candidat détecté par les motifs locaux | Chemins utilisateur, UUID de sessions, clés/tokens connus et e-mails hors exemples ; contrôle non exhaustif |

Le premier passage du test d'installation a révélé une comparaison incorrecte entre /var et /private/var sur macOS. Le test a été corrigé pour comparer les chemins canoniques ; la suite complète a ensuite réussi. Le lanceur et les protections n'ont pas été modifiés.

## Simulations et limites
La simulation d'installation vérifie la conservation de clés fictives étrangères au fragment Claude, une sauvegarde/restauration et le lien relatif du lanceur Codex. Elle n'est pas une installation réelle de tous les adaptateurs ni une validation de fusion complète de réglages utilisateur. La validation syntaxique du manifeste Codex et les tests du faux exécutable ne requalifient pas le CLI Codex réel. Aucun test Java, cloud, quota ou sandbox fournisseur n'est rejoué par ces suites.

Les archives dans tests/claude, tests/codex et tests/antigravity sont historiques et anonymisées. Certaines traces brutes temporaires ont disparu. Les chemins des exécutables installés observés avant préparation désignaient Claude Code 2.1.296 et Codex 0.161.0, versions plus récentes que les campagnes historiques : aucune qualification complète actuelle n'est revendiquée.

## Revue indépendante
Deux passes réelles : Claude Code, processus neufs, modèle Opus, effort high, analyse statique des seuls contenus publics contrôlés. Verdict final : PRÊT POUR VALIDATION HUMAINE, aucun nouveau Bloquant ou Important ; les corrections secondaires postérieures sont contrôlées par l’implémenteur. Aucun test exécuté par le reviewer. Voir REVUE_PUBLIQUE.md pour le suivi.

## Précisions après revue
Le test de fusion préserve des clés étrangères, pas tous les éléments préexistants des listes ; la procédure manuelle demande leur conservation par union revue. Le sous-processus de l’empreinte ne transmet pas GIT_CONFIG_GLOBAL/GIT_CONFIG_NOSYSTEM ; l’isolation de ces variables ne concerne que git init/status du banc. Aucun commit n’est créé. Le contrôle doit donc se dérouler sans données sensibles et sans supposer une isolation globale complète.

Les bits exécutables et le lien relatif du lanceur sont contrôlables sur les fichiers avant staging ; les modes Git 100755 et 120000 devront être vérifiés dans l’index après autorisation de staging. Aucun index public n’existe encore. L’affichage du chemin Codex résolu reste une suggestion différée : le lanceur n’est pas modifié. La note IDENTITE_GITHUB est volontairement générique et conservée pour aider les utilisateurs à séparer les identités privées et publiques.

Le 17 octobre 2026, la matrice du hook a aussi été rejouée avec l’interpréteur réellement référencé par les hooks, /usr/bin/python3 3.9.6 : 118/118, aucun écart. /usr/bin/git répond en version 2.54.0 (Apple Git-157). Cela vérifie le hook source, pas une installation dans les réglages utilisateur.

Les preuves finales et la liste SHA-256 de la copie figée sont enregistrées dans le rapport local de préparation, hors du dépôt public, pour éviter une auto-empreinte récursive. Elles distinguent fichiers revus et corrections documentaires postérieures. La vérification finale du .gitignore porte sur 9 cas exclus et 7 cas conservés dans un dépôt temporaire sans commit : aucun écart.
