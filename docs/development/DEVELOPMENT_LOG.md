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


## Session 2026-11-26 — Modèle local par défaut

### Réalisations
- FaceLandmarker accepte désormais l'absence de model_path et utilise le chemin déterminé par face_landmarker_model_path().
- Ajout d'un test garantissant que l'adaptateur pointe vers le modèle local par défaut.

### Validation
- desktop/.venv/bin/python -m pytest -q : 52 tests réussis.
- compileall et git diff --check : réussis.

### Commit
- 968062a — feat(vision): use bundled face model by default.


## Session 2026-11-26 — Préparation du packaging MediaPipe

### Réalisations
- Mise à jour de desktop/IRIS.spec pour collecter les ressources, binaires et imports dynamiques de cv2 et mediapipe.
- Ajout du modèle local face_landmarker.task dans les données du bundle.
- Les scripts build.sh et build.ps1 utilisent désormais le spec commun au lieu de dupliquer les options PyInstaller.

### Validations
- bash -n desktop/build.sh : réussi.
- Compilation syntaxique de desktop/IRIS.spec : réussie.
- Suite desktop : 52 tests réussis.
- Le build PyInstaller réel n'a pas été exécuté, car l'installation MediaPipe est encore en cours.

### Commit
- 4f9b8d6 — build(desktop): bundle face model and MediaPipe runtime.


## Session 2026-11-26 — Intégration du suivi facial temps réel

### Objectif
Installer et valider le runtime MediaPipe réel, puis connecter le Face Landmarker au flux webcam sans transférer la détection dans MainWindow.

### Installation et validation du modèle
- Installation de MediaPipe 1.2.3 dans desktop/.venv. L'import de mediapipe.tasks.vision est fonctionnel.
- Chargement réel de desktop/assets/models/face_landmarker.task réussi.
- Inférence sur une image synthétique noire : exécution réussie et zéro visage détecté, résultat attendu.
- Test direct webcam : cinq frames successives, chacune renvoyant un visage avec 478 landmarks. La webcam est libérée proprement après le test.

### Réalisations techniques
- Création de desktop/iris/vision/overlay.py : dessin des landmarks normalisés sur une copie BGR de la frame, en réutilisant la conversion coordonnées→pixels.
- Intégration de FaceVisionPipeline dans CameraThread. Le thread ouvre le détecteur au démarrage, utilise des timestamps monotones, lisse les coordonnées et applique l'overlay avant le rendu.
- Ajout des signaux face_count_updated et vision_error. Une panne de vision n'empêche pas la caméra de continuer à afficher le flux.
- MainWindow reste une couche d'affichage : elle reçoit le nombre de visages et affiche séparément le statut caméra et le statut de détection.
- Fermeture du pipeline et de la caméra dans le bloc finally du thread.

### Fichiers créés ou modifiés
- desktop/iris/vision/overlay.py
- desktop/tests/test_vision_overlay.py
- desktop/iris/camera.py
- desktop/iris/main_window.py
- desktop/tests/test_camera_vision.py
- desktop/IRIS.spec

### Validations exécutées
| Vérification | Résultat |
| --- | --- |
| Suite pytest desktop | 61 tests réussis. |
| compileall iris tests | Réussi. |
| git diff --check | Réussi. |
| Face Landmarker réel sur 5 frames webcam | 1 visage et 478 landmarks par frame. |
| CameraThread + boucle événementielle Qt pendant 3,5 s | 39 échantillons positifs ; aucun message d'erreur ; thread arrêté. |
| MainWindow réelle pendant 4,5 s | CAMÉRA ACTIVE ; 1 VISAGE DÉTECTÉ ; frame reçue ; environ 17 FPS au moment du contrôle. |

### Packaging
- PyInstaller 6.22.3 a produit le bundle Linux et l'exécutable est resté ouvert pendant un smoke test de 8 secondes (timeout volontaire, code 124).
- Le bundle actuel pèse environ 743 Mio. L'environnement utilise encore OpenCV système 4.10.0, dont les dépendances natives embarquent des bibliothèques système lourdes (notamment VTK, GDAL, FFmpeg et OpenBLAS). Ce n'est pas une taille cible acceptable.
- Le spec a été affiné pour collecter les ressources et binaires MediaPipe nécessaires, et limiter les imports cachés aux modules Face Landmarker. Le prochain build devra être refait dans un environnement utilisant le wheel opencv-contrib-python du lockfile.
- Une installation de opencv-contrib-python 5.1.0.95 a été tentée, mais son téléchargement de 84,9 Mio est resté trop lent et a été interrompu. Elle n'est donc pas déclarée installée.
- Le lanceur pyinstaller a aussi révélé un shebang lié à l'ancien chemin de montage du disque ; l'exécution par python -m PyInstaller fonctionne correctement dans le venv et a été utilisée pour le build.

