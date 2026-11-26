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

---

## Session 2026-11-17 — Camera Studio : acces camera, photo et video

### Objectif
Remplacer le placeholder Camera Studio par une premiere experience camera reelle, executee localement dans le navigateur, avec controle du flux et capture de medias.

### Realisations
- Creation du composant autonome `CameraStudio.tsx`.
- Demande de permission camera uniquement apres action explicite de l'utilisateur.
- Ouverture du flux via `navigator.mediaDevices.getUserMedia()`, avec contraintes video HD et mode selfie par defaut.
- Apercu video temps reel, miroir selfie et bascule vers la camera arriere.
- Gestion des cas d'erreur : API indisponible / contexte non securise, permission refusee, aucune camera trouvee, camera occupee et erreur generique.
- Capture photo via Canvas, export JPEG et telechargement local.
- Enregistrement video via MediaRecorder, assemblage Blob WebM et telechargement local.
- Affichage du dernier media capture avec possibilite de le telecharger a nouveau.
- Arret des pistes media a la sortie de Camera Studio et liberation de l'URL objet du dernier media.
- Ajout d'indicateurs d'etat, controles accessibles, etats des boutons, interface responsive desktop/mobile.
- Integration du nouveau composant dans la navigation React.
- Ajout de quatre tests dedies au consentement camera, au refus de permission, au changement de camera et au retour vers Explore.

### Fichiers modifies
- `apps/web/src/CameraStudio.tsx` — logique camera, capture et enregistrement.
- `apps/web/src/CameraStudio.test.tsx` — tests du composant Camera Studio.
- `apps/web/src/App.tsx` — integration dans le parcours de navigation.
- `apps/web/src/App.test.tsx` — mise a jour du test de navigation vers le vrai studio.
- `apps/web/src/index.css` — interface du studio et adaptations responsive.

### Validations executees
| Commande | Resultat |
| --- | --- |
| `npm test` | Reussi — 11 tests passes sur 2 fichiers |
| `npm run lint` | Reussi — 0 warning, 0 erreur |
| `npm run typecheck` | Reussi |
| `npm run build` | Reussi — bundle production genere |
| `git diff --check` | Reussi |

### Limites et points a verifier sur appareil
- Le test automatique simule l'API MediaDevices ; il ne remplace pas un essai avec une vraie webcam.
- L'acces camera necessite HTTPS en production, ou localhost en developpement.
- La capture photo est exportee en JPEG ; l'enregistrement video utilise WebM lorsque le navigateur le prend en charge.
- Les effets Computer Vision ne sont pas encore appliques au flux. La prochaine etape est l'integration de MediaPipe Face Landmarker et le dessin des landmarks.
- Les medias sont telecharges localement ; aucun upload ni partage distant n'est encore implemente.

### Commits
A enregistrer en commits atomiques apres cette validation.

### Prochaines actions
1. Committer le composant camera, son integration et la documentation separement.
2. Verifier le flux avec une webcam reelle sur localhost et sur un telephone via HTTPS.
3. Integrer MediaPipe Face Landmarker, afficher les landmarks et mesurer la stabilite du tracking.
4. Implementer ensuite les premiers effets de deformation faciale : bouche et tete.

---

## Session 2026-11-17 — Integration initiale de MediaPipe Face Landmarker

### Objectif
Introduire le suivi facial temps réel dans Camera Studio, visualiser les landmarks et exposer une première mesure d'ouverture de la bouche, sans encore appliquer de déformation au visage.

### Réalisations
- Ajout de la dépendance officielle `@mediapipe/tasks-vision` (version résolue `1.2.3`) au workspace web et mise à jour du lockfile.
- Création de `FaceLandmarkerOverlay.tsx`, composant isolé chargé d'initialiser MediaPipe Face Landmarker en mode VIDEO.
- Chargement des fichiers WASM depuis jsDelivr et du modèle Face Landmarker depuis Google Cloud Storage au moment où l'utilisateur active la caméra et le suivi.
- Tentative d'exécution GPU avec repli CPU si l'initialisation GPU échoue.
- Détection d'un visage à chaque nouvelle frame vidéo via `requestAnimationFrame`, avec limitation du traitement aux frames vidéo réellement nouvelles.
- Dessin des points faciaux sur un canvas superposé à la vidéo ; les points des lèvres sont mis en évidence.
- Activation des blendshapes et lecture du score `jawOpen` pour afficher une première indication d'ouverture de la bouche.
- Synchronisation du miroir de l'overlay avec l'aperçu selfie.
- Fermeture du FaceLandmarker et annulation de la boucle d'animation au démontage du composant.
- Intégration dans Camera Studio uniquement lorsque la caméra est prête.
- Ajout des styles de superposition et d'un indicateur d'état : chargement, recherche de visage, visage suivi ou erreur.
- Ajout d'un test vérifiant que l'overlay ne s'initialise pas lorsque le suivi est désactivé.

