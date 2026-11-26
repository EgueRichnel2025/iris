"""Composition of face detection and temporal landmark smoothing."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from iris.vision.smoothing import LandmarkSmoother


@dataclass(frozen=True, slots=True)
class VisionFrameResult:
    """Raw and temporally smoothed normalized landmarks for a frame."""

    timestamp_ms: int
    faces: tuple[NDArray[np.float32], ...]
    smoothed_faces: tuple[NDArray[np.float32], ...]
    facial_transformation_matrices: tuple[NDArray[np.float32], ...] = ()

    @property
    def face_count(self) -> int:
        return len(self.faces)


class FaceVisionPipeline:
    """Compose a detector with one independent smoother per detected face."""

    def __init__(self, detector, *, smoother_alpha: float = 0.65) -> None:
        if not 0.0 <= smoother_alpha <= 1.0:
            raise ValueError("smoother_alpha must be between 0.0 and 1.0")
        self.detector = detector
        self.smoother_alpha = float(smoother_alpha)
        self._smoothers: list[LandmarkSmoother] = []
        self._is_open = False

    @property
    def is_open(self) -> bool:
        return self._is_open

    def open(self) -> None:
        if self._is_open:
            return
        self.detector.open()
        self._smoothers.clear()
        self._is_open = True

    def process(
        self, frame_bgr: NDArray[np.uint8], timestamp_ms: int
    ) -> VisionFrameResult:
        if not self._is_open:
            raise RuntimeError("FaceVisionPipeline is not open; call open() first.")

        detection = self.detector.detect(frame_bgr, timestamp_ms)
        faces = detection.faces
        matrices = tuple(
            np.asarray(matrix, dtype=np.float32)
            for matrix in getattr(detection, "facial_transformation_matrices", ())
        )
        if not faces:
            self._smoothers.clear()
            return VisionFrameResult(timestamp_ms, faces, (), ())

        if len(self._smoothers) != len(faces):
            self._smoothers = [
                LandmarkSmoother(alpha=self.smoother_alpha) for _ in faces
            ]

        smoothed = tuple(
            smoother.smooth(face)
            for smoother, face in zip(self._smoothers, faces, strict=True)
        )
        return VisionFrameResult(timestamp_ms, faces, smoothed, matrices)

    def close(self) -> None:
        if self._is_open:
            self.detector.close()
            self._is_open = False
        self._smoothers.clear()

    def __enter__(self) -> FaceVisionPipeline:
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
