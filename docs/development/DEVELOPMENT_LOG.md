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

Publication sur `origin/main` : commits `9923bec` et `1e471b6` publiés avec le commit de journal `d3592a1`.

### Prochaines actions
1. Vérifier l'exécution du workflow CI dans GitHub Actions.
2. Faire une revue visuelle de la coque React dans le navigateur.
3. Commencer la première véritable tranche frontend à partir de la maquette approuvée.

### Vérification du serveur de développement
- Serveur Vite démarré avec `npm run dev --workspace @iris/web -- --host 0.0.0.0`.
- Requête HTTP locale sur `http://localhost:5173/` : réponse `200 OK` et document HTML servi.
- Le serveur reste actif dans le processus local `30184` pendant la session.
- Le workflow GitHub Actions est ajouté au dépôt ; son exécution distante reste à confirmer dans l'onglet Actions de GitHub.

---

## Session 2026-11-17 — Design system et parcours d'accueil React

### Objectif
Remplacer la coque React temporaire par les premiers vrais ecrans IRIS, en reprenant l'identite visuelle de la maquette HTML/CSS/JS approuvee.

### Realisations
- Reprise des couleurs de la maquette : paper `#F7F5F0`, ink `#202321`, violet `#7357D9`, soft violet `#EEE9FF`, coral `#F27E70`, lime `#C7E56B`.
- Mise en place des typographies DM Sans et Manrope, des boutons, champs, labels, focus visibles et tokens CSS.
- Creation d'un Splash Screen IRIS avec identite, proposition de valeur et acces aux parcours Sign in / Sign up.
- Creation de l'ecran Sign in : email, mot de passe, affichage/masquage du mot de passe, option remember me, lien de recuperation et bouton Google (placeholder explicite, non connecte).
- Creation de l'ecran Sign up : nom, email, mot de passe avec longueur minimale, consentement aux conditions.
- Creation de l'ecran Password Recovery avec etat de confirmation local.
- Ajout d'une mise en page responsive desktop/mobile, d'etats focus clavier et du respect de prefers-reduced-motion.
- Conservation d'une communication honnete : les formulaires sont interactifs cote frontend, mais aucun compte n'est cree et aucune authentification reelle n'est encore branchee.

### Fichiers modifies
- `apps/web/src/App.tsx` — composants Splash, VisualPanel, AuthLayout, Recovery et navigation locale.
- `apps/web/src/index.css` — design tokens, composants et responsive styles.
- `apps/web/src/App.test.tsx` — quatre tests du parcours d'accueil et de recuperation.

### Validations executees
| Commande | Resultat |
| --- | --- |
| `npm test` | Reussi — 4 tests passes |
| `npm run lint` | Reussi — 0 warning, 0 erreur |
| `npm run typecheck` | Reussi |
| `npm run build` | Reussi — bundle production genere |
| `git diff --check` | Reussi |

### Commits
A enregistrer apres validation du diff et publication.

### Suite
1. Faire une revue visuelle dans le navigateur et ajuster les details si necessaire.
2. Construire le shell de l'application connectee : sidebar, topbar, navigation et page Explore.
3. Integrer ensuite Camera Studio et le flux de capture, puis la couche Computer Vision.

---

## Session 2026-11-17 — Dashboard Explore et navigation vers Camera Studio

### Objectif
Construire le premier espace principal IRIS apres l'onboarding : navigation, recherche et filtres de galerie, acces a Camera Studio.

### Realisations
- Ajout d'un acces "Explore IRIS first" depuis le Splash Screen pour parcourir le produit sans compte.
- Ajout d'un mode visiteur clairement identifie "PREVIEW MODE" ; aucune authentification reelle n'est simulee.
- Creation du shell dashboard avec sidebar sur desktop, navigation adaptee en barre inferieure sur mobile, topbar, fil d'Ariane et profil visiteur.
- Creation d'un hero Explore et d'une galerie de six cartes de filtres fictifs clairement presentees comme contenu de demonstration.
- Ajout de categories interactives : All effects, Funny, Beauty, Animals, Distortion et Fantasy.
- Ajout de la recherche dans la galerie ; categories et recherche se combinent.
- Ajout de points d'entree vers Camera Studio depuis le hero, les cartes et le menu.
- Creation d'un ecran Camera Studio placeholder qui annonce explicitement la prochaine etape Computer Vision.
- Ajout de sept tests couvrant onboarding, recuperation, preview visiteur, filtrage/recherche et navigation vers Camera Studio.

### Fichiers modifies
- `apps/web/src/App.tsx` — ecrans Explore et Camera Studio placeholder, navigation et donnees de demonstration.
- `apps/web/src/index.css` — styles dashboard, galerie, sidebar, responsive et mobile navigation.
- `apps/web/src/App.test.tsx` — suite portee a sept tests.

### Validations executees
| Commande | Resultat |
| --- | --- |
| `npm test` | Reussi — 7 tests passes |
| `npm run lint` | Reussi — 0 warning, 0 erreur |
| `npm run typecheck` | Reussi |
| `npm run build` | Reussi — bundle production genere |
| `git diff --check` | Reussi |
| Requete HTTP `http://localhost:5173/` | Reussi — HTTP 200, entree Vite servie |

Un premier test a echoue car son expression reguliere ne prenait pas en compte la ponctuation du titre accessible. Le test a ete corrige pour verifier le nom accessible exact ; la suite complete est ensuite passee.

### Commits
A enregistrer apres creation des commits atomiques et push.

### Limites explicites
- Les cartes de filtres sont des apercus de catalogue, pas encore des effets CV appliques a une image.
- La recherche et les categories fonctionnent localement dans le navigateur.
- Camera Studio n'ouvre pas encore la camera : l'acces media, le tracking facial et le rendu temps reel constituent la prochaine tranche.

### Prochaines actions
1. Committer le dashboard et ses tests, puis le journal dans un commit documentaire separe.
2. Pousser les changements sur `origin/main`.
3. Demarrer Camera Studio : demande de permission camera, flux video, selection camera et gestion des erreurs.
4. Integrer le suivi facial et les premiers effets apres validation du flux video.