### Fichiers créés ou modifiés
- `apps/web/src/FaceLandmarkerOverlay.tsx` — initialisation MediaPipe, détection vidéo, dessin des landmarks et lecture de jawOpen.
- `apps/web/src/FaceLandmarkerOverlay.test.tsx` — test de rendu lorsque le suivi est désactivé.
- `apps/web/src/CameraStudio.tsx` — connexion de l'élément vidéo au composant de suivi.
- `apps/web/src/index.css` — canvas de landmarks et badge d'état.
- `apps/web/package.json` — dépendance MediaPipe.
- `package-lock.json` — verrouillage de la dépendance.

### Validations exécutées
| Commande | Résultat |
| --- | --- |
| `npm test` | Réussi — 3 fichiers de test, 12 tests passés |
| `npm run lint` | Réussi — 0 warning, 0 erreur |
| `npm run typecheck` | Réussi |
| `npm run build` | Réussi — bundle production généré |
| `git diff --check` | Réussi |

Le premier lint a signalé des avertissements liés à l'accès à une ref dans le nettoyage React. Le code de nettoyage a été simplifié ; le lint final est à zéro avertissement. Le premier build exécuté avant cette correction a échoué sur une variable devenue inutilisée ; le build final après correction a réussi.

### Limites à ce stade
- La détection réelle doit encore être essayée avec une webcam physique dans un navigateur compatible. Les tests automatisés ne valident pas le chargement réseau du modèle, l'accélération GPU/CPU ni la précision du tracking.
- Le modèle WASM et le fichier `.task` sont chargés depuis des CDN externes ; une stratégie d'hébergement local et de versionnement des assets pourra être étudiée avant la production.
- Les points faciaux sont visualisés, mais aucun maillage déformable ni filtre de déformation n'est encore appliqué.
- Le score jawOpen est une mesure de blendshape, pas encore un contrôleur calibré pour une animation ou un filtre.
- Le traitement sur chaque frame peut être coûteux sur des appareils modestes ; il faudra mesurer les FPS et adapter la fréquence de détection.

### Commits
À créer après revue du diff : dépendance MediaPipe, intégration Face Landmarker, puis journal de session dans des commits distincts. Publication distante à confirmer après push.

### Prochaines actions
1. Faire un essai webcam réel dans Chrome et confirmer que le modèle se charge et que les landmarks suivent correctement le visage.
2. Mesurer la fréquence d'images et ajuster le coût du tracking si nécessaire.
3. Ajouter l'analyse des points de bouche et de l'orientation de tête avec des seuils calibrables.
4. Concevoir le premier moteur de déformation de bouche sur une copie du flux, sans altérer la capture originale.
5. Étendre ensuite aux déformations de tête : Big Head, Small Head, élargissement, rétrécissement et squash/stretch.

---

## Session 2026-11-17 — Responsive hardening et branchement de l'authentification

### Objectifs
- Corriger les débordements et les dispositions fragiles sur mobile/tablette/desktop.
- Remplacer les faux retours de formulaire par une vraie intégration d'authentification.
- Documenter les paramètres externes nécessaires sans exposer de secret.

### Responsive
- Ajout d'une couche CSS de durcissement responsive pour Splash, Sign In, Sign Up, Recovery, Explore et Camera Studio.
- Prévention des débordements horizontaux au niveau de la page et des conteneurs.
- Réduction des colonnes, espacements et tailles typographiques selon les breakpoints.
- Navigation basse du Dashboard adaptée aux petits écrans avec prise en compte de la safe area.
- Grille d'effets conservée en deux colonnes sur mobile ; les composants ont des largeurs minimales contrôlées.
- Camera Studio passe en colonne unique sur tablette/mobile, avec cadre vidéo vertical sur téléphone.
- Formulaires et champs contraints à la largeur disponible ; ajustements spécifiques aux écrans de 320–390 px et aux faibles hauteurs desktop.

