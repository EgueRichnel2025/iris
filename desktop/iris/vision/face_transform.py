"""Convert MediaPipe face transforms into GLB accessory transforms."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


GLB_METERS_TO_MEDIAPIPE_CENTIMETERS = 100.0
# Offset from the MediaPipe canonical-face origin to the GLB root.
# The GLB front frame center is at y=2.30 cm after its root translation;
# the canonical outer-eye midpoint is at approximately (0, 2.66, 3.17) cm.
GLASSES_MODEL_ANCHOR_CM = np.array([0.0, 0.36, 3.17], dtype=np.float64)


def face_model_anchor_position(
    facial_transformation_matrix: ArrayLike,
    anchor_offset_cm: ArrayLike = GLASSES_MODEL_ANCHOR_CM,
) -> NDArray[np.float64]:
    """Return the camera-space position of a model anchor in face coordinates.

    The anchor offset is expressed in MediaPipe canonical-face centimeters and
    is transformed by the full facial pose, so it follows yaw, pitch and roll.
    """
    matrix = np.asarray(facial_transformation_matrix, dtype=np.float64)
    offset = np.asarray(anchor_offset_cm, dtype=np.float64)
    if matrix.shape != (4, 4) or not np.isfinite(matrix).all():
        raise ValueError("facial_transformation_matrix must be a finite 4x4 matrix")
    if offset.shape != (3,) or not np.isfinite(offset).all():
        raise ValueError("anchor_offset_cm must be a finite 3D vector")
    if not np.allclose(matrix[3], (0.0, 0.0, 0.0, 1.0), atol=1e-4):
        raise ValueError("facial_transformation_matrix must be affine")
    return matrix[:3, :3] @ offset + matrix[:3, 3]


def build_face_actor_matrix(
    facial_transformation_matrix: ArrayLike,
    *,
    model_to_centimeters: float = GLB_METERS_TO_MEDIAPIPE_CENTIMETERS,
) -> NDArray[np.float64]:
    """Map a glTF model (meters) into MediaPipe's face-camera coordinates.

    MediaPipe Face Geometry expresses its canonical/runtime face space in
    centimeters. glTF assets conventionally use meters, so the local model
    coordinates are scaled before the facial pose is applied.
    """
    face_matrix = np.asarray(facial_transformation_matrix, dtype=np.float64)
    if face_matrix.shape != (4, 4):
        raise ValueError("facial_transformation_matrix must have shape (4, 4)")
    if not np.isfinite(face_matrix).all():
        raise ValueError("facial_transformation_matrix must contain finite values")
    if not np.isfinite(model_to_centimeters) or model_to_centimeters <= 0:
        raise ValueError("model_to_centimeters must be a finite positive number")
    if not np.allclose(face_matrix[3], (0.0, 0.0, 0.0, 1.0), atol=1e-4):
        raise ValueError("facial_transformation_matrix must be affine (last row 0,0,0,1)")

    model_scale = np.diag(
        [model_to_centimeters, model_to_centimeters, model_to_centimeters, 1.0]
    )
    return face_matrix @ model_scale


def apply_face_transform(scene: Any, facial_transformation_matrix: ArrayLike) -> None:
    """Apply a MediaPipe facial pose to a previously loaded VTK glasses scene.

    Call this function on the Qt/VTK GUI thread. MediaPipe inference may run
    in the camera worker, but VTK actors and render windows belong to the GUI.
    """
    transform = build_face_actor_matrix(facial_transformation_matrix)
    from vtkmodules.vtkCommonMath import vtkMatrix4x4

    vtk_matrix = vtkMatrix4x4()
    for row in range(4):
        for column in range(4):
            vtk_matrix.SetElement(row, column, float(transform[row, column]))
    scene.actor.SetUserMatrix(vtk_matrix)
    if getattr(scene, "initialized", False):
        scene.widget.GetRenderWindow().Render()
