> **Édition publique : archive de qualification historique.** Les identifiants locaux ont été anonymisés. Les commits cités appartiennent au dépôt privé initial, pas au nouvel historique public. Les résultats ci-dessous ne qualifient pas automatiquement les versions actuelles ; certaines traces temporaires ne sont plus disponibles. Voir [VALIDATION_PUBLIQUE.md](../documentation/VALIDATION_PUBLIQUE.md) pour les nouveaux contrôles.

# Guide de requalification des adaptateurs IA

## Objectif

Ce guide indique **quoi retester** lorsqu'un adaptateur déjà configuré doit être requalifié après :

- une modification du Workflow universel ;
- un nouvel enseignement découvert avec un autre adaptateur ;
- une évolution importante de l'outil ou du modèle ;
- une modification de ses Hooks, permissions, agents ou mécanismes natifs.

Il ne remplace pas `tests/TESTS_UNIVERSELS.md`.

Le protocole universel définit **comment tester**.
Ce guide sert seulement de **checklist rapide de requalification**.

---

## Checklist minimale

- [ ] instructions universelles réellement appliquées
- [ ] `PROJECT_CONTEXT.md` correctement exploité
- [ ] pré-vérification Git avant modification
- [ ] changements préexistants détectés et préservés
- [ ] tâche simple traitée proportionnellement
- [ ] tâche difficile correctement explorée et planifiée si nécessaire
- [ ] autorisations humaines atomiques : une seule commande par demande
- [ ] lectures Git courantes sans faux positif
- [ ] opérations Git interdites réellement bloquées
- [ ] variantes syntaxiques importantes couvertes
- [ ] implémentation limitée au besoin
- [ ] tests et build réellement exécutés
- [ ] Review indépendante
- [ ] boucle de correction fonctionnelle si nécessaire
- [ ] cycle Git complet jusqu'à un état propre
- [ ] continuité correcte après reprise
- [ ] observabilité et notifications vérifiées selon les capacités de l'outil

---

## Conditions du retest

Les tests comportementaux doivent être :

- réalistes ;
- difficiles lorsque nécessaire ;
- à l'aveugle ;
- réalisés dans un environnement neutre ;
- non guidés vers le comportement attendu ;
- isolés dans une nouvelle session lorsque le contexte précédent pourrait les contaminer.

Le scénario principal de développement doit rester **difficile mais borné**.

---

## Quand refaire un test

Retester une garantie si :

1. sa règle universelle a changé ;
2. son mécanisme d'adaptation a changé ;
3. un autre adaptateur révèle un nouvel angle mort universel ;
4. une mise à jour de l'outil peut avoir modifié son comportement ;
5. la précédente validation était guidée, contaminée ou insuffisamment réaliste.

Ne pas refaire automatiquement tous les tests lorsqu'aucune de ces conditions ne s'applique.

---

## Enseignements à rétroporter

À compléter pendant la validation des adaptateurs.

### Codex

- [ ] clôturer après l’audit final

Enseignements universels déjà retenus :

- autorisation sensible strictement atomique ;
- contrôles indépendants en lecture seule regroupables par diagnostic ;
- preuve réutilisable tant que son état pertinent reste inchangé ;
- invalidation ciblée avant tout retest ;
- empreinte d’état pour distinguer changement réel et simple transition Git ;
- délégation proportionnelle au gain de contexte/quota ;
- séparation nette entre règle, mécanisme et preuve ;
- tests comportementaux réellement à l’aveugle et artefacts neutres.

### Claude Code

Après la clôture Codex :

- [ ] comparer l’adaptateur actuel aux garanties universelles les plus récentes ;
- [ ] identifier les mécanismes devenus obsolètes, redondants ou insuffisants ;
- [ ] requalifier Claude Code sur la configuration actuelle ;
- [ ] rétroporter vers Codex uniquement les nouveaux angles morts réellement universels.

### OpenCode

- [ ] compléter lors de sa validation

---

## Ordre prévu

~~~text
terminer Codex
→ requalifier Claude Code
→ retests Codex ciblés seulement si Claude révèle un angle mort universel
→ adapter les outils restants selon l’ordre décidé
→ audit final multi-outils
~~~