### Authentification
- Ajout de `@supabase/supabase-js` au workspace web.
- Création de `apps/web/src/lib/supabase.ts` : client initialisé uniquement lorsque les deux variables Vite sont présentes.
- Inscription réelle via `supabase.auth.signUp`, avec le nom transmis comme métadonnée `full_name`.
- Connexion réelle via `supabase.auth.signInWithPassword`.
- Récupération réelle via `supabase.auth.resetPasswordForEmail`.
- Gestion des états de chargement et affichage des erreurs renvoyées par Supabase.
- En l'absence de configuration, les formulaires expliquent explicitement quelles variables ajouter au lieu d'afficher une fausse confirmation.
- Ajout des modèles de variables dans `apps/web/.env.example` et `.env.example`.
- Documentation du paramétrage Supabase dans `docs/development/AUTHENTICATION_SETUP.md`.

### Tests
- Mise à jour du test de récupération pour vérifier le message de configuration quand Supabase n'est pas paramétré.
- Ajout d'un test du parcours d'inscription sans identifiants de backend.
- Résultats finaux :
  - `npm test` : 3 fichiers, 13 tests réussis.
  - `npm run lint` : 0 warning, 0 erreur.
  - `npm run typecheck` : réussi.
  - `npm run build` : réussi.
  - `git diff --check` : réussi.
- Le build signale encore un chunk JavaScript supérieur à 500 kB, principalement lié au moteur MediaPipe. Une séparation différée du bundle est à planifier.
- Les breakpoints CSS sont couverts par inspection et tests unitaires fonctionnels ; un contrôle visuel manuel sur plusieurs tailles d'écran reste nécessaire.

### Configuration utilisateur encore nécessaire
- Créer/choisir un projet Supabase.
- Copier `apps/web/.env.example` vers `apps/web/.env.local`.
- Renseigner `VITE_SUPABASE_URL` et la clé publique publishable/anon.
- Configurer les URL autorisées et l'envoi d'emails dans Supabase.
- Aucun compte réel ne peut être créé tant que ces paramètres ne sont pas fournis.
- Ne jamais utiliser la clé `service_role` dans le frontend.

### Fichiers principaux
- `apps/web/src/index.css`
- `apps/web/src/App.tsx`
- `apps/web/src/App.test.tsx`
- `apps/web/src/lib/supabase.ts`
- `apps/web/package.json`
- `package-lock.json`
- `apps/web/.env.example`
- `.env.example`
- `docs/development/AUTHENTICATION_SETUP.md`

### Commits
À créer après revue : intégration Supabase, correctifs responsive, puis documentation/journal. Push à confirmer séparément.

### Prochaines actions
1. Récupérer les deux paramètres publics du projet Supabase et les placer dans `apps/web/.env.local` (fichier non versionné).
2. Tester une inscription et une connexion avec une vraie adresse email.
3. Ajouter la restauration de session et les routes protégées avant de considérer l'authentification complète.
4. Vérifier visuellement les écrans sur un téléphone réel et sur plusieurs largeurs d'écran.
5. Charger MediaPipe à la demande pour réduire le bundle initial.

---

## Session 2026-11-17 — Création et connexion du projet Supabase IRIS

### Infrastructure créée
- Projet Supabase `iris` créé dans l'organisation Richnel organisation.
- Référence projet : `dvsdqwtklqvxahmkgwln`.
- Région : `eu-west-1` (Ireland).
- Statut vérifié après création : `ACTIVE_HEALTHY`.
- URL API et clé publique publishable récupérées via les outils Supabase.
- Fichier local `apps/web/.env.local` créé avec les variables Vite requises. Le fichier est couvert par `.gitignore` et n'est pas versionné.
- Le serveur Vite a été redémarré pour charger les variables d'environnement.

