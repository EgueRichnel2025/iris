"""Head orientation estimation from MediaPipe facial landmarks."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

# Stable Face Mesh landmark IDs used by the classic six-point PnP model.
_POSE_LANDMARK_IDS = (1, 152, 33, 263, 61, 291)

# Approximate 3D face reference points in millimetres. The coordinate system
# is centred at the nose; only relative geometry is important for orientation.
_FACE_MODEL_POINTS = np.array(
    [
        (0.0, 0.0, 0.0),          # Nose tip
        (0.0, -330.0, -65.0),     # Chin
        (-225.0, 170.0, -135.0),  # Outer eye corner A
        (225.0, 170.0, -135.0),   # Outer eye corner B
        (-150.0, -150.0, -125.0), # Mouth corner A
        (150.0, -150.0, -125.0),  # Mouth corner B
    ],
    dtype=np.float64,
)


@dataclass(frozen=True, slots=True)
class HeadPose:
    """Estimated head orientation in degrees plus OpenCV pose vectors."""

    yaw: float
    pitch: float
    roll: float
    rotation_vector: NDArray[np.float64]
    translation_vector: NDArray[np.float64]


class HeadPoseEstimator:
    """Estimate yaw, pitch and roll with a six-point solvePnP model."""

    landmark_ids = _POSE_LANDMARK_IDS

    def estimate(
        self,
        landmarks: NDArray[np.floating],
        image_width: int,
        image_height: int,
    ) -> HeadPose:
        """Estimate head orientation from normalized MediaPipe landmarks.

        The camera intrinsics use a focal-length approximation based on the
        image width and a principal point at the image centre. A calibrated
        camera matrix can be added later for more accurate metric pose.
        """
        if image_width <= 0 or image_height <= 0:
            raise ValueError("image dimensions must be positive")

        points = np.asarray(landmarks, dtype=np.float64)
        if points.ndim != 2 or points.shape[1] not in (2, 3):
            raise ValueError("landmarks must have shape (N, 2) or (N, 3)")
        if points.shape[0] <= max(self.landmark_ids):
            raise ValueError("landmarks do not contain all required face points")
        if not np.isfinite(points).all():
            raise ValueError("landmarks must contain only finite coordinates")

        image_points = np.ascontiguousarray(
            points[list(self.landmark_ids), :2]
            * np.array((image_width, image_height), dtype=np.float64),
            dtype=np.float64,
        )
        camera_matrix = np.array(
            [
                [float(image_width), 0.0, image_width / 2.0],
                [0.0, float(image_width), image_height / 2.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        distortion = np.zeros((4, 1), dtype=np.float64)

        success, rotation_vector, translation_vector = cv2.solvePnP(
            _FACE_MODEL_POINTS,
            image_points,
            camera_matrix,
            distortion,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        if not success:
            raise RuntimeError("OpenCV could not estimate the head pose")

        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        yaw, pitch, roll = self._rotation_to_euler(rotation_matrix)
        angles = np.degrees((yaw, pitch, roll))
        if not np.isfinite(angles).all():
            raise RuntimeError("Head pose estimation produced non-finite angles")

        return HeadPose(
            yaw=float(angles[0]),
            pitch=float(angles[1]),
            roll=float(angles[2]),
            rotation_vector=np.asarray(rotation_vector, dtype=np.float64).reshape(3),
            translation_vector=np.asarray(translation_vector, dtype=np.float64).reshape(3),
        )

    @staticmethod
    def _rotation_to_euler(
        rotation_matrix: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Convert a rotation matrix to yaw, pitch and roll in radians."""
        horizontal_norm = np.sqrt(
            rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2
        )
        singular = horizontal_norm < 1e-6

        if not singular:
            pitch = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
            yaw = np.arctan2(-rotation_matrix[2, 0], horizontal_norm)
            roll = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        else:
            pitch = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
            yaw = np.arctan2(-rotation_matrix[2, 0], horizontal_norm)
            roll = 0.0

        return float(yaw), float(pitch), float(roll)
