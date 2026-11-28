# IRIS — Backlog

> Suivi vivant du travail restant et historique opérationnel du dépôt.
> Toute session de développement doit mettre à jour ce fichier : tâches terminées, nouvelles tâches, validations, fichiers touchés, commits et publication.

## Périmètre actif

L'application de référence est la version native Python située dans `desktop/`. Le prototype web historique est conservé dans `legacy/web/` et ne doit pas être présenté comme le runtime actif.

## Backlog priorisé

### P0 — Suivi facial sur desktop
- [x] Implémenter un utilitaire de lissage temporel EMA indépendant et le couvrir par des tests unitaires.
- [x] Intégrer MediaPipe Face Landmarker dans le pipeline de frames de l'application desktop.
  - [x] Créer l'adaptateur Python isolé : chargement explicite, mode VIDEO, validation des frames, extraction des landmarks et fermeture propre.
  - [x] Télécharger le modèle local officiel et vérifier son SHA-256.
  - [x] Installer et tester le runtime MediaPipe réel (MediaPipe 1.2.3).
- [x] Définir une première composition détection + lissage dans un pipeline vision indépendant de l'UI.
- [x] Ajouter le suivi temporel et le lissage EMA des landmarks ; mesurer la stabilité et les FPS sur le poste de développement.
- [x] Prévoir la gestion du modèle (chargement, erreurs, fermeture propre et asset local intégré au bundle).
- [x] Estimer la pose de tête (yaw, pitch, roll) depuis six landmarks stables et publier les angles en temps réel.

### P1 — Effets AR 2D
- [x] Ajouter un premier accessoire ancré au visage (lunettes) ; chapeaux et oreilles restent à faire.
- [x] Exploiter les landmarks lissés pour stabiliser la position, l’échelle et la rotation des lunettes ; validation visuelle prolongée en mouvement encore à effectuer.
- [ ] Prévoir une sélection et un aperçu des effets.

### P1 — Rendu 3D des accessoires
- [x] Évaluer un moteur de rendu GLB compatible avec Qt sans intégrer le backend VTK instable.
- [x] Charger et afficher le modèle GLB avec Qt Quick 3D `RuntimeLoader`.
- [x] Vérifier un compositing statique image caméra + modèle 3D dans `QQuickWidget`.
- [ ] Déclarer les dépendances Qt Quick 3D dans l'extra desktop et préparer le packaging.
- [ ] Remplacer l'aperçu QLabel par le rendu composite dans l'application.
- [ ] Connecter le flux vidéo temps réel et la matrice MediaPipe au modèle.
- [ ] Calibrer projection, axes, pivot et échelle sur un visage réel ; valider en mouvement.

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


### 2026-11-26 — Intégration du suivi facial temps réel

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Installation de MediaPipe 1.2.3 dans desktop/.venv. | Import réel de mediapipe.tasks.vision validé. |
| 2 | Chargement du modèle officiel avec FaceLandmarker. | Modèle chargé ; inférence sur image synthétique réussie (0 visage attendu). |
| 3 | Test direct sur la webcam. | 5 frames traitées ; 1 visage et 478 landmarks détectés sur chacune ; libération caméra confirmée. |
| 4 | Création de desktop/iris/vision/overlay.py et de ses tests. | Rendu des points faciaux sur une copie de l'image ; 7 cas de tests ajoutés. Commit 11dec19 — feat(vision): render facial landmarks on camera frames. |
| 5 | Intégration du pipeline dans CameraThread et exposition du nombre de visages à MainWindow. | Détection et EMA exécutées dans le thread caméra ; erreurs vision isolées des erreurs caméra ; fermeture du détecteur à l'arrêt. Commit 84d065f — feat(camera): integrate real-time face tracking. |
| 6 | Tests automatisés. | 61 tests réussis ; compileall et git diff --check réussis. |
| 7 | Test QThread avec boucle Qt. | 39 échantillons de détection positive en 3,5 s ; aucun problème vision/caméra ; thread arrêté proprement. |
| 8 | Test de l'interface réelle. | CAMÉRA ACTIVE ; 1 VISAGE DÉTECTÉ ; frame reçue ; mesure observée autour de 17 FPS pendant le smoke test. |
| 9 | Build PyInstaller Linux. | Build réussi et lancement smoke test 8 s sans crash. Bundle de 743 Mio dans l'environnement système actuel ; réduction de taille à traiter car OpenCV système embarque de nombreuses bibliothèques natives non nécessaires. |
| 10 | Installation du wheel OpenCV contrib verrouillé. | Tentative interrompue car le téléchargement de 84,9 Mio n'avançait pas suffisamment ; l'environnement actif utilise encore OpenCV système 4.10.0. |
| 11 | Mise à jour du spec PyInstaller. | Collecte MediaPipe ciblée (ressources, bibliothèques dynamiques et imports Face Landmarker), exclusions de modules non utilisés. |