### Authentification vérifiée côté projet
Lecture de `/auth/v1/settings` :
- Email activé.
- Inscriptions activées (`disable_signup=false`).
- Confirmation email requise (`mailer_autoconfirm=false`).
- Google OAuth désactivé.
- Aucun tableau public créé pour le moment ; la première étape repose sur Supabase Auth et les métadonnées utilisateur.

### Intégration frontend
- Inscription via email/mot de passe avec le nom enregistré dans `user_metadata.full_name`.
- URL de redirection après confirmation configurée côté client vers l'origine courante.
- Connexion email/mot de passe.
- Récupération de mot de passe par email.
- Restauration de session à l'ouverture de l'application et écoute des changements d'état Auth.
- Retrait du bouton Google trompeur tant que le fournisseur OAuth n'est pas configuré.
- Tests UI isolés du vrai projet Supabase pour éviter les appels réseau et la création accidentelle de comptes pendant les tests.

### Configuration Dashboard encore nécessaire
Le connecteur Supabase disponible permet de créer le projet, récupérer URL/clé, inspecter Auth et gérer la base, mais ne fournit pas d'action pour modifier la configuration Auth URL/SMTP. Il reste donc à vérifier dans Supabase Dashboard :
- Site URL local : `http://localhost:5173`.
- Redirect allow-list : `http://localhost:5173/**`.
- Ajouter l'origine HTTPS de production au moment du déploiement.
- Configurer un SMTP personnalisé pour la délivrabilité des emails de confirmation et de récupération.

Le fournisseur Google est désactivé et aucun client OAuth n'a été configuré ; l'option est masquée dans l'interface.

### Validations
- Endpoint public Auth settings : accessible et cohérent avec les réglages décrits ci-dessus.
- `npm test` : 13 tests réussis (3 fichiers).
- `npm run lint` : 0 warning, 0 erreur.
- `npm run typecheck` : réussi.
- `npm run build` : réussi.
- `git diff --check` : réussi.
- Avertissement de bundle supérieur à 500 kB toujours présent (MediaPipe) ; le découpage dynamique sera traité dans une étape dédiée.

### Fichiers
- `apps/web/.env.local` — variables locales, ignorées par Git.
- `apps/web/src/lib/supabase.ts` — client Supabase.
- `apps/web/src/App.tsx` — flux Auth, redirection et restauration de session.
- `apps/web/src/App.test.tsx` — mock Supabase pour tests indépendants.
- `docs/development/SUPABASE_SETUP.md` — référence de configuration.
- `docs/development/DEVELOPMENT_LOG.md` — journal de session.

### Prochaines étapes
1. Renseigner les URL autorisées dans Authentication → URL Configuration.
2. Configurer SMTP pour envoyer les emails aux utilisateurs externes.
3. Effectuer un test d'inscription réel avec une adresse email contrôlée, puis confirmer le compte et se connecter.
4. Ajouter le profil utilisateur en base et les politiques RLS avant les fonctionnalités sociales.


---

## Session 2026-11-22 — Pivot vers IRIS Desktop

### Décision produit
Le produit actif devient une application native de bureau destinée aux démonstrations locales. L'application web, l'authentification, les profils, les fonctions sociales, le backend et les dépendances cloud ne font plus partie du périmètre actif. L'ancien code web est conservé dans `legacy/web/` afin de préserver le travail et l'historique Git.

### Réalisations
- Création de `desktop/` comme nouveau projet Python indépendant.
- Définition de Python 3.12+ et des dépendances : MediaPipe, NumPy, OpenCV contrib et PySide6 Essentials.
- Création d'une fenêtre PySide6 avec une interface camera-first, un panneau de filtres, un aperçu caméra, des contrôles et un indicateur FPS.
- Création d'un thread caméra OpenCV distinct du thread UI.
- Ajout de six effets locaux : Original, Warm glow, Cool tone, Noir, Vivid et Soft focus.
- Ajout de la capture photo vers `~/Pictures/IRIS`.
- Ajout de tests unitaires pour les effets d'image et les entrées invalides.
- Mise à jour du README racine et ajout du plan produit/technique desktop.
- Remplacement du workflow GitHub Actions npm par un workflow Python/uv.
- Retrait des manifestes npm actifs de la racine et déplacement du code web suivi par Git dans `legacy/web/`. Les ressources locales ignorées ne sont pas versionnées.

