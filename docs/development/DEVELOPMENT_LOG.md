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

---

## Session 2026-11-17 — Installation stabilisée, tests et intégration continue

### Objectif
Terminer l'installation des dépendances du workspace, introduire des tests automatisés, puis vérifier le cycle qualité local et préparer GitHub Actions.

### Réalisations
- L'installation initiale des dépendances a abouti : 88 paquets ajoutés et un premier `package-lock.json` généré.
- Vérification de l'arbre des dépendances : React 19.3.1, React DOM 19.3.1, TypeScript 7.0.2, Vite 7.3.1, Tailwind CSS 4.1.18, plugin React 5.1.1 et Oxlint 1.94.0.
- Installation des outils de test : Vitest 3.2.4, jsdom 26.1.0, Testing Library React 16.3.0 et jest-dom 6.9.1.
- Configuration de Vitest avec jsdom et un fichier de setup qui nettoie le DOM après chaque test.
- Ajout de deux tests de rendu pour la coque React d'IRIS.
- Ajout des scripts `test` et `test:watch` dans le workspace web et du script `test` à la racine.
- Ajout du workflow GitHub Actions `.github/workflows/ci.yml` : installation reproductible via `npm ci`, lint, typecheck, tests et build sur push/pull request vers main.

### Fichiers créés ou modifiés
- `package-lock.json` — verrouillage des dépendances npm.
- `package.json` — commande de test racine.
- `apps/web/package.json` — dépendances de test et scripts.
- `apps/web/vite.config.ts` — configuration Vitest/jsdom.
- `apps/web/src/test/setup.ts` — extensions jest-dom et nettoyage après test.
- `apps/web/src/App.test.tsx` — deux tests de rendu.
- `.github/workflows/ci.yml` — pipeline qualité GitHub Actions.
- `docs/development/DEVELOPMENT_LOG.md` — journal de cette session.

### Validations exécutées
| Commande | Résultat |
| --- | --- |
| `npm test` | Réussi — 1 fichier de test, 2 tests passés |
| `npm run lint` | Réussi — 0 warning, 0 erreur |
| `npm run typecheck` | Réussi — aucune erreur TypeScript |
| `npm run build` | Réussi — bundle de production généré par Vite |
| `npm ci --no-audit --no-fund` | Réussi — installation propre et reproductible, 180 paquets installés |

Le premier passage des tests a révélé un problème de nettoyage du DOM entre les cas de test. Le setup Vitest a été corrigé avec `cleanup()` après chaque test ; le second passage est entièrement vert.

### État Git
Deux commits atomiques ont été créés localement :
| Commit | Message | Contenu |
| --- | --- | --- |
| `9923bec` | `test(web): configure Vitest and add app shell tests` | Lockfile, dépendances Vitest, configuration et deux tests React |
| `1e471b6` | `ci(github): add web quality pipeline` | Workflow GitHub Actions |

Publication sur `origin/main` : les deux commits sont en attente du push groupé.

### Prochaines actions
1. Pousser les commits tests/CI et journal sur GitHub.
2. Lancer le serveur Vite et vérifier l'application dans le navigateur.
3. Commencer la première véritable tranche frontend à partir de la maquette approuvée.
