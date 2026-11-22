"""Threaded webcam capture and frame processing."""

from __future__ import annotations

import sys
import time

import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from iris.effects import apply_effect


def camera_backend() -> int:
    """Select the native camera backend for the current operating system."""
    if sys.platform.startswith("linux"):
        return cv2.CAP_V4L2
    if sys.platform == "win32":
        return cv2.CAP_DSHOW
    if sys.platform == "darwin":
        return cv2.CAP_AVFOUNDATION
    return cv2.CAP_ANY


class CameraThread(QThread):
    """Read webcam frames away from the GUI thread and emit display-ready images."""

    image_ready = Signal(QImage)
    raw_frame_ready = Signal(object)
    camera_ready = Signal(str)
    camera_error = Signal(str)
    fps_updated = Signal(float)

    def __init__(self, camera_index: int = 0) -> None:
        super().__init__()
        self.camera_index = camera_index
        self._running = False
        self._effect = "original"

    def set_effect(self, effect: str) -> None:
        self._effect = effect

    def stop(self) -> None:
        self._running = False
        self.wait(3000)

    def run(self) -> None:
        capture = cv2.VideoCapture(self.camera_index, camera_backend())
        if not capture.isOpened():
            capture.release()
            self.camera_error.emit(
                "Impossible d'ouvrir la caméra. Vérifie qu'elle est connectée "
                "et qu'aucune autre application ne l'utilise."
            )
            return

        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self._running = True
        self.camera_ready.emit("CAMÉRA ACTIVE")
        frame_count = 0
        fps_started = time.perf_counter()

        try:
            while self._running:
                success, frame = capture.read()
                if not success:
                    self.camera_error.emit("La caméra ne fournit plus d'images.")
                    break

                frame = cv2.flip(frame, 1)
                processed = apply_effect(frame, self._effect)
                rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
                height, width, _ = rgb.shape
                image = QImage(
                    rgb.data, width, height, width * 3, QImage.Format.Format_RGB888
                ).copy()

                self.raw_frame_ready.emit(processed.copy())
                self.image_ready.emit(image)

                frame_count += 1
                elapsed = time.perf_counter() - fps_started
                if frame_count >= 15:
                    self.fps_updated.emit(frame_count / max(elapsed, 0.001))
                    frame_count = 0
                    fps_started = time.perf_counter()
        finally:
            capture.release()
            self._running = False