### Fichiers principaux créés
- `desktop/pyproject.toml`
- `desktop/uv.lock`
- `desktop/README.md`
- `desktop/iris/__init__.py`
- `desktop/iris/__main__.py`
- `desktop/iris/camera.py`
- `desktop/iris/effects.py`
- `desktop/iris/main_window.py`
- `desktop/tests/test_effects.py`
- `docs/requirements/IRIS_DESKTOP_PLAN.md`

### Validations et blocages
- Dépôt initial vérifié propre sur `main`, synchronisé avec `origin/main` avant le début des changements.
- `git ls-remote` a confirmé l'accès au dépôt GitHub.
- Première résolution de dépendances refusée car la plage Python déclarée incluait Python 3.10/3.11, incompatibles avec les versions NumPy retenues. La version minimale a été relevée à Python 3.12.
- La seconde synchronisation `uv sync --extra dev` a résolu 34 paquets et commencé le téléchargement des wheels MediaPipe, OpenCV contrib et PySide6 Essentials. Au moment de la rédaction, le processus d'installation est encore en cours ; aucune réussite d'installation n'est déclarée.
- Les tests, le lancement GUI, l'accès à une webcam physique, le build PyInstaller et la CI distante restent à exécuter.

### État Git
- Aucun commit n'a encore été créé pour cette migration.
- Aucun push n'a été effectué.
- Les changements doivent être inspectés, validés, puis découpés en commits atomiques avant publication.

### Prochaines actions
1. Terminer `uv sync --extra dev` et corriger les éventuelles incompatibilités de dépendances.
2. Exécuter `uv run pytest` et les contrôles de compilation Python.
3. Lancer IRIS sur le bureau Linux et vérifier la caméra physique.
4. Améliorer les états caméra et la gestion du cycle de vie si nécessaire.
5. Valider la compilation Windows sur l'environnement Windows cible avec PyInstaller.
6. Créer les commits validés, puis pousser sur `origin/main`.
7. Implémenter le Face Landmarker Python, les accessoires AR et les déformations faciales.


### Vérifications complémentaires — caméra et syntaxe
- `python3 -m compileall -q desktop/iris desktop/tests` : réussi.
- `git diff --check` : réussi.
- Tests unitaires exécutés avec l'environnement Python système déjà présent : `9 passed in 0.33s`.
- Test caméra OpenCV direct : `/dev/video0` ouvert et une frame lue (640×480).
- Le premier lancement de l'interface a montré que le backend OpenCV automatique sélectionnait GStreamer et échouait sur ce poste. Le backend a été rendu explicite selon l'OS (V4L2 Linux, DirectShow Windows, AVFoundation macOS).
- Test de la classe `CameraThread` après correction : état `CAMÉRA ACTIVE`, 29 frames reçues en 2,2 secondes, arrêt propre.
- L'interface a été relancée sur le bureau après le test du thread caméra. La vérification visuelle du rendu et la capture photo par clic restent à effectuer manuellement.


### Historique Git mis à jour après validation
Les changements ont ensuite été découpés en commits et publiés sur `origin/main` :
| Commit | Message | État |
| --- | --- | --- |
| `71bb495` | `feat(desktop): add native camera studio and local filters` | Publié |
| `b550678` | `docs(product): define IRIS desktop direction and CI` | Publié |
| `63caeff` | `docs(development): record IRIS desktop migration` | Publié |
| `c0afd52` | `chore(desktop): ignore Python package metadata` | Publié |
| `a18859b` | `build(desktop): add standalone packaging scripts` | Commit local, push à confirmer |