État : le suivi facial est désormais intégré et validé en direct sur la webcam. La taille du bundle Linux reste à optimiser dans un environnement installé avec le wheel OpenCV du lockfile. Le build Windows reste à produire sur Windows.


### 2026-11-26 — Estimation de la pose de tête

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Création de desktop/iris/vision/head_pose.py. | Estimateur HeadPoseEstimator basé sur six landmarks MediaPipe et cv2.solvePnP ; retourne yaw, pitch, roll et les vecteurs de pose. |
| 2 | Création de desktop/tests/test_head_pose.py. | 18 tests couvrant les trois axes, rotations positives/négatives, rotations combinées, images miroir et entrées invalides. |
| 3 | Alignement du modèle 3D avec les axes caméra OpenCV. | Correction d'une rotation de base proche de 180° observée sur le visage réel ; pose frontale ramenée autour de yaw 0°, pitch 4°, roll -7°. |
| 4 | Intégration à CameraThread. | Nouveau signal head_pose_updated ; estimation sur landmarks lissés ; erreur de pose isolée de la détection ; angles remis à zéro en absence de visage. |
| 5 | Intégration dans MainWindow. | Affichage séparé YAW / PITCH / ROLL ; la fenêtre ne calcule pas la pose. |
| 6 | Tests complets. | 81 tests réussis ; compileall et git diff --check réussis. |
| 7 | Smoke test de l'application réelle. | CAMÉRA ACTIVE, 1 VISAGE DÉTECTÉ, frame reçue, environ 17 FPS ; pose affichée : YAW -0°, PITCH +4°, ROLL -7°. |
| 8 | Commits de code. | 3d948a4 — fix(vision): align head pose model with camera axes ; 3644023 — feat(camera): publish live head pose estimates ; b631430 — feat(ui): display live head orientation. |
| 9 | Publication GitHub. | À confirmer après le push du jalon. |