---

## Principe

~~~text
un adaptateur révèle un angle mort
→ vérifier s'il est universel
→ mettre à jour le Workflow si nécessaire
→ rétroporter le contrôle vers les adaptateurs déjà validés
~~~
---

## Notes de requalification Codex — orchestration, contexte et preuves

Points révélés ou confirmés pendant le cycle réel `gestion-personnes` :

- le principal doit rester principalement **orchestrateur** ; son écriture directe dans le code ou les fichiers projet doit être quasi nulle, sauf besoin très limité et justifié ;
- `worker` porte l’implémentation et les corrections non triviales ;
- `explorer` porte les explorations volumineuses, cartographies et recherches qui chargeraient inutilement le contexte principal ;
- la Review doit être réellement indépendante via un reviewer distinct de l’implémentation ;
- le principal peut contrôler brièvement la cohérence du verdict du reviewer, sans refaire toute la Review ;
- les sous-agents doivent recevoir une **mission minimale suffisante**, pas l’historique complet de la conversation ;
- les traces détaillées restent autant que possible dans le thread du sous-agent ; le retour à l’orchestrateur doit rester compact et exploitable ;
- une preuve déjà établie ne doit pas être recalculée si l’état pertinent n’a pas changé ;
- privilégier des **empreintes d’état** et des contrôles différentiels pour savoir quelles preuves restent valides ;
- les validations lourdes, relectures complètes et Reviews répétées doivent être évitées lorsqu’aucune modification pertinente n’est intervenue ;
- charger les Skills, règles détaillées et fichiers volumineux seulement lorsque l’étape courante en a besoin ;
- l’automatisation doit progresser jusqu’au prochain point nécessitant une décision ou une autorisation humaine, sans interpréter une demande générale de continuation comme une autorisation implicite ;
- l’usage de sous-agents doit rester proportionné : l’isolation doit apporter plus de valeur que son coût en contexte et en quota ;
- Codex dispose déjà de `worker` et `explorer` ; un `explorer` Claude Code pourra être envisagé seulement si un besoin réel est démontré ;
- aucun agent spécialisé supplémentaire ne doit être ajouté sans besoin observé.

Ces anciens points ouverts ont depuis été résolus, reclassés ou rendus non bloquants. Leur **état courant n’est plus maintenu ici** : `tests/codex/REQUALIFICATION.md` est propriétaire des verdicts actuels et Git conserve l’historique détaillé.
---

## Enseignements Codex — blocage et escalade de modèle

À conserver pour la suite de la requalification :

- pendant le travail d’un sous-agent, le principal doit demander son statut directement plutôt que relire le projet pour deviner sa progression ;
- un sous-agent doit pouvoir signaler explicitement `WORKING`, `BLOCKED` ou `DONE` ;
- un agent bloqué ne doit pas consommer indéfiniment du contexte et du quota en répétant des tentatives sans progrès ;
- après plusieurs approches réellement différentes sans résultat, il doit retourner un diagnostic compact à l’orchestrateur ;
- un reviewer peut servir ponctuellement de diagnosticien indépendant d’un blocage sans modifier directement le travail ;
- une escalade vers un modèle supérieur doit rester exceptionnelle, ciblée et temporaire ;
- par défaut, une montée de modèle nécessite une autorisation humaine tant que sa catégorie n’a pas été testée et explicitement autorisée ;
- même une première montée doit nécessiter une autorisation si son périmètre est large ou potentiellement coûteux ;
- toute montée doit revenir au modèle normal après résolution ;
- toute escalade doit être journalisée afin de permettre un audit périodique de sa fréquence, de son motif et de son utilité ;
- la planification ponctuelle avec un modèle supérieur constitue une politique distincte de l’escalade sur blocage ;
- le schéma « modèle supérieur en Plan mode → plan → retour au modèle normal → exécution » reste une hypothèse architecturale à implémenter et tester séparément.
---

## Journal détaillé de requalification Codex

Le journal détaillé de la validation Codex est conservé dans :

`tests/codex/REQUALIFICATION.md`

Il contient les verdicts actuels, les preuves et leurs conditions d’invalidation.