### Installation légère, tests et compilation Linux
- La synchronisation complète des dépendances isolées a été interrompue après plusieurs minutes de téléchargement très lent des gros wheels Qt/OpenCV/MediaPipe. Le lockfile complet reste disponible pour une installation reproductible sur une connexion plus rapide.
- L'environnement local a été recréé avec le Python système 3.14.4 et l'option system-site-packages, car cet environnement possède déjà NumPy, OpenCV et PySide6 installés. PyInstaller 6.22.3 et pytest 9.2.0 ont été ajoutés dans le venv.
- `uv run --no-sync pytest -q` : réussi — 9 tests passés.
- Compilation PyInstaller Linux : réussie — dossier `desktop/dist/IRIS/` généré.
- Exécutable Linux : `desktop/dist/IRIS/IRIS` (environ 4,6 Mo pour le binaire principal, les bibliothèques sont regroupées dans le dossier).
- Smoke test de l'exécutable compilé : processus lancé sans erreur, fenêtre maintenue ouverte et caméra `/dev/video0` occupée par le processus IRIS, ce qui confirme l'ouverture de la caméra par le bundle.
- Le binaire Linux a été relancé sur le bureau et reste ouvert pour la démonstration.
- Cette compilation est un bundle Linux. Le fichier Windows `.exe` devra être produit en lançant `desktop/build.ps1` sur Windows ; PyInstaller ne fait pas de compilation croisée entre systèmes.


### Confirmation complémentaire de l'exécutable compilé
- Le binaire compilé a été relancé directement depuis `desktop/dist/IRIS/IRIS`.
- Une trace système sur le bundle a confirmé 55 buffers vidéo V4L2 livrés avec succès au processus IRIS pendant le smoke test.
- Un lancement interactif ultérieur a confirmé que le processus IRIS détenait bien `/dev/video0`.
- Le bundle Linux est généré et exécutable sur le poste Ubuntu utilisé pour cette session. Il n'est pas un exécutable Windows.
- Commits additionnels : `b248990` (correction des scripts de lancement/build pour ne pas relancer une synchronisation complète) et `d270274` (documentation du build Linux). Les deux sont publiés sur `origin/main`.
- La branche `main` est synchronisée avec `origin/main` après le push du commit `d270274`.

---

## Session 2026-11-26 — Documentation des stacks et création du backlog

### Objectif
Clarifier la présentation GitHub de l'application desktop, séparer les stacks et mettre en place un suivi durable des tâches et des actions.

### Inspection
- Reconnexion à Desktop Commander et accès au dépôt /run/media/richnel/Richnel_disque/Projet/iris.
- Branche active : main, suivie de origin/main.
- Dépôt distant : https://github.com/EgueRichnel2025/iris.git.
- L'état initial de cette session contenait uniquement les deux README modifiés lors du travail précédent.
- Aucun fichier Backlog dédié n'existait. Le journal de développement existant a été conservé.

### Réalisations
- Réécriture du README racine : produit, fonctionnalités actuelles/prévues, stacks, architecture, installation, tests, packaging, structure et roadmap.
- Organisation des technologies par responsabilités : desktop, vision/caméra, traitement d'image, packaging, qualité/développement et prototype web historique.
- Distinction explicite de MediaPipe : dépendance déclarée, intégration au pipeline desktop encore à réaliser.
- Réécriture de desktop/README.md pour documenter la stack desktop et ses commandes.
- Création de BACKLOG.md à la racine, car aucun fichier de backlog n'était présent. Le fichier contient les tâches priorisées et l'historique des actions.

### Fichiers créés ou modifiés
- README.md — réorganisation complète.
- desktop/README.md — guide desktop clarifié.
- BACKLOG.md — nouveau suivi des tâches et de l'historique.
- docs/development/DEVELOPMENT_LOG.md — ajout de cette entrée de session.

### Validations exécutées
| Commande | Résultat |
| --- | --- |
| git diff --check | Réussie. |
| cd desktop && .venv/bin/python -m pytest -q | Réussie — 9 tests passés en 0,45 s. |

La commande uv run --directory desktop pytest -q a été tentée, mais uv a commencé à télécharger plusieurs wheels volumineux pendant sa synchronisation. La suite a donc été exécutée avec l'interpréteur de l'environnement desktop existant ; le résultat final est vert.

### Commits et publication
Deux commits atomiques ont été créés et poussés avec succès vers origin/main :

| Commit | Message | Publication |
| --- | --- | --- |
| `9030c88` | `docs(readme): reorganize desktop stack documentation` | Push confirmé sur origin/main. |
| `15edd15` | `docs(development): add project backlog and session log` | Push confirmé sur origin/main. |

Le push a confirmé la mise à jour de `d289df8` vers `15edd15` sur `main`. Une dernière mise à jour du backlog consignera la vérification finale.