### Commits de code
- 11dec19 — feat(vision): render facial landmarks on camera frames.
- 84d065f — feat(camera): integrate real-time face tracking.

### État final de la session
Le pipeline de détection faciale est fonctionnel en direct avec la webcam et le rendu de landmarks est visible dans l'aperçu. MainWindow ne fait que présenter les résultats. La suite logique est l'exploitation des landmarks pour les accessoires AR et la pose de tête, puis les déformations faciales. La réduction du bundle Linux reste une tâche de packaging distincte.


## Session 2026-11-26 — Estimation de la pose de tête

### Objectif
Exploiter les landmarks déjà suivis pour estimer l'orientation de la tête sur les trois axes, puis exposer les résultats à l'interface pour préparer les accessoires AR.

### Réalisations
- Création de desktop/iris/vision/head_pose.py avec HeadPoseEstimator et HeadPose.
- Utilisation de six points de référence stables (IDs MediaPipe 1, 152, 33, 263, 61 et 291 : nez, menton, coins externes des yeux et de la bouche).
- Estimation 3D par cv2.solvePnP en mode ITERATIVE, conversion du vecteur de rotation par cv2.Rodrigues, puis extraction des angles yaw, pitch et roll.
- Retour des vecteurs de rotation et de translation pour les futurs besoins de pose/placement 3D.
- Alignement du modèle 3D sur les axes caméra OpenCV (X droite, Y bas, Z vers l'avant). Le premier essai utilisait un repère visage différent et renvoyait une rotation de base proche de 180 degrés ; la correction donne une pose frontale cohérente.
- Ajout d'un paramètre explicite mirrored_input pour les appels dont les coordonnées proviennent d'une image horizontalement inversée.
- Intégration de l'estimateur dans CameraThread. La pose est calculée à partir des landmarks déjà lissés ; les angles sont transmis via head_pose_updated. Une erreur ponctuelle de solvePnP ne coupe plus la détection faciale.
- Si aucun visage n'est présent, les angles sont réinitialisés à zéro.
- MainWindow affiche séparément YAW, PITCH et ROLL, en conservant les responsabilités UI/vision distinctes.

### Fichiers créés ou modifiés
- desktop/iris/vision/head_pose.py
- desktop/tests/test_head_pose.py
- desktop/iris/camera.py
- desktop/iris/main_window.py
- desktop/tests/test_camera_vision.py
- README.md
- desktop/README.md
- BACKLOG.md

### Validations
| Vérification | Résultat |
| --- | --- |
| Tests dédiés pose + caméra | 22 tests passés après ajout du cas « visage perdu ». |
| Suite complète desktop | 81 tests réussis. |
| compileall iris tests | Réussi. |
| git diff --check | Réussi. |
| Tests synthétiques yaw/pitch/roll | Rotations positives, négatives et combinées récupérées à 0,2° près. |
| Tests de coordonnées miroir | 8 configurations validées. |
| Smoke test GUI réel 6 s | CAMÉRA ACTIVE ; 1 VISAGE DÉTECTÉ ; frame reçue ; environ 17 FPS ; pose affichée YAW -0°, PITCH +4°, ROLL -7°. |

### Limites et précision
La pose utilise un modèle facial générique à six points et une matrice caméra approximative : focale estimée par la largeur de l'image, centre optique au centre de l'image, distorsion nulle. Les angles donnent une orientation utile pour l'ancrage des accessoires, mais la translation et les distances 3D ne doivent pas encore être considérées comme métriquement calibrées. Une calibration réelle de la webcam pourra améliorer la précision.

### Commits de code
- b4c8607 — feat(vision): estimate head pose from facial landmarks.
- 3d948a4 — fix(vision): align head pose model with camera axes.
- 3644023 — feat(camera): publish live head pose estimates.
- b631430 — feat(ui): display live head orientation.

### Prochaine étape
Ajouter un premier accessoire 2D (lunettes) ancré sur les landmarks des yeux, puis stabiliser sa position, son échelle et sa rotation à partir de la pose de tête. Les déformations de bouche et de visage viendront après ce socle AR.


## Session 2026-11-26 — Premier accessoire AR : lunettes

### Objectif
Créer un premier accessoire 2D ancré aux landmarks des yeux, le rendre sélectionnable dans l’application et le traiter dans le thread caméra sans déplacer la logique vision dans l’interface.

### Réalisations
- Création de `desktop/iris/vision/glasses.py` avec `GlassesStyle` et `draw_glasses` : verres elliptiques teintés, contours, pont nasal et branches. Les centres, dimensions et rotations proviennent des landmarks des coins des yeux MediaPipe (33, 133, 263, 362).
- Le rendu accepte les landmarks 2D/3D et travaille sur une copie de la frame. Les landmarks proviennent du pipeline déjà lissé, ce qui stabilise l’ancrage image par image.
- Création de `desktop/iris/accessories.py` comme catalogue et routeur des accessoires.
- Ajout du sélecteur « AR ACCESSORIES » dans `MainWindow`. L’interface transmet uniquement le choix à `CameraThread`; le rendu reste dans la couche traitement caméra/vision.
- Intégration de `apply_accessory` dans `CameraThread`, avant le filtre couleur et l’affichage.
- Ajout de tests dédiés au rendu, au catalogue et au chemin d’intégration caméra.

### Fichiers créés ou modifiés
- `desktop/iris/vision/glasses.py`
- `desktop/iris/accessories.py`
- `desktop/iris/camera.py`
- `desktop/iris/main_window.py`
- `desktop/tests/test_glasses.py`
- `desktop/tests/test_accessories.py`
- `desktop/tests/test_camera_vision.py`

### Validations
| Vérification | Résultat |
| --- | --- |
| Suite pytest desktop | 97 tests réussis. |
| `compileall iris tests` | Réussi. |
| `git diff --check` | Réussi. |
| Smoke test `CameraThread` avec lunettes sélectionnées | 25 frames reçues ; aucune erreur caméra/vision ; arrêt propre. |
| Détection de visage pendant ce smoke test | Aucun visage confirmé dans le dernier échantillon ; le placement visuel sur visage réel reste à vérifier avec un visage présent dans le champ. |

### Commits de code
- `65de655` — `feat(ar): render face-anchored glasses`.
- `c175b9d` — `feat(camera): integrate selectable AR accessories`.
- `1000738` — `test(camera): cover AR accessory frame integration`.

### État et suite
Le premier accessoire est intégré et sélectionnable. Sa géométrie suit les landmarks des yeux lissés. Il reste à effectuer un contrôle visuel en mouvement avec un visage dans le champ, puis à améliorer le rendu (monture plus réaliste, occlusion/ajustement en yaw) et ajouter chapeaux et oreilles.


## Session 2026-11-26 — Amélioration géométrique des lunettes AR

### Objectif
Améliorer le rendu des lunettes pour qu'il épouse mieux les contours oculaires et s'adapte indépendamment à la perspective de chaque œil.

### Réalisations
- Préservation et revue d'une modification locale existante qui mesurait séparément la largeur de chaque œil et son ouverture palpébrale.
- Ajout de tests géométriques pour le raccourcissement d'un œil en perspective, l'orientation de la ligne oculaire, la variation de l'ouverture des paupières et le rejet de coordonnées invalides.
- Ajout de `LensGeometry.contour`, composé des coins de l'œil et de points des paupières supérieures/inférieures. Le contour est agrandi autour du centre dans le repère local de l'œil : largeur et hauteur sont ajustées indépendamment.
- Remplacement des ellipses génériques par des polygones de lentilles remplis en transparence (`fillPoly`) et des montures tracées (`polylines`). Le pont nasal et les branches restent ancrés aux bords internes/externes calculés.
- Chaque lentille reste calculée à partir de son propre œil ; le raccourcissement perspectif d'un côté ne force donc pas l'autre côté à garder la même taille.

### Fichiers modifiés
- `desktop/iris/vision/glasses.py`
- `desktop/tests/test_glasses.py`

### Validations
| Vérification | Résultat |
| --- | --- |
| Tests ciblés lunettes | 14 tests réussis. |
| Suite complète desktop | 101 tests réussis. |
| `compileall iris tests` | Réussi. |
| `git diff --check` | Réussi. |
| Test caméra réel avec visage présent | Non effectué pendant cette étape ; aucune validation visuelle réelle n'est revendiquée. |

### Commits
- `392565b` — `test(ar): cover perspective-aware glasses geometry`.
- `a303495` — `feat(ar): render glasses from expanded eye contours`.

### Suite
Effectuer un contrôle visuel webcam avec un visage présent, mesurer les résultats sur plusieurs angles de tête, puis travailler l'occlusion et les branches des lunettes.


## Session 2026-11-26 — Préparation du moteur d'accessoires 3D

### Objectif
Remplacer à terme le dessin OpenCV des lunettes par un vrai asset 3D, aligné sur la transformation faciale MediaPipe.

### Asset 3D sélectionné
- Modèle : `desktop/assets/models/accessories/rectangular-acetate-glasses.glb` (GLB 2.0, environ 223 Ko).
- Source : Innerscene 3D Parts Library, page `https://www.innerscene.com/tools/library/3d-parts/rectangular-acetate-glasses-a635b3cb`.
- Licence déclarée dans les métadonnées GLB et sur la page source : CC0 1.0 Universal.
- Le modèle comporte des sous-maillages séparés pour monture acétate, monture métal, plaquettes nasales, verres et branches.
- SHA-256 : `d31285108a295bbbe381cdaff60d0b9aa318c4d052f6a7fd6e06ad8ec102d16a`.
- Provenance, licence et statut d'intégration consignés dans `desktop/assets/models/accessories/README.md`.

### Évolution MediaPipe
- `FaceLandmarkerOptions` active `output_facial_transformation_matrixes=True`.
- `FaceLandmarkResult` expose `facial_transformation_matrices`, tuple de matrices 4×4 `float32` renvoyées par MediaPipe.
- Cette donnée complète les landmarks et doit servir à positionner l'objet 3D dans le repère facial.

### Fichiers créés/modifiés
- `desktop/assets/models/accessories/rectangular-acetate-glasses.glb` (nouveau modèle).
- `desktop/assets/models/accessories/README.md` (provenance/licence/hash).
- `desktop/iris/vision/face_landmarker.py` (sortie matrice faciale).
- `desktop/tests/test_face_landmarker.py` (test de la sortie matrice).

### Validation
- `pytest -q` : **102 tests réussis**.
- `compileall iris tests` : réussi.
- `git diff --check` : réussi.
- Inspection de l'en-tête GLB : version 2.0, chunks JSON/BIN cohérents, 5 meshes, 4 matériaux, sous-maillages nommés.
- Essai exploratoire `vtkGLTFImporter` : échec de chargement des données binaires (`Error loading binary data`), donc VTK n'est pas retenu comme renderer à ce stade.

### Commits
- `ed8cadf` — `feat(ar): add CC0 3D glasses model asset`.
- `87389b6` — `feat(vision): expose facial transformation matrices`.
- `24754d5` — `test(vision): cover facial transform matrix output`.

### Limitation et prochaine étape
Aucun rendu 3D n'est encore branché à `CameraThread`. Le GLB est acquis et la matrice faciale est disponible, mais il faut encore sélectionner et valider un moteur de rendu glTF/GLB compatible avec l'architecture PySide6 et le flux caméra. Il faudra ensuite calibrer le repère local du modèle (échelle, axes, pivot) et gérer l'occlusion du visage. Ne pas annoncer l'accessoire 3D comme fonctionnel avant validation visuelle sur webcam.


## Session 2026-11-26 — Première scène 3D GLB intégrée à Qt

### Objectif
Charger réellement l'asset GLB dans un widget 3D intégré à l'application PySide6, avant toute connexion au flux caméra.

### Choix du moteur
- Qt Quick 3D a été évalué, mais les bindings `PySide6-Addons==6.10.2` représentent environ 163 Mo de téléchargement et le transfert est resté bloqué sans progression exploitable. Le processus a été interrompu.
- VTK 9.5.2 est déjà disponible sur la machine et fournit `vtkGLTFReader` ainsi que `QVTKRenderWindowInteractor`, ce dernier compatible avec PySide6 (`QT_API=pyside6`).
- `vtkGLTFReader` a correctement chargé le fichier `rectangular-acetate-glasses.glb` et renvoyé un bloc de géométrie. VTK affiche un avertissement : l'extension glTF `KHR_materials_specular` n'est pas prise en charge et est ignorée.
- Le rendu VTK hors écran direct a provoqué un segfault ; le test retenu passe par `QVTKRenderWindowInteractor` dans une fenêtre Qt, où l'initialisation, le rendu et la capture PNG ont réussi.

### Implémentation
- Nouveau module `desktop/iris/vision/glasses_3d.py` : validation du conteneur GLB 2.0, lecture du chunk JSON, vérification de la présence de meshes, puis création d'une scène VTK intégrée à Qt.
- Nouveau type `Glasses3DScene` conserve le widget, le renderer, le lecteur GLTF et l'acteur pour assurer leur durée de vie.
- Nouvelle erreur `Glasses3DAssetError` pour les assets manquants, tronqués ou invalides.
- Dépendance VTK isolée dans l'extra facultatif `ar3d` : `vtk>=9.5.2,<9.6`. Le socle d'installation IRIS ne récupère donc pas automatiquement VTK. `uv.lock` actualisé.
- Six tests unitaires couvrent les en-têtes GLB, la taille déclarée, la version, le chunk JSON et les meshes.

### Validation
- Smoke test PySide6 + VTK : scène GLB créée et affichée dans `QVTKRenderWindowInteractor`, capture `/tmp/iris-glasses-scene-smoke.png` enregistrée.
- `pytest -q` : **108 tests réussis**.
- `compileall iris tests` : réussi.
- `git diff --check` : réussi.

### Fichiers créés/modifiés
- `desktop/iris/vision/glasses_3d.py`
- `desktop/tests/test_glasses_3d_asset.py`
- `desktop/pyproject.toml`
- `desktop/uv.lock`

### Commits
- `c1e7d48` — `test(ar): validate binary glTF accessory assets`.
- `7c0c6a1` — `feat(ar): add VTK glTF accessory scene loader`.
- `2c45f5d` — `build(ar): add optional VTK rendering dependencies`.

### Limites / suite
La scène statique charge et rend le GLB dans un widget Qt. Elle n'est pas encore connectée à `CameraThread`, ne suit pas la matrice faciale MediaPipe et ne gère pas encore l'occlusion. Prochaine étape : intégrer ce widget à l'interface sans remplacer prématurément l'aperçu caméra, définir/calibrer le repère du modèle, puis piloter l'acteur avec la transformation faciale et vérifier le résultat sur webcam.


## Session 2026-11-26 — Ancrage mathématique du GLB à la pose faciale

### Inspection et mesures
- Inspection de `CameraThread`, `FaceVisionPipeline`, `FaceLandmarker`, `MainWindow` et des tests existants.
- Test réel de `FaceLandmarker` sur la webcam : image 640×480, un visage détecté, une matrice 4×4 retournée. Exemple de translation observée : (-2,57, -8,41, -26,39), cohérente avec un espace facial/caméra en centimètres.
- Inspection de la géométrie chargée par `vtkGLTFReader` : largeur totale ≈ 0,1456 m, hauteur ≈ 0,046 m, profondeur des branches ≈ 0,1413 m. Le modèle GLB est exprimé en mètres.

### Implémentation
- `desktop/iris/vision/face_transform.py` : validation stricte de la matrice 4×4 (finitude, dernière ligne affine), validation du facteur d'unité, conversion `M_actor = M_face @ diag(100,100,100,1)` pour passer des mètres GLB aux centimètres MediaPipe.
- Fonction `apply_face_transform` : conversion vers `vtkMatrix4x4`, puis `SetUserMatrix` sur l'acteur. Le rendu est déclenché uniquement si la scène VTK a été initialisée. L'appel doit être effectué sur le thread GUI Qt, jamais dans le worker caméra.
- `VisionFrameResult` conserve désormais `facial_transformation_matrices` issues du détecteur. Les matrices sont vidées quand aucun visage n'est présent.
- `CameraThread` émet `face_transform_updated(object)` avec une copie de la matrice faciale ou `None`. Le thread caméra ne manipule aucun objet VTK.
- `Glasses3DScene` possède un état `initialized` ; l'initialisation du contexte VTK est reportée à `initialize_glasses_3d_scene` pour attendre l'affichage du widget Qt.

### Validation
- Webcam : matrice faciale réellement récupérée.
- Tests ciblés : 33 tests réussis avant ajout du test final d'application VTK.
- Suite complète finale : **126 tests réussis**.
- `compileall iris tests` : réussi.
- `git diff --check` : réussi.
- Tentative de test visuel combiné QVTK + webcam : échec X11 `BadWindow`. Le problème de cycle de vie a conduit à différer l'initialisation du widget après affichage, mais le smoke test graphique n'a pas été validé ensuite. Pas de preuve visuelle d'un alignement correct sur le visage.

### Fichiers modifiés/créés
- `desktop/iris/vision/face_transform.py` (nouveau)
- `desktop/iris/vision/pipeline.py`
- `desktop/iris/vision/glasses_3d.py`
- `desktop/iris/camera.py`
- `desktop/tests/test_face_transform.py` (nouveau)
- `desktop/tests/test_vision_pipeline.py`
- `desktop/tests/test_camera_vision.py`
- `desktop/tests/test_glasses_3d_asset.py`

### Commits
- `feat(ar): map facial pose to GLB model coordinates`
- `test(ar): cover facial matrix and GLB unit conversion`
- `feat(vision): preserve facial transformation matrices`
- `feat(camera): publish facial transforms to the UI thread`
- `fix(ar): initialize VTK after Qt widget is shown`

### Limites et suite
Le flux caméra de `MainWindow` reste rendu dans un QLabel. Le widget 3D n'est pas encore intégré en superposition au flux ; aucun rendu « lunettes portées » n'a été validé visuellement. Prochaine étape : mettre en place une surface de rendu compositée compatible avec le contexte graphique de la machine, connecter `face_transform_updated` au thread GUI, puis régler pivot/axes/échelle et occlusion sur la webcam.


## Session 2026-11-26 — Préparation du compositing webcam + scène 3D

### Implémentation conservée
- `CameraThread` publie maintenant `video_frame_ready(object)` contenant une copie RGB (`uint8`, H×W×3) après application des effets, en complément du signal QImage existant.
- `Glasses3DScene` possède un renderer VTK d'arrière-plan qui reçoit les images par `vtkImageImport` et `vtkImageActor`, ainsi qu'un renderer 3D au premier plan pour le modèle.
- `update_glasses_video_frame` valide la forme RGB, inverse verticalement les lignes pour respecter l'origine image VTK, met à jour l'importer, positionne le plan vidéo à 100 cm et configure une caméra perspective initiale. La focale utilisée est une approximation (1,25 × dimension image maximale), pas encore une calibration issue des paramètres intrinsèques réels de la webcam.
- Tests du signal RGB et du compositing (format, orientation, taille, caméra) ajoutés.

### Tentative d'intégration UI et blocage
- La tentative d'héberger `QVTKRenderWindowInteractor` dans le layout `MainWindow` provoque un crash X11 `BadWindow` (X_ChangeWindowAttributes).
- Le problème persiste lorsque l'initialisation VTK est différée après l'affichage et lorsque le widget reste visible en permanence.
- Tous les changements de `MainWindow` liés à cette intégration ont été annulés pour préserver la stabilité de l'application. Le flux vidéo QImage actuel et l'interface existante restent inchangés.
- Aucune capture de lunettes 3D superposées au visage n'a été obtenue ; ne pas présenter l'intégration comme achevée.

### Validation
- `pytest -q` : **128 tests réussis**.
- `compileall iris tests` : réussi.
- `git diff --check` : réussi.
- Test visuel MainWindow + QVTK : échoue sous X11 `BadWindow`, identifié comme bloqueur d'intégration.

### Fichiers
- `desktop/iris/camera.py`
- `desktop/iris/vision/glasses_3d.py`
- `desktop/tests/test_camera_vision.py`
- `desktop/tests/test_glasses_3d_asset.py`

### Commits
- `feat(camera): publish RGB frames for AR composition`
- `feat(ar): composite camera frames behind 3D accessories`

### Suite
Remplacer le widget natif QVTK/X11 par un widget Qt/OpenGL basé sur un contexte OpenGL géré par Qt (`QOpenGLWidget` + `vtkGenericOpenGLRenderWindow`) ou un autre mécanisme de rendu compatible. Ne réintégrer le modèle à `MainWindow` qu'après un smoke test graphique reproductible. Ensuite calibrer les intrinsèques webcam, le repère du modèle, le pivot et l'occlusion.

## Session 2026-11-26 — Diagnostic Qt/OpenGL après l'échec X11

### Vérifications
- État initial : `main` propre, `HEAD` et `origin/main` à `4d0f856`.
- PySide6 Essentials 6.10.2 installé dans le système ne contient pas les modules Python `QtOpenGLWidgets` et `QtOpenGL`, bien que les bibliothèques Qt natives soient installées.
- Téléchargement des paquets Ubuntu `python3-pyside6.qtopenglwidgets` et `python3-pyside6.qtopengl`, puis extraction locale dans `/tmp` et copie temporaire des modules dans `.venv`. Aucun fichier suivi par Git ni aucune dépendance projet n'a été modifié par cette manipulation.
- Smoke test indépendant : un `QOpenGLWidget` PySide6 obtient un contexte OpenGL valide et se ferme proprement.

### Résultats VTK
- `vtkmodules.qt.QVTKRWIBase = "QOpenGLWidget"` permet de construire le widget QVTK avec la classe de base OpenGL de Qt.
- Avec `vtkGenericOpenGLRenderWindow`, le test d'une scène VTK simple segfault au premier rendu (`Render()`).
- `vtkEGLRenderWindow` en mode offscreen segfault également pendant le rendu sur cette machine.
- Les bindings Python VTK disponibles n'exposent que `QVTKRenderWindowInteractor`, pas `QVTKOpenGLNativeWidget`. La documentation VTK identifie ce dernier comme le widget natif adapté à `vtkGenericOpenGLRenderWindow`.

### Décision
Ne pas intégrer ni reconnecter VTK à `MainWindow` sur la base d'un simple changement de classe Qt : le rendu n'est pas stable. Comparer maintenant un prototype Qt Quick 3D (PySide6 Addons) avec un prototype OpenGL dédié dans `QOpenGLWidget` utilisant un parseur glTF Python. Choisir seulement après un chargement GLB et une capture graphique stables.

### Limites
La caméra et la matrice MediaPipe restent disponibles, mais aucun rendu GLB superposé à la webcam n'est validé. Pas de commit fonctionnel ni de push pour cette session de diagnostic. Les paquets ajoutés manuellement à `.venv` sont des essais locaux non déclarés dans le projet.


### 2026-11-26 — Prototype Qt Quick 3D et compositing statique

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Relecture du backlog, du journal, du statut Git et des modules actifs. | `main` propre et synchronisée avec `origin/main`, HEAD `c2b5fc0`. Aucun code applicatif modifié au début de cette étape. |
| 2 | Vérification des bindings PySide6 Quick/QML/Quick3D. | Absents de l'installation Essentials seule. Téléchargement et extraction temporaires des paquets Ubuntu Qt 6.10.2 dans `/tmp/iris-qtquick3d` ; aucune installation système ni modification des dépendances du projet. |
| 3 | Résolution des dépendances runtime Qt Quick 3D. | Modules PySide6 QtQuick, QtQml, QtQuick3D et QtQuickWidgets importables dans le venv après copie locale temporaire. Le plugin `qt6-quick3d-assetimporters-plugin` et `libassimp6` sont nécessaires pour l'import glTF. |
| 4 | Prototype autonome `QQuickView` + `RuntimeLoader`. | `rectangular-acetate-glasses.glb` chargé avec statut `RuntimeLoader.Success`; capture `/tmp/iris-qtquick3d/glasses-preview.png` obtenue. La monture rectangulaire et ses branches sont visibles. |
| 5 | Prototype `QQuickWidget` avec image caméra en arrière-plan et scène 3D transparente au premier plan. | Capture composite 1280×720 réussie dans `/tmp/iris-qtquick3d/composite-preview.png`. Le modèle 3D est rendu par-dessus l'image. Il s'agit d'une image caméra fixe de test, pas encore du flux vidéo continu. |
| 6 | Test du Face Landmarker sur l'image de la webcam. | 0 visage détecté : la caméra était orientée vers le plafond. Aucune validation de l'ancrage ou de l'alignement sur visage réel n'est donc revendiquée. |
| 7 | Validation du dépôt. | Les prototypes sont entièrement sous `/tmp`; aucun fichier source applicatif, dépendance ou lockfile n'a été modifié. Le statut Git est resté propre avant cette mise à jour documentaire. |

### Décision et limites
Qt Quick 3D est retenu comme piste de rendu à poursuivre : `RuntimeLoader` accepte glTF 2.0 `.glb` et la scène peut être composée dans un `QQuickWidget`, sans passer par le backend VTK qui segfaultait. Référence API : https://doc.qt.io/qt-6.10/qml-qtquick3d-assetutils-runtimeloader.html.

Il reste à déclarer proprement `PySide6-Addons`/Qt Quick 3D dans l'extra de packaging, intégrer le widget à `MainWindow`, transmettre les frames RGB et convertir la matrice MediaPipe en position/rotation/échelle Qt Quick 3D. La caméra doit être orientée vers un visage pour valider le placement. Ne pas présenter le compositing statique comme un filtre AR temps réel terminé.


### 2026-11-26 — Intégration initiale du compositing Qt Quick 3D dans le desktop

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Ajout de `desktop/iris/qt_quick_glasses.py`. | Nouveau widget `GlassesQuickView`: fournisseur d'images RGB en mémoire, chargement du GLB, activation du modèle et conversion de la matrice MediaPipe vers position/rotation Qt. |
| 2 | Ajout de `desktop/iris/ui/qml/glasses_view.qml`. | Scène QML qui superpose un `View3D` transparent au flux caméra avec une caméra perspective et `RuntimeLoader`. La scène 3D suit la zone réellement peinte de l'image (aspect ratio préservé). |
| 3 | Mise à jour de `CameraThread`. | Le rendu GLB n'utilise plus l'ancien dessin 2D des lunettes. Les autres accessoires conservent leur pipeline actuel. Les frames RGB et matrices faciales sont transmises à l'interface. |
| 4 | Intégration dans `MainWindow`. | `QStackedWidget` bascule vers le rendu Quick 3D lorsque « Lunettes » est sélectionné et revient à l'aperçu classique pour « Aucun accessoire ». Les frames vidéo et matrices faciales sont reliées au widget. Repli vers la vue classique si Qt Quick 3D n'est pas disponible. |
| 5 | Dépendances. | Extra `ar3d` remplacé par `PySide6-Addons==6.10.2`, `PySide6-Essentials` épinglé à `6.10.2` pour garantir la cohérence des binaires Qt. `uv lock` exécuté. |
| 6 | Tests ciblés. | `24 passed` sur rendu, transformations faciales et caméra. |
| 7 | Tests complets. | `132 passed in 2.01s`. `compileall` et `git diff --check` réussis. |
| 8 | Smoke test graphique du widget. | `QQuickWidget` chargé avec `QML_STATUS Status.Ready`; capture `integrated-widget.png` montrant les lunettes GLB rectangulaires complètes sur un fond test, avec une matrice de pose synthétique (Z = -30 cm). |
| 9 | Smoke test de la fenêtre desktop. | `MainWindow` démarre, caméra ouverte, `GlassesQuickView` présent, pile de vues = 2, sélection « Lunettes » bascule bien vers le widget 3D. Capture `main-window.png` obtenue. |

### Limites restantes / validation réelle
Le smoke test de la fenêtre indique `AUCUN VISAGE` : la caméra était ouverte mais aucun visage n'était visible dans son champ (image sombre). La pose utilisée pour vérifier l'apparence du modèle dans le widget était synthétique, pas issue d'un visage réel. Le suivi facial temps réel n'est donc PAS encore validé visuellement. Il faut orienter la webcam vers un visage puis calibrer l'orientation, le pivot, la taille et la position des lunettes sur le visage. La capture de la fenêtre a aussi révélé que le flux caméra était très sombre dans cette session ; vérifier l'exposition et le cadrage au prochain essai.

### Dépendances de développement temporaires
Les modules Qt Quick 3D et plugins Asset Importers utilisés pour le smoke test ont été extraits dans `/tmp/iris-qtquick3d` et le venv a reçu des modules Python copiés manuellement lors du diagnostic précédent. Le dépôt déclare maintenant le bon extra `ar3d`, mais un environnement propre doit être validé via `uv sync --extra ar3d --extra dev` avant de considérer le packaging terminé. Aucun de ces chemins temporaires n'est requis par le code source.

## Session 2026-11-27 — Diagnostic et installation locale Qt Quick 3D

### Diagnostic
- Dépôt initial : branche `main`, HEAD `987aa6a`, synchronisée avec `origin/main`, arbre propre.
- Environnement : Python 3.14.4, MediaPipe 1.2.3, OpenCV 4.10.0, NumPy 2.3.5 ; les 132 tests existants passent.
- Les bindings QtQuick/QtQml étaient présents, mais `from PySide6.QtQuick3D import ...` échouait avec `libQt6Quick3D.so.6: cannot open shared object file`.
- Les paquets Qt Quick 3D Ubuntu 6.10.2 ont été téléchargés et extraits sous `/tmp` pour diagnostiquer les bibliothèques et plugins manquants. Aucun paquet système n'a été installé et aucun `sudo` n'a été utilisé.
- L'import Python Quick3D fonctionne en ajoutant les bibliothèques natives au `LD_LIBRARY_PATH` et le module Python QtQuick3D au venv.
- Le premier chargement GLB renvoyait `Unsupported: Unknown error` car le plugin d'import Assimp manquait. Après extraction de `qt6-quick3d-assetimporters-plugin`, le QML est `Status.Ready` et `RuntimeLoader` atteint `Success` avec `rectangular-acetate-glasses.glb`.

### Changements de code et d'installation
- Ajout de `desktop/scripts/install_qt_quick3d_runtime.sh` : télécharge et extrait les petits paquets Qt 6.10.2 dans `$XDG_DATA_HOME/iris/qt6-runtime` ou `~/.local/share/iris/qt6-runtime`, sans droits administrateur, puis installe le binding Python dans le venv.
- Ajout de `desktop/run.sh` : prépare `LD_LIBRARY_PATH`, `QML2_IMPORT_PATH` et `QT_PLUGIN_PATH` avant de lancer `python -m iris`.
- `desktop/pyproject.toml` : l'extra `ar3d` devient vide afin d'éviter le téléchargement inutile de PySide6-Addons (wheel >160 Mo) ; le runtime Qt natif est géré par le script Linux dédié.
- `desktop/uv.lock` régénéré en mode offline ; le package `pyside6-addons` est retiré du lock.
- `desktop/README.md` et `BACKLOG.md` mis à jour avec la nouvelle procédure.

### Validations
- Suite desktop : `132 passed in 0.93s` avant les changements d'installation.
- `uv lock --offline` et `uv lock --check` : réussis.
- `bash -n` sur les scripts : réussi.
- Smoke test Qt Quick 3D Python : import réussi.
- Smoke test QML : `Status.Ready`, aucune erreur QML.
- Smoke test GLB : `RuntimeLoader.Success`, `GLB_LOADED True` après ajout du plugin Assimp.
- L'exécution du script d'installation persistante et le démarrage de MainWindow via `desktop/run.sh` restent en cours de validation.

### Fichiers modifiés/créés
- `desktop/pyproject.toml`
- `desktop/uv.lock`
- `desktop/README.md`
- `desktop/run.sh` (nouveau)
- `desktop/scripts/install_qt_quick3d_runtime.sh` (nouveau)
- `BACKLOG.md`
- `docs/development/DEVELOPMENT_LOG.md`

### Limites
Le chargement GLB est maintenant validé dans un runtime isolé, mais le suivi et l'alignement des lunettes sur un visage réel ne sont pas encore validés. Ne pas déclarer le filtre AR fini avant le test webcam.
