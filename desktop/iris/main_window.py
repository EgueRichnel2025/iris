"""Main PySide6 window for the IRIS camera experience."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from iris.accessories import ACCESSORIES
from iris.camera import CameraThread
from iris.effects import EFFECTS

try:
    from iris.qt_quick_glasses import GlassesQuickView
except ImportError:
    GlassesQuickView = None


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("IRIS — Filtres en temps réel")
        self.setMinimumSize(1120, 760)
        self.resize(1380, 860)
        self.current_frame = None
        self.camera = CameraThread()
        self.glasses_view = None

        self._build_interface()
        self.camera.image_ready.connect(self._show_frame)
        self.camera.video_frame_ready.connect(self._show_video_frame)
        self.camera.face_transform_updated.connect(self._update_glasses_pose)
        self.camera.raw_frame_ready.connect(self._remember_frame)
        self.camera.camera_ready.connect(self._camera_started)
        self.camera.camera_error.connect(self._camera_failed)
        self.camera.fps_updated.connect(self._show_fps)
        self.camera.face_count_updated.connect(self._show_face_count)
        self.camera.head_pose_updated.connect(self._show_head_pose)
        self.camera.vision_error.connect(self._vision_failed)
        QTimer.singleShot(450, self.camera.start)

    def _build_interface(self) -> None:
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #F7F5F0; color: #202321;
                font-family: 'DM Sans', 'DejaVu Sans', sans-serif; }
            QFrame#sidebar { background: #FFFFFF; border-right: 1px solid #EAE8E2; }
            QLabel#brand { font-size: 30px; font-weight: 800; color: #202321; }
            QLabel#brand span { color: #7357D9; }
            QLabel#eyebrow { color: #85877F; font-size: 10px; font-weight: 800;
                letter-spacing: 2px; }
            QLabel#pageTitle { font-size: 26px; font-weight: 800; }
            QLabel#subtitle { color: #85877F; font-size: 12px; }
            QLabel#cameraView { background: #171817; border: 1px solid #353735;
                border-radius: 18px; color: #AAA; font-size: 15px; }
            QListWidget { background: transparent; border: 0; outline: 0;
                padding: 5px; font-size: 13px; }
            QListWidget::item { padding: 13px 12px; margin: 3px 0;
                border-radius: 10px; color: #555850; }
            QListWidget::item:selected { background: #EEE9FF; color: #6045C5;
                font-weight: 700; }
            QPushButton { border: 0; border-radius: 10px; padding: 12px 18px;
                font-weight: 700; font-size: 12px; }
            QPushButton#primary { background: #7357D9; color: white; }
            QPushButton#primary:hover { background: #6045C5; }
            QPushButton#secondary { background: #EEE9FF; color: #6045C5; }
            QPushButton#secondary:hover { background: #E1D9FF; }
            QLabel#status { color: #477B42; font-size: 11px; font-weight: 800; }
            QLabel#visionStatus { color: #7357D9; font-size: 11px; font-weight: 800; }
            QLabel#hint { color: #85877F; font-size: 11px; }
            QLabel#sideNote { color: #85877F; font-size: 11px; line-height: 1.4; }
        """)

        shell = QWidget()
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(238)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(22, 28, 18, 22)
        side.setSpacing(16)

        brand = QLabel('iris<span>.</span>')
        brand.setObjectName("brand")
        side.addWidget(brand)
        eyebrow = QLabel("CAMÉRA EN DIRECT")
        eyebrow.setObjectName("eyebrow")
        side.addWidget(eyebrow)
        side.addSpacing(28)

        section = QLabel("FILTRES")
        section.setObjectName("eyebrow")
        side.addWidget(section)

        self.filter_list = QListWidget()
        self.filter_list.setSpacing(2)
        self.filter_list.setAccessibleName("Camera filters")
        for effect_id, label in EFFECTS:
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, effect_id)
            self.filter_list.addItem(item)
        self.filter_list.setCurrentRow(0)
        self.filter_list.currentItemChanged.connect(self._select_effect)
        side.addWidget(self.filter_list, 1)

        accessory_title = QLabel("ACCESSOIRES AR")
        accessory_title.setObjectName("eyebrow")
        side.addWidget(accessory_title)

        self.accessory_list = QListWidget()
        self.accessory_list.setSpacing(2)
        self.accessory_list.setAccessibleName("AR accessories")
        for accessory_id, label in ACCESSORIES:
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, accessory_id)
            self.accessory_list.addItem(item)
        self.accessory_list.setCurrentRow(0)
        self.accessory_list.currentItemChanged.connect(self._select_accessory)
        side.addWidget(self.accessory_list, 0)

        note_title = QLabel("VOTRE IMAGE, VOS RÈGLES")
        note_title.setWordWrap(True)
        note_title.setObjectName("eyebrow")
        side.addWidget(note_title)
        note = QLabel("Tout est traité localement. Votre flux vidéo reste sur votre appareil.")
        note.setObjectName("sideNote")
        note.setWordWrap(True)
        note.setMinimumWidth(0)
        side.addWidget(note)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 26, 30, 22)
        content_layout.setSpacing(18)

        top = QHBoxLayout()
        title_box = QVBoxLayout()
        page_title = QLabel("Voyez-vous autrement.")
        page_title.setObjectName("pageTitle")
        title_box.addWidget(page_title)
        subtitle = QLabel("Choisissez un effet et profitez de l’aperçu en direct.")
        subtitle.setObjectName("subtitle")
        title_box.addWidget(subtitle)
        top.addLayout(title_box)
        top.addStretch(1)
        self.status_label = QLabel("DÉMARRAGE DE LA CAMÉRA")
        self.status_label.setObjectName("status")
        top.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.vision_label = QLabel("INITIALISATION DU SUIVI FACIAL")
        self.vision_label.setObjectName("visionStatus")
        top.addWidget(self.vision_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        content_layout.addLayout(top)

        self.camera_stack = QStackedWidget()
        self.camera_view = QLabel("Démarrage de la caméra…")
        self.camera_view.setObjectName("cameraView")
        self.camera_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_view.setMinimumSize(760, 470)
        self.camera_view.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.camera_stack.addWidget(self.camera_view)
        if GlassesQuickView is not None:
            try:
                self.glasses_view = GlassesQuickView()
                self.glasses_view.setMinimumSize(760, 470)
                self.camera_stack.addWidget(self.glasses_view)
            except (RuntimeError, FileNotFoundError) as exc:
                self.vision_label.setToolTip(f"Rendu 3D indisponible : {exc}")
                self.glasses_view = None
        content_layout.addWidget(self.camera_stack, 1)

        controls = QHBoxLayout()
        self.camera_button = QPushButton("Désactiver la caméra")
        self.camera_button.setObjectName("secondary")
        self.camera_button.clicked.connect(self._toggle_camera)
        controls.addWidget(self.camera_button)

        self.capture_button = QPushButton("Prendre une photo  •")
        self.capture_button.setObjectName("primary")
        self.capture_button.clicked.connect(self._capture_photo)
        self.capture_button.setEnabled(False)
        controls.addWidget(self.capture_button)
        controls.addStretch(1)

        self.pose_label = QLabel("YAW —° · PITCH —° · ROLL —°")
        self.pose_label.setObjectName("hint")
        controls.addWidget(self.pose_label)

        self.fps_label = QLabel("— FPS")
        self.fps_label.setObjectName("hint")
        controls.addWidget(self.fps_label)
        content_layout.addLayout(controls)

        hint = QLabel("Les effets sont appliqués directement à l'image de la caméra.")
        hint.setObjectName("hint")
        content_layout.addWidget(hint)

        shell_layout.addWidget(sidebar)
        shell_layout.addWidget(content, 1)
        self.setCentralWidget(shell)

    def _select_effect(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        if current:
            self.camera.set_effect(str(current.data(Qt.ItemDataRole.UserRole)))

    def _select_accessory(
        self, current: QListWidgetItem | None, _previous: QListWidgetItem | None
    ) -> None:
        if current:
            accessory = str(current.data(Qt.ItemDataRole.UserRole))
            self.camera.set_accessory(accessory)
            if accessory == "glasses" and self.glasses_view is not None:
                self.glasses_view.set_glasses_enabled(True)
                self.camera_stack.setCurrentWidget(self.glasses_view)
            else:
                if self.glasses_view is not None:
                    self.glasses_view.set_glasses_enabled(False)
                self.camera_stack.setCurrentWidget(self.camera_view)

    def _show_video_frame(self, frame: object) -> None:
        if self.glasses_view is not None and self.camera_stack.currentWidget() is self.glasses_view:
            self.glasses_view.set_video_frame(frame)

    def _update_glasses_pose(self, matrix: object) -> None:
        if self.glasses_view is not None:
            self.glasses_view.set_face_transform(matrix)

    def _show_frame(self, image: QImage) -> None:
        pixmap = QPixmap.fromImage(image).scaled(
            self.camera_view.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.camera_view.setPixmap(pixmap)
        self.capture_button.setEnabled(True)

    def _remember_frame(self, frame: object) -> None:
        self.current_frame = frame

    def _camera_started(self, message: str) -> None:
        self.status_label.setText(message)
        self.camera_button.setText("Désactiver la caméra")
        self.camera_button.setEnabled(True)

    def _camera_failed(self, message: str) -> None:
        self.status_label.setText("CAMÉRA INDISPONIBLE")
        self.camera_view.setText(message)
        self.camera_stack.setCurrentWidget(self.camera_view)
        self.capture_button.setEnabled(False)
        self.camera_button.setText("Réessayer")

    def _show_fps(self, fps: float) -> None:
        self.fps_label.setText(f"{fps:.0f} FPS")

    def _show_face_count(self, count: int) -> None:
        if count == 0:
            self.vision_label.setText("AUCUN VISAGE")
        elif count == 1:
            self.vision_label.setText("1 VISAGE DÉTECTÉ")
        else:
            self.vision_label.setText(f"{count} VISAGES DÉTECTÉS")

    def _show_head_pose(self, yaw: float, pitch: float, roll: float) -> None:
        self.pose_label.setText(
            f"YAW {yaw:+.0f}° · PITCH {pitch:+.0f}° · ROLL {roll:+.0f}°"
        )

    def _vision_failed(self, message: str) -> None:
        self.vision_label.setText("SUIVI FACIAL INDISPONIBLE")
        self.vision_label.setToolTip(message)
        self.pose_label.setText("POSE INDISPONIBLE")

    def _toggle_camera(self) -> None:
        if self.camera.isRunning():
            self.camera.stop()
            self.camera_button.setText("Activer la caméra")
            self.capture_button.setEnabled(False)
            self.camera_view.clear()
            self.camera_view.setText("Caméra désactivée")
            self.camera_stack.setCurrentWidget(self.camera_view)
            if self.glasses_view is not None:
                self.glasses_view.set_face_transform(None)
            self.status_label.setText("CAMÉRA EN PAUSE")
            self.vision_label.setText("SUIVI EN PAUSE")
            self.pose_label.setText("POSE EN PAUSE")
        else:
            self.camera_view.setText("Démarrage de la caméra…")
            self.status_label.setText("DÉMARRAGE DE LA CAMÉRA")
            self.vision_label.setText("INITIALISATION DU SUIVI FACIAL")
            self.pose_label.setText("YAW —° · PITCH —° · ROLL —°")
            self.camera.start()

    def _capture_photo(self) -> None:
        if self.current_frame is None:
            return
        output_dir = Path.home() / "Pictures" / "IRIS"
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"iris-{datetime.now():%Y%m%d-%H%M%S}.jpg"
        destination = output_dir / filename
        if cv2.imwrite(str(destination), self.current_frame):
            self.status_label.setText("PHOTO ENREGISTRÉE")
            self.fps_label.setText(str(destination))
        else:
            self.status_label.setText("ÉCHEC DE LA CAPTURE")

    def closeEvent(self, event) -> None:  # noqa: N802
        if self.camera.isRunning():
            self.camera.stop()
        event.accept()