### Suite
- Publier les changements documentaires sur origin/main.
- Poursuivre l'intégration de MediaPipe Face Landmarker au pipeline desktop.
- Tenir BACKLOG.md et ce journal à jour à chaque session.

---

## Session 2026-11-26 — Première brique de stabilisation des landmarks

### Objectif
Commencer le chantier P0 du suivi facial par une brique mathématique indépendante de MediaPipe et de l'interface : le lissage temporel des coordonnées de landmarks.

### Diagnostic
- Branche `main` synchronisée avec `origin/main` au début de la session.
- Environnement desktop actif : Python 3.14.4, NumPy et OpenCV présents.
- MediaPipe 1.2.3 est déclaré dans `pyproject.toml` et verrouillé dans `uv.lock`, avec une roue Linux x86_64 disponible, mais il n'est pas installé dans l'environnement actuellement utilisé.
- Aucun modèle Face Landmarker `.task` n'est encore présent dans le dépôt.
- Une tentative de `uv sync --extra dev` a commencé à télécharger plusieurs grosses dépendances (NumPy, OpenCV, MediaPipe, PySide6, etc.) ; elle a été interrompue avant la fin pour ne pas bloquer la session. Aucun résultat d'installation n'a été revendiqué.

### Réalisations
- Création du package `desktop/iris/vision/`.
- Ajout de `LandmarkSmoother` dans `desktop/iris/vision/smoothing.py`.
- Lissage par moyenne mobile exponentielle : alpha proche de 1 = plus réactif ; alpha proche de 0 = plus lissé mais plus de latence.
- Validation des valeurs alpha et des tableaux de coordonnées 2D/3D.
- Réinitialisation automatique lorsque la forme des landmarks change et méthode `reset()` en cas de perte du visage.
- Ajout de tests unitaires dédiés couvrant les limites alpha, le calcul EMA, reset, changement de forme, entrées invalides et coordonnées non finies.

### Fichiers créés
- `desktop/iris/vision/__init__.py`
- `desktop/iris/vision/smoothing.py`
- `desktop/tests/test_smoothing.py`

### Validations
| Commande | Résultat |
| --- | --- |
| `.venv/bin/python -m pytest -q` depuis `desktop/` | **21 tests réussis** en 0,37 s. |
| `.venv/bin/python -m compileall -q iris tests` | Réussie. |
| `git diff --check` | Réussie. |

### État d'intégration
Le lisseur est une brique testée mais il n'est pas encore branché au pipeline caméra. L'intégration Face Landmarker attend l'installation complète de MediaPipe et l'ajout du modèle `.task`. Le flux caméra et l'interface existants n'ont pas été modifiés dans cette étape.

### Commit et publication
Commits créés : `b19bdba` — `feat(vision): add temporal landmark smoothing` et `6922ab2` — `docs(development): record landmark smoothing milestone`. Push réussi vers `origin/main` : `ef1adb0..6922ab2 main -> main`. Vérification finale : `main` et `origin/main` pointent sur `6922ab2`, arbre de travail propre.


## Session 2026-11-26 — Adaptateur MediaPipe Face Landmarker

### Objectif
Créer une première frontière logicielle propre entre le pipeline IRIS et MediaPipe, sans coupler la détection à la fenêtre principale ni à la caméra.

### Réalisations
- Vérification de la documentation officielle Face Landmarker et confirmation de l'usage du mode VIDEO pour les frames webcam successives.
- Création de desktop/iris/vision/face_landmarker.py : chargement explicite du modèle local, création de la tâche VIDEO, validation des images BGR uint8, conversion RGB contiguë, contrôle des timestamps strictement croissants, extraction des coordonnées normalisées (x, y, z) et fermeture idempotente.
- Import de MediaPipe différé jusqu'à l'ouverture du détecteur : le reste du package vision et les tests restent utilisables si la dépendance n'est pas encore installée.
- Création de desktop/tests/test_face_landmarker.py avec un faux runtime MediaPipe afin de couvrir le contrat de l'adaptateur sans exiger le modèle ni charger le runtime natif pendant les tests unitaires.

### Fichiers créés
- desktop/iris/vision/face_landmarker.py
- desktop/tests/test_face_landmarker.py

