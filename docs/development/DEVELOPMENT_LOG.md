# IRIS — Development Log

Ce fichier est le journal de bord permanent du développement d'IRIS.
Chaque session de travail doit ajouter une entrée datée, sans effacer les entrées précédentes.

## Règles de suivi

Pour chaque session, consigner :
- l'objectif et le périmètre de la session ;
- les tâches réellement effectuées ;
- les fichiers créés, modifiés ou supprimés ;
- les commandes et validations exécutées, avec leurs résultats ;
- les commits créés (hash et message) et leur état de publication ;
- les problèmes rencontrés, les décisions prises et le travail restant.

Ne jamais déclarer une validation réussie si la commande correspondante n'a pas été exécutée avec succès. Les commits doivent rester petits, atomiques, utiles et vérifiables. Objectif de cadence : au moins un commit par jour de travail sur IRIS, sans fabriquer de changements artificiels.

---

## Session 2026-11-17 — Prototype validé et initialisation du workspace

### Objectif
Conserver la maquette approuvée, documenter le produit et préparer le passage à une application React/TypeScript maintenable.

### Réalisations confirmées
- Cahier des charges et direction visuelle conservés dans `docs/requirements/`.
- Prototype interactif conservé dans `prototype/` avec HTML, CSS et JavaScript.
- Workspace npm initialisé à la racine avec les workspaces `apps/*` et `packages/*`.
- Application web initialisée dans `apps/web/` avec React, TypeScript et Vite.
- Tailwind CSS v4 référencé dans les dépendances et branché dans la configuration Vite.
- Fichiers de base ajoutés : `.editorconfig`, `.gitignore`, `README.md`, `index.html`, `App.tsx`, `main.tsx`, `index.css`.
- Scripts npm racine et scripts applicatifs définis pour dev, build, lint et typecheck.

### Historique Git confirmé
| Commit | Message | Publication |
| --- | --- | --- |
| `d383014` | `docs(product): establish IRIS requirements and visual direction` | Inclus dans la publication de la branche main |
| `e45baa2` | `feat(prototype): add interactive IRIS product walkthrough` | Inclus dans la publication de la branche main |
| `639be91` | `chore(setup): scaffold React TypeScript workspace` | Push confirmé vers `origin/main` |

### Environnement observé
- Node.js : `v24.14.1`
- npm : `11.11.0`
- Runtime compatible avec les contraintes Node/npm déclarées dans le workspace.

### Blocage technique à résoudre
Les premières tentatives d'installation npm n'ont pas abouti. Les manifestes contenaient également certaines versions de paquets qui n'avaient pas été correctement vérifiées. Aucun `node_modules/` ni `package-lock.json` n'était présent lors de la vérification de cette session. Le build, le lint, le typecheck et les tests ne sont donc **pas encore validés**.

Diagnostic en cours : vérifier l'accès au registre npm, puis contrôler les versions disponibles et corriger les manifestes avant de générer le lockfile. Ne pas déclarer l'environnement prêt avant une installation reproductible et des vérifications réussies.

---

## Session 2026-11-17 — Journalisation et diagnostic npm

### Objectif
Mettre en place ce journal durable et reprendre le diagnostic de l'installation des dépendances.

### Réalisations
- Création de ce fichier : `docs/development/DEVELOPMENT_LOG.md`.
- Lecture et inspection des manifestes racine et applicatif, de la configuration Vite, du TypeScript et des points d'entrée React.
- Confirmation de Node.js `v24.14.1`, npm `11.11.0`, et du registre configuré `https://registry.npmjs.org/`.
- Confirmation que `node_modules/` et `package-lock.json` sont absents au début du diagnostic.

### Validation / résultat
- La commande de vérification des versions npm et du runtime a répondu correctement.
- Une requête de test vers le registre npm a été lancée ; son résultat reste à relever.
- Aucune installation, compilation ou suite de tests n'est déclarée réussie à ce stade.

### Prochaines actions
1. Relever le résultat de `npm ping` et les détails du journal npm.
2. Si le registre est accessible, vérifier les versions des dépendances et corriger les versions invalides.
3. Installer les dépendances et générer `package-lock.json`.
4. Exécuter lint, typecheck et build ; ajouter les tests une fois l'installation stabilisée.
5. Ajouter les workflows CI GitHub Actions après validation locale.
6. Créer un commit dédié au journal et aux changements de configuration effectivement validés, puis le pousser.
