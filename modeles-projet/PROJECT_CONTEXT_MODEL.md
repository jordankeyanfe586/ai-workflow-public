<!-- CONTEXT_METADATA
Context-Version: [YYYY-MM-DD.N]
Updated: [YYYY-MM-DD]
Scope: [nom-du-projet]
-->

# Contexte du projet — [Nom du projet]

**Workflow IA :** activé

## Projet
- **Nom :** [nom du projet]
- **Objectif :** [objectif principal du projet en quelques lignes]
- **État :** [prototype / développement / maintenance / production]
- **Branche de référence :** `main`

## Architecture et structure
- `[chemin/]` : [rôle du composant]
- `[chemin/]` : [rôle du composant]
- `[chemin/]` : [rôle du composant]

Documentation complémentaire : [chemin si nécessaire]

## Stack technique
- **Langage :** [langage et version]
- **Framework :** [framework principal]
- **Build / dépendances :** [outil de build ou gestionnaire de paquets]
- **Base de données :** [si applicable]
- **Autres :** [technologies structurantes]

Les fichiers de configuration du projet restent la source de vérité pour les versions exactes.

## Commandes canoniques

### Lancement
```bash
[commande]
```

### Tests
```bash
[commande]
```

### Build
```bash
[commande]
```

### Autres validations
```bash
[lint / format / analyse statique / autre]
```

## Conventions durables
- [convention d'architecture ou de nommage propre au projet]
- [convention de test ou de packaging propre au projet]

## Contraintes et points d'attention
- [contrainte technique ou métier structurante]
- [point d'attention critique]

## État et point de reprise
- **Étape en cours :** [description succincte du travail actif]
- **Prochaine grande étape :** [objectif structurant suivant]

## Coordination avec ChatGPT
Si ce projet utilise ChatGPT comme couche de pilotage ou de continuité :
- `~/.ai-workflow/CAP_WORKFLOW_IA.md` = résumé portable du Workflow (méthode et gouvernance).
- `PROJECT_CONTEXT.md` = résumé portable du projet courant.
- Les deux fichiers sont **INFORMATIFS** ; les sources locales du dépôt font autorité.
- Une Source importée dans ChatGPT n'est jamais supposée se synchroniser automatiquement.

**Règle opérationnelle CHATGPT_SYNC :**
Lorsqu'une modification matérielle d'un fichier de contexte portable intervient :

- **AVANT COMMIT (Review / Staging) :**
  ```text
  CHATGPT_SYNC :
  STATUT : EN_ATTENTE_COMMIT
  ACTION_UTILISATEUR : AUCUNE POUR L’INSTANT
  ```
- **APRÈS COMMIT VALIDÉ :**
  ```text
  CHATGPT_SYNC :
  REQUISE : OUI
  ACTION_UTILISATEUR : Remplacer la Source ChatGPT correspondante par la version commitée.
  ```

Pour le protocole complet : `~/.ai-workflow/architecture/PORTABLE.md`.

## Sources de vérité
Ce fichier est **INFORMATIF et synthétique**. Il ne remplace jamais les sources du dépôt :
- Code source et configurations → **SOURCE DE VERITE** technique.
- Règles de développement universelles → `~/.ai-workflow/AI_WORKFLOW.md`.
- Architecture portable et dispatch → `~/.ai-workflow/architecture/PORTABLE.md`.

## Garde-fous de maintenance
- **OBLIGATION de mise à jour matérielle uniquement** : modifier ce fichier lors d'un changement significatif (architecture, stack, commandes canoniques, conventions durables, bascule d'état ou étape majeure).
- **INTERDIT d'en faire un journal de commits** : ne pas modifier pour des retouches locales, corrections de bugs ordinaires ou micro-ajustements.
