# Procédure universelle : Préparer un commit

Ce document décrit la procédure universelle pour préparer une unité logique de commit sans l'exécuter. Il définit les besoins logiques et les décisions requises, indépendamment des outils ou interfaces spécifiques.

---

## 1. Principes directeurs

- **Garde de cohérence :** Le processus constate la propreté de l'unité, réutilise les preuves matérielles existantes et prévient les erreurs de périmètre, sans réexécuter de vérifications superflues.
- **Minimalité pour toute opération autonome :** Pour toute action relevant du périmètre autonome (lecture, inspection, validation, test, build, lint), préférer le mécanisme le plus direct, natif ou atomique suffisant. Éviter la complexité technique évitable (pipelines superflus, scripts intermédiaires non nécessaires) dès lors qu'un mécanisme simple répond au besoin.
- **Préservation des frontières de décision :** Toute opération modifiant durablement l'état Git (staging, création de commit) relève d'une décision humaine explicite. La minimalité ne s'applique jamais dans le but d'éviter ou d'affaiblir une autorisation humaine obligatoire.

---

## 2. Séquence universelle

1. **Établir l'état matériel :**
   Relever l'état matériel du projet et l'empreinte de l'arbre de travail avec le mécanisme d'état qualifié de l'environnement (ex. empreinte Git déterministe et état synthétique des fichiers).
2. **Délimiter l'unité logique :**
   Identifier strictement les fichiers modifiés appartenant à l'objectif courant. Distinguer et préserver toute modification préexistante ou indépendante de l'unité.
3. **Réutiliser les preuves et la Review existantes :**
   Identifier les preuves dynamiques (tests, build, linters) et les verdicts de Review déjà produits sur cet arbre. Réutiliser obligatoirement toute preuve encore valide sans rejeu aveugle.
4. **Évaluer le delta manquant :**
   Selon le risque réel du changement et l'impact potentiel (heuristiques d'impact), déterminer si une validation ciblée ou une Review indépendante minimale est requise. L'absence de Review antérieure n'impose pas une Review indépendante si le risque ne la justifie pas (la documentation pure, le formatage ou les modifications triviales se valident au niveau d'analyse statique adapté).
5. **Vérifier les garde-fous :**
   Interdire la préparation du commit si un test requis échoue, si un finding bloquant ou important subsiste, si des secrets, tokens ou caches temporaires non ignorés sont détectés, ou si le périmètre n'est pas atomique.
6. **Barrière Staging (`git add`) :**
   Présenter explicitement la liste exacte des fichiers à stager constituant l'unité logique (éviter tout ajout global aveugle) → **STOP** → attendre la validation humaine explicite → exécuter `git add` uniquement sur le périmètre validé.
7. **Barrière Commit (`git commit`) :**
   Présenter l'unité stagée, l'`ETAT` et preuves pertinentes, le verdict de Review et le message proposé en français (titre court, description si utile, complété des trailers d'attribution réelle `AI-Agent:`, et `AI-Reviewer:` si une Review indépendante distincte a été menée) → **STOP** → attendre la validation humaine explicite → seulement ensuite exécuter `git commit`.
8. **Bilan post-commit :**
   Constater la révision du commit créé, vérifier la propreté du working tree et recalculer l'`ETAT`.
