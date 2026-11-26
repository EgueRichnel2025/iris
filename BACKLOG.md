# IRIS — Backlog

> Suivi vivant du travail restant et historique opérationnel du dépôt.
> Toute session de développement doit mettre à jour ce fichier : tâches terminées, nouvelles tâches, validations, fichiers touchés, commits et publication.

## Périmètre actif

L'application de référence est la version native Python située dans `desktop/`. Le prototype web historique est conservé dans `legacy/web/` et ne doit pas être présenté comme le runtime actif.

## Backlog priorisé

### P0 — Suivi facial sur desktop
- [x] Implémenter un utilitaire de lissage temporel EMA indépendant et le couvrir par des tests unitaires.
- [ ] Intégrer MediaPipe Face Landmarker dans le pipeline de frames de l'application desktop.
  - [x] Créer l'adaptateur Python isolé : chargement explicite, mode VIDEO, validation des frames, extraction des landmarks et fermeture propre.
  - [x] Télécharger le modèle local officiel et vérifier son SHA-256.
  - [ ] Installer et tester le runtime MediaPipe réel.
- [x] Définir une première composition détection + lissage dans un pipeline vision indépendant de l'UI.
- [ ] Ajouter le suivi temporel et le lissage des landmarks ; mesurer la stabilité et les FPS.
- [ ] Prévoir la gestion du modèle (chargement, erreurs, fermeture propre et stratégie d'assets locaux).

### P1 — Effets AR 2D
- [ ] Ajouter des accessoires ancrés au visage (lunettes, chapeaux, oreilles, etc.).
- [ ] Stabiliser leur position, leur échelle et leur rotation pendant les mouvements de tête.
- [ ] Prévoir une sélection et un aperçu des effets.

### P2 — Déformations faciales
- [ ] Construire un maillage facial exploitable pour le warping.
- [ ] Implémenter les déformations de bouche sur une région complète, pas sur un seul landmark.
- [ ] Implémenter les déformations de tête/visage : agrandir, réduire, élargir, rétrécir et squash/stretch.
- [ ] Éviter les trous, déchirures et déformations cumulatives d'une frame à l'autre.

### P3 — Expériences et distribution
- [ ] Relier certains effets aux expressions et mouvements (bouche ouverte, sourire, clignement, orientation).
- [ ] Ajouter l'enregistrement vidéo avec les effets appliqués.
- [ ] Tester le build Windows sur Windows et réaliser un smoke test sur une machine propre.
- [ ] Ajouter des tests ciblés à chaque nouvelle brique vision/effets.

### P4 — Documentation continue
- [x] Séparer visuellement les stacks actives, planifiées et historiques dans le README principal.
- [x] Réorganiser le guide README de l'application desktop.
- [x] Créer ce fichier de backlog et établir une règle de journalisation par session.

## Historique des actions

### 2026-11-26 — Documentation, stacks et publication

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Reconnexion à la machine via Desktop Commander et accès au disque du projet avec le chemin `/run/media/richnel/Richnel_disque`. | Accès au dépôt confirmé. |
| 2 | Inspection de `iris/`, de la branche, du remote et de l'état Git. | Dépôt `EgueRichnel2025/iris`, branche `main`, remote `origin`; aucun changement préexistant non lié à cette session. |
| 3 | Recherche d'un fichier de backlog. | Aucun fichier Backlog/TODO/Changelog dédié trouvé ; le journal `docs/development/DEVELOPMENT_LOG.md` existait déjà. |
| 4 | Lecture des README, `desktop/pyproject.toml`, CI et code desktop. | Stack active confirmée : Python, PySide6, OpenCV et NumPy. MediaPipe est une dépendance déclarée, mais son intégration desktop reste à faire. Le prototype React/TypeScript/Supabase est historique (`legacy/web/`). |
| 5 | Réécriture du README racine. | Présentation du produit, fonctionnalités, stacks distinctes, architecture, installation, tests, packaging, structure et roadmap. |
| 6 | Réécriture de `desktop/README.md`. | Guide desktop et responsabilités des technologies clarifiés. |
| 7 | Vérification documentaire `git diff --check`. | Réussie, aucune erreur d'espacement détectée. |
| 8 | Tests avec l'environnement desktop déjà installé : `.venv/bin/python -m pytest -q`. | **9 tests réussis**. |
| 9 | Tentative de `uv run --directory desktop pytest -q`. | `uv` a commencé une synchronisation/téléchargement de grosses dépendances ; le test a été validé via le venv existant pour éviter de dépendre de cette synchronisation. |
| 10 | Création de `BACKLOG.md` et ajout de cette session au journal de développement. | Fichier de suivi créé ; journal permanent complété. |
| 11 | Commit des README. | `9030c88` — `docs(readme): reorganize desktop stack documentation`. |
| 12 | Commit du backlog et du journal. | `15edd15` — `docs(development): add project backlog and session log`. |
| 13 | Push des deux commits vers `origin/main`. | Réussi : `d289df8..15edd15 main -> main`. |
| 14 | Vérification finale du dépôt distant et de l’arbre de travail. | À confirmer après la dernière vérification Git. |

## Règles de mise à jour

1. Commencer chaque session par lire ce backlog et vérifier `git status`.
2. Mettre à jour les cases du backlog quand une tâche est réellement terminée.
3. Ajouter une entrée datée à l'historique pour les actions importantes, y compris les fichiers touchés, commandes lancées et résultats.
4. Mettre à jour aussi `docs/development/DEVELOPMENT_LOG.md` à chaque session.
5. Après chaque commit, inscrire son hash et son message ; après chaque push, inscrire la branche et confirmer le résultat.
6. Ne jamais marquer une tâche ou une validation comme terminée sans preuve d'exécution.


### 2026-11-26 — Première brique de stabilisation des landmarks

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Vérification de la branche et du dépôt distant. | `main` était synchronisée avec `origin/main` avant le travail. |
| 2 | Inspection de l'environnement Python, des dépendances verrouillées et des assets. | Python 3.14.4, NumPy et OpenCV présents ; MediaPipe absent de l'environnement actif ; aucun modèle Face Landmarker `.task` dans le dépôt. La dépendance MediaPipe 1.2.3 est bien présente dans `uv.lock` avec une roue Linux x86_64. |
| 3 | Tentative de synchronisation `uv sync --extra dev`. | Téléchargements de plusieurs dépendances lourdes commencés ; synchronisation interrompue avant installation complète. L'environnement existant a été conservé et utilisé pour les tests. |
| 4 | Création de `desktop/iris/vision/` et de `LandmarkSmoother`. | Lissage EMA, validation de alpha, coordonnées 2D/3D, reset et réinitialisation si le nombre/la forme des points change. |
| 5 | Ajout de `desktop/tests/test_smoothing.py`. | 12 cas de test ajoutés, y compris les valeurs limites, les formes invalides et les coordonnées non finies. |
| 6 | Exécution de la suite complète. | **21 tests réussis** ; `compileall` et `git diff --check` réussis. |
| 7 | Commit de la brique EMA. | `b19bdba` — `feat(vision): add temporal landmark smoothing`. |
| 8 | Mise à jour du backlog et du journal avec le hash du commit. | Commit documentaire `6922ab2` créé. |
| 9 | Push des commits de cette étape. | Réussi : `ef1adb0..6922ab2 main -> main`. |
| 10 | Vérification finale de la branche et de l’arbre de travail. | `main` synchronisée avec `origin/main`, arbre de travail propre. |

La détection faciale MediaPipe n'est pas encore intégrée à la caméra : le paquet n'est pas encore installé dans l'environnement actif et le modèle `.task` manque. La prochaine tâche est de finaliser les dépendances, récupérer et versionner proprement l'asset du modèle, puis créer l'adaptateur Face Landmarker.


### 2026-11-26 — Adaptateur MediaPipe Face Landmarker

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Vérification de la branche, du remote, du backlog et de l'environnement. | main propre et synchronisée avec origin/main ; MediaPipe absent du venv actif. |
| 2 | Vérification de la documentation officielle Face Landmarker et de l'URL du modèle. | API Python VIDEO confirmée ; asset face_landmarker.task disponible sur Google Cloud Storage (3,58 Mio). |
| 3 | Création de desktop/iris/vision/face_landmarker.py. | Adaptateur isolé avec chargement explicite, mode VIDEO, horodatages strictement croissants, validation des frames, conversion RGB, extraction des coordonnées normalisées et fermeture idempotente. |
| 4 | Création de desktop/tests/test_face_landmarker.py. | Tests unitaires du cycle de vie, des entrées invalides, de la conversion BGR vers RGB, des timestamps et de l'extraction des landmarks. |
| 5 | Validation de la suite et de la compilation. | 33 tests réussis ; compileall et git diff --check réussis. |
| 6 | Commit de l'adaptateur et de ses tests. | 93d656b — feat(vision): add MediaPipe face landmarker adapter. |
| 7 | Téléchargement du modèle et installation MediaPipe. | En cours ; téléchargement lent observé. L'intégration réelle à la caméra n'est pas encore déclarée terminée. |



### 2026-11-26 — Conversion des coordonnées faciales

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Création de desktop/iris/vision/coordinates.py. | Conversion des coordonnées normalisées en pixels pour les points 2D/3D, avec validation des dimensions et des valeurs. |
| 2 | Création de desktop/tests/test_coordinates.py. | 11 assertions/cas couvrant les conversions, les entrées invalides et la non-modification des données source. |
| 3 | Tests et compilation. | 44 tests réussis ; compileall et git diff --check réussis. |
| 4 | Commit. | 487315e — feat(vision): convert normalized landmarks to pixels. |


### 2026-11-26 — Ajout de l'asset Face Landmarker

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Téléchargement du modèle Face Landmarker officiel. | Fichier desktop/assets/models/face_landmarker.task téléchargé (3,58 Mio). |
| 2 | Vérification de l'intégrité. | SHA-256 vérifié : 64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff. |
| 3 | Ajout de la provenance. | README dans le dossier models avec URL source, date et empreinte SHA-256. |
| 4 | Commit de l'asset. | 7ddf5c9 — assets(vision): add MediaPipe face landmarker model. |
| 5 | Installation de MediaPipe. | Toujours en cours via uv ; le runtime réel n'est pas encore validé. |


### 2026-11-26 — Résolution du chemin du modèle

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Création de desktop/iris/vision/model_assets.py. | Résolution du modèle en mode source et depuis le dossier temporaire PyInstaller. |
| 2 | Création de desktop/tests/test_model_assets.py. | Tests des chemins source et bundle. |
| 3 | Validation. | 46 tests réussis ; compilation et git diff --check réussis. |
| 4 | Commit. | ff02bf3 — feat(vision): resolve local face model asset path. |


### 2026-11-26 — Pipeline vision indépendant

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Création de desktop/iris/vision/pipeline.py. | Composition du détecteur et d'un lisseur EMA par visage ; perte de visage = remise à zéro de l'historique. |
| 2 | Création de desktop/tests/test_vision_pipeline.py. | Tests du cycle de vie, du lissage, de la perte/réacquisition et des paramètres. |
| 3 | Validation. | 51 tests réussis ; compilation et git diff --check réussis. |
| 4 | Commit. | 3bf99b9 — feat(vision): compose face detection and landmark smoothing. |


### 2026-11-26 — Modèle local par défaut

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Connexion de FaceLandmarker au résolveur d'asset. | Le constructeur peut maintenant être utilisé sans chemin explicite et charge le modèle local IRIS par défaut. |
| 2 | Test du chemin par défaut. | Cas ajouté à la suite dédiée Face Landmarker. |
| 3 | Validation. | 52 tests réussis ; compilation réussie. |
| 4 | Commit. | 968062a — feat(vision): use bundled face model by default. |


### 2026-11-26 — Préparation du packaging MediaPipe

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Mise à jour de desktop/IRIS.spec. | Inclusion du runtime MediaPipe, de ses ressources et du modèle face_landmarker.task. |
| 2 | Simplification de desktop/build.sh et desktop/build.ps1. | Les deux scripts appellent désormais le spec commun. |
| 3 | Validation statique. | bash -n build.sh et compilation syntaxique IRIS.spec réussis ; 52 tests réussis. |
| 4 | Commit. | 4f9b8d6 — build(desktop): bundle face model and MediaPipe runtime. |
| 5 | Packaging réel. | Non exécuté : attente de l'installation du runtime MediaPipe dans le venv. |
