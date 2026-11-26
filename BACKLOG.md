# IRIS — Backlog

> Suivi vivant du travail restant et historique opérationnel du dépôt.
> Toute session de développement doit mettre à jour ce fichier : tâches terminées, nouvelles tâches, validations, fichiers touchés, commits et publication.

## Périmètre actif

L'application de référence est la version native Python située dans `desktop/`. Le prototype web historique est conservé dans `legacy/web/` et ne doit pas être présenté comme le runtime actif.

## Backlog priorisé

### P0 — Suivi facial sur desktop
- [ ] Intégrer MediaPipe Face Landmarker dans le pipeline de frames de l'application desktop.
- [ ] Définir les modules de détection, landmarks, tracking et pose avec des responsabilités distinctes.
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
| 11 | Commit des README, commit de suivi puis push vers `origin/main`. | À renseigner après exécution et vérification des retours Git. |

## Règles de mise à jour

1. Commencer chaque session par lire ce backlog et vérifier `git status`.
2. Mettre à jour les cases du backlog quand une tâche est réellement terminée.
3. Ajouter une entrée datée à l'historique pour les actions importantes, y compris les fichiers touchés, commandes lancées et résultats.
4. Mettre à jour aussi `docs/development/DEVELOPMENT_LOG.md` à chaque session.
5. Après chaque commit, inscrire son hash et son message ; après chaque push, inscrire la branche et confirmer le résultat.
6. Ne jamais marquer une tâche ou une validation comme terminée sans preuve d'exécution.
