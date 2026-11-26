"""MediaPipe Face Landmarker adapter for IRIS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from iris.vision.model_assets import face_landmarker_model_path


@dataclass(frozen=True, slots=True)
class FaceLandmarkResult:
    """Normalized face landmarks returned for one video frame."""

    timestamp_ms: int
    faces: tuple[NDArray[np.float32], ...]
    facial_transformation_matrices: tuple[NDArray[np.float32], ...] = ()

    @property
    def face_count(self) -> int:
        return len(self.faces)


class FaceLandmarker:
    """Small lifecycle-safe adapter around MediaPipe's VIDEO Face Landmarker.

    MediaPipe is imported lazily so geometry utilities and the rest of the
    desktop application remain importable when the optional runtime is absent.
    """

    def __init__(
        self,
        model_path: str | Path | None = None,
        *,
        num_faces: int = 1,
        min_detection_confidence: float = 0.5,
        min_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self.model_path = (
            Path(model_path) if model_path is not None else face_landmarker_model_path()
        )
        self.num_faces = num_faces
        self.min_detection_confidence = min_detection_confidence
        self.min_presence_confidence = min_presence_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self._task = None
        self._last_timestamp_ms: int | None = None

    @property
    def is_open(self) -> bool:
        """Whether the underlying MediaPipe task is currently open."""
        return self._task is not None

    def open(self) -> None:
        """Load the local model and create the VIDEO task."""
        if self.is_open:
            return
        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Face Landmarker model not found: {self.model_path}"
            )
        if self.num_faces < 1:
            raise ValueError("num_faces must be at least 1")

        try:
            import mediapipe as mp
        except ImportError as exc:
            raise RuntimeError(
                "MediaPipe is not installed. Install the desktop dependencies."
            ) from exc

        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=str(self.model_path)
            ),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_faces=self.num_faces,
            min_face_detection_confidence=self.min_detection_confidence,
            min_face_presence_confidence=self.min_presence_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
            output_facial_transformation_matrixes=True,
        )
        self._task = mp.tasks.vision.FaceLandmarker.create_from_options(options)
        self._last_timestamp_ms = None

    def detect(
        self, frame_bgr: NDArray[np.uint8], timestamp_ms: int
    ) -> FaceLandmarkResult:
        """Detect faces in a BGR uint8 frame using a strictly increasing timestamp."""
        if not self.is_open:
            raise RuntimeError("FaceLandmarker is not open; call open() first.")
        if (
            not isinstance(frame_bgr, np.ndarray)
            or frame_bgr.ndim != 3
            or frame_bgr.shape[2] != 3
            or frame_bgr.size == 0
        ):
            raise ValueError("frame_bgr must be a non-empty HxWx3 image")
        if frame_bgr.dtype != np.uint8:
            raise ValueError("frame_bgr must use uint8 pixel values")
        if timestamp_ms < 0:
            raise ValueError("timestamp_ms must be non-negative")
        if (
            self._last_timestamp_ms is not None
            and timestamp_ms <= self._last_timestamp_ms
        ):
            raise ValueError("timestamp_ms must increase for every video frame")

        import mediapipe as mp

        frame_rgb = np.ascontiguousarray(frame_bgr[:, :, ::-1])
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb,
        )
        detection = self._task.detect_for_video(mp_image, timestamp_ms)
        self._last_timestamp_ms = timestamp_ms

        faces = tuple(
            np.asarray(
                [[point.x, point.y, point.z] for point in face],
                dtype=np.float32,
            )
            for face in detection.face_landmarks
        )
        matrices = tuple(
            np.asarray(matrix, dtype=np.float32)
            for matrix in getattr(detection, "facial_transformation_matrixes", ())
        )
        return FaceLandmarkResult(
            timestamp_ms=timestamp_ms,
            faces=faces,
            facial_transformation_matrices=matrices,
        )

    def close(self) -> None:
        """Release MediaPipe resources; safe to call more than once."""
        if self._task is not None:
            self._task.close()
            self._task = None
        self._last_timestamp_ms = None

    def __enter__(self) -> FaceLandmarker:
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