Note technique : les angles utilisent un modèle facial générique et une matrice intrinsèque approximative (focale estimée à partir de la largeur de l'image). C'est une estimation d'orientation pour stabiliser les accessoires, pas encore une mesure métrique calibrée de la caméra.


### 2026-11-26 — Premier accessoire AR : lunettes

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Inspection de la branche et du travail local. | `main` était propre mais en avance de trois commits sur `origin/main` ; les trois commits AR étaient présents localement. |
| 2 | Création du rendu des lunettes dans `desktop/iris/vision/glasses.py`. | Deux verres elliptiques teintés, monture, pont nasal et branches calculés à partir des landmarks des coins des yeux ; la frame d’entrée n’est pas modifiée. |
| 3 | Ajout des tests du rendu. | Tests de géométrie, transparence, landmarks 2D/3D et validation des entrées. Commit `65de655` — `feat(ar): render face-anchored glasses`. |
| 4 | Ajout du catalogue d’accessoires et intégration à l’application. | Sélecteur « Lunettes » dans la sidebar ; `CameraThread` applique l’accessoire aux landmarks lissés. Commit `c175b9d` — `feat(camera): integrate selectable AR accessories`. |
| 5 | Couverture du chemin caméra. | Test vérifiant que l’accessoire sélectionné est appliqué à chaque frame détectée. Commit `1000738` — `test(camera): cover AR accessory frame integration`. |
| 6 | Suite de tests et compilation. | **97 tests réussis** ; `compileall` et `git diff --check` réussis. |
| 7 | Smoke test caméra réelle avec « Lunettes » sélectionné. | 25 frames reçues, aucune erreur caméra/vision, thread arrêté proprement. Le dernier échantillon ne signalait aucun visage : le placement visuel sur visage réel reste à confirmer en présence d’un visage dans le champ. |
| 8 | Journalisation et mise à jour du backlog. | Premier accessoire marqué livré ; validation visuelle prolongée et autres accessoires restent au backlog. |
| 9 | Publication GitHub. | À confirmer après push des commits locaux. |


### 2026-11-26 — Amélioration géométrique des lunettes AR

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Inspection du code et du diff local existant. | Travail local préexistant préservé ; géométrie indépendante par œil et mesure de l'ouverture palpébrale conservées. |
| 2 | Ajout de tests géométriques. | Tests de raccourcissement perspectif indépendant, rotation de l'œil, ouverture des paupières et valeurs invalides. Commit `392565b` — `test(ar): cover perspective-aware glasses geometry`. |
| 3 | Remplacement des ellipses par des contours de lentilles. | Les lentilles sont construites à partir des coins et repères supérieurs/inférieurs des yeux, puis agrandies selon les axes locaux de chaque œil ; remplissage translucide et contour de monture polygonal. Commit `a303495` — `feat(ar): render glasses from expanded eye contours`. |
| 4 | Validation complète. | **101 tests réussis** ; compilation Python et `git diff --check` réussis. |
| 5 | Test caméra avec visage. | Non effectué pendant cette étape ; le dernier smoke test caméra antérieur avait reçu des frames mais aucun visage n'avait été confirmé. |
| 6 | Publication GitHub. | À confirmer après le push des commits. |

À faire ensuite : validation visuelle webcam avec visage présent, ajustement des proportions/style sur différents yaw/roll, puis amélioration de l'occlusion et des branches.


### 2026-11-26 — Préparation du moteur d'accessoires 3D

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Étude du pipeline MediaPipe et des dépendances de rendu présentes. | Face Landmarker ne renvoyait jusqu'ici que les landmarks ; VTK 9.5.2 est présent dans l'environnement système, mais pas déclaré comme dépendance projet. |
| 2 | Sélection d'un modèle de lunettes 3D. | Modèle GLB rectangulaire de 223 Ko provenant de la bibliothèque Innerscene, dédié sous CC0 1.0 ; licence et SHA-256 consignés à côté de l'asset. |
| 3 | Ajout de la sortie matrice faciale. | `FaceLandmarker` demande maintenant `output_facial_transformation_matrixes=True` et expose les matrices 4×4 dans `FaceLandmarkResult`. |
| 4 | Tests et validation. | **102 tests réussis**, compilation Python et `git diff --check` réussis. |
| 5 | Essai de rendu GLB via VTK. | `vtkGLTFImporter` signale `Error loading binary data` pour cet asset ; cette voie n'est pas validée et n'est pas intégrée. |
| 6 | Publication des changements de code et de l'asset. | Commits `ed8cadf`, `87389b6`, `24754d5` ; push à effectuer/contrôler. |

**Important :** le modèle 3D est maintenant présent dans le dépôt et MediaPipe expose la transformation faciale, mais l'accessoire 3D n'est pas encore affiché dans la caméra. L'ancien rendu 2D polygonal reste le rendu sélectionnable tant que le moteur 3D n'est pas prêt. Prochaine tâche bloquante : choisir et valider un renderer glTF/GLB compatible PySide6 et le pipeline caméra, puis aligner le modèle (échelle, axes, pivot) sur la matrice faciale et vérifier l'occlusion.


### 2026-11-26 — Première scène 3D GLB dans Qt

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Diagnostic Qt Quick 3D. | `PySide6-Addons==6.10.2` nécessite un téléchargement d'environ 163 Mo, qui ne progressait pas ; processus interrompu. Aucun module Qt Quick/Qt Quick 3D installé. |
| 2 | Essai du lecteur glTF VTK. | `vtkGLTFReader` lit le GLB correctement (1 bloc de géométrie). L'extension glTF `KHR_materials_specular` n'est pas prise en charge par VTK et est ignorée. |
| 3 | Validation Qt + VTK. | `QVTKRenderWindowInteractor` s'intègre à une fenêtre PySide6 ; affichage de la scène et capture PNG réussis. Le rendu offscreen VTK direct a provoqué un segfault ; la voie retenue utilise le widget Qt. |
| 4 | Création du chargeur 3D. | `desktop/iris/vision/glasses_3d.py` valide le GLB, charge sa géométrie et crée un widget VTK intégré à Qt. |
| 5 | Dépendance facultative. | Extra `ar3d = ["vtk>=9.5.2,<9.6"]` ajouté ; VTK n'est pas imposé aux installations sans accessoires 3D. |
| 6 | Tests. | 6 nouveaux tests GLB ; suite complète **108 tests réussis** ; compilation et `git diff --check` réussis. |
| 7 | Commits. | `c1e7d48` validation GLB ; `7c0c6a1` chargeur VTK ; `2c45f5d` dépendance optionnelle. Publication à vérifier. |

**Limites restantes :** scène 3D statique validée, mais non encore raccordée à la caméra ou à la matrice MediaPipe. Le repère du modèle (orientation, pivot, échelle) reste à calibrer ; l'occlusion et le suivi temps réel ne sont pas encore réalisés.


### 2026-11-26 — Conversion de la pose MediaPipe vers le modèle GLB

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Capture d'une matrice faciale sur webcam réelle. | 1 visage et 1 matrice 4×4 détectés sur une frame 640×480 ; translations observées en coordonnées faciales/caméra (ex. environ -2,6 / -8,4 / -26,4). |
| 2 | Inspection de la géométrie GLB. | Dimensions mesurées par VTK : largeur 14,56 cm, hauteur 4,60 cm, branches jusqu'à 14,13 cm en profondeur ; sommets stockés en mètres. |
| 3 | Création de `desktop/iris/vision/face_transform.py`. | Conversion explicite GLB mètres → espace MediaPipe centimètres, multiplication `M_face @ S_model`, validation de matrice affine et des valeurs finies. |
| 4 | Propagation des matrices dans le pipeline. | `VisionFrameResult` conserve les matrices faciales ; aucune matrice propagée quand le visage est perdu. |
| 5 | Signal caméra → GUI. | Nouveau signal `face_transform_updated(object)` émet une copie de la première matrice ou `None`, sans manipuler VTK dans le thread caméra. |
| 6 | Cycle de vie Qt/VTK. | Initialisation VTK différée après affichage du widget ; la mise à jour de l'acteur n'appelle pas Render sur un widget non initialisé. |
| 7 | Tests. | **126 tests réussis** ; compilation et `git diff --check` réussis. 14 nouveaux tests de conversion/acteur/pipeline/caméra/cycle de vie. |
| 8 | Test visuel webcam + widget VTK. | Non validé : le test combiné webcam/Qt/VTK a échoué avec X11 `BadWindow` dans l'environnement de test. Aucun screenshot de lunettes portées par le visage n'est revendiqué. Le signal de matrice et l'application de la matrice à un acteur VTK non rendu sont testés. |
| 9 | Commits. | Conversion, tests, propagation pipeline, signal caméra et cycle de vie VTK publiés localement ; push à effectuer/contrôler. |

**Limite actuelle :** l'interface principale affiche toujours le flux caméra dans un QLabel et n'héberge pas encore le widget 3D. Le modèle n'est donc pas encore superposé à l'image. La matrice MediaPipe est désormais disponible côté GUI, mais le repère exact, le cadrage caméra, l'occlusion et le rendu composite restent à valider.


### 2026-11-26 — Préparation de la composition vidéo + 3D

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Ajout du flux RGB côté caméra. | Nouveau signal `video_frame_ready(object)` émet une copie RGB de chaque frame après effets ; le signal Qt peut être consommé côté interface. |
| 2 | Composition VTK. | La scène GLB possède maintenant un renderer d'arrière-plan avec `vtkImageImport`/`vtkImageActor` et un renderer 3D au premier plan. La fonction `update_glasses_video_frame` actualise la texture et configure une caméra perspective initiale. |
| 3 | Tests. | 2 tests de composition vidéo (format RGB, orientation verticale, dimensions, caméra) et assertion du signal RGB ; suite complète **128 tests réussis**. Compilation et `git diff --check` réussis. |
| 4 | Intégration QVTK dans MainWindow. | Tentative rejetée : le widget `QVTKRenderWindowInteractor` enfant déclenche `X Error: BadWindow` sous X11 dans l'interface IRIS, y compris lorsque l'initialisation est différée et que le widget reste visible. Les changements d'interface ont été annulés pour préserver le lancement normal de l'application. |
| 5 | Commits. | `feat(camera): publish RGB frames for AR composition` et `feat(ar): composite camera frames behind 3D accessories`. Publication à contrôler. |

**État honnête :** les frames RGB sont disponibles et la scène VTK sait recevoir une image de fond, mais la scène 3D n'est pas encore intégrée à `MainWindow`. L'alignement visuel des lunettes avec le visage et le rendu sur webcam restent non validés. Prochaine étape technique : remplacer le widget VTK natif X11 par une intégration Qt/OpenGL compatible (ou une surface de rendu indépendante), puis refaire le smoke test complet avant de reconnecter l'interface.

### 2026-11-26 — Diagnostic du backend Qt/OpenGL pour le compositing AR

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Vérification de l'état initial. | Branche `main` propre et synchronisée avec `origin/main` au commit `4d0f856`. Les limites de la tentative QVTK/X11 précédente sont conservées. |
| 2 | Vérification des bindings Qt installés. | PySide6 Essentials 6.10.2 ne fournit pas `QtOpenGLWidgets` ni `QtOpenGL` dans l'environnement initial ; les bibliothèques système Qt sont présentes. |
| 3 | Smoke test Qt OpenGL. | Les paquets Ubuntu correspondants ont été extraits dans un environnement local temporaire (sans modification des dépendances du projet). Un `QOpenGLWidget` indépendant crée un contexte valide et se ferme proprement. |
| 4 | Test VTK avec base QOpenGLWidget et `vtkGenericOpenGLRenderWindow`. | Le widget QVTK passe bien à la classe de base `QOpenGLWidget`, mais le rendu provoque un segmentation fault. Le rendu EGL hors écran VTK provoque également un crash sur cette machine. Ces voies ne sont pas intégrables en l'état. |
| 5 | Inspection des bindings VTK. | Seul `QVTKRenderWindowInteractor` est exposé en Python ; le widget moderne `QVTKOpenGLNativeWidget`, qui gère le contexte Qt et `vtkGenericOpenGLRenderWindow`, n'est pas disponible dans les bindings installés. |
| 6 | État du dépôt. | Aucun code applicatif modifié pendant ce diagnostic ; les essais de paquets restent locaux à `.venv` et `/tmp`. Aucune régression introduite dans le code versionné. |

**Décision technique :** ne pas connecter QVTK à `MainWindow` et ne pas contourner le segmentation fault. Deux pistes à comparer avec un prototype minimal avant choix : (a) Qt Quick 3D avec le module PySide6 Addons, qui sait charger glTF/GLB ; (b) un renderer OpenGL dédié dans `QOpenGLWidget` avec un parseur glTF Python. Le critère est un rendu GLB stable dans la fenêtre Qt, pas seulement un import de fichier.

**État honnête :** la caméra et la matrice faciale sont disponibles ; le modèle GLB est présent ; aucun rendu 3D composité sur la webcam n'est encore validé. Aucun commit fonctionnel ni push n'est revendiqué pour cette session de diagnostic.


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

### 2026-11-27 — Stabilisation du runtime Qt Quick 3D

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Vérification du dépôt, du backlog, de l'environnement et des modules réellement importables. | `main` était propre et synchronisée ; les 132 tests passent. Les bindings QtQuick3D seuls ne suffisaient pas : `libQt6Quick3D.so.6` et plusieurs composants natifs manquaient. |
| 2 | Diagnostic du runtime Ubuntu Qt 6.10.2. | Les paquets nécessaires sont disponibles en petits paquets apt ; aucun besoin de télécharger le wheel PySide6-Addons de plus de 160 Mo. |
| 3 | Extraction temporaire des bibliothèques Qt Quick 3D et des modules QML. | Imports Python Quick3D et QML `Status.Ready` validés en isolant `LD_LIBRARY_PATH`, `QML2_IMPORT_PATH` et `QT_PLUGIN_PATH`. |
| 4 | Installation du plugin d'import glTF/GLB Assimp. | `RuntimeLoader` a d'abord signalé `Unsupported`; après ajout de `qt6-quick3d-assetimporters-plugin`, le GLB est chargé avec `RuntimeLoader.Success`. |
| 5 | Préparation d'une installation locale reproductible. | Ajout de `desktop/scripts/install_qt_quick3d_runtime.sh` et `desktop/run.sh` ; aucun privilège administrateur requis. |
| 6 | Allègement de l'extra Python AR. | `ar3d` ne déclenche plus le téléchargement du wheel PySide6-Addons ; les bindings et bibliothèques Qt natifs sont préparés par le script local. |
| 7 | Documentation. | `desktop/README.md` décrit désormais la procédure de préparation et le lanceur dédié au rendu GLB. |

**Validation importante :** QML `Status.Ready` et chargement GLB `RuntimeLoader.Success` confirmés avec les composants extraits dans `/tmp`. Le lancement de l'application complète avec l'installation persistante et le suivi sur visage réel reste à valider avant de marquer le rendu AR comme terminé.

### 2026-11-28 — Amélioration de l'éclairage et de l'interface

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Lecture de la capture du 28/11 à 06:45 et diagnostic du flux caméra. | Caméra active, un visage détecté, pose faciale stable, 17 FPS ; image sous-exposée avec une forte différence entre visage et fenêtre de fond. |
| 2 | Mesure du flux caméra brut. | Luminance LAB moyenne observée autour de 75 sur 60 frames (la mesure dépend de l'éclairage ambiant). |
| 3 | Ajout d'une correction locale d'éclairage CLAHE sur le canal de luminance LAB. | Les ombres sont relevées sans appliquer un gain global aux hautes lumières ; traitement après inférence pour préserver les pixels transmis à MediaPipe. |
| 4 | Mesure de coût et effet sur 60 frames réelles. | Luminance moyenne mesurée : 75,2 → 90,7 ; coût CLAHE moyen : 5,19 ms/frame (P95 5,59 ms). |
| 5 | Traduction de l'interface. | Titres, filtres, statuts et textes latéraux traduits en français ; titres latéraux autorisés à passer à la ligne. |
| 6 | Ajustement de l'éclairage du modèle 3D. | Intensité de la lumière directionnelle réduite de 1,5 à 1,0 pour limiter les reflets trop agressifs sur les parties métalliques. Aucun changement aveugle de géométrie du pont nasal : la capture ne permet pas d'isoler suffisamment les sous-maillages. |
| 7 | Tests et smoke test GUI réel. | **135 tests réussis** ; compilation et `git diff --check` réussis ; MainWindow ouverte, caméra active, 1 visage détecté, QML `Status.Ready`, lunettes sélectionnées, environ 17 FPS. |

**Limites restantes :** la correction logicielle ne remplace pas une meilleure lumière frontale ; la calibration du modèle de lunettes (pivot, échelle, pont nasal et ajustement en mouvement) doit encore être validée visuellement. La géométrie du GLB n'a pas été modifiée dans cette étape.

### 2026-11-28 — Réduction de la taille des lunettes

| # | Action | Résultat |
| --- | --- | --- |
| 1 | Vérification du modèle GLB et de l'échelle active. | Monture frontale déclarée à 134 mm de large ; échelle QML précédente : 100 %. |
| 2 | Ajustement conservateur de l'échelle globale. | Échelle réduite de 100 % à 88 % (−12 %) en conservant le pivot, la pose faciale et les proportions. |
| 3 | Validation statique. | Fichier QML contrôlé ; tests et vérification visuelle en cours sur la webcam. |

**À confirmer :** le rendu doit être vérifié sur la caméra en mouvement ; si la largeur n'est pas encore adaptée, la prochaine correction portera sur la calibration visage/échelle plutôt que sur des diminutions arbitraires.
