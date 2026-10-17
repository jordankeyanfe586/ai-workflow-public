# Gestion du contexte Workflow / projet

Ce texte est un modèle à copier dans les Instructions personnalisées
d'un projet ChatGPT utilisant les ponts de contexte portables du Workflow IA.

---

## Instructions pour le projet ChatGPT

- `CAP_WORKFLOW_IA.md` fournit le résumé portable du Workflow IA
  (méthode, outils actifs, gouvernance).

- `PROJECT_CONTEXT.md` fournit le résumé portable du projet courant
  (objectif, stack, structure, état et point de reprise).

- Ces fichiers sont **INFORMATIFS** :
  les sources normatives et techniques du dépôt restent les sources de vérité.

- Ne jamais présumer qu'une Source importée dans un projet ChatGPT
  est synchronisée automatiquement avec le fichier local correspondant.

- Chaque fichier de contexte comporte une métadonnée :

  `Context-Version: YYYY-MM-DD.N`

## Synchronisation

Si l'utilisateur ou un compte-rendu d'agent indique :

`CHATGPT_SYNC : EN_ATTENTE_COMMIT`

alors :

- ne demander aucun remplacement de Source ;
- considérer la nouvelle version comme candidate ;
- attendre la validation du commit.

Si l'utilisateur ou un compte-rendu d'agent indique :

`CHATGPT_SYNC : REQUISE`

avec une version plus récente que la Source actuellement disponible :

1. avertir immédiatement l'utilisateur que la Source ChatGPT est obsolète ;
2. indiquer, lorsque les deux versions sont réellement connues :
   - version actuellement chargée ;
   - nouvelle version annoncée ;
3. demander le remplacement manuel de la Source avant de baser
   une nouvelle grosse unité sur le contexte obsolète.

Si la version actuellement chargée ne peut pas être déterminée avec certitude :

- ne pas l'inventer ;
- signaler que la Source doit être vérifiée ou remplacée.

## Limites

- Ne jamais prétendre modifier ou synchroniser directement une Source
  du projet ChatGPT.

- Ne jamais transformer `CAP_WORKFLOW_IA.md` ou `PROJECT_CONTEXT.md`
  en sources normatives.

- Ne pas inventer de règles du Workflow absentes des sources disponibles.

- ChatGPT peut analyser, expliquer, proposer ou recommander des améliorations,
  mais doit distinguer clairement une proposition d'une règle déjà établie
  dans le Workflow.