### Validations
| Commande | Résultat |
| --- | --- |
| desktop/.venv/bin/python -m pytest -q | 33 tests réussis. |
| desktop/.venv/bin/python -m compileall -q iris tests | Réussie. |
| git diff --check | Réussie. |

### Commit
- 93d656b — feat(vision): add MediaPipe face landmarker adapter.

### En cours / limites
- Le modèle face_landmarker.task est en cours de téléchargement dans desktop/assets/models/.
- L'installation de MediaPipe 1.2.3 est prévue juste après ce téléchargement ; elle n'est pas encore confirmée.
- L'adaptateur n'est pas encore relié à CameraThread ; cette intégration attend le test du runtime et du modèle réels.


## Session 2026-11-26 — Conversion des coordonnées faciales

### Objectif
Préparer une représentation en pixels utilisable par le rendu d'accessoires et le futur moteur de déformation, sans mélanger les coordonnées normalisées du modèle avec les dimensions de l'image.

### Réalisations
- Création de desktop/iris/vision/coordinates.py avec normalized_to_pixels pour les tableaux de coordonnées 2D et 3D.
- Mise à l'échelle de X et Z par la largeur de l'image, et de Y par sa hauteur, conformément à la convention des coordonnées normalisées MediaPipe.
- Validation des dimensions positives, de la forme des tableaux et des valeurs finies ; l'entrée n'est pas modifiée.

### Fichiers créés
- desktop/iris/vision/coordinates.py
- desktop/tests/test_coordinates.py

### Validations
- desktop/.venv/bin/python -m pytest -q : 44 tests réussis.
- compileall et git diff --check : réussis.

### Commit
- 487315e — feat(vision): convert normalized landmarks to pixels.


## Session 2026-11-26 — Ajout de l'asset Face Landmarker

### Réalisations
- Téléchargement du modèle officiel Google MediaPipe Face Landmarker dans desktop/assets/models/face_landmarker.task.
- Vérification du fichier (3,58 Mio) et de son empreinte SHA-256 : 64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff.
- Ajout de desktop/assets/models/README.md pour conserver la provenance, l'URL source, la date de récupération et l'empreinte.

### Commit
- 7ddf5c9 — assets(vision): add MediaPipe face landmarker model.

### En cours
- Installation de MediaPipe 1.2.3 dans le venv desktop via uv pip ; l'installation télécharge les wheels lourds et reste en cours.
- Le modèle est présent localement mais le chargement réel via MediaPipe et le test caméra restent à valider.


## Session 2026-11-26 — Résolution du chemin du modèle

### Réalisations
- Création de desktop/iris/vision/model_assets.py pour localiser face_landmarker.task depuis le projet source et depuis le répertoire d'extraction PyInstaller.
- Ajout de tests couvrant les deux contextes de lancement.

### Fichiers créés
- desktop/iris/vision/model_assets.py
- desktop/tests/test_model_assets.py

### Validations
- desktop/.venv/bin/python -m pytest -q : 46 tests réussis.
- compileall et git diff --check : réussis.

### Commit
- ff02bf3 — feat(vision): resolve local face model asset path.


## Session 2026-11-26 — Pipeline vision indépendant

### Objectif
Assembler la détection et le lissage temporel dans une couche vision dédiée, distincte de MainWindow et de CameraThread.

### Réalisations
- Création de desktop/iris/vision/pipeline.py avec FaceVisionPipeline et VisionFrameResult.
- Un lisseur EMA indépendant est utilisé par visage.
- Quand aucun visage n'est détecté, l'historique de lissage est réinitialisé afin que la réacquisition reparte sur les nouvelles coordonnées sans traîner l'ancienne position.
- Le pipeline gère son cycle de vie sans dépendre directement du runtime MediaPipe ; un détecteur injectable permet des tests rapides et déterministes.

### Fichiers créés
- desktop/iris/vision/pipeline.py
- desktop/tests/test_vision_pipeline.py

### Validations
- desktop/.venv/bin/python -m pytest -q : 51 tests réussis.
- compileall et git diff --check : réussis.

### Commit
- 3bf99b9 — feat(vision): compose face detection and landmark smoothing.
